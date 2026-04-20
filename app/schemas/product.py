from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


class SubCategoryBase(BaseModel):
    name: str
    category_id: int


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None


class SubCategoryResponse(SubCategoryBase):
    id: int

    class Config:
        from_attributes = True


class SubCategoryWithProductsResponse(SubCategoryBase):
    id: int
    products: list["ProductResponse"] = []

    class Config:
        from_attributes = True


class CategoryWithSubCategoriesResponse(CategoryBase):
    id: int
    subcategories: list[SubCategoryResponse] = []

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    subcategory_id: int


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    subcategory_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None
    subcategory_id: int | None = None


class ProductResponse(ProductBase):
    id: int
    last_price: float | None = None

    class Config:
        from_attributes = True


class ProductWithPricesResponse(ProductBase):
    id: int
    prices: list["PriceResponse"] = []

    class Config:
        from_attributes = True


class PriceBase(BaseModel):
    price: Decimal
    discount_price: Decimal | None = None
    is_discount: bool = False


class PriceCreate(PriceBase):
    product_id: int
    store_id: int


class PriceUpdate(BaseModel):
    price: Decimal | None = None
    discount_price: Decimal | None = None
    is_discount: bool | None = None


class PriceResponse(PriceBase):
    id: int
    date: datetime
    product_id: int
    store_id: int

    class Config:
        from_attributes = True


class StoreBase(BaseModel):
    name: str
    location: str | None = None


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: str | None = None
    location: str | None = None


class StoreResponse(StoreBase):
    id: int

    class Config:
        from_attributes = True