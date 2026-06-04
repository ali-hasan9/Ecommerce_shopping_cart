from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ---------- Cart Item Schemas ----------

class CartItemCreate(BaseModel):
    """Schema for a single item when adding to cart."""
    prodId: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(1, gt=0, description="Quantity to add")


class CartItemResponse(BaseModel):
    """Schema for returning a cart item in responses."""
    id: int
    prodId: int
    quantity: int

    class Config:
        from_attributes = True


# ---------- Cart Schemas ----------

class CartCreate(BaseModel):
    """Schema for creating a new cart."""
    custId: int = Field(..., gt=0, description="Customer ID")
    couponCode: Optional[str] = None
    discountAmount: Optional[float] = Field(0, ge=0)


class AddItemsRequest(BaseModel):
    """Schema for adding items — items passed as array (best practice)."""
    items: list[CartItemCreate] = Field(
        ..., min_length=1, description="List of items to add"
    )


class RemoveItemsRequest(BaseModel):
    """Schema for removing items by their cart_item IDs."""
    cartItemIds: list[int] = Field(
        ..., min_length=1, description="List of cart item IDs to remove"
    )


class CartResponse(BaseModel):
    """Schema for returning cart data."""
    id: int
    custId: int
    createdAt: datetime
    couponCode: Optional[str] = None
    discountAmount: float
    status: str
    cartItems: list[CartItemResponse] = []

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic response with a message."""
    message: str