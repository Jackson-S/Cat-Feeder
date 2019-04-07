from flask import Flask, request, render_template, redirect
from datetime import datetime, timezone
import json
import sqlite3

app = Flask(__name__)
database_name = "./cat_feed_times.sql"

def init_database():
    db = sqlite3.connect(database_name)
    db.execute("CREATE TABLE IF NOT EXISTS FeedTimes (Time INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS CheckTimes (Time INTEGER)")
    db.commit()
    db.close()
    return "Success."

init_database()

@app.route("/record_feed", methods = ["POST"])
def record_feed():
    db = sqlite3.connect(database_name)
    db.execute("INSERT INTO FeedTimes VALUES (datetime('now'))")
    db.commit()
    db.close()
    return redirect("/")


@app.route("/get_last_feed", methods = ["GET"])
def get_last_feed():
    db = sqlite3.connect(database_name)
    # Log this check
    db.execute("INSERT INTO CheckTimes VALUES (datetime('now'))")
    # Fetch the last feed time.
    last_time_query = db.execute("""SELECT datetime(Time, 'localtime') 
                                    FROM FeedTimes 
                                    ORDER BY Time DESC""")
    last_time = last_time_query.fetchone()
    db.commit()
    db.close()
    return last_time[0]


def generate_title_text(last_feed_time):
    last_datetime = datetime.fromisoformat(last_feed_time)
    # Convert the time difference from seconds to hours
    time_diff = (datetime.now() - last_datetime).total_seconds() / 3600
    if time_diff < 1:
        return "The cat was <i>just</i> fed."
    elif time_diff < 2:
        return "The cat was fed 1 hour ago."
    else:
        return "The cat was fed {} hours ago.".format(int(round(time_diff)))


def generate_subtitle_text(last_feed_time):
    last_datetime = datetime.fromisoformat(last_feed_time)
    last_datetime_local = last_datetime.replace(tzinfo=timezone.utc)
    last_datetime_local = last_datetime_local.astimezone(tz=None)
    current_local_time = datetime.now()
    print(last_datetime_local.day)
    if last_datetime_local.day == current_local_time.day:
        return "Today at {}".format(
            last_datetime_local.strftime("%I:%M %p"))
    elif current_local_time.day - 1 == last_datetime_local.day:
        return "Yesterday at {}".format(
            last_datetime_local.strftime("%I:%M %p"))
    else:
        return "{} at {}".format(
            last_datetime_local.strftime("%x"), 
            last_datetime_local.strftime("%H:%M"))


@app.route("/get_last_feed_string", methods = ["GET"])
def get_last_feed_string():
    last_time = get_last_feed()
    title_text = generate_title_text(last_time)
    subtitle_text = generate_subtitle_text(last_time)
    return_objects = {"title": title_text, "subtitle": subtitle_text}
    return json.dumps(return_objects)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)