"""
JARBAS Memory Module — SQLite-based conversation memory.

Tables:
  - messages   : Full conversation history per session
  - user_facts : Long-term facts about the user (extracted from conversations)
  - sessions   : Session metadata
  - movements  : Financial movements (entradas/saídas)

The DB is created automatically on first use.
"""

import sqlite3
import json
import re
from datetime import datetime
from typing import Optional
from config import config


# ── Database bootstrap ─────────────────────────────────────────────────────

def get_connection() -> sqlite3.Connection:
    """Open (and cache) a SQLite connection with row_factory set."""
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create all tables if they don't already exist."""
    conn = get_connection()
    try:
        conn.executescript("""
            PRAGMA journal_mode=WAL;

            CREATE TABLE IF NOT EXISTS messages (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT    NOT NULL,
                role        TEXT    NOT NULL CHECK(role IN ('user','assistant','tool')),
                content     TEXT    NOT NULL,
                timestamp   TEXT    NOT NULL DEFAULT (datetime('now')),
                metadata    TEXT    DEFAULT '{}'
            );

            CREATE INDEX IF NOT EXISTS idx_messages_session
                ON messages(session_id, timestamp);

            CREATE TABLE IF NOT EXISTS user_facts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                category    TEXT    NOT NULL,
                fact        TEXT    NOT NULL,
                confidence  REAL    NOT NULL DEFAULT 1.0,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
                updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT    UNIQUE NOT NULL,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
                last_active TEXT    NOT NULL DEFAULT (datetime('now')),
                metadata    TEXT    DEFAULT '{}'
            );

            CREATE TABLE IF NOT EXISTS movements (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                type        TEXT    NOT NULL CHECK(type IN ('entrada', 'saida')),
                amount      REAL    NOT NULL,
                description TEXT    NOT NULL,
                category    TEXT    NOT NULL DEFAULT 'geral',
                created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
            );

            CREATE INDEX IF NOT EXISTS idx_movements_created
                ON movements(created_at);
        """)
        conn.commit()
    finally:
        conn.close()


# ── Messages ───────────────────────────────────────────────────────────────

