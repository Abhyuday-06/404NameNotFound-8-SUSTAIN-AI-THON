from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from models import db, User
from forms import LoginForm, SignupForm

# Authentication Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard.home'))
        flash('Invalid email or password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        role = form.role.data

        # Conditional validation
        if role == 'parent' and not form.child_registration_number.data:
            flash('Child Registration Number is required for Parents.', 'error')
        elif role == 'professional' and not form.professional_id.data:
            flash('Professional ID is required for Mental Health Professionals.', 'error')
        elif role == 'student' and not form.student_id.data:
            flash('Student ID is required for Students.', 'error')
        elif role == 'teacher' and not form.teacher_id.data:
            flash('Teacher ID is required for Teachers.', 'error')
        elif role == 'counselor' and not form.counselor_license.data:
            flash('Counselor License is required for School Counselors.', 'error')
        else:
            # Proceed with user creation
            flash('Signup successful!', 'success')
            return redirect(url_for('home'))

    return render_template('auth/signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# Dashboard Blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    if current_user.role == 'student':
        return render_template('dashboard/student_dashboard.html')
    elif current_user.role == 'teacher':
        return render_template('dashboard/teacher_dashboard.html')
    elif current_user.role == 'parent':
        return render_template('dashboard/parent_dashboard.html')
    elif current_user.role == 'counselor':
        return render_template('dashboard/counselor_dashboard.html')
    elif current_user.role == 'professional':
        return render_template('dashboard/professional_dashboard.html')
    return redirect(url_for('auth.login'))

# Reports Blueprint
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        answers = request.form
        result = analyze_mental_health(answers)
        return render_template('reports/result.html', result=result)
    return render_template('reports/quiz.html')

@reports_bp.route('/appointment')
@login_required
def appointment():
    return render_template('reports/appointment.html')

# Error Handling Blueprint (Optional for Error Views)
error_bp = Blueprint('error', __name__)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@error_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500

