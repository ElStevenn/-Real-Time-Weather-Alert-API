from pydantic import BaseModel
import uuid

# SCHEMAS FOR REQUEST
 
class BaseUser(BaseModel):
    username: str

class RegisterUser(BaseUser):
    email: str
    password: str

class User(BaseUser):
    id: uuid.UUID
    email: str

class LoginUser(BaseUser):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# SCHEMAS FOR RESPONSE



