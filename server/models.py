from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db


class products (db.models,SerializerMixin);
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('categories', backref=db.backref('products', lazy=True))
    orders = association_proxy('order_items', 'product')
    # Add more columns as needed!
    def __repr__(self):
        return f'<Product {self.name}>'
class shop(db.models,SerializerMixin)
    id = db.column(db.integer,primary_key=True)
# Models go here!


class merchants(db.models,SerializerMixin)
    #Models go here

class user(db.models)