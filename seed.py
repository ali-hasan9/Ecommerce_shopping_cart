"""
Run once to populate the database with test data.
Usage: python -m app.seed
"""
from app.database import SessionLocal, engine, Base
from app.models import Customer, Category, Product

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Only seed if empty
    if db.query(Customer).count() == 0:
        # Customers
        db.add_all([
            Customer(name="Ali"),
            Customer(name="Sara"),
            Customer(name="Ahmed"),
        ])

        # Categories
        db.add_all([
            Category(name="Electronics"),
            Category(name="Clothing"),
        ])

        db.commit()

        # Products (need category IDs, so commit first)
        db.add_all([
            Product(name="Laptop", price=75000.00, discount_price=70000.00, category_id=1),
            Product(name="Mouse", price=1500.00, category_id=1),
            Product(name="T-Shirt", price=800.00, discount_price=650.00, category_id=2),
            Product(name="Jeans", price=2500.00, category_id=2),
        ])

        db.commit()
        print("Database seeded successfully!")
    else:
        print("Database already has data, skipping seed.")

finally:
    db.close()