from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
ma = Marshmallow(app)

Migrate(app, db)

from .routes import routes
from .models import User, Product
