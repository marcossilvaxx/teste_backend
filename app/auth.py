from functools import wraps

import jwt
from flask import current_app, jsonify, request

from app.models.User import User, user_schema

def jwt_protected(func):
    @wraps(func)
    
    def wrapper(*args, **kwargs):

        token = None

        if 'authorization' in request.headers:
            token = request.headers['authorization']
        
        if not token:
            return jsonify({"error": "Not authorized."}), 401

        if not 'Bearer' in token:
            return jsonify({"error": "Invalid token."}), 401

        try:
            token_pure = token.replace("Bearer ", "")

            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(_id=decoded['id']).first()
        except:
            return jsonify({"error": "Invalid token."}), 401

        return func(current_user, *args, **kwargs)
    
    return wrapper