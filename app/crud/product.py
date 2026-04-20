from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.category import Category
from app.models.subcategory import SubCategory
from app.models.product import Product
from app.models.price import Price
from app.models.store import Store
from app.schemas.product import (
    CategoryCreate, CategoryUpdate,
    SubCategoryCreate, SubCategoryUpdate,
    ProductCreate, ProductUpdate,
    StoreCreate, StoreUpdate
)


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category: CategoryUpdate):
    db_category = get_category(db, category_id)
    if db_category is None:
        return None
    for field, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category is None:
        return False
    db.delete(db_category)
    db.commit()
    return True


def get_subcategory(db: Session, subcategory_id: int):
    return db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()


def get_subcategory_by_name(db: Session, name: str):
    return db.query(SubCategory).filter(SubCategory.name == name).first()


def get_subcategories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SubCategory).offset(skip).limit(limit).all()


def get_subcategories_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(SubCategory).filter(SubCategory.category_id == category_id).offset(skip).limit(limit).all()


def create_subcategory(db: Session, subcategory: SubCategoryCreate):
    db_subcategory = SubCategory(name=subcategory.name, category_id=subcategory.category_id)
    db.add(db_subcategory)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


def update_subcategory(db: Session, subcategory_id: int, subcategory: SubCategoryUpdate):
    db_subcategory = get_subcategory(db, subcategory_id)
    if db_subcategory is None:
        return None
    for field, value in subcategory.model_dump(exclude_unset=True).items():
        setattr(db_subcategory, field, value)
    db.commit()
    db.refresh(db_subcategory)
    return db_subcategory


def delete_subcategory(db: Session, subcategory_id: int):
    db_subcategory = get_subcategory(db, subcategory_id)
    if db_subcategory is None:
        return False
    db.delete(db_subcategory)
    db.commit()
    return True


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_name(db: Session, name: str):
    return db.query(Product).filter(Product.name == name).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    products = db.query(Product).offset(skip).limit(limit).all()

    # Add last_price to each product
    for product in products:
        last_price = get_current_price(db, product.id)
        product.last_price = float(last_price.price) if last_price else None

    return products


def get_products_by_subcategory(db: Session, subcategory_id: int, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(Product.subcategory_id == subcategory_id).offset(skip).limit(limit).all()


def get_products_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(Product).join(SubCategory).filter(SubCategory.category_id == category_id).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
        name=product.name,
        description=product.description,
        image_url=product.image_url,
        subcategory_id=product.subcategory_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # Add last_price to response
    last_price = get_current_price(db, db_product.id)
    if last_price:
        db_product.last_price = float(last_price.price)

    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product is None:
        return None
    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product is None:
        return False
    db.delete(db_product)
    db.commit()
    return True


def get_price(db: Session, price_id: int):
    return db.query(Price).filter(Price.id == price_id).first()


def get_prices_by_product(db: Session, product_id: int, skip: int = 0, limit: int = 100):
    return db.query(Price).filter(Price.product_id == product_id).order_by(Price.date.desc()).offset(skip).limit(limit).all()


def get_current_price(db: Session, product_id: int):
    return db.query(Price).filter(Price.product_id == product_id).order_by(Price.date.desc()).first()


def create_price(db: Session, product_id: int, price_data: dict):
    db_price = Price(product_id=product_id, **price_data)
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


def delete_price(db: Session, price_id: int):
    db_price = get_price(db, price_id)
    if db_price is None:
        return False
    db.delete(db_price)
    db.commit()
    return True


def get_store(db: Session, store_id: int):
    return db.query(Store).filter(Store.id == store_id).first()


def get_store_by_name(db: Session, name: str):
    return db.query(Store).filter(Store.name == name).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()


def create_store(db: Session, store: StoreCreate):
    db_store = Store(name=store.name, location=store.location)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def update_store(db: Session, store_id: int, store: StoreUpdate):
    db_store = get_store(db, store_id)
    if db_store is None:
        return None
    for field, value in store.model_dump(exclude_unset=True).items():
        setattr(db_store, field, value)
    db.commit()
    db.refresh(db_store)
    return db_store


def delete_store(db: Session, store_id: int):
    db_store = get_store(db, store_id)
    if db_store is None:
        return False
    db.delete(db_store)
    db.commit()
    return True


def get_prices_by_product_and_store(db: Session, product_id: int, store_id: int, skip: int = 0, limit: int = 100):
    return db.query(Price).filter(
        Price.product_id == product_id,
        Price.store_id == store_id
    ).order_by(Price.date.desc()).offset(skip).limit(limit).all()


def get_current_price_by_product_and_store(db: Session, product_id: int, store_id: int):
    return db.query(Price).filter(
        Price.product_id == product_id,
        Price.store_id == store_id
    ).order_by(Price.date.desc()).first()


def get_all_current_prices_by_product(db: Session, product_id: int):
    subquery = db.query(
        Price.store_id,
        func.max(Price.date).label('max_date')
    ).filter(Price.product_id == product_id).group_by(Price.store_id).subquery()

    return db.query(Price).join(
        subquery,
        (Price.store_id == subquery.c.store_id) & (Price.date == subquery.c.max_date)
    ).filter(Price.product_id == product_id).all()