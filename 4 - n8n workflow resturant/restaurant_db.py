import sqlite3
import os

DEFAULT_DB_PATH = "restaurant.db"

def initialize_database(db_path: str = DEFAULT_DB_PATH):
    """Initialize the database and create necessary tables."""
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        # Create opening_hours table for the restaurant schedule.
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS opening_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week TEXT NOT NULL,
                open_time TEXT NOT NULL,
                close_time TEXT NOT NULL
            )
            """
        )
        
        # Create reservations table with soft-delete support.
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                party_size INTEGER NOT NULL,
                contact TEXT,
                status TEXT NOT NULL DEFAULT 'confirmed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def book_reservation(
    db_path: str, 
    customer_name: str, 
    date: str, 
    time: str, 
    party_size: int, 
    contact: str = None
) -> int:
    """Insert a new reservation and return its ID."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO reservations (customer_name, date, time, party_size, contact)
            VALUES (?, ?, ?, ?, ?)
            """,
            (customer_name, date, time, party_size, contact)
        )
        conn.commit()
        return cursor.lastrowid


def cancel_reservation(db_path: str, reservation_id: int) -> None:
    """Mark a reservation as cancelled (soft delete)."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE reservations SET status = 'cancelled' WHERE id = ?",
            (reservation_id,)
        )
        conn.commit()


def get_reservations(db_path: str, customer_name: str = None) -> list:
    """Return confirmed reservations, optionally filtered by customer name."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        if customer_name:
            rows = conn.execute(
                """
                SELECT * FROM reservations 
                WHERE status = 'confirmed' AND customer_name LIKE ?
                """, 
                (f"%{customer_name}%",)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM reservations WHERE status = 'confirmed'"
            ).fetchall()
        return [dict(r) for r in rows]
