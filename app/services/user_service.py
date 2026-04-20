from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.security import get_password_hash, verify_password
from app.utils.validators import (
    validate_role_exists,
    validate_user_exists,
    check_last_administrator,
)


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate, requesting_user: dict) -> User:
        requesting_role_id = requesting_user.get("role_id")

        requesting_role = db.query(Role).filter(Role.id == requesting_role_id).first()
        if requesting_role and requesting_role.name != "administrator":
            if user_data.role_id and user_data.role_id != 1:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only administrators can assign administrator role"
                )

        if user_data.role_id:
            validate_role_exists(db, user_data.role_id)
        else:
            user_data.role_id = 1

        normalized_email = user_data.email.strip().lower()
        existing = db.query(User).filter(User.email == normalized_email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        db_user = User(
            email=normalized_email,
            hashed_password=get_password_hash(user_data.password),
            full_name=user_data.full_name.strip() if user_data.full_name else None,
            role_id=user_data.role_id
        )
        db.add(db_user)
        try:
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate, requesting_user: dict) -> User:
        target_user = db.query(User).filter(User.id == user_id).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        is_admin = requesting_user.get("role") == "administrator"
        target_role = db.query(Role).filter(Role.id == target_user.role_id).first()
        is_target_admin = target_role and target_role.name == "administrator"

        if user_data.role_id is not None:
            if not is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only administrators can change user roles"
                )
            validate_role_exists(db, user_data.role_id)

            new_role = db.query(Role).filter(Role.id == user_data.role_id).first()
            if new_role and new_role.name == "administrator":
                if check_last_administrator(db):
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Cannot change role: there must be at least one administrator"
                    )

        if user_data.email:
            normalized_email = user_data.email.strip().lower()
            existing = db.query(User).filter(
                User.email == normalized_email,
                User.id != user_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )
            target_user.email = normalized_email

        if user_data.full_name is not None:
            target_user.full_name = user_data.full_name.strip() if user_data.full_name else None

        if user_data.is_active is not None:
            target_user.is_active = user_data.is_active

        if user_data.role_id is not None:
            target_user.role_id = user_data.role_id

        try:
            db.commit()
            db.refresh(target_user)
            return target_user
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

    @staticmethod
    def delete_user(db: Session, user_id: int, requesting_user: dict) -> bool:
        target_user = db.query(User).filter(User.id == user_id).first()
        if not target_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        target_role = db.query(Role).filter(Role.id == target_user.role_id).first()
        if target_role and target_role.name == "administrator":
            if check_last_administrator(db, exclude_user_id=user_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot delete last administrator"
                )

        db.delete(target_user)
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting user"
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        normalized_email = email.strip().lower()
        user = db.query(User).filter(User.email == normalized_email).first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive"
            )

        return user

    @staticmethod
    def get_user_from_token(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        return user