import sqlite3
import csv
import requests

def create_tables():
    with sqlite3.connect('songs.db') as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS daily_songs(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, artist TEXT, url TEXT, sent_date TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS subscribers(chat_id INTEGER PRIMARY KEY, active INTEGER)")
        connection.commit()

def insert_songs_from_google_sheet(path):
    try:
        res = requests.get(path)
        res.raise_for_status()
    except requests.RequestException as e: 
        print(f"Error fetching songs: {e}")
        return
    try:
        with sqlite3.connect('songs.db') as connection:
            cursor = connection.cursor()
            reader = csv.reader(res.text.splitlines())   
            next(reader)
            for row in reader:
                cursor.execute("INSERT OR IGNORE INTO daily_songs (title, artist, url, sent_date) VALUES (?, ?, ?, ?)", (row[0], row[1], row[2], row[3],))
            connection.commit()   
    except sqlite3.Error as e:
        print(f"Error inserting into database: {e}")

def get_song_from_date(date):
    with sqlite3.connect('songs.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM daily_songs WHERE sent_date= ?", (date.strftime('%Y-%m-%d'),))
        song = cursor.fetchone()
        return song
    
def get_weeks_songs(today, week):
     with sqlite3.connect('songs.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM daily_songs WHERE sent_date >= ? AND sent_date <= ?", (week.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'),))
        songs = cursor.fetchall()
        return songs

def add_subscriber(chat):
    with sqlite3.connect('songs.db') as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT OR IGNORE INTO subscribers VALUES (?,?)", (chat.id, 1,))
        connection.commit()

def to_unsubscribe(chat):
    with sqlite3.connect('songs.db') as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE subscribers SET active = 0 WHERE chat_id = ?", (chat.id,))
        connection.commit()

def get_subscribers():
        with sqlite3.connect('songs.db') as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM subscribers WHERE active=1")
            subscribers = cursor.fetchall()
            return subscribers