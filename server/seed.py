import requests
from app import app
from config import db
from models import Product, Category, User, Inventory, Transaction, Supplier, SupplyRequest, Payment, SupplierProduct, Sale, SaleReturn, Purchase
from faker import Faker
import random

fake = Faker()

def fetch_data(url, limit=None):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if limit and len(data) < limit:
        data.extend([None] * (limit - len(data)))  # Add placeholders for additional data
    return data[:limit]  # Ensure we only return the specified limit

def seed_categories(limit=10):
    categories = fetch_data('https://api.escuelajs.co/api/v1/categories', limit)
    for i, category in enumerate(categories):
        if category:
            new_category = Category(
                id=category['id'],
                name=category['name'],
                description=f"{category['name']} category"
            )
        else:  # Create dummy data
            new_category = Category(
                name=fake.word(),
                description=fake.sentence()
            )
        db.session.add(new_category)
    db.session.commit()
    print(f"Seeded {limit} categories.")

def seed_products(limit=10):
    products = fetch_data('https://api.escuelajs.co/api/v1/products', limit)
    for i, product in enumerate(products):
        if product:
            new_product = Product(
                name=product['title'],
                category_id=product['category']['id'],
                bp=float(product['price']) * 0.8,
                sp=float(product['price']),
                image_url=product['images'][0] if product['images'] else None
            )
        else:  # Create dummy data
            new_product = Product(
                name=fake.word(),
                category_id=random.randint(1, limit),
                bp=random.uniform(5.0, 50.0),
                sp=random.uniform(50.0, 100.0),
                image_url=fake.image_url()
            )
        db.session.add(new_product)
    db.session.commit()
    print(f"Seeded {limit} products.")

def seed_users(limit=10):
    users = fetch_data('https://api.escuelajs.co/api/v1/users', limit)
    for i, user in enumerate(users):
        if user:
            new_user = User(
                name=user['name'],
                email=user['email'],
                password=user['password'],
                role=user["role"]
            )
        else:  # Create dummy data
            new_user = User(
                name=fake.name(),
                email=fake.email(),
                password=fake.password(),
                role=random.choice(['admin', 'customer', 'clerk'])
            )
        db.session.add(new_user)
    db.session.commit()
    print(f"Seeded {limit} users.")

def seed_inventory(limit=10):
    for i in range(1, limit+1):
        new_inventory = Inventory(
            product_id=random.randint(1, limit),
            quantity=random.randint(10, 100),
            spoilt_quantity=random.randint(0, 10),
            payment_status=random.choice(['Paid', 'Pending', 'Overdue'])
        )
        db.session.add(new_inventory)
    db.session.commit()
    print(f"Seeded {limit} inventory items.")

def seed_transactions(limit=10):
    for i in range(1, limit+1):
        new_transaction = Transaction(
            user_id=random.randint(1, limit),
            inventory_id=random.randint(1, limit),
            transaction_type=random.choice(['sale', 'purchase', 'return']),
            quantity=random.randint(1, 10)
        )
        db.session.add(new_transaction)
    db.session.commit()
    print(f"Seeded {limit} transactions.")

def seed_suppliers(limit=10):
    for i in range(limit):
        new_supplier = Supplier(
            name=fake.company(),
            contact_info=fake.address()
        )
        db.session.add(new_supplier)
    db.session.commit()
    print(f"Seeded {limit} suppliers.")

def seed_supply_requests(limit=10):
    for i in range(limit):
        new_supply_request = SupplyRequest(
            product_id=random.randint(1, limit),
            quantity=random.randint(10, 100),
            clerk_id=random.randint(1, limit),
            status=random.choice(['pending', 'approved', 'rejected'])
        )
        db.session.add(new_supply_request)
    db.session.commit()
    print(f"Seeded {limit} supply requests.")

def seed_payments(limit=10):
    for i in range(limit):
        new_payment = Payment(
            inventory_id=random.randint(1, limit),
            amount=random.uniform(50.0, 500.0)
        )
        db.session.add(new_payment)
    db.session.commit()
    print(f"Seeded {limit} payments.")

def seed_supplier_products(limit=10):
    for i in range(limit):
        new_supplier_product = SupplierProduct(
            supplier_id=random.randint(1, limit),
            product_id=random.randint(1, limit),
            quantity=random.randint(10, 100),
            price=random.uniform(10.0, 100.0)
        )
        db.session.add(new_supplier_product)
    db.session.commit()
    print(f"Seeded {limit} supplier products.")

def seed_sales(limit=10):
    for i in range(limit):
        new_sale = Sale(
            product_id=random.randint(1, limit),
            quantity=random.randint(1, 10),
            price=random.uniform(20.0, 200.0)
        )
        db.session.add(new_sale)
    db.session.commit()
    print(f"Seeded {limit} sales.")

def seed_sale_returns(limit=10):
    for i in range(limit):
        new_sale_return = SaleReturn(
            sale_id=random.randint(1, limit),
            quantity=random.randint(1, 5)
        )
        db.session.add(new_sale_return)
    db.session.commit()
    print(f"Seeded {limit} sale returns.")

def seed_purchases(limit=10):
    for i in range(limit):
        new_purchase = Purchase(
            product_id=random.randint(1, limit),
            quantity=random.randint(10, 50),
            price=random.uniform(100.0, 500.0)
        )
        db.session.add(new_purchase)
    db.session.commit()
    print(f"Seeded {limit} purchases.")

def seed_database():
    db.drop_all()
    db.create_all()
    limit = 10  # Ensure each table has at least 10 records
    seed_categories(limit)
    seed_products(limit)
    seed_users(limit)
    seed_inventory(limit)
    seed_transactions(limit)
    seed_suppliers(limit)
    seed_supply_requests(limit)
    seed_payments(limit)
    seed_supplier_products(limit)
    seed_sales(limit)
    seed_sale_returns(limit)
    seed_purchases(limit)

if __name__ == "__main__":
    with app.app_context():
        seed_database()
