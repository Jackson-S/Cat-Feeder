from flask import Flask, request, render_template, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)
database_name = "./cat_feed_times.sql"

@app.route("/record_feed", methods = ['GET'])
def record_feed():
    db = sqlite3.connect(database_name)
    db.execute("INSERT INTO FeedTimes VALUES (datetime('now'))")
    db.commit()
    db.close()
    return redirect("/")


@app.route("/get_last_feed", methods = ['GET'])
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


@app.route("/init_database")
def init_database():
    db = sqlite3.connect(database_name)
    db.execute("CREATE TABLE FeedTimes (Time INTEGER)")
    db.execute("CREATE TABLE CheckTimes (Time INTEGER)")
    db.commit()
    db.close()
    return "Success."


@app.route("/")
def index():
    db = sqlite3.connect(database_name)
    # Fetches the time as local time (stored as UTC)
    last_time_query = db.execute("""SELECT datetime(Time, 'localtime') 
                                    FROM FeedTimes 
                                    ORDER BY Time DESC""")
    last_time = last_time_query.fetchone()[0]
    last_datetime = datetime.fromisoformat(last_time)
    
    # Convert the time difference from seconds to hours
    time_diff = (datetime.now() - last_datetime).total_seconds() / 3600

    return render_template("index.html", time_diff=time_diff)

if __name__ == "__main__":
    app.run(debug=True)