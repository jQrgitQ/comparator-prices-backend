from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.subcategory import SubCategory
from app.models.product import Product
from app.models.store import Store
from app.schemas.product import (
    CategoryCreate, SubCategoryCreate, ProductCreate, StoreCreate
)
from app.utils.validators import (
    validate_name,
    validate_pagination,
    validate_category_exists,
    validate_subcategory_exists,
    validate_product_exists,
    validate_store_exists,
    check_category_has_subcategories,
    check_subcategory_has_products,
    check_product_has_prices,
    check_store_has_prices,
)


class CatalogService:
    @staticmethod
    def create_category(db: Session, data: CategoryCreate) -> Category:
        normalized_name = validate_name(data.name, "name")
        existing = db.query(Category).filter(Category.name.ilike(normalized_name)).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists"
            )

        db_category = Category(name=normalized_name)
        db.add(db_category)
        try:
            db.commit()
            db.refresh(db_category)
            return db_category
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category already exists"
            )

    @staticmethod
    def update_category(db: Session, category_id: int, data: dict) -> Category:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        if data.get("name"):
            normalized_name = validate_name(data["name"], "name")
            existing = db.query(Category).filter(
                Category.name.ilike(normalized_name),
                Category.id != category_id
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Category name already exists"
                )
            category.name = normalized_name

        try:
            db.commit()
            db.refresh(category)
            return category
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Category name already exists"
            )

    @staticmethod
    def delete_category(db: Session, category_id: int) -> bool:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        if check_category_has_subcategories(db, category_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete category: has subcategories"
            )

        db.delete(category)
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting category"
            )

    @staticmethod
    def create_subcategory(db: Session, data: SubCategoryCreate) -> SubCategory:
        validate_category_exists(db, data.category_id)
        normalized_name = validate_name(data.name, "name")
        existing = db.query(SubCategory).filter(
            SubCategory.name.ilike(normalized_name),
            SubCategory.category_id == data.category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="SubCategory already exists in this category"
            )

        db_subcategory = SubCategory(name=normalized_name, category_id=data.category_id)
        db.add(db_subcategory)
        try:
            db.commit()
            db.refresh(db_subcategory)
            return db_subcategory
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="SubCategory already exists"
            )

    @staticmethod
    def delete_subcategory(db: Session, subcategory_id: int) -> bool:
        subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
        if not subcategory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SubCategory not found"
            )

        if check_subcategory_has_products(db, subcategory_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete subcategory: has products"
            )

        db.delete(subcategory)
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting subcategory"
            )

    @staticmethod
    def create_product(db: Session, data: ProductCreate) -> Product:
        validate_subcategory_exists(db, data.subcategory_id)
        normalized_name = validate_name(data.name, "name")
        existing = db.query(Product).filter(
            Product.name.ilike(normalized_name),
            Product.subcategory_id == data.subcategory_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists in this subcategory"
            )

        db_product = Product(
            name=normalized_name,
            description=data.description.strip() if data.description else None,
            subcategory_id=data.subcategory_id
        )
        db.add(db_product)
        try:
            db.commit()
            db.refresh(db_product)
            return db_product
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists"
            )

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        if check_product_has_prices(db, product_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete product: has price history"
            )

        db.delete(product)
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting product"
            )

    @staticmethod
    def create_store(db: Session, data: StoreCreate) -> Store:
        normalized_name = validate_name(data.name, "name")
        existing = db.query(Store).filter(Store.name.ilike(normalized_name)).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Store already exists"
            )

        db_store = Store(
            name=normalized_name,
            location=data.location.strip() if data.location else None
        )
        db.add(db_store)
        try:
            db.commit()
            db.refresh(db_store)
            return db_store
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Store already exists"
            )

    @staticmethod
    def delete_store(db: Session, store_id: int) -> bool:
        store = db.query(Store).filter(Store.id == store_id).first()
        if not store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Store not found"
            )

        if check_store_has_prices(db, store_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete store: has price history"
            )

        db.delete(store)
        try:
            db.commit()
            return True
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting store"
            )

    @staticmethod
    def list_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
        skip, limit = validate_pagination(skip, limit)
        return db.query(Category).offset(skip).limit(limit).all()

    @staticmethod
    def list_subcategories(db: Session, category_id: int = None, skip: int = 0, limit: int = 100) -> list[SubCategory]:
        skip, limit = validate_pagination(skip, limit)
        query = db.query(SubCategory)
        if category_id:
            query = query.filter(SubCategory.category_id == category_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def list_products(db: Session, subcategory_id: int = None, category_id: int = None, skip: int = 0, limit: int = 100) -> list[Product]:
        skip, limit = validate_pagination(skip, limit)
        query = db.query(Product)
        if subcategory_id:
            query = query.filter(Product.subcategory_id == subcategory_id)
        elif category_id:
            query = query.join(SubCategory).filter(SubCategory.category_id == category_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def list_stores(db: Session, skip: int = 0, limit: int = 100) -> list[Store]:
        skip, limit = validate_pagination(skip, limit)
        return db.query(Store).offset(skip).limit(limit).all()