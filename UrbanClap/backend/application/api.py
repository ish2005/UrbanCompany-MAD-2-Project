from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from application.models import db, User, Customer, ServiceProfessional, Admin,City  
import re
from datetime import datetime
from application.Service_api import cache
def custom_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
class CityAPI(Resource):
    @cache.cached(timeout=50)
    def get(self):
        cities = City.query.all()
        return {
            "cities": [{
                "id": city.id,
                "name": city.name,
                "pincode": city.pincode
            } for city in cities]
        }, 200
    @jwt_required()
    def post(self):
        user = User.query.get(get_jwt_identity())
        if user.role != 'admin':
            return {"message": "Unauthorized"}, 403
        data = request.get_json()
        city_name = data.get("name")
        pincode = data.get("pincode")
        if not city_name or not pincode:
            return {"message": "City name and pincode are required"}, 400
        if City.query.filter_by(name=city_name).first():
            return {"message": "City already exists"}, 400
        new_city = City(name=city_name, pincode=pincode)
        db.session.add(new_city)
        db.session.commit()
        return {"message": "City added successfully", "city_id": new_city.id}, 201
    @jwt_required()
    def put(self, city_id):
        user = User.query.get(get_jwt_identity())
        if user.role != 'admin':
            return {"message": "Unauthorized"}, 403
        city = City.query.get(city_id)
        if not city:
            return {"message": "City not found"}, 404
        data = request.get_json()
        city_name = data.get("name", city.name)
        pincode = data.get("pincode", city.pincode)
        if city_name != city.name and City.query.filter_by(name=city_name).first():
            return {"message": "A city with this name already exists"}, 400
        city.name = city_name
        city.pincode = pincode
        db.session.commit()
        return {"message": "City updated successfully"}, 200
    @jwt_required()
    def delete(self, city_id):
        user = User.query.get(get_jwt_identity())
        if user.role != 'admin':
            return {"message": "Unauthorized"}, 403
        city = City.query.get(city_id)
        if not city:
            return {"message": "City not found"}, 404
        db.session.delete(city)
        db.session.commit()
        return {"message": "City deleted successfully"}, 200
class SignupAPI(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password') or not data.get('role'):
            return {"message": "Email, password, and role are required"}, 400
        email = data['email']
        password_hash = generate_password_hash(data['password'])
        role = data['role']
        city_id = data.get('city_id')  
        if role in ["customer", "professional"] and not city_id:
            return {"message": "city_id is required for customers and professionals"}, 400
        if city_id and not City.query.get(city_id):
            return {"message": "Invalid or unsupported city selected"}, 400
        if User.query.filter_by(email=email).first():
            return {"message": "Email already registered"}, 400
        is_verified = True if role in ["admin", "customer"] else False
        new_user = User(
            email=email,
            username=data.get('username', email),
            password_hash=password_hash,
            role=role,
            is_verified=is_verified, 
            is_blocked=False, 
            created_on=datetime.utcnow()
        )
        db.session.add(new_user)
        db.session.commit()  
        if role == "customer":
            customer_profile = Customer(
                user_id=new_user.id,
                name=data.get('name', 'Unknown'),
                email=email,
                phone=data.get('phone', '0000000000'),
                address=data.get('address', 'Not Provided'),
                city_id=city_id
            )
            db.session.add(customer_profile)
        elif role == "professional":
            professional_profile = ServiceProfessional(
                user_id=new_user.id,
                name=data.get('name', 'Unknown'),
                email=email,
                phone=data.get('phone', '0000000000'),
                service_type=data.get('service_type'),
                experience=data.get('experience', 0),
                city_id=city_id
            )
            db.session.add(professional_profile)
        elif role == "admin":
            admin = Admin(
                username=data.get('username', email),
                password_hash=password_hash
            )
            db.session.add(admin)
        db.session.commit() 
        return {"message": "Signup successful", "user_id": new_user.id}, 201
class LoginAPI(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return {"message": "Email and password are required"}, 400
        email = data['email']
        password = data['password']
        if not custom_email(email):
            return {"message": "Invalid email format"}, 400
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return {"message": "Invalid email or password"}, 401
        if not user.is_verified:
            return {"message": "Your verification is pending by admin"}, 403
        if user.is_blocked:
            return {"message": "Your account is blocked by admin"}, 403
        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        response = {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "token": token,
                "email": user.email,
                "username": user.username,
                "role": user.role
            }
        }
        if user.role == "customer":
            customer = Customer.query.filter_by(user_id=user.id).first()
            if customer:
                response["user"]["name"] = customer.name
                response["user"]["phone"] = customer.phone
                response["user"]["address"] = customer.address
        elif user.role == "professional":
            professional = ServiceProfessional.query.filter_by(user_id=user.id).first()
            if professional:
                response["user"]["name"] = professional.name
                response["user"]["phone"] = professional.phone
                response["user"]["service_type"] = professional.service_type
                response["user"]["experience"] = professional.experience
        elif user.role == "admin":
            admin = Admin.query.filter_by(username=user.username).first()
            if admin:
                response["user"]["username"] = admin.username
        return response, 200
