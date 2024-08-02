#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource
from models import Product,Category,User
# Local imports  SQLAlchemyError
from config import app, db, api
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from flask import request, jsonify, session,make_response
from werkzeug.security import generate_password_hash, check_password_hash
# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 422

    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role="User"  # Default role
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    session['user_id'] = user.id
    return jsonify({'success': True, 'message': 'Login successful'})

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/checksession', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route("/users/<int:user_id>", methods=["GET", "PATCH"])
def get_user(user_id):
    if request.method == "GET":
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user.to_dict())
    elif request.method == "PATCH":
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()
        role = data.get('role')

        if role is not None:
            user.role = role
            try:
                db.session.commit()
                return jsonify(user.to_dict()), 200
            except SQLAlchemyError as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 500

        return jsonify({"error": "Invalid data"}), 404

@app.route('/user', methods=['GET'])
def user_details():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(user_id)
    return make_response(jsonify(user.to_dict()), 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)

@app.route('/product',method=['Get'])
def get_product():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_detail(product_id):
    if request.method == 'GET':
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product.to_dict())
    elif request.method == 'PUT':
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        data = request.get_json()
        name = data.get('name')
        category_id = data.get('category_id')
        bp = data.get('bp')
        sp = data.get('sp')

        if name is not None:
            product.name = name
        if category_id is not None:
            product.category_id = category_id
        if bp is not None:
            product.bp = bp
        if sp is not None:
            product.sp = sp

@app.route('./payment',method=['Get','Post'])
def make_payment():
    if request.method == 'GET':
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments])
    elif request.method == 'POST':
        data = request.get_json()
        inventory_id = data.get('inventory_id')
        amount = data.get('amount')
        payment_date = data.get('payment_date')

        if inventory_id is not None and amount is not None and payment_date is not None:
            payment = Payment(
                inventory_id=inventory_id,
                amount=amount,
                payment_date=payment_date
            )
            db.session.add(payment)
            db.session.commit()
            return jsonify({'message': 'Payment made successfully'}), 201
        else:
            return jsonify({'error': 'Invalid data'}), 400 
        
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_data = [product.to_dict() for product in products]
    return make_response(jsonify(products_data), 200)

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_data = [category.to_dict() for category in categories]
    return make_response(jsonify(categories_data), 200)

@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    suppliers_data = [supplier.to_dict() for supplier in suppliers]
    return make_response(jsonify(suppliers_data), 200)

@app.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    products_data = [product.to_dict() for product in products]
    return make_response(jsonify(products_data), 200)

@app.route('/supplyrequests', methods=['GET'])
def get_supply_requests():
    supply_requests = SupplyRequest.query.all()
    supply_requests_data = [request.to_dict() for request in supply_requests]
    return make_response(jsonify(supply_requests_data), 200)                  