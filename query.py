import sqlite3

database_name = "./cat_feed_times.sql"


def init_database():
    db = sqlite3.connect(database_name)
    db.execute("CREATE TABLE IF NOT EXISTS FeedTimes (Time INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS CheckTimes (Time INTEGER)")
    db.commit()
    db.close()


def add_feed_to_db():
    db = sqlite3.connect(database_name)
    db.execute("INSERT INTO FeedTimes VALUES (datetime('now'))")
    db.commit()
    db.close()


def add_check_to_db():
    db = sqlite3.connect(database_name)
    db.execute("INSERT INTO CheckTimes VALUES (datetime('now'))")
    db.commit()
    db.close()


def get_feed_from_db():
    db = sqlite3.connect(database_name)
    query = """SELECT datetime(Time, 'localtime')
                FROM FeedTimes
                ORDER BY Time DESC"""
    previous_feeds = db.execute(query).fetchall()
    db.commit()
    db.close()
    return previous_feeds


def get_last_feed_from_db():
    db = sqlite3.connect(database_name)
    query = """SELECT datetime(Time, 'localtime')
                FROM FeedTimes
                ORDER BY Time DESC
                LIMIT 1"""
    previous_feed = db.execute(query).fetchone()
    db.commit()
    db.close()
    return previous_feed


def get_check_from_db():
    db = sqlite3.connect(database_name)
    query = """SELECT datetime(Time, 'localtime')
                FROM CheckTimes
                ORDER BY Time DESC"""
    times = db.execute(query).fetchall()
    db.commit()
    db.close()
    return times
