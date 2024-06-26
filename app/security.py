from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from typing import Union
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64decode
from dotenv import load_dotenv
import jwt, os, pickle

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY_TOKEN")

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await verify_token(token) 
    if not user:
        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user['sub']

async def verify_token(token: str):
    try:
        payload = decode_token(token)
        return payload
    except HTTPException as e:
        raise e

class AES_256_encrypter:
    def __init__(self):
        # Generate RSA key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def get_public_key(self):
        # Return the public key in PEM format
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
    
    def encrypt(self, plaintext, password: str):
        # generate a random salt
        salt = os.urandom(16)
        
        # use the Scrypt KDF to get a private key from the password
        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
        private_key = kdf.derive(password.encode())
        
        # create cipher config
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(private_key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # pad the plaintext
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        
        # encrypt the plaintext
        cipher_text = encryptor.update(padded_data) + encryptor.finalize()
        
        # serialize the data to bytes
        encrypted_data = {
            'cipher_text': cipher_text,
            'salt': salt,
            'iv': iv,
            'tag': encryptor.tag
        }
        serialized_data = pickle.dumps(encrypted_data)
        
        return serialized_data

    def decrypt(self, serialized_data: bytes, provided_password: str):
        try:
            # deserialize the data
            enc_dict = pickle.loads(serialized_data)
            
            # extract data from the dictionary
            salt = enc_dict['salt']
            cipher_text = enc_dict['cipher_text']
            iv = enc_dict['iv']
            tag = enc_dict['tag']
            
            # generate the private key from the password and salt
            kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
            private_key = kdf.derive(provided_password.encode())
            
            # create the cipher config
            cipher = Cipher(algorithms.AES(private_key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            # decrypt the cipher text
            decrypted_padded = decryptor.update(cipher_text) + decryptor.finalize()
            
            # unpad the decrypted data
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
            
            return decrypted.decode()
        except Exception as e:
            # The password provided is wrong or other decryption error
            return None

    def encrypt_password_with_public_key(self, password: str, public_key_pem: str):
        public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'), backend=default_backend())
        encrypted_password = public_key.encrypt(
            password.encode(),
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_password
        
encrypter = AES_256_encrypter()


if __name__ == "__main__":
    """
   # Example usage for password encrytion
    user_name = "mrpau"
    password = "helo123"
    
    # Get the public key
    public_key = encrypter.get_public_key()
    print(f"Public Key:\n{public_key}")
    
    # Encrypt password using public key (simulating front-end encryption)
    encrypted_password = encrypter.encrypt_password_with_public_key(password, public_key)
    print(f"Encrypted Password (with public key): {encrypted_password}")
    
    # Encrypt some plaintext
    encrypted_data = encrypter.encrypt(user_name, password)
    print(f"Encrypted Data: {encrypted_data}")
    
    # Decrypt the data
    decrypted_data = encrypter.decrypt(encrypted_data, password)
    print(f"Decrypted Data: {decrypted_data}")
    """
    # Exampe for token
    token = create_access_token({"sub": "mrpau"})
    print(token)

    # Decode token
    decoded_token = decode_token(token)
    print(decoded_token)
