from unicodedata import category
from flask import Blueprint, render_template, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Text, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        text = request.form.get("text")
        if len(text) < 1:
            flash("Text is too short", category="error")
        else:
            new_text = Text(data=text, user_id=current_user.id)
            db.session.add(new_text)
            db.session.commit()          
            flash("Text added!", category="success")
    return render_template("home.html", title="Home", username=current_user.username, user=current_user)

@views.route("/delete-text", methods=["DELETE"])
def delete_text():
    text = json.loads(request.data)
    textId = text['textId']
    text = Text.query.get(textId)
    if text:
        if text.user_id == current_user.id:
            db.session.delete(text)
            db.session.commit()
            flash("Text deleted!", category="success")

    return jsonify({})


@views.route("/friends")
def show_friends():
    user_list = User.query.all()
    return render_template("friends.html", user=current_user, username=current_user.username, title="Friends", user_list=user_list)