from app import db, ma

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(255), nullable=False)
    price = db.Column('price', db.Float, nullable=False)
    cost = db.Column('cost', db.Float, nullable=False)

    def __init__(self, name, price, cost):
        if not(name and price and cost):
            raise Exception('Missing parameters.')
        self.name = name
        self.price = price
        self.cost = cost

    def __repr__(self):
        return f'< Product : {self.name} >'
    

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)