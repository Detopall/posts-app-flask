from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

from .models import User, Text

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Username does not exist", category="error")
            
        elif not check_password_hash(user.password, password):
            flash("Incorrect password", category="error")

        else:
            flash("Logged in successfully", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))
    return render_template("login.html", title="Login", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash("This user already exists", category="error")
        elif password1 != password2:
             flash("Passwords do not match", category="error")
        elif len(password1) < 7:
            flash("Password is less than 7", category="error")
        elif len(username) == 0:
            flash("Username is not filled in", category="error")
        else:
            new_user = User(password=generate_password_hash(password1, method="sha256"), username=username)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", title="Sign up", user=current_user)
    