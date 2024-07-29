from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

class Product(db.Model, SerializerMixin):
    prod_id = db.Column(db.Integer, primary_key= True)
    prod_name = db.Column(db.String(20), nullable = False)
    prod_name = db.Column(db.String(20),unique = True ,nullable = False)
    prod_qty = db.Column(db.Integer, nullable = False)
    def __repr__(self):
        return f"Product('{self.prod_id}','{self.prod_name}','{self.prod_qty}')"




# Define your models here!
class user(db.model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.string(100),nullable=False)

class category(db.model,SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.string,primary_key=True)
    items = db.relationship('item', backref='category', lazy=True)
    description = db.Column(db.string,primary_key=True)

    
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.Text, nullable=False)

class SupplyRequest(db.Model):
    __tablename__ = 'supply_requests'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)