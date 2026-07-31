"""
Restaurant Database Layer - Clean single-version implementation.
Provides initialization, seeding, and reservation/menu/hours helpers.
"""
import sqlite3
import os
from typing import List, Dict, Optional

DEFAULT_DB = "restaurant.db"


def initialize_database(db_path: str = DEFAULT_DB) -> None:
    """Create tables and seed minimal data if missing."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        # Use DELETE mode to keep a single database file and avoid .db-wal/.db-shm sidecar files
        try:
            conn.execute("PRAGMA journal_mode = DELETE")
        except Exception:
            pass

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                is_vegetarian BOOLEAN DEFAULT 0,
                is_spicy BOOLEAN DEFAULT 0
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS opening_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day TEXT NOT NULL,
                open_time TEXT NOT NULL,
                close_time TEXT NOT NULL,
                location TEXT
            )
            """
        )

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

        _seed_database(conn)


def _seed_database(conn: sqlite3.Connection) -> None:
    """Insert sensible defaults for menu and hours (idempotent)."""
    menu_count = conn.execute("SELECT COUNT(*) FROM menu_items").fetchone()[0]
    if menu_count == 0:
        menu = [
            ("Margherita Pizza", "Pizza", "Tomato, mozzarella, fresh basil", 12.50, False, False),
            ("Spicy Arrabbiata", "Pasta", "Tomato sauce with chili flakes", 11.90, True, True),
            ("Caesar Salad", "Salad", "Romaine, parmesan, croutons", 9.50, True, False),
            ("Tiramisu", "Dessert", "Coffee-flavored Italian dessert", 7.90, True, False),
        ]
        # Adapt to schema: older DBs may lack is_vegetarian/is_spicy columns
        cols = [c[1] for c in conn.execute("PRAGMA table_info(menu_items)").fetchall()]
        if 'is_vegetarian' in cols and 'is_spicy' in cols:
            conn.executemany(
                "INSERT INTO menu_items (name, category, description, price, is_vegetarian, is_spicy) VALUES (?, ?, ?, ?, ?, ?)",
                menu,
            )
        else:
            # insert without the newer boolean columns
            menu_simple = [m[:4] for m in menu]
            conn.executemany(
                "INSERT INTO menu_items (name, category, description, price) VALUES (?, ?, ?, ?)",
                menu_simple,
            )

    hours_count = conn.execute("SELECT COUNT(*) FROM opening_hours").fetchone()[0]
    if hours_count == 0:
        hours = [
            ("Monday", "11:00", "23:00", None),
            ("Tuesday", "11:00", "23:00", None),
            ("Wednesday", "11:00", "23:00", None),
            ("Thursday", "11:00", "00:00", None),
            ("Friday", "11:00", "01:00", None),
            ("Saturday", "12:00", "01:00", None),
            ("Sunday", "12:00", "22:00", None),
        ]
        conn.executemany(
            "INSERT INTO opening_hours (day, open_time, close_time, location) VALUES (?, ?, ?, ?)",
            hours,
        )

    conn.commit()


def book_reservation(
    db_path: str,
    customer_name: str,
    date: str,
    time: str,
    party_size: int,
    contact: Optional[str] = None,
) -> int:
    """Add a new reservation and return the inserted ID."""
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO reservations (customer_name, date, time, party_size, contact, status) VALUES (?, ?, ?, ?, ?, 'confirmed')",
            (customer_name, date, time, party_size, contact),
        )
        conn.commit()
        return cur.lastrowid


def cancel_reservation(db_path: str, reservation_id: int) -> bool:
    """Mark a reservation cancelled; return True if updated."""
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(
            "UPDATE reservations SET status = 'cancelled' WHERE id = ? AND status != 'cancelled'",
            (reservation_id,),
        )
        conn.commit()
        return cur.rowcount > 0


def get_reservation_by_id(db_path: str, reservation_id: int) -> Optional[Dict]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,)).fetchone()
        return dict(row) if row else None


def get_reservations(db_path: str, customer_name: Optional[str] = None, status: str = "confirmed") -> List[Dict]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        if customer_name:
            rows = conn.execute(
                "SELECT * FROM reservations WHERE status = ? AND customer_name LIKE ?",
                (status, f"%{customer_name}%"),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM reservations WHERE status = ?", (status,)).fetchall()
        return [dict(r) for r in rows]


def get_menu(db_path: str, category: Optional[str] = None) -> List[Dict]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        if category:
            rows = conn.execute("SELECT * FROM menu_items WHERE category = ?", (category,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM menu_items").fetchall()
        return [dict(r) for r in rows]


def get_opening_hours(db_path: str, location: Optional[str] = None) -> List[Dict]:
    """Return opening hours; if `location` provided, filter by it when present."""
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cols = [c[1] for c in conn.execute("PRAGMA table_info(opening_hours)").fetchall()]
        if 'location' in cols and location:
            rows = conn.execute("SELECT * FROM opening_hours WHERE location = ? ORDER BY id", (location,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM opening_hours ORDER BY id").fetchall()
        return [dict(r) for r in rows]
