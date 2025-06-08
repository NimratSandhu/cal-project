from datetime import datetime, timezone
from dateutil.parser import isoparse

from flask import Blueprint, render_template, request, jsonify
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

@main.route("/get_events_json", methods=["GET"])
def get_events_json():
    events = Event.query.all()
    event_list = []

    for event in events:
        event_list.append({
            "id": event.id,
            "title": event.name,
            "start": event.start_time.astimezone(timezone.utc).isoformat() if event.start_time else "",
            "end": event.end_time.astimezone(timezone.utc).isoformat() if event.end_time else "",
            "description": event.description,
        })

    return jsonify(event_list)

@main.route("/update_event", methods=["POST"])
def update_event():
    print("update event triggred")
    data = request.get_json()
    event_id = data.get("id")
    start = data.get("start")
    end = data.get("end")

    event = Event.query.get(event_id)
    print(event.id)
    if event:
        event.start_time = isoparse(start)
        event.end_time = isoparse(end) if end else None
        db.session.commit()
        print("success")
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 404

