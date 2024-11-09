import sqlite3
from datetime import datetime

def create_connection():
    """
    Erstellt eine Verbindung zur SQLite-Datenbank.
    """
    conn = sqlite3.connect('drinking_data.db')
    return conn

def create_table():
    """
    Erstellt die Tabelle für die Trinkereignisse, falls sie nicht existiert.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drinking_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_count INTEGER NOT NULL,
            duration INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_drinking_event(event_count, duration):
    """
    Fügt ein neues Trinkereignis in die Datenbank ein.
    """
    conn = create_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO drinking_events (timestamp, event_count, duration)
        VALUES (?, ?, ?)
    ''', (timestamp, event_count, duration))
    conn.commit()
    conn.close()

def get_all_drinking_events():
    """
    Ruft alle Trinkereignisse aus der Datenbank ab.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM drinking_events')
    rows = cursor.fetchall()
    conn.close()
    return rows
