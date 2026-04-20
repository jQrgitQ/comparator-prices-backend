import re
from decimal import Decimal
from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def normalize_email(email: str) -> str:
    return email.strip().lower()


def validate_email_format(email: str) -> str:
    email = email.strip().lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid email format"
        )
    return email


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 8 characters"
        )
    if len(password) > 50:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at most 50 characters"
        )
    if not re.search(r'[A-Z]', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least 1 uppercase letter"
        )
    if not re.search(r'[a-z]', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least 1 lowercase letter"
        )
    if not re.search(r'\d', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least 1 number"
        )
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must contain at least 1 symbol"
        )
    return password


def validate_name(name: str, field_name: str = "name", min_len: int = 2, max_len: int = 255) -> str:
    if not name or not name.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} is required"
        )
    name = name.strip()
    if len(name) < min_len:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be at least {min_len} characters"
        )
    if len(name) > max_len:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be at most {max_len} characters"
        )
    if re.search(r'\s{2,}', name):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} cannot have consecutive spaces"
        )
    return name


def validate_price(price: Decimal | float, field_name: str = "price") -> Decimal:
    if price is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} is required"
        )
    try:
        price = Decimal(str(price))
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid {field_name} value"
        )
    if price <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} must be greater than 0"
        )
    return price


def validate_discount_price(price: Decimal, discount_price: Decimal | None, is_discount: bool) -> Decimal | None:
    if is_discount and discount_price is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="discount_price is required when is_discount is true"
        )
    if not is_discount and discount_price is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="discount_price must be null when is_discount is false"
        )
    if discount_price is not None and discount_price >= price:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="discount_price must be less than price"
        )
    return discount_price


def validate_pagination(skip: int, limit: int, max_limit: int = 100) -> tuple[int, int]:
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="skip must be >= 0"
        )
    if limit < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="limit must be >= 1"
        )
    if limit > max_limit:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"limit must be at most {max_limit}"
        )
    return skip, limit


def validate_future_date(date: datetime, field_name: str = "date") -> datetime:
    if date > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{field_name} cannot be in the future"
        )
    return date


def validate_role_exists(db: Session, role_id: int) -> Any:
    from app.models.role import Role
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with id {role_id} does not exist"
        )
    return role


def validate_category_exists(db: Session, category_id: int) -> Any:
    from app.models.category import Category
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} not found"
        )
    return category


def validate_subcategory_exists(db: Session, subcategory_id: int) -> Any:
    from app.models.subcategory import SubCategory
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SubCategory with id {subcategory_id} not found"
        )
    return subcategory


def validate_product_exists(db: Session, product_id: int) -> Any:
    from app.models.product import Product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return product


def validate_store_exists(db: Session, store_id: int) -> Any:
    from app.models.store import Store
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Store with id {store_id} not found"
        )
    return store


def validate_user_exists(db: Session, user_id: int) -> Any:
    from app.models.user import User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


def check_category_has_subcategories(db: Session, category_id: int) -> bool:
    from app.models.subcategory import SubCategory
    count = db.query(SubCategory).filter(SubCategory.category_id == category_id).count()
    return count > 0


def check_subcategory_has_products(db: Session, subcategory_id: int) -> bool:
    from app.models.product import Product
    count = db.query(Product).filter(Product.subcategory_id == subcategory_id).count()
    return count > 0


def check_product_has_prices(db: Session, product_id: int) -> bool:
    from app.models.price import Price
    count = db.query(Price).filter(Price.product_id == product_id).count()
    return count > 0


def check_store_has_prices(db: Session, store_id: int) -> bool:
    from app.models.price import Price
    count = db.query(Price).filter(Price.store_id == store_id).count()
    return count > 0


def check_last_administrator(db: Session, exclude_user_id: int | None = None) -> bool:
    from app.models.user import User
    from app.models.role import Role
    admin_role = db.query(Role).filter(Role.name == "administrator").first()
    if not admin_role:
        return False
    query = db.query(User).filter(User.role_id == admin_role.id)
    if exclude_user_id:
        query = query.filter(User.id != exclude_user_id)
    count = query.count()
    return count == 0