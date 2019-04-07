from flask import Flask, render_template, redirect
from datetime import datetime
import json

import query

app = Flask(__name__)

query.init_database()

@app.route("/record_feed", methods = ["POST"])
def record_feed():
    query.add_feed_to_db()
    return redirect("/")


@app.route("/get_last_feed", methods = ["GET"])
def get_last_feed():
    query.add_check_to_db()
    last_feed = query.get_feed_from_db()[0]
    last_feed_json = json.dumps(last_feed)
    return last_feed_json


@app.route("/get_feed_history", methods = ["GET"])
def get_feed_history():
    query.add_check_to_db()
    feed_history = query.get_feed_from_db()
    feed_history_json = json.dumps(feed_history)
    return feed_history_json


@app.route("/get_check_history", methods = ["GET"])
def get_check_history():
    check_history = query.get_check_from_db()
    check_history_json = json.dumps(check_history)
    return check_history_json


def generate_title_text():
    last_feed = query.get_feed_from_db()[0][0]
    last_feed_time = datetime.fromisoformat(last_feed)
    # Convert the time difference from seconds to hours
    current_time = datetime.now()
    time_difference = current_time - last_feed_time
    time_difference_hours = time_difference.total_seconds() / 3600
    
    if time_difference_hours < 1:
        return "The cat was <i>just</i> fed."
    elif time_difference_hours < 2:
        return "The cat was fed 1 hour ago."
    else:
        rounded_difference = "{:.0f}".format(round(time_difference_hours))
        return "The cat was fed {} hours ago.".format(rounded_difference)


def generate_subtitle_text():
    last_feed = query.get_feed_from_db()[0][0]
    last_feed_time = datetime.fromisoformat(last_feed)
    current_time = datetime.now()
    
    # Selects from two strings, if not in range then prints alternative
    days = ["Today", "Yesterday"]
    day_index = abs(last_feed_time.day - current_time.day)
    if day_index < len(days):
        return "{} at {}".format(days[day_index], last_feed_time.strftime("%I:%M %p"))
    else:
        return last_feed_time.strftime("%a %x at %I:%M %p")


@app.route("/get_last_feed_string", methods = ["GET"])
def get_last_feed_string():
    last_time = get_last_feed()
    title_text = generate_title_text()
    subtitle_text = generate_subtitle_text()
    return json.dumps({"title": title_text, "subtitle": subtitle_text})


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)