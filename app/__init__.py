from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Load environment variables
app.config['S3_AWS_ACCESS_KEY_ID'] = os.getenv('S3_AWS_ACCESS_KEY_ID')
app.config['S3_AWS_SECRET_ACCESS_KEY'] = os.getenv('S3_AWS_SECRET_ACCESS_KEY')
app.config['BUCKET_NAME'] = 'chirpit-test' 

app.config['DYNAMODB_USER_CRED_ACCESS_KEY_ID'] = os.getenv('DYNAMODB_USER_CRED_ACCESS_KEY_ID')
app.config['DYNAMODB_USER_CRED_SECRET_ACCESS_KEY'] = os.getenv('DYNAMODB_USER_CRED_SECRET_ACCESS_KEY')


# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'


# Register blueprints
from app.home.routes import home_bp
from app.submit.routes import submit_bp
from app.timeline.routes import timeline_bp
from app.auth.routes import auth_bp

app.register_blueprint(home_bp)
app.register_blueprint(submit_bp)
app.register_blueprint(timeline_bp)
app.register_blueprint(auth_bp)

# Ensure models and forms are imported
# from app import models, forms
