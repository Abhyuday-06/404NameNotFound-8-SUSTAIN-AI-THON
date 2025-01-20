from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(min=2, max=50)],
        render_kw={"placeholder": "Your full name"}
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Your email address"}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Create a password"}
    )
    role = SelectField(
        'Role',
        choices=[
            ('user', 'User'),
            ('parent', 'Parent'),
            ('professional', 'Mental Health Professional'),
            ('student', 'Student'),
            ('teacher', 'Teacher'),
            ('counselor', 'School Counselor')
        ],
        validators=[DataRequired()]
    )
    child_registration_number = StringField(
        'Child Registration Number (Parents Only)',
        render_kw={"placeholder": "Child registration number"}
    )
    professional_id = StringField(
        'Professional ID (Professionals Only)',
        render_kw={"placeholder": "Professional ID proof"}
    )
    student_id = StringField(
        'Student ID (Students Only)',
        render_kw={"placeholder": "Your student ID"}
    )
    teacher_id = StringField(
        'Teacher ID (Teachers Only)',
        render_kw={"placeholder": "Your teacher ID"}
    )
    counselor_license = StringField(
        'Counselor License (School Counselors Only)',
        render_kw={"placeholder": "Counselor license or certification"}
    )
    submit = SubmitField('Sign Up')