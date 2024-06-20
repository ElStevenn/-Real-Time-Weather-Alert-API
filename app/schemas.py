from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

# SCHEMAS FOR REQUEST
 
class BaseUser(BaseModel):
    username: str

class RegisterUser(BaseUser):
    email: EmailStr
    hashed_password: Optional[str] = None

class User(BaseUser):
    id: uuid.UUID
    email: str

class LoginUser(BaseUser):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# SCHEMAS FOR RESPONSE



