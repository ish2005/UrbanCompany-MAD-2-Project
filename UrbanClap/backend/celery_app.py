from celery import Celery
from flask import Flask, render_template
from flask_mail import Mail, Message
from application.models import User, db
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure Database
instance_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "instance")
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_dir, 'database.sqlite3')

# Configure Mail
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None

# Initialize extensions
db.init_app(app)
mail = Mail(app)

# Initialize Celery
celery_app = Celery('urbanclap')
celery_app.config_from_object('celery_config')

# Create task context
class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask

@celery_app.task(name='celery_app.test_task')
def test_task():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Test task running at {current_time}!")
    return f"Test task completed at {current_time}!"

@celery_app.task(name='celery_app.send_daily_reminders')
def send_daily_reminders():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Starting daily reminders at {current_time}")
    try:
        professionals = User.query.filter_by(role='professional').all()
        logger.info(f"Found {len(professionals)} professionals")
        for professional in professionals:
            html = render_template('daily_reminder.html', username=professional.username)
            msg = Message(
                subject="Daily Reminder",
                sender="noreply@example.com",
                recipients=[professional.email],
                html=html
            )
            logger.info(f"Sending daily reminder to {professional.email}")
            mail.send(msg)
        logger.info(f"Completed sending daily reminders at {current_time}")
        return f"Daily reminders sent at {current_time}!"
    except Exception as e:
        logger.error(f"Error sending daily reminders: {str(e)}")
        raise

@celery_app.task(name='celery_app.send_monthly_report')
def send_monthly_report():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Starting monthly reports at {current_time}")
    try:
        customers = User.query.filter_by(role='customer').all()
        logger.info(f"Found {len(customers)} customers")
        current_month = datetime.now().strftime("%B")
        current_year = datetime.now().year
        
        for customer in customers:
            # Here you would typically get these stats from your database
            # For now, we'll use dummy data
            stats = {
                'username': customer.username,
                'month': current_month,
                'year': current_year,
                'total_requests': 5,
                'completed_services': 3,
                'pending_services': 2,
                'average_rating': 4.5
            }
            
            html = render_template('monthly_report.html', **stats)
            msg = Message(
                subject="Monthly Report",
                sender="noreply@example.com",
                recipients=[customer.email],
                html=html
            )
            logger.info(f"Sending monthly report to {customer.email}")
            mail.send(msg)
        logger.info(f"Completed sending monthly reports at {current_time}")
        return f"Monthly reports sent at {current_time}!"
    except Exception as e:
        logger.error(f"Error sending monthly reports: {str(e)}")
        raise 