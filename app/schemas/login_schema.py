from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime

class LoginPayload(BaseModel):
    email:EmailStr
    password:str = Field(min_length=6,max_length=50)

class LoginFailureResponse(BaseModel):
    status: str
    message :str

class LoginResponse(BaseModel):
    status:str
    message:str
    access_token:str
    refresh_token:str
    created_at:datetime