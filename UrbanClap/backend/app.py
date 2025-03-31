from flask import Flask, request, jsonify
from application.models import db, User
from flask_restful import Api
from application.Service_api import (
    ServiceListAPI, AdminServiceRequestsAPI, ServiceRequestAPI, ProfessionalProfileAPI,
    ReviewAPI, AdminUserManagementAPI, GetProfessionalsAPI, CustomerProfileAPI,
    ServiceManagementAPI, ExportServiceRequestsAPI
)
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from flask_cors import CORS
from datetime import timedelta
import os
from application.api import *
from application.Service_api import cache
import logging

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urbanclap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# Update CORS configuration to accept ports 5170-5179
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://127.0.0.1:5170",
            "http://127.0.0.1:5171",
            "http://127.0.0.1:5172",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:5175",
            "http://127.0.0.1:5176",
            "http://127.0.0.1:5177",
            "http://127.0.0.1:5178",
            "http://127.0.0.1:5179",
            "http://localhost:5170",
            "http://localhost:5171",
            "http://localhost:5172",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:5175",
            "http://localhost:5176",
            "http://localhost:5177",
            "http://localhost:5178",
            "http://localhost:5179"
        ]
    }
}, supports_credentials=True)

# Configure Redis and Cache
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# Initialize cache after config
cache.init_app(app)
api = Api(app)

# Initialize JWT
jwt = JWTManager(app)

# Configure Mail
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
mail = Mail(app)

# Configure Database
instance_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance")
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'database.sqlite3')
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Initialize Database
db.init_app(app)
app.app_context().push()

# Configure Logging
logging.basicConfig(level=logging.INFO)

# API Routes
api.add_resource(ServiceListAPI, '/api/services')
api.add_resource(ServiceRequestAPI, '/api/service-requests', '/api/service-requests/<int:request_id>')
api.add_resource(ProfessionalProfileAPI, '/api/professionalprofile')
api.add_resource(AdminUserManagementAPI, '/api/admin/users', '/api/admin/users/<int:user_id>')
api.add_resource(GetProfessionalsAPI, '/api/professionals')
api.add_resource(CustomerProfileAPI, "/api/customer/profile")
api.add_resource(ServiceManagementAPI, "/api/manageservices", "/api/manageservices/<int:request_id>")
api.add_resource(ReviewAPI, "/api/reviews", "/api/reviews/<int:service_request_id>")
api.add_resource(AdminServiceRequestsAPI, "/api/admin/service-requests")
api.add_resource(ExportServiceRequestsAPI, "/api/admin/export-service-requests")
api.add_resource(CityAPI, "/api/cities", "/api/cities/<int:city_id>")
api.add_resource(SignupAPI, "/api/signup")
api.add_resource(LoginAPI, "/api/login")

@app.route('/')
def hello():
    return "hello there"

@app.route('/send-email')
def send_email():
    msg = Message(
        'Hello from Flask',
        sender='no-reply@example.com',
        recipients=['recipient@example.com'],
        body='This is a test email from Flask.',
        html='<p>This is a <b>test email</b> from Flask.</p>'
    )
    mail.send(msg)
    return 'Email sent successfully!'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)