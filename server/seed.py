from datetime import datetime
from faker import Faker
from werkzeug.security import generate_password_hash
from app import app
from models import Product, db, Inventory, Category, Payment, Supplier, SupplyRequest, User

fake = Faker()

def init_db():
    db.drop_all()
    db.create_all()

    # Create some categories
    categories = []
    for _ in range(10):
        category = Category(name=fake.word(), description=fake.text())
        categories.append(category)
    db.session.add_all(categories)
    db.session.commit()

    # Create some products
    products = []
    for _ in range(100):
        product = Product(
            name=fake.word(),
            category_id=fake.random_element(categories).id,
            bp=fake.random_number(digits=2),
            sp=fake.random_number(digits=2),
            created_at=datetime.utcnow()
        )
        products.append(product)
    db.session.add_all(products)
    db.session.commit()

    # Create some inventory records
    inventories = []
    for product in products:
        inventory = Inventory(
            product_id=product.id,
            quantity=fake.random_number(digits=3),
            spoilt_quantity=fake.random_number(digits=1),
            payment_status=fake.random_element(["Paid", "Unpaid"]),
            created_at=datetime.utcnow()
        )
        inventories.append(inventory)
    db.session.add_all(inventories)
    db.session.commit()

    # Create some users
    users = []
    for _ in range(50):
        user = User(
            name=fake.name(),
            email=fake.email(),
            password=generate_password_hash(fake.password(length=fake.random_int(min=8, max=16))),
            role=fake.random_element(elements=("Admin", "User"))
        )
        users.append(user)
    
    db.session.add_all(users)
    db.session.commit()
    print("Users seeding complete.")

    # Create some suppliers
    suppliers = []
    for _ in range(25):
        supplier = Supplier(
            name=fake.company(),
            contact_info=fake.phone_number()
        )
        suppliers.append(supplier)
    db.session.add_all(suppliers)
    db.session.commit()

    # Create some supply requests
    supply_requests = []
    for _ in range(10):
        supply_request = SupplyRequest(
            product_id=fake.random_element(products).id,
            quantity=fake.random_number(digits=2),
            clerk_id=fake.random_element(users).id,
            status=fake.random_element(["Pending", "Approved", "Rejected"]),
            created_at=datetime.utcnow()
        )
        supply_requests.append(supply_request)
    db.session.add_all(supply_requests)
    db.session.commit()

    # Create some payments
    payments = []
    for inventory in inventories:
        payment = Payment(
            inventory_id=inventory.id,
            amount=fake.random_number(digits=4),
            payment_date=datetime.utcnow()
        )
        payments.append(payment)
    db.session.add_all(payments)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        print("Starting seed...")
        init_db()
        print("Database seeded successfully!")
