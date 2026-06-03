from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
import models

# create tables (safe for assignment)
Base.metadata.create_all(bind=engine)

app = FastAPI()
# 👇 ADD ROOT ROUTE HERE
@app.get("/")
def root():
    return {"message": "Cart API is running"}
# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# 1. CREATE CART
# -----------------------------
@app.post("/cart")
def create_cart(cust_id: int, db: Session = Depends(get_db)):

    cart = models.Cart(cust_id=cust_id)

    db.add(cart)
    db.commit()
    db.refresh(cart)

    return {
        "cart_id": cart.id,
        "message": "Cart created"
    }


# -----------------------------
# 2. ADD ITEM
# -----------------------------
@app.post("/cart/{cart_id}/items")
def add_item(cart_id: int, prod_id: int, quantity: int, db: Session = Depends(get_db)):

    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = models.CartItem(
        cart_id=cart_id,
        prod_id=prod_id,
        quantity=quantity
    )

    db.add(item)
    db.commit()

    return {"message": "Item added"}


# -----------------------------
# 3. REMOVE ITEM
# -----------------------------
@app.delete("/cart/items/{item_id}")
def remove_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item removed"}


# -----------------------------
# 4. CHECKOUT
# -----------------------------
@app.post("/cart/{cart_id}/checkout")
def checkout(cart_id: int, db: Session = Depends(get_db)):

    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).all()

    if len(items) == 0:
        raise HTTPException(status_code=400, detail="Cart is empty")

    cart.coupon_code = None
    db.commit()

    return {"message": "Checkout successful"}


# -----------------------------
# 5. DELETE CART
# -----------------------------
@app.delete("/cart/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):

    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).delete()
    db.delete(cart)

    db.commit()

    return {"message": "Cart deleted"}