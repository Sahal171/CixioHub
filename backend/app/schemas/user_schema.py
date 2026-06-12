from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        if not re.match(pattern, value):
            raise ValueError(
                "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, one number, and one special character"
            )

        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str