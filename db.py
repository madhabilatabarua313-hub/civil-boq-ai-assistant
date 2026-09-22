import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = Path(os.getenv("BOQ_DB_PATH", "civil_boq.db"))

def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        project_type TEXT NOT NULL,
        floor_area REAL DEFAULT 0,
        floors INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS takeoff_items (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        item_code TEXT NOT NULL,
        description TEXT NOT NULL,
        unit TEXT NOT NULL,
        quantity REAL NOT NULL,
        rate REAL DEFAULT 0,
        amount REAL DEFAULT 0,
        notes TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id)
    );

    CREATE TABLE IF NOT EXISTS market_rates (
        id TEXT PRIMARY KEY,
        material TEXT NOT NULL,
        location TEXT NOT NULL,
        unit TEXT NOT NULL,
        rate REAL NOT NULL,
        source TEXT DEFAULT 'User entered',
        effective_date TEXT NOT NULL,
        verified INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id TEXT PRIMARY KEY,
        display_name TEXT NOT NULL,
        rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        comment TEXT NOT NULL,
        status TEXT DEFAULT 'approved',
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS ai_messages (
        id TEXT PRIMARY KEY,
        project_id TEXT,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def now():
    return datetime.utcnow().isoformat(timespec="seconds")

def create_project(name, location, project_type, floor_area, floors):
    pid = str(uuid.uuid4())
    conn = _connect()
    conn.execute(
        """INSERT INTO projects
        (id,name,location,project_type,floor_area,floors,created_at,updated_at)
        VALUES (?,?,?,?,?,?,?,?)""",
        (pid, name, location, project_type, floor_area, floors, now(), now()),
    )
    conn.commit()
    conn.close()
    return pid

def get_projects():
    conn = _connect()
    rows = conn.execute("SELECT * FROM projects ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_project(project_id):
    conn = _connect()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def save_project(project_id, **fields):
    allowed = {"name", "location", "project_type", "floor_area", "floors"}
    updates = {k: v for k, v in fields.items() if k in allowed}
    if not updates:
        return
    updates["updated_at"] = now()
    sql = ", ".join(f"{k}=?" for k in updates)
    conn = _connect()
    conn.execute(f"UPDATE projects SET {sql} WHERE id=?", (*updates.values(), project_id))
    conn.commit()
    conn.close()

def add_takeoff(project_id, item_code, description, unit, quantity, rate=0, notes=""):
    iid = str(uuid.uuid4())
    amount = float(quantity) * float(rate)
    conn = _connect()
    conn.execute(
        """INSERT INTO takeoff_items
        (id,project_id,item_code,description,unit,quantity,rate,amount,notes,created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (iid, project_id, item_code, description, unit, quantity, rate, amount, notes, now()),
    )
    conn.commit()
    conn.close()
    return iid

def get_takeoff(project_id):
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM takeoff_items WHERE project_id=? ORDER BY created_at DESC",
        (project_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_takeoff(item_id):
    conn = _connect()
    conn.execute("DELETE FROM takeoff_items WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

def add_market_rate(material, location, unit, rate, source, effective_date, verified=False):
    rid = str(uuid.uuid4())
    conn = _connect()
    conn.execute(
        """INSERT INTO market_rates
        (id,material,location,unit,rate,source,effective_date,verified)
        VALUES (?,?,?,?,?,?,?,?)""",
        (rid, material, location, unit, rate, source, effective_date, int(verified)),
    )
    conn.commit()
    conn.close()
    return rid

def get_market_rates(location=None):
    conn = _connect()
    if location:
        rows = conn.execute(
            "SELECT * FROM market_rates WHERE location=? ORDER BY effective_date DESC",
            (location,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM market_rates ORDER BY effective_date DESC"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def add_review(display_name, rating, comment):
    rid = str(uuid.uuid4())
    conn = _connect()
    conn.execute(
        """INSERT INTO reviews
        (id,display_name,rating,comment,status,created_at)
        VALUES (?,?,?,?,?,?)""",
        (rid, display_name, int(rating), comment, "approved", now()),
    )
    conn.commit()
    conn.close()

def get_reviews():
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM reviews WHERE status='approved' ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_ai_message(project_id, role, content):
    mid = str(uuid.uuid4())
    conn = _connect()
    conn.execute(
        "INSERT INTO ai_messages (id,project_id,role,content,created_at) VALUES (?,?,?,?,?)",
        (mid, project_id, role, content, now()),
    )
    conn.commit()
    conn.close()

def get_ai_messages(project_id):
    conn = _connect()
    rows = conn.execute(
        "SELECT role,content FROM ai_messages WHERE project_id=? ORDER BY created_at",
        (project_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
