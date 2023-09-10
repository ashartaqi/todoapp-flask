import flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Note

views = Blueprint('views', __name__)


@login_required
@views.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        return render_template("home.html", user=current_user)

    if request.method == 'POST':
        note = request.form.get('note')
        print(note)
        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            if current_user.is_anonymous:
                flash("User not Logged in!", category="error")
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category='success')

    return render_template("home.html", user=current_user)
