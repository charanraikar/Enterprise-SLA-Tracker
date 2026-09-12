import os
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime

from app.sla import calculate_due_at, is_valid_status, should_set_resolved_at


SQLITE_SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_name TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL,
    created_at TEXT NOT NULL,
    due_at TEXT NOT NULL,
    resolved_at TEXT,
    updated_at TEXT NOT NULL
);
"""


MYSQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_name VARCHAR(120) NOT NULL,
    title VARCHAR(180) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(80) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    owner VARCHAR(120) NOT NULL,
    created_at DATETIME NOT NULL,
    due_at DATETIME NOT NULL,
    resolved_at DATETIME NULL,
    updated_at DATETIME NOT NULL
);
"""


def _utc_now():
    return datetime.now(UTC).replace(tzinfo=None, microsecond=0)


def _to_db_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat(sep=" ")
    return str(value)


def _dict_from_sqlite(cursor, row):
    return {cursor.description[index][0]: row[index] for index in range(len(row))}


class TicketRepository:
    def __init__(self):
        self.backend = os.getenv("DB_BACKEND", "sqlite").lower()
        self.sqlite_path = os.getenv("SQLITE_PATH", "data/tickets.db")

    @contextmanager
    def connect(self):
        if self.backend == "mysql":
            try:
                import pymysql
            except ImportError as exc:
                raise RuntimeError("Install pymysql or use DB_BACKEND=sqlite for local demo") from exc

            connection = pymysql.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", ""),
                database=os.getenv("MYSQL_DATABASE", "sla_tracker"),
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            try:
                yield connection
            finally:
                connection.close()
        else:
            os.makedirs(os.path.dirname(self.sqlite_path), exist_ok=True)
            connection = sqlite3.connect(self.sqlite_path)
            connection.row_factory = _dict_from_sqlite
            try:
                yield connection
                connection.commit()
            finally:
                connection.close()

    def _placeholder(self):
        return "%s" if self.backend == "mysql" else "?"

    def init_db(self):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(MYSQL_SCHEMA if self.backend == "mysql" else SQLITE_SCHEMA)

    def create_ticket(self, payload):
        created_at = payload.get("created_at") or _utc_now()
        due_at = calculate_due_at(payload["priority"], created_at)
        now = _utc_now()

        status = payload.get("status", "Open")
        resolved_at = payload.get("resolved_at")
        if should_set_resolved_at(status) and not resolved_at:
            resolved_at = now

        fields = {
            "client_name": payload["client_name"],
            "title": payload["title"],
            "description": payload["description"],
            "category": payload["category"],
            "priority": payload["priority"],
            "status": status,
            "owner": payload["owner"],
            "created_at": _to_db_datetime(created_at),
            "due_at": due_at.isoformat(sep=" "),
            "resolved_at": _to_db_datetime(resolved_at),
            "updated_at": now.isoformat(sep=" "),
        }

        if not is_valid_status(fields["status"]):
            raise ValueError("Invalid ticket status")

        placeholder = self._placeholder()
        columns = ", ".join(fields)
        markers = ", ".join([placeholder] * len(fields))

        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO tickets ({columns}) VALUES ({markers})",
                list(fields.values()),
            )
            ticket_id = cursor.lastrowid

        return self.get_ticket(ticket_id)

    def list_tickets(self, status=None):
        placeholder = self._placeholder()
        with self.connect() as connection:
            cursor = connection.cursor()
            if status:
                cursor.execute(f"SELECT * FROM tickets WHERE status = {placeholder} ORDER BY id DESC", (status,))
            else:
                cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
            return cursor.fetchall()

    def get_ticket(self, ticket_id):
        placeholder = self._placeholder()
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM tickets WHERE id = {placeholder}", (ticket_id,))
            row = cursor.fetchone()
        if not row:
            raise LookupError("Ticket not found")
        return row

    def update_status(self, ticket_id, status):
        if not is_valid_status(status):
            raise ValueError("Invalid ticket status")

        now = _utc_now().isoformat(sep=" ")
        resolved_at = now if should_set_resolved_at(status) else None
        placeholder = self._placeholder()

        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE tickets SET status = {placeholder}, resolved_at = {placeholder}, updated_at = {placeholder} WHERE id = {placeholder}",
                (status, resolved_at, now, ticket_id),
            )

        return self.get_ticket(ticket_id)
