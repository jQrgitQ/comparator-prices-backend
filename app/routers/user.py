from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.security import require_role
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    return UserService.create_user(db, user, current_user)


@router.get("/", response_model=list[UserResponse])
def read_users(
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    from app.utils.validators import validate_pagination
    skip, limit = validate_pagination(skip, limit)
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    return UserService.update_user(db, user_id, user, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    UserService.delete_user(db, user_id, current_user)