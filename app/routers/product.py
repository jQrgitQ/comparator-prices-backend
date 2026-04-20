from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud import product as crud_product
from app.schemas.product import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    SubCategoryCreate, SubCategoryUpdate, SubCategoryResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    PriceCreate, PriceUpdate, PriceResponse,
    StoreCreate, StoreUpdate, StoreResponse
)
from app.security import get_current_user, require_role

router = APIRouter(tags=["products"])

categories_router = APIRouter(prefix="/categories", tags=["categories"])
subcategories_router = APIRouter(prefix="/subcategories", tags=["subcategories"])
products_router = APIRouter(prefix="/products", tags=["products"])
stores_router = APIRouter(prefix="/stores", tags=["stores"])
prices_router = APIRouter(prefix="/prices", tags=["prices"])


@categories_router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    db_category = crud_product.get_category_by_name(db, category.name)
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    return crud_product.create_category(db, category)


@categories_router.get("/", response_model=list[CategoryResponse])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_product.get_categories(db, skip=skip, limit=limit)


@categories_router.get("/{category_id}", response_model=CategoryResponse)
def read_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = crud_product.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@categories_router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    db_category = crud_product.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_product.update_category(db, category_id, category)


@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    if not crud_product.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Category not found")


@subcategories_router.post("/", response_model=SubCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    subcategory: SubCategoryCreate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    category = crud_product.get_category(db, subcategory.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    db_subcategory = crud_product.get_subcategory_by_name(db, subcategory.name)
    if db_subcategory:
        raise HTTPException(status_code=400, detail="SubCategory already exists")
    return crud_product.create_subcategory(db, subcategory)


@subcategories_router.get("/", response_model=list[SubCategoryResponse])
def read_subcategories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_product.get_subcategories(db, skip=skip, limit=limit)


@subcategories_router.get("/{subcategory_id}", response_model=SubCategoryResponse)
def read_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db)
):
    subcategory = crud_product.get_subcategory(db, subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return subcategory


@subcategories_router.get("/by-category/{category_id}", response_model=list[SubCategoryResponse])
def read_subcategories_by_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = crud_product.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_product.get_subcategories_by_category(db, category_id)


@subcategories_router.patch("/{subcategory_id}", response_model=SubCategoryResponse)
def update_subcategory(
    subcategory_id: int,
    subcategory: SubCategoryUpdate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    db_subcategory = crud_product.get_subcategory(db, subcategory_id)
    if not db_subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    if subcategory.category_id:
        category = crud_product.get_category(db, subcategory.category_id)
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")
    return crud_product.update_subcategory(db, subcategory_id, subcategory)


@subcategories_router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(
    subcategory_id: int,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    if not crud_product.delete_subcategory(db, subcategory_id):
        raise HTTPException(status_code=404, detail="SubCategory not found")


@products_router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    subcategory = crud_product.get_subcategory(db, product.subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=400, detail="SubCategory not found")
    db_product = crud_product.get_product_by_name(db, product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    return crud_product.create_product(db, product)


@products_router.get("/", response_model=list[ProductResponse])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_product.get_products(db, skip=skip, limit=limit)


@products_router.get("/by-category/{category_id}", response_model=list[ProductResponse])
def read_products_by_category(
    category_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    category = crud_product.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_product.get_products_by_category(db, category_id, skip=skip, limit=limit)


@products_router.get("/by-subcategory/{subcategory_id}", response_model=list[ProductResponse])
def read_products_by_subcategory(
    subcategory_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    subcategory = crud_product.get_subcategory(db, subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return crud_product.get_products_by_subcategory(db, subcategory_id, skip=skip, limit=limit)


@products_router.get("/{product_id}", response_model=ProductResponse)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@products_router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    db_product = crud_product.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.subcategory_id:
        subcategory = crud_product.get_subcategory(db, product.subcategory_id)
        if not subcategory:
            raise HTTPException(status_code=400, detail="SubCategory not found")
    return crud_product.update_product(db, product_id, product)


@products_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    if not crud_product.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")


@products_router.get("/{product_id}/prices", response_model=list[PriceResponse])
def read_product_prices(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud_product.get_prices_by_product(db, product_id, skip=skip, limit=limit)


@products_router.get("/{product_id}/prices/current", response_model=list[PriceResponse])
def read_current_price(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    prices = crud_product.get_all_current_prices_by_product(db, product_id)
    if not prices:
        raise HTTPException(status_code=404, detail="No price found for this product")
    return prices


@products_router.post("/{product_id}/prices", response_model=PriceResponse, status_code=status.HTTP_201_CREATED)
def create_price(
    product_id: int,
    price: PriceCreate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    store = crud_product.get_store(db, price.store_id)
    if not store:
        raise HTTPException(status_code=400, detail="Store not found")
    price_data = price.model_dump()
    price_data.pop("product_id", None)
    return crud_product.create_price(db, product_id, price_data)


@products_router.delete("/{product_id}/prices/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_price(
    product_id: int,
    price_id: int,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Verify the price belongs to this product
    price = crud_product.get_price(db, price_id)
    if not price or price.product_id != product_id:
        raise HTTPException(status_code=404, detail="Price not found for this product")

    if not crud_product.delete_price(db, price_id):
        raise HTTPException(status_code=404, detail="Price not found")


@products_router.get("/{product_id}/prices/by-store/{store_id}", response_model=list[PriceResponse])
def read_prices_by_product_and_store(
    product_id: int,
    store_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    store = crud_product.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return crud_product.get_prices_by_product_and_store(db, product_id, store_id, skip=skip, limit=limit)


@products_router.get("/{product_id}/prices/by-store/{store_id}/current", response_model=PriceResponse)
def read_current_price_by_store(
    product_id: int,
    store_id: int,
    db: Session = Depends(get_db)
):
    product = crud_product.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    store = crud_product.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    price = crud_product.get_current_price_by_product_and_store(db, product_id, store_id)
    if not price:
        raise HTTPException(status_code=404, detail="No price found")
    return price


@stores_router.post("/", response_model=StoreResponse, status_code=status.HTTP_201_CREATED)
def create_store(
    store: StoreCreate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    db_store = crud_product.get_store_by_name(db, store.name)
    if db_store:
        raise HTTPException(status_code=400, detail="Store already exists")
    return crud_product.create_store(db, store)


@stores_router.get("/", response_model=list[StoreResponse])
def read_stores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud_product.get_stores(db, skip=skip, limit=limit)


@stores_router.get("/{store_id}", response_model=StoreResponse)
def read_store(
    store_id: int,
    db: Session = Depends(get_db)
):
    store = crud_product.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@stores_router.patch("/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: int,
    store: StoreUpdate,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    db_store = crud_product.get_store(db, store_id)
    if not db_store:
        raise HTTPException(status_code=404, detail="Store not found")
    return crud_product.update_store(db, store_id, store)


@stores_router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(
    store_id: int,
    current_user: Annotated[dict, Depends(require_role("administrator"))],
    db: Session = Depends(get_db)
):
    if not crud_product.delete_store(db, store_id):
        raise HTTPException(status_code=404, detail="Store not found")


@stores_router.get("/{store_id}/prices", response_model=list[PriceResponse])
def read_store_prices(
    store_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    store = crud_product.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store.prices


def include_routers(app):
    app.include_router(categories_router)
    app.include_router(subcategories_router)
    app.include_router(products_router)
    app.include_router(stores_router)