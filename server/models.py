import datetime
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine
from config import db
from flask_login import UserMixin

class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)  
    inventory_id = db.Column(db.Integer, ForeignKey("inventory.id"), nullable=False)
    transaction_type = db.Column(String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='transactions')

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    bp = db.Column(db.Float, nullable=False)
    sp = db.Column(db.Float, nullable=False)
    category = db.relationship('Category', back_populates='products')
    inventory_items = db.relationship('Inventory', back_populates='product', cascade='all, delete-orphan')
    serialize_rules = ('-inventory_items.product',)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'bp': self.bp,
            'sp': self.sp
        }

class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    spoilt_quantity = db.Column(db.Integer, nullable=False, default=0)
    payment_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    product = db.relationship('Product',back_populates='inventory_items', lazy=True)

class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at
        }

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', back_populates='category')
    serialize_rules = ('-products.category',)
    description = db.Column(db.String(200), nullable=True)



class Supplier(db.Model, SerializerMixin):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.Text, nullable=False)


class SupplyRequest(db.Model, SerializerMixin):
    __tablename__ = 'supply_requests'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Payment(db.Model, SerializerMixin):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey("inventory.id"), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    def to_dict(self):
        return {
            'id': self.id,
            'inventory_id': self.inventory_id,
            'amount': self.amount,
            'payment_date': self.payment_date.strftime('%Y-%m-%d') 
        }


class SupplierProduct(db.Model):
    __tablename__ = "supplier_products"
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    supplier = db.relationship(
        "Supplier",
        backref=db.backref("supplier_products", cascade="all, delete-orphan"),
    )
    product = db.relationship(
        "Product", backref=db.backref("supplier_products", cascade="all, delete-orphan")
    )


class ProductCategory(db.Model):
    __tablename__ = "product_categories"
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship(
        "Product",
        backref=db.backref("product_categories", cascade="all, delete-orphan"),
    )
    category = db.relationship(
        "Category",
        backref=db.backref("product_categories", cascade="all, delete-orphan"),
    )
