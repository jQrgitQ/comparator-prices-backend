from sqlalchemy.orm import Session

from app.models.role import Role


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def get_all_roles(db: Session):
    return db.query(Role).all()