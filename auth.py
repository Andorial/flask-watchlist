from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models import User
from forms import LoginForm, RegisterForm

auth = Blueprint("auth", __name__)


#Login
@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("watchlist.show_watchlist"))
        else:
            flash("Invalid username or password")

    return render_template("login.html", form=form)


#Register
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("User with this name already existing")
            return redirect(url_for("auth.register"))
        
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=16)
        new_user = User(username=form.username.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html", form=form)


#Logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))