from pydantic import BaseModel, Field, field_validator
import re

class Login(BaseModel):
    user_id:str

    email: str = Field(..., min_length=1)

    @field_validator("email")
    def validate_email(cls, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Invalid email format")
        return value
    
    password: str


class signup(BaseModel):
    first_name:str
    last_name:str
    password:str
    user_id:str
    email: str = Field(..., min_length=1)

    @field_validator("email")
    def validate_email(cls, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError("Invalid email format")
        return value