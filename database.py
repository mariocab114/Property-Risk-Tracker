import sqlite3
from models import Property

def create_connection():
    conn = sqlite3.connect("properties.db")
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            value REAL NOT NULL,
            risk_category TEXT NOT NULL,
            risk_score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_property(prop):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (name, location, value, risk_category, risk_score)
        VALUES (?, ?, ?, ?, ?)
    """, (prop.name, prop.location, prop.value, prop.risk_category, prop.risk_score))
    conn.commit()
    conn.close()

def get_all_properties():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_property(property_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
    conn.commit()
    conn.close()

def update_property(property_id, name, location, value, risk_category, risk_score):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE properties
        SET name = ?, location = ?, value = ?, risk_category = ?, risk_score = ?
        WHERE id = ?
    """, (name, location, value, risk_category, risk_score, property_id))
    conn.commit()
    conn.close()