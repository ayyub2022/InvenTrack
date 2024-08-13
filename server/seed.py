import requests
from app import app
from config import db
from models import Product, Category, User, Inventory, Transaction, Supplier, SupplyRequest, Payment, SupplierProduct, Sale, SaleReturn, Purchase
from faker import Faker
from sqlalchemy.exc import IntegrityError
import random

fake = Faker()

def fetch_data(url, limit=None):
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if limit:
        data = data[:limit]  # Apply limit if specified
    return data

def seed_categories():
    categories = fetch_data('https://fakestoreapi.com/products/categories')
    
    for category in categories:
        if category and category != "Testing Category":
            existing_category = Category.query.filter_by(name=category).first()
            
            if not existing_category:
                new_category = Category(
                    name=category,
                    description=f"{category} category",
                    image_url=None  # or a placeholder URL if needed
                )
                db.session.add(new_category)
    
    try:
        db.session.commit()
        print(f"Seeded {len(categories)} categories (excluding 'Testing Category').")
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error occurred while seeding categories: {e}")

def seed_products():
    products = fetch_data('https://fakestoreapi.com/products')
    seeded_count = 0

    for i, product in enumerate(products):
        if product:
            existing_product = Product.query.filter_by(name=product['title']).first()
            if not existing_product:
                new_product = Product(
                    name=product['title'],
                    category_id=Category.query.filter_by(name=product["category"]).first().id,
                    bp=float(product['price']) * 0.8,
                    sp=float(product['price']),
                    image_url=product["image"]
                )
                db.session.add(new_product)
                seeded_count += 1
        else:
            max_category_id = db.session.query(db.func.max(Category.id)).scalar()
            new_product = Product(
                name=fake.word(),
                category_id=random.randint(1, max_category_id),
                bp=random.uniform(5.0, 50.0),
                sp=random.uniform(50.0, 100.0),
                image_url=fake.image_url()
            )
            db.session.add(new_product)
            seeded_count += 1

    db.session.commit()
    print(f"Seeded {seeded_count} products.")

def seed_users():
    users = fetch_data('https://api.escuelajs.co/api/v1/users')
    
    for user in users:
        if user:
            existing_user = User.query.filter_by(email=user['email']).first()
            
            if not existing_user:
                new_user = User(
                    name=user['name'],
                    email=user['email'],
                    password=user['password'],  # Ensure this is handled securely in practice
                    role=user["role"]
                )
                db.session.add(new_user)
    
    try:
        db.session.commit()
        print(f"Seeded {len(users)} users.")
    except IntegrityError:
        db.session.rollback()
        print("Error occurred while seeding users.")

def seed_inventory(limit=20):
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

def seed_transactions(limit=20):
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

def seed_suppliers(limit=20):
    for i in range(limit):
        new_supplier = Supplier(
            name=fake.company(),
            contact_info=fake.address()
        )
        db.session.add(new_supplier)
    db.session.commit()
    print(f"Seeded {limit} suppliers.")

def seed_supply_requests(limit=20):
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

def seed_payments(limit=20):
    for i in range(limit):
        new_payment = Payment(
            inventory_id=random.randint(1, limit),
            amount=random.uniform(50.0, 500.0)
        )
        db.session.add(new_payment)
    db.session.commit()
    print(f"Seeded {limit} payments.")

def seed_supplier_products(limit=20):
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

def seed_sales(limit=20):
    for i in range(limit):
        new_sale = Sale(
            product_id=random.randint(1, limit),
            quantity=random.randint(1, 10),
            price=random.uniform(20.0, 200.0)
        )
        db.session.add(new_sale)
    db.session.commit()
    print(f"Seeded {limit} sales.")

def seed_sale_returns(limit=20):
    for i in range(limit):
        new_sale_return = SaleReturn(
            sale_id=random.randint(1, limit),
            quantity=random.randint(1, 5)
        )
        db.session.add(new_sale_return)
    db.session.commit()
    print(f"Seeded {limit} sale returns.")

def seed_purchases(limit=20):
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
    seed_categories()
    seed_products()  # Keep limit for products if needed
    seed_users()  # No limit for users
    seed_inventory(90)  # Keep limit for inventory if needed
    seed_transactions(90)  # Keep limit for transactions if needed
    seed_suppliers(90)  # Keep limit for suppliers if needed
    seed_supply_requests(90)  # Keep limit for supply requests if needed
    seed_payments(90)  # Keep limit for payments if needed
    seed_supplier_products(90)  # Keep limit for supplier products if needed
    seed_sales(90)  # Keep limit for sales if needed
    seed_sale_returns(90)  # Keep limit for sale returns if needed
    seed_purchases(90)  # Keep limit for purchases if needed

if __name__ == "__main__":
    with app.app_context():
        seed_database()
