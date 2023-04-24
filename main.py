from flask import Flask, jsonify
from faker import Faker
import sqlite3 as sql

app = Flask(__name__)
fake = Faker()

conn = sql.connect('music.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT NOT NULL);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tracks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                duration INTEGER NOT NULL);''')

conn.commit()
conn.close()


@app.route('/customers', methods=['POST'])
def populate_customers_table():
    conn = sql.connect('music.db')
    cursor = conn.cursor()

    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.phone_number()

        cursor.execute("INSERT INTO customers (first_name, last_name, email, phone_number) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, email, phone_number))

    conn.commit()
    conn.close()
    return "Customers table populated successfully!"


@app.route('/tracks', methods=['POST'])
def populate_tracks_table():
    conn = sql.connect('music.db')
    cursor = conn.cursor()

    for _ in range(10):
        title = fake.sentence(nb_words=3)
        artist = fake.name()
        duration = fake.random_int(min=60, max=300)

        cursor.execute("INSERT INTO tracks (title, artist, duration) VALUES (?, ?, ?)",
                       (title, artist, duration))

    conn.commit()
    conn.close()
    return "Tracks table populated successfully!"


@app.route('/names')
def get_unique_names_count():
    conn = sql.connect('music.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(DISTINCT first_name) FROM customers")
    unique_names_count = cursor.fetchone()[0]

    conn.close()
    return jsonify({'unique_names_count': unique_names_count})


@app.route('/tracks')
def get_tracks_count():
    conn = sql.connect('music.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tracks")
    tracks_count = cursor.fetchone()[0]

    conn.close()
    return jsonify({'tracks_count': tracks_count})


@app.route('/tracks-sec')
def get_tracks_and_duration():
    conn = sql.connect('music.db')
    cursor = conn.cursor()

    cursor.execute("SELECT title, duration FROM tracks")
    tracks = cursor.fetchall()

    tracks_info = [{'title': track[0], 'duration_sec': track[1]} for track in tracks]

    conn.close()
    return jsonify({'tracks_info': tracks_info})
