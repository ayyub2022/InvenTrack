#!/usr/bin/env python3

# Standard library imports
from datetime import datetime

# Local imports
from app import app
from models import Product, db, Inventory

def init_db():
    with app.app_context():
        db.drop_all()  # WARNING: This will drop all tables. Use with caution!
        db.create_all()

        # Create some products
        product1 = Product(name="Product 1", bp=10.0, sp=15.0, created_at=datetime.utcnow())
        product2 = Product(name="Product 2", bp=20.0, sp=25.0, created_at=datetime.utcnow())
        product3 = Product(name="Product 3", bp=30.0, sp=35.0, created_at=datetime.utcnow())

        # Add products to the session
        db.session.add_all([product1, product2, product3])
        db.session.commit()

        # Create some inventory records
        inventory1 = Inventory(product_id=product1.id, quantity=100, spoilt_quantity=5, payment_status="paid", created_at=datetime.utcnow())
        inventory2 = Inventory(product_id=product2.id, quantity=200, spoilt_quantity=10, payment_status="unpaid", created_at=datetime.utcnow())
        inventory3 = Inventory(product_id=product3.id, quantity=150, spoilt_quantity=7, payment_status="paid", created_at=datetime.utcnow())

        # Add inventory records to the session
        db.session.add_all([inventory1, inventory2, inventory3])
        db.session.commit()

if __name__ == '__main__':
    print("Starting seed...")
    init_db()
    print("Database seeded successfully!")
