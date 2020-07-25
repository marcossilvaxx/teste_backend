from app import app, db
from flask import jsonify, request, make_response
import datetime
import jwt
from app.models.Product import Product, product_schema, products_schema
from app.models.User import User, user_schema

from app.auth import jwt_protected

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Hello World'})

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json

    if not('name' in data and 'email' in data and 'password' in data):
        return jsonify({ "error": "Bad request. Missing fields." }), 400

    user = User(data['name'], data['email'], data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({ "message": "User successfully registered!" }), 200

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json

    if not('email' in data and 'password' in data):
        return jsonify({ "error": "Bad request. Missing fields." }), 400

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return jsonify({ "error": "Invalid credentials." }), 401

    payload = {
        "id": user._id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'])

    return jsonify({ "token": token.decode('utf-8') }), 200

@app.route('/products', methods=['GET', 'POST'])
@app.route('/products/<int:id>', methods=['PUT', 'DELETE'])
@jwt_protected
def products(current_user, id=None):
    if request.method == 'GET':
        all_products = Product.query.all()
        return jsonify(products_schema.dump(all_products)), 200

    elif request.method == 'POST':
        data = request.json

        if not('name' in data and 'price' in data and 'cost' in data):
            return jsonify({ "error": "Bad request. Missing fields." }), 400

        product = Product(data['name'], data['price'], data['cost'])
        db.session.add(product)
        db.session.commit()
        return jsonify({ "message": "Product was registered" }), 200

    elif request.method == 'PUT':
        data = request.json

        if not data:
            return jsonify({ "error": "Bad request. Updating without fields." }), 400

        old_product = Product.query.filter_by(id=id).first()

        if not old_product:
            return jsonify({ "error": "Product not found." }), 404

        if 'name' in data:
            old_product.name = data['name']
        
        if 'price' in data:
            old_product.price = data['price']

        if 'cost' in data:
            old_product.cost = data['cost']

        db.session.commit()

        return jsonify({ "message": "Product was updated" }), 200

    elif request.method == 'DELETE':
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({ "error": "Product not found." }), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({ "message": "Product was removed" }), 200