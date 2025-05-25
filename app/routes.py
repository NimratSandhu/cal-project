from flask import Blueprint, render_template, request
from .models import Event
from . import db

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/add_event", methods=["POST"])
def add_event():
    new_event = Event(name="Sample Event")
    db.session.add(new_event)
    db.session.commit()
    print("Event Added!")
    return "Event Added"

