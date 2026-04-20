from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"), nullable=False)

    subcategory = relationship("SubCategory", back_populates="products")
    prices = relationship("Price", back_populates="product", cascade="all, delete-orphan")