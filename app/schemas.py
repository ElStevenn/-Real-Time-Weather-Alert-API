from typing import Optional
import base64
from pydantic import BaseModel, EmailStr, ValidationError
import uuid

class EncodedBytes(bytes):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            try:
                return base64.b64decode(v.encode('utf-8'))
            except Exception as e:
                raise ValueError(f'Invalid base64-encoded data: {e}')
        elif isinstance(v, bytes):
            return v
        raise ValueError('Invalid type for EncodedBytes')

    def __str__(self):
        return base64.b64encode(self).decode('utf-8')

class BaseUser(BaseModel):
    username: str

class RegisterUser(BaseUser):
    email: EmailStr
    hashed_password: EncodedBytes
class User(BaseUser):
    id: uuid.UUID
    email: str

class LoginUser(BaseUser):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# SCHEMAS FOR RESPONSE



