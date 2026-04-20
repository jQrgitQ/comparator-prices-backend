from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import Session
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        action: str,
        entity_type: str = None,
        entity_id: int = None,
        user_id: int = None,
        details: str = None
    ):
        audit = AuditLog(
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details
        )
        db.add(audit)
        try:
            db.commit()
        except Exception:
            db.rollback()

    @staticmethod
    def log_user_action(db: Session, user_id: int, action: str, details: str = None):
        AuditService.log_action(db, action, "user", user_id=user_id, details=details)

    @staticmethod
    def log_catalog_action(db: Session, entity_type: str, entity_id: int, action: str, user_id: int = None):
        AuditService.log_action(db, action, entity_type, entity_id, user_id)

    @staticmethod
    def log_price_action(db: Session, product_id: int, store_id: int, action: str, user_id: int = None):
        details = f"product:{product_id}, store:{store_id}"
        AuditService.log_action(db, action, "price", user_id=user_id, details=details)