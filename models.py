from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from database import Base
import datetime


class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class Category(Base):
    __tablename__ = "Category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


class Product(Base):
    __tablename__ = "Product"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("Category.id"))
    name = Column(String(150), nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
    discount_price = Column(DECIMAL(10,2), nullable=True)


class Cart(Base):
    __tablename__ = "Cart"

    id = Column(Integer, primary_key=True, index=True)
    cust_id = Column(Integer, ForeignKey("Customer.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    coupon_code = Column(String(50), nullable=True)
    discount_amount = Column(DECIMAL(10,2), default=0)


class CartItem(Base):
    __tablename__ = "Cart_Item"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("Cart.id"))
    prod_id = Column(Integer, ForeignKey("Product.id"))
    quantity = Column(Integer, default=1)


class Wishlist(Base):
    __tablename__ = "Wishlist"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("Customer.id"))
    product_id = Column(Integer, ForeignKey("Product.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)