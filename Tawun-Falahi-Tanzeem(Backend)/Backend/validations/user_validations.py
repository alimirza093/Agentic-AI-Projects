from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr  
    password: str 

class UserSign(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    password: str 

    @field_validator("username")
    def username_must_not_contain_spaces(cls, v):
        if " " in v:
            raise ValueError("Username must not contain spaces")
        return v

    @field_validator("password")
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v