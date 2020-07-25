from app import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    _id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(255), nullable=False)
    email = db.Column('email', db.String(255), nullable=False, unique=True)
    password = db.Column('password', db.String(255), nullable=False)

    def __init__(self, name, email, password):
        if not(name and email and password):
            raise Exception('Missing parameters.')
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        if not password:
            raise Exception('Password not entered.')
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"< User : {self.name} >"

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)