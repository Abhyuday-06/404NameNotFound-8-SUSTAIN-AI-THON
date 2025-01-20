from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, logout_user
from forms import LoginForm, SignupForm
from models import db, User

routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return render_template("base.html")

@routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            flash("Logged in successfully!", "success")
            return redirect(url_for("routes.dashboard"))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template("auth/login.html", form=form)

@routes.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            password=form.password.data,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("routes.login"))
    return render_template("auth/signup.html", form=form)

@routes.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "student":
        return render_template("dashboard/student_dashboard.html")
    # Add role-based logic here for other dashboards
    return render_template("dashboard/default_dashboard.html")

@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("routes.home"))
