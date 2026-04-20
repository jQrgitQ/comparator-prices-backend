from pydantic import BaseModel, EmailStr, field_validator
from decimal import Decimal


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str
    role_id: int | None = None

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        from app.utils.validators import validate_password_strength
        return validate_password_strength(v)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    is_active: bool | None = None
    role_id: int | None = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    role_id: int = 1

    model_config = {"from_attributes": True}


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        from app.utils.validators import validate_password_strength
        return validate_password_strength(v)