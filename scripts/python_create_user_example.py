import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

URL_BASE = 'http://localhost:8000'

class AES_256_encrypter:
    def __init__(self):
        self.public_key = self.get_public_key()
    
    def get_public_key(self):
        """Get public key"""
        public_key_str = requests.get(f'{URL_BASE}/get_public_key').content
        public_key = serialization.load_pem_public_key(
            public_key_str,
            backend=default_backend()
        )
        return public_key

    def encrypt_password_with_public_key(self, password: str):
        """Encrypt password with the given public key"""
        encrypted_password = self.public_key.encrypt(
            password.encode(),
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_password

encripter = AES_256_encrypter()

def register_new_user(username, email, password: str):
    url = URL_BASE + "/register"
    encrypted_password = encripter.encrypt_password_with_public_key(password)
    encrypted_password_base64 = base64.b64encode(encrypted_password).decode('utf-8')

    # Create the request body
    request_body = {
        "username": username,
        "email": email,
        "hashed_password": encrypted_password_base64
    }

    result = requests.post(url, json=request_body)
    print(result)

if __name__ == "__main__":
    register_new_user("example_user", "example_user@example.com", "helo123")
