from pydantic import BaseModel

# SCHEMAS FOR REQUEST
 
class BaseUser(BaseModel):
    username: str

class RegisterUser(BaseUser):
    email: str
    password: str

class LoginUser(BaseUser):
    password: str

# SCHEMAS FOR RESPONSE



