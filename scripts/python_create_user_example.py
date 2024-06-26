import requests
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import logging

URL_BASE = 'http://localhost:8000'

class AES_256_encrypter:
    def __init__(self):
        self.public_key = self.get_public_key()

    def get_public_key(self):
        public_key_str = requests.get(f'{URL_BASE}/get_public_key').content
        public_key = serialization.load_pem_public_key(
            public_key_str,
            backend=default_backend()
        )
        return public_key

    def encrypt_password_with_public_key(self, password: str):
        encrypted_password = self.public_key.encrypt(
            password.encode(),
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_password

encrypter = AES_256_encrypter()

def register_new_user(username, email, password: str):
    url = URL_BASE + "/register"
    encrypted_password = encrypter.encrypt_password_with_public_key(password)
    encrypted_password_base64 = base64.b64encode(encrypted_password).decode('utf-8')


    request_body = {
        "username": username,
        "email": email,
        "hashed_password": encrypted_password_base64
    }

    try:
        result = requests.post(url, json=request_body)
        result.raise_for_status()
        print("response: ", result.json())  
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")

if __name__ == "__main__":
    register_new_user("pepo gracia", "pepogracia@example.com", "hello123")
