from flask import Flask, render_template, redirect, jsonify
from datetime import datetime
import json
import requests

import query

ENDPOINT = "https://asia-northeast1-test-2bfef.cloudfunctions.net/time"


app = Flask(__name__)

query.init_database()


def last_feed():
    response = requests.get(ENDPOINT)
    response.raise_for_status()
    time = datetime.fromtimestamp(response.json()["time"] / 1000)
    return time


@app.route("/record_feed", methods=["POST"])
def record_feed():
    query.add_feed_to_db()

    r = requests.post(ENDPOINT, json={
        "time": datetime.now().timestamp() * 1000
    })
    r.raise_for_status()

    return redirect("/")


@app.route("/get_last_feed", methods=["GET"])
def get_last_feed():
    query.add_check_to_db()
    feed = last_feed()
    feed_json = jsonify([feed.isoformat()])
    return feed_json


@app.route("/get_feed_history", methods=["GET"])
def get_feed_history():
    query.add_check_to_db()
    feed_history = query.get_feed_from_db()
    feed_history_json = json.dumps(feed_history)
    return feed_history_json


@app.route("/get_check_history", methods=["GET"])
def get_check_history():
    check_history = query.get_check_from_db()
    check_history_json = json.dumps(check_history)
    return check_history_json


@app.route("/get_last_feed_string", methods=["GET"])
def get_last_feed_string():
    feed = last_feed()
    title_text = generate_title_text(feed)
    subtitle_text = generate_subtitle_text(feed)
    return json.dumps({"title": title_text, "subtitle": subtitle_text})


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def generate_title_text(last_feed_time):
    # Convert the time difference from seconds to hours
    current_time = datetime.now()
    time_difference = current_time - last_feed_time
    time_difference_hours = time_difference.total_seconds() / 3600

    if time_difference_hours < 1:
        return "The cat was just fed."
    elif time_difference_hours < 2:
        return "The cat was fed 1 hour ago."
    else:
        rounded_difference = "{:.0f}".format(round(time_difference_hours))
        return "The cat was fed {} hours ago.".format(rounded_difference)


def generate_subtitle_text(last_feed_time):
    current_time = datetime.now()

    # Selects from two strings, if not in range then prints alternative
    days = ["Today", "Yesterday"]
    day_index = abs(last_feed_time.day - current_time.day)
    if day_index < len(days):
        time_string = last_feed_time.strftime("%I:%M %p")
        return "{} at {}".format(days[day_index], time_string)
    else:
        return last_feed_time.strftime("%a %x at %I:%M %p")


if __name__ == "__main__":
    app.run(debug=True)
