from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Union
from uuid import UUID
from datetime import datetime

class UserSchema(BaseModel):
    id: UUID
    username: str = Field(max_length=40)
    email: EmailStr
    hashed_password: bytes
    
    class Config:
        orm_mode = True

class SubscriptionSchema(BaseModel):
    id: UUID
    location: str = Field(max_length=100)
    alert_type: str = Field(max_length=50)
    notification_method: str = Field(max_length=50)
    user_id: UUID
    
    class Config:
        orm_mode = True

class WeatherDataSchema(BaseModel):
    id: UUID
    location: str = Field(max_length=200)
    temperature: float
    conditions: str = Field(max_length=200)
    timestamp: datetime
    
    class Config:
        orm_mode = True

class AlertSchema(BaseModel):
    id: UUID
    location: str = Field(max_length=100)
    alert_type: str = Field(max_length=100)
    message: str
    timestamp: datetime
    user_id: UUID
    
    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    hashed_password: bytes

class SubscriptionCreateSchema(BaseModel):
    location: str = Field(max_length=100)
    alert_type: str = Field(max_length=50)
    notification_method: str = Field(max_length=50)
    user_id: UUID

class WeatherDataCreateSchema(BaseModel):
    location: str = Field(max_length=200)
    temperature: float
    conditions: str = Field(max_length=200)
    timestamp: Optional[datetime] = None

class AlertCreateSchema(BaseModel):
    location: str = Field(max_length=100)
    alert_type: str = Field(max_length=100)
    message: str
    timestamp: Optional[datetime] = None
    user_id: UUID

# Example schemas for responses that include relationships
class UserDetailSchema(UserSchema):
    subscriptions: List[SubscriptionSchema]
    alerts: List[AlertSchema]

class SubscriptionDetailSchema(SubscriptionSchema):
    user: UserSchema

class AlertDetailSchema(AlertSchema):
    user: UserSchema
