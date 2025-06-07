from flask import Blueprint, render_template, request
from .models import Event
from . import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/add_event", methods=["POST"])
def add_event():
    name = request.form.get("name")
    description = request.form.get("description")
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")

    new_event = Event(
        name=name,
        description=description,
        start_time=start_time,
        end_time=end_time,
    )
    db.session.add(new_event)
    db.session.commit()
    print("Event Added!")
    return "Event Added"


@main.route("/get_events", methods=["GET"])
def get_events():
    events = Event.query.order_by(Event.start_time).all()
    return render_template("events_list.html", events=events)