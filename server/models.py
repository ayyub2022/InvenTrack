import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

from config import db

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    spoilt_quantity = db.Column(db.Integer, nullable=False, default=0)
    payment_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('inventories', lazy=True))

class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

class Category(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Supplier(db.Model, SerializerMixin):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.Text, nullable=False)

class SupplyRequest(db.Model, SerializerMixin):
    __tablename__ = 'supply_requests'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
