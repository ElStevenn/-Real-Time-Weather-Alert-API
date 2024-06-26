from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr, SecretBytes, Field

class BaseUser(BaseModel):
    username: str

class RegisterUser(BaseUser):
    email: EmailStr
    hashed_password: SecretBytes

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    hashed_password: bytes

        
class User(BaseUser):
    id: uuid.UUID
    email: str

class LoginUser(BaseUser):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    hashed_password: SecretBytes
