import sqlite3
import os
from datetime import datetime

DB_PATH = "medinsight_patients.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def create_patient(full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks=""):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks,
              datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def read_all_patients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def read_patient_by_id(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_patient(patient_id, full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patients SET full_name=?, date_of_birth=?, email=?, glucose=?, haemoglobin=?, cholesterol=?,
        remarks=?, updated_at=? WHERE id=?
    """, (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks,
          datetime.now().isoformat(), patient_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def delete_patient(patient_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0

def search_patients(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM patients WHERE full_name LIKE ? OR email LIKE ?
        ORDER BY created_at DESC
    """, (f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
