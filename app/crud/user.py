from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.crud.role import get_role
from app.schemas.user import UserCreate, UserUpdate


DEFAULT_ROLE_ID = 1


def normalize_email(email: str) -> str:
    return email.strip().lower()


def resolve_role_id(db: Session, role_id: int | None) -> int:
    final_role_id = role_id if role_id is not None else DEFAULT_ROLE_ID
    db_role = get_role(db, final_role_id)
    if db_role is None:
        raise ValueError(f"Role with id {final_role_id} does not exist")
    return final_role_id


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    normalized_email = normalize_email(email)
    return db.query(User).filter(func.lower(User.email) == normalized_email).first()


def get_user_by_email_excluding_id(db: Session, email: str, user_id: int):
    normalized_email = normalize_email(email)
    return (
        db.query(User)
        .filter(func.lower(User.email) == normalized_email)
        .filter(User.id != user_id)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate, role_id: int | None = None):
    from app.security import get_password_hash
    hashed_password = get_password_hash(user.password)
    normalized_email = normalize_email(user.email)
    final_role_id = resolve_role_id(db, role_id if role_id is not None else user.role_id)

    if get_user_by_email(db, normalized_email):
        raise ValueError("Email already registered")

    db_user = User(
        email=normalized_email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role_id=final_role_id
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Email already registered") from exc


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    if 'role_id' in update_data:
        if update_data['role_id'] is None:
            del update_data['role_id']
        else:
            update_data['role_id'] = resolve_role_id(db, update_data['role_id'])

    new_email = update_data.get('email')
    if new_email:
        existing_user = get_user_by_email_excluding_id(db, new_email, user_id)
        if existing_user:
            raise ValueError("Email already registered")
        update_data['email'] = normalize_email(new_email)
    
    for field, value in update_data.items():
        setattr(db_user, field, value)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Email already registered") from exc


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True