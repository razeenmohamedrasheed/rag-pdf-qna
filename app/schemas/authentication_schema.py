from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator



class Registration(BaseModel):
    name:str = Field(min_length=3,max_length=50)
    email:EmailStr
    password:str = Field(min_length=6,max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain an uppercase letter")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain a number")

        return value


class RegistrationResponse(BaseModel):
    status:str
    user_id:str
    created_at: datetime

class RegistartionFailureResponse(BaseModel):
    status:str
    message:str