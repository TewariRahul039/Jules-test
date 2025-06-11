# This file will define the Product model using SQLAlchemy.
from .. import db # Assuming db is initialized in project/__init__.py

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True)
    stock_quantity = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Product {self.name} (ID: {self.id})>"

    def to_dict(self):
        """Serializes the product object to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'stock_quantity': self.stock_quantity
        }
