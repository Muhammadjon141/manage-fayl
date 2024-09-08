from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]

class Settings(BaseModel):
    authjwt_secret_key: str = "bdddcbea774c82aa8d9a83e21c5297e2f5ca28123baaaf179cf42d83ef1795b3"

class UserLogin(BaseModel):
    username_or_email: Optional[str]
    password: Optional[str]

class UserPasswordReset(BaseModel):
    password: Optional[str]
    confirm_password: Optional[str]
