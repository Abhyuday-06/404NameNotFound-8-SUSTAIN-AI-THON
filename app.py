# Full implementation of the mental health platform using Flask
"""
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_mail import Mail, Message
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_health.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_password'

db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # student, teacher, parent, counselor, professional
    approved = db.Column(db.Boolean, default=False)  # For professionals
    child_registration_number = db.Column(db.String(50), nullable=True)  # For parents

# Forms
class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('student', 'Student'), ('teacher', 'Teacher'), 
                                        ('parent', 'Parent'), ('counselor', 'School Counselor'), 
                                        ('professional', 'Mental Health Professional')], validators=[DataRequired()])
    child_registration_number = StringField('Child Registration Number (For Parents)')
    professional_id = FileField('Professional ID Proof (For Professionals)')
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, 
                    password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Await approval for professionals.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return render_template('student_dashboard.html')
    elif current_user.role == 'teacher':
        return render_template('teacher_dashboard.html')
    elif current_user.role == 'parent':
        return render_template('parent_dashboard.html')
    elif current_user.role == 'counselor':
        return render_template('counselor_dashboard.html')
    elif current_user.role == 'professional':
        return render_template('professional_dashboard.html')
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Quiz Submission and Analysis
@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        answers = request.form
        # Placeholder for ML model analysis logic
        result = analyze_mental_health(answers)  # Implement your analysis logic
        return render_template('result.html', result=result)
    return render_template('quiz.html')

# Google Calendar Integration
@app.route('/schedule_appointment', methods=['POST'])
@login_required
def schedule_appointment():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=['https://www.googleapis.com/auth/calendar'])
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Mental Health Appointment',
        'start': {'dateTime': '2025-01-20T10:00:00Z', 'timeZone': 'UTC'},
        'end': {'dateTime': '2025-01-20T11:00:00Z', 'timeZone': 'UTC'},
        'attendees': [{'email': 'student@example.com'}],
    }
    service.events().insert(calendarId='primary', body=event).execute()
    flash('Appointment scheduled successfully.', 'success')
    return redirect(url_for('dashboard'))

# Utility functions
def analyze_mental_health(answers):
    # Placeholder for mental health analysis logic (e.g., ML model integration)
    return {'status': 'Good', 'recommendation': 'Maintain a healthy routine.'}

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    app.run(debug=True)
"""

# app.py - Entry point for the Flask application

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from routes import auth_bp, dashboard_bp, error_bp, reports_bp
from config import Config
from utils import create_app

# Initialize the Flask application
app = create_app()
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# User loader function
@login_manager.user_loader
def load_user(user_id):
    user =  User.query.get(int(user_id))
    if user:
        print(f"User loaded: {user.name} (ID: {user.id})")
    else:
        print(f"No user found with ID: {user_id}")
    return user

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(error_bp)
app.register_blueprint(reports_bp)

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Run the application
if __name__ == '__main__':
    with app.app_context():
        # Ensure the database tables are created
        db.create_all()
    app.run(debug=True)