def save_message(
    session_id: str,
    role: str,
    content: str,
    metadata: Optional[dict] = None,
) -> int:
    """Persist a single message and return its ID."""
    conn = get_connection()
    try:
        # Upsert the session record (touch last_active)
        conn.execute(
            """
            INSERT INTO sessions (session_id, created_at, last_active)
            VALUES (?, datetime('now'), datetime('now'))
            ON CONFLICT(session_id) DO UPDATE SET last_active = datetime('now')
            """,
            (session_id,),
        )
        cursor = conn.execute(
            """
            INSERT INTO messages (session_id, role, content, timestamp, metadata)
            VALUES (?, ?, ?, datetime('now'), ?)
            """,
            (session_id, role, content, json.dumps(metadata or {})),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_history(session_id: str, limit: int = 20) -> list[dict]:
    """
    Return the last `limit` messages for a session in chronological order.
    Each item is a dict with keys: role, content, timestamp.
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT role, content, timestamp, metadata
            FROM messages
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit),
        ).fetchall()
        # Reverse so oldest message is first (chronological)
        return [
            {
                "role": r["role"],
                "content": r["content"],
                "timestamp": r["timestamp"],
                "metadata": json.loads(r["metadata"] or "{}"),
            }
            for r in reversed(rows)
        ]
    finally:
        conn.close()


def clear_session(session_id: str) -> None:
    """Delete all messages for a session (keeps the session record)."""
    conn = get_connection()
    try:
        conn.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
        conn.commit()
    finally:
        conn.close()


def get_all_sessions() -> list[dict]:
    """Return metadata for all sessions."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT session_id, created_at, last_active FROM sessions ORDER BY last_active DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── User Facts ─────────────────────────────────────────────────────────────

def save_fact(category: str, fact: str, confidence: float = 1.0) -> None:
    """
    Upsert a user fact. If the same fact text already exists in the category,
    update its confidence and updated_at timestamp.
    """
    conn = get_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM user_facts WHERE category = ? AND fact = ?",
            (category, fact),
        ).fetchone()

        if existing:
            conn.execute(
                "UPDATE user_facts SET confidence = ?, updated_at = datetime('now') WHERE id = ?",
                (confidence, existing["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO user_facts (category, fact, confidence) VALUES (?, ?, ?)",
                (category, fact, confidence),
            )
        conn.commit()
    finally:
        conn.close()


def get_facts(category: Optional[str] = None) -> list[dict]:
    """Return all user facts, optionally filtered by category."""
    conn = get_connection()
    try:
        if category:
            rows = conn.execute(
                "SELECT category, fact, confidence FROM user_facts WHERE category = ? ORDER BY confidence DESC",
                (category,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT category, fact, confidence FROM user_facts ORDER BY category, confidence DESC"
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_facts_as_string() -> str:
    """
    Format all user facts as a human-readable string suitable for injecting
    into the system prompt so JARBAS remembers persistent info.
    """
    facts = get_facts()
    if not facts:
        return ""

    lines: list[str] = ["Fatos conhecidos sobre o usuário:"]
    current_category = None
    for f in facts:
        if f["category"] != current_category:
            current_category = f["category"]
            lines.append(f"\n[{current_category.upper()}]")
        lines.append(f"  • {f['fact']}")

    return "\n".join(lines)


# ── Financial Movements ────────────────────────────────────────────────────

def add_movement(movement_type: str, amount: float, description: str, category: str = "geral") -> int:
    """Insert a financial movement and return its ID."""
    conn = get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO movements (type, amount, description, category) VALUES (?, ?, ?, ?)",
            (movement_type, amount, description, category),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def list_movements(limit: int = 20, category: Optional[str] = None) -> list[dict]:
    """Return the most recent movements, optionally filtered by category."""
    conn = get_connection()
    try:
        if category:
            rows = conn.execute(
                "SELECT * FROM movements WHERE category = ? ORDER BY created_at DESC LIMIT ?",
                (category, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM movements ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_balance() -> dict:
    """Return totals: entradas, saidas, saldo líquido, total de movimentos."""
    conn = get_connection()
    try:
        row = conn.execute(
            """
            SELECT
                COALESCE(SUM(CASE WHEN type = 'entrada' THEN amount ELSE 0 END), 0) AS total_entradas,
                COALESCE(SUM(CASE WHEN type = 'saida'   THEN amount ELSE 0 END), 0) AS total_saidas,
                COUNT(*) AS total_movimentos
            FROM movements
            """
        ).fetchone()
        entradas = row["total_entradas"]
        saidas = row["total_saidas"]
        return {
            "entradas": entradas,
            "saidas": saidas,
            "saldo": entradas - saidas,
            "total_movimentos": row["total_movimentos"],
        }
    finally:
        conn.close()


# ── Fact extraction ────────────────────────────────────────────────────────

# Simple keyword patterns for extracting facts from user messages.
# Each tuple: (category, regex_pattern, lambda to format the fact string)
_EXTRACTION_PATTERNS: list[tuple[str, str, callable]] = [
    # Name patterns: "meu nome é X", "me chamo X"
    ("identity", r"(?:meu nome é|me chamo)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", lambda m: f"Nome: {m.group(1)}"),
    # Location: "moro em X", "sou de X"
    ("identity", r"(?:moro em|sou de)\s+([A-Z][a-zÀ-ú]+(?:\s+[A-Z][a-zÀ-ú]+)*)", lambda m: f"Localização: {m.group(1)}"),
    # Goals: "quero X", "meu objetivo é X"
    ("goals", r"(?:quero|desejo|meu objetivo é|minha meta é)\s+(.{10,60})(?:\.|,|$)", lambda m: f"Meta: {m.group(1).strip()}"),
    # Businesses: "minha empresa X", "trabalho com X"
    ("business", r"(?:minha empresa|meu negócio|trabalho com)\s+(.{5,50})(?:\.|,|$)", lambda m: f"Negócio: {m.group(1).strip()}"),
    # Platforms mentioned
    ("business", r"\b(Hotmart|Kiwify|Monetizze|Braip|Shopify|WooCommerce)\b", lambda m: f"Usa a plataforma: {m.group(1)}"),
]


def extract_facts_from_message(message: str) -> list[tuple[str, str]]:
    """
    Run simple regex patterns over a user message and return a list of
    (category, fact) tuples for any facts found.
    Does NOT persist — call save_fact() separately.
    """
    found: list[tuple[str, str]] = []
    for category, pattern, formatter in _EXTRACTION_PATTERNS:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            try:
                fact_text = formatter(match)
                found.append((category, fact_text))
            except Exception:
                pass  # Pattern matched but formatter failed — skip silently
    return found


def auto_extract_and_save(message: str) -> None:
    """Extract facts from a user message and persist any found."""
    facts = extract_facts_from_message(message)
    for category, fact in facts:
        save_fact(category, fact)


# ── Module init ────────────────────────────────────────────────────────────
# Tables are created when this module is first imported.
init_db()
