from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("admin", "customer", "professional", name="user_role_enum"), nullable=False)
    is_blocked = db.Column(db.Boolean, default="unblocked")  
    is_verified = db.Column(db.Boolean, nullable=False, default=lambda context: 
        "verified" if context.get_current_parameters()["role"] in ["admin", "customer"] else "unverified")  
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    customer_profile = db.relationship("Customer", back_populates="user", uselist=False)
    professional_profile = db.relationship("ServiceProfessional", back_populates="user", uselist=False)
    notifications = db.relationship("Notification", back_populates="user", lazy=True)
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  
    phone = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    user = db.relationship("User", back_populates="customer_profile")
    service_requests = db.relationship("ServiceRequest", back_populates="customer", lazy=True)
    transactions = db.relationship("Transaction", back_populates="customer", lazy=True)
    reviews = db.relationship("Review", back_populates="customer", lazy=True)
    city = db.relationship("City", back_populates="customers")
class ServiceProfessional(db.Model):
    __tablename__ = 'service_professionals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  
    phone = db.Column(db.String(15), unique=True, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False) 
    experience = db.Column(db.Float, nullable=True, default=0)
    rating = db.Column(db.Integer, nullable=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="professional_profile")
    service_requests = db.relationship("ServiceRequest", back_populates="professional", lazy=True)
    reviews = db.relationship("Review", back_populates="professional", lazy=True)
    city = db.relationship("City", back_populates="professionals")
    service_addition_requests = db.relationship("ServiceAdditionRequest", back_populates="professional_profile", lazy=True)
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    service_requests = db.relationship("ServiceRequest", back_populates="service", lazy=True)
class ServiceAdditionRequest(db.Model):
    __tablename__ = 'service_addition_requests'
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id'), nullable=False)  
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="pending")
    professional_profile = db.relationship("ServiceProfessional", back_populates="service_addition_requests")
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id'), nullable=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_completion = db.Column(db.DateTime, nullable=True)
    service_status = db.Column(db.String(255), default="requested")
    pin = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)  
    service = db.relationship("Service", back_populates="service_requests")
    customer = db.relationship("Customer", back_populates="service_requests")
    professional = db.relationship("ServiceProfessional", back_populates="service_requests")
    transactions = db.relationship("Transaction", back_populates="service_request", lazy=True)
    city = db.relationship("City", back_populates="service_requests")
    review = db.relationship("Review", back_populates="service_request", uselist=False) 
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(255), default="pending")
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.Column(db.String(255), default="Unknown")
    customer = db.relationship("Customer", back_populates="transactions")
    service_request = db.relationship("ServiceRequest", back_populates="transactions")
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    service_request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)  
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professionals.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)  
    comment = db.Column(db.Text, nullable=False, default="")  
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    customer = db.relationship("Customer", back_populates="reviews")
    professional = db.relationship("ServiceProfessional", back_populates="reviews")
    service_request = db.relationship("ServiceRequest", back_populates="review")  
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", back_populates="notifications")
class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(100), nullable=False, unique=True)  
    pincode = db.Column(db.String(20), nullable=False)  
    customers = db.relationship("Customer", back_populates="city", lazy=True)
    professionals = db.relationship("ServiceProfessional", back_populates="city", lazy=True)
    service_requests = db.relationship("ServiceRequest", back_populates="city", lazy=True)
