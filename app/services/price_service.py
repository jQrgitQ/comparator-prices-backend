from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.price import Price
from app.models.product import Product
from app.models.store import Store
from app.schemas.product import PriceCreate
from app.utils.validators import (
    validate_price,
    validate_discount_price,
    validate_product_exists,
    validate_store_exists,
    validate_pagination,
)


class PriceService:
    @staticmethod
    def create_price(db: Session, product_id: int, data: PriceCreate) -> Price:
        validate_product_exists(db, product_id)
        validate_store_exists(db, data.store_id)

        if data.product_id != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="product_id in path does not match product_id in body"
            )

        price = validate_price(data.price, "price")
        discount_price = validate_discount_price(price, data.discount_price, data.is_discount if data.is_discount else False)

        db_price = Price(
            price=price,
            discount_price=discount_price,
            is_discount=data.is_discount if data.is_discount else False,
            date=datetime.utcnow(),
            product_id=product_id,
            store_id=data.store_id
        )
        db.add(db_price)
        try:
            db.commit()
            db.refresh(db_price)
            return db_price
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating price"
            )

    @staticmethod
    def get_prices_by_product(db: Session, product_id: int, skip: int = 0, limit: int = 100) -> list[Price]:
        validate_product_exists(db, product_id)
        skip, limit = validate_pagination(skip, limit)
        return (
            db.query(Price)
            .filter(Price.product_id == product_id)
            .order_by(Price.date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_all_current_prices_by_product(db: Session, product_id: int) -> list[Price]:
        validate_product_exists(db, product_id)

        from sqlalchemy import func
        subquery = (
            db.query(
                Price.store_id,
                func.max(Price.date).label('max_date')
            )
            .filter(Price.product_id == product_id)
            .group_by(Price.store_id)
            .subquery()
        )

        return (
            db.query(Price)
            .join(
                subquery,
                and_(
                    Price.store_id == subquery.c.store_id,
                    Price.date == subquery.c.max_date
                )
            )
            .filter(Price.product_id == product_id)
            .all()
        )

    @staticmethod
    def get_prices_by_product_and_store(
        db: Session,
        product_id: int,
        store_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Price]:
        validate_product_exists(db, product_id)
        validate_store_exists(db, store_id)
        skip, limit = validate_pagination(skip, limit)

        return (
            db.query(Price)
            .filter(
                Price.product_id == product_id,
                Price.store_id == store_id
            )
            .order_by(Price.date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_current_price_by_product_and_store(
        db: Session,
        product_id: int,
        store_id: int
    ) -> Price:
        validate_product_exists(db, product_id)
        validate_store_exists(db, store_id)

        price = (
            db.query(Price)
            .filter(
                Price.product_id == product_id,
                Price.store_id == store_id
            )
            .order_by(Price.date.desc())
            .first()
        )
        if not price:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No price found"
            )
        return price

    @staticmethod
    def delete_price(db: Session, price_id: int) -> bool:
        price = db.query(Price).filter(Price.id == price_id).first()
        if not price:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Price not found"
            )

        db.delete(price)
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting price"
            )