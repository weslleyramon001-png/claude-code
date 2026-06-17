import sqlite3, json, re
from datetime import datetime
from config import MEMORY_DB

def get_db():
    conn = sqlite3.connect(MEMORY_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(category, key)
        );
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            summary TEXT
        );
        """)

def save_message(session_id: str, role: str, content: str):
    with get_db() as db:
        db.execute("INSERT INTO messages (session_id, role, content) VALUES (?,?,?)",
                   (session_id, role, content))
        db.execute("INSERT OR IGNORE INTO sessions (id) VALUES (?)", (session_id,))
        db.execute("UPDATE sessions SET last_active=CURRENT_TIMESTAMP WHERE id=?", (session_id,))

def get_history(session_id: str, limit: int = 20) -> list:
    with get_db() as db:
        rows = db.execute(
            "SELECT role, content FROM messages WHERE session_id=? ORDER BY ts DESC LIMIT ?",
            (session_id, limit)
        ).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

def save_fact(category: str, key: str, value: str):
    with get_db() as db:
        db.execute("INSERT OR REPLACE INTO facts (category, key, value) VALUES (?,?,?)",
                   (category, key, value))

def get_facts(category: str = None) -> list:
    with get_db() as db:
        if category:
            rows = db.execute("SELECT category,key,value FROM facts WHERE category=?", (category,)).fetchall()
        else:
            rows = db.execute("SELECT category,key,value FROM facts").fetchall()
    return [{"category": r["category"], "key": r["key"], "value": r["value"]} for r in rows]

def clear_session(session_id: str):
    with get_db() as db:
        db.execute("DELETE FROM messages WHERE session_id=?", (session_id,))

def get_long_term_context() -> str:
    facts = get_facts()
    if not facts: return ""
    lines = ["[MEMÓRIA DE LONGO PRAZO]"]
    for f in facts:
        lines.append(f"• {f['category']} / {f['key']}: {f['value']}")
    return "\n".join(lines)
