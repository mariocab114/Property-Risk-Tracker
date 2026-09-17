import pyodbc
from models import Property

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=PropertyRiskTracker;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


def create_connection():
    return pyodbc.connect(CONNECTION_STRING)


def create_table():
    # Tables are now created in SQL Server by 01_create_tables.sql.
    # This stays so main.py can still call it without breaking.
    pass


def get_or_create_category_id(cursor, category_name):
    cursor.execute("SELECT id FROM risk_categories WHERE name = ?", category_name)
    row = cursor.fetchone()
    if row:
        return row.id
    cursor.execute(
        "INSERT INTO risk_categories (name) OUTPUT INSERTED.id VALUES (?)",
        category_name,
    )
    return cursor.fetchone()[0]


def add_property(prop):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        category_id = get_or_create_category_id(cursor, prop.risk_category)
        cursor.execute(
            """
            INSERT INTO properties (name, location, risk_category_id)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?)
            """,
            prop.name, prop.location, category_id,
        )
        property_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO valuations (property_id, value, risk_score) VALUES (?, ?, ?)",
            property_id, prop.value, prop.risk_score,
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_all_properties():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT p.id, p.name, p.location, v.value, r.name, v.risk_score
            FROM properties p
            JOIN risk_categories r ON p.risk_category_id = r.id
            JOIN valuations v ON v.property_id = p.id
            ORDER BY p.id
            """
        )
        rows = cursor.fetchall()
    finally:
        conn.close()
    return [(r[0], r[1], r[2], float(r[3]), r[4], r[5]) for r in rows]


def delete_property(property_id):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM valuations WHERE property_id = ?", property_id)
        cursor.execute("DELETE FROM properties WHERE id = ?", property_id)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def update_property(property_id, name, location, value, risk_category, risk_score):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        category_id = get_or_create_category_id(cursor, risk_category)
        cursor.execute(
            "UPDATE properties SET name = ?, location = ?, risk_category_id = ? WHERE id = ?",
            name, location, category_id, property_id,
        )
        cursor.execute(
            "UPDATE valuations SET value = ?, risk_score = ? WHERE property_id = ?",
            value, risk_score, property_id,
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()