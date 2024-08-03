from flask import Flask, request, jsonify, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config import app, db, api, login_manager
from models import Product, Category, User, Payment, SupplierProduct, SupplyRequest, Supplier, Transaction
from datetime import datetime

@app.route('/')
def index():
    return '<h1>WELCOME !!</h1>'

@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 422

    if role not in ['Admin', 'User']:
        return jsonify({"error": "Invalid role"}), 422

    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role=role
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        message = "Admin created successfully" if role == 'Admin' else "User created successfully"
        return jsonify({"message": message}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    login_user(user)
    return jsonify({'success': True, 'message': 'Login successful'})

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/checksession', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users/<int:user_id>', methods=['GET', 'PATCH'])
def manage_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        return jsonify(user.to_dict())

    elif request.method == 'PATCH':
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

        return jsonify({"error": "Invalid data"}), 400

@app.route('/user', methods=['GET'])
@login_required
def user_details():
    user_id = current_user.id
    user = User.query.get(user_id)
    return make_response(jsonify(user.to_dict()), 200)

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user = current_user
    transactions = Transaction.query.filter_by(user_id=user.id).all()
    transaction_history = [transaction.to_dict() for transaction in transactions]
    activities = get_user_activities(user.id)

    user_profile = {
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at,
        'transaction_history': transaction_history,
        'activities': activities
    }

    return jsonify(user_profile), 200

def get_user_activities(user_id):
    activities = [
        {'activity': 'Logged in', 'timestamp': datetime.utcnow()},
        {'activity': 'Made a purchase', 'timestamp': datetime.utcnow()},
    ]
    return activities

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_detail(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    if request.method == 'GET':
        return jsonify(product.to_dict())

    elif request.method == 'PUT':
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

        try:
            db.session.commit()
            return jsonify(product.to_dict()), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/create_product', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    category_id = data.get('category_id')
    bp = data.get('bp')
    sp = data.get('sp')

    if not all([name, category_id, bp, sp]):
        return jsonify({'error': 'Missing data'}), 400

    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    new_product = Product(
        name=name,
        category_id=category_id,
        bp=bp,
        sp=sp
    )

    try:
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/payment', methods=['GET', 'POST'])
def manage_payment():
    if request.method == 'GET':
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments])

    elif request.method == 'POST':
        data = request.get_json()
        inventory_id = data.get('inventory_id')
        amount = data.get('amount')
        payment_date_str = data.get('payment_date')

        if inventory_id is None:
            return jsonify({'error': 'Missing inventory_id'}), 400
        if amount is None:
            return jsonify({'error': 'Missing amount'}), 400
        if payment_date_str is None:
            return jsonify({'error': 'Missing payment_date'}), 400

        try:
           
            payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid payment_date format'}), 400

        try:
            amount = float(amount)
        except ValueError:
            return jsonify({'error': 'Invalid amount format'}), 400
        
        payment = Payment(
            inventory_id=inventory_id,
            amount=amount,
            payment_date=payment_date
        )
        try:
            db.session.add(payment)
            db.session.commit()
            return jsonify({'message': 'Payment made successfully'}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@app.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    return jsonify([product.to_dict() for product in products])

@app.route('/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers])

@app.route('/supplyrequests', methods=['GET'])
def get_supply_requests():
    supply_requests = SupplyRequest.query.all()
    return jsonify([request.to_dict() for request in supply_requests])

if __name__ == '__main__':
    app.run(port=5555, debug=True)
