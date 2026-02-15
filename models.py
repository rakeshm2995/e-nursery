from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    pincode = db.Column(db.String(10))
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    cart_items = db.relationship('Cart', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Plant(db.Model):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Medicinal, Flower, Vegetable, Fruit
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    sunlight = db.Column(db.String(50))
    water = db.Column(db.String(50))
    care_instructions = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200), default='default_plant.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reviews = db.relationship('Review', backref='plant', lazy=True)
    wishlists = db.relationship('Wishlist', backref='plant', lazy=True)

    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)

    @property
    def is_low_stock(self):
        return 0 < self.stock <= 5

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    def __repr__(self):
        return f'<Plant {self.name}>'


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Fertilizer, Soil, Pot, Tools, Seeds
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    usage_instructions = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200), default='default_ingredient.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def is_low_stock(self):
        return 0 < self.stock <= 5

    @property
    def is_out_of_stock(self):
        return self.stock == 0

    def __repr__(self):
        return f'<Ingredient {self.name}>'


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'plant' or 'ingredient'
    item_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_item(self):
        if self.item_type == 'plant':
            return Plant.query.get(self.item_id)
        else:
            return Ingredient.query.get(self.item_id)

    @property
    def subtotal(self):
        item = self.get_item()
        if item:
            return item.price * self.quantity
        return 0

    def __repr__(self):
        return f'<Cart User:{self.user_id} Item:{self.item_type}:{self.item_id}>'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.String(50), default='Pending')
    payment_status = db.Column(db.String(50), default='Pending')
    payment_method = db.Column(db.String(50))
    tracking_number = db.Column(db.String(50), unique=True)
    shipping_address = db.Column(db.Text)
    estimated_delivery = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def generate_tracking_number(self):
        self.tracking_number = f"ENO{secrets.token_hex(6).upper()}"

    def __repr__(self):
        return f'<Order {self.id} User:{self.user_id}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)  # 'plant' or 'ingredient'
    item_id = db.Column(db.Integer, nullable=False)
    item_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} {self.item_type}:{self.item_id}>'


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Wishlist User:{self.user_id} Plant:{self.plant_id}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review User:{self.user_id} Plant:{self.plant_id} Rating:{self.rating}>'