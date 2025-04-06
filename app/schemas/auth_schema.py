from pydantic import BaseModel, Field

class RegisterSchema(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    role: str = "user"

class LoginSchema(BaseModel):
    username: str
    password: str
