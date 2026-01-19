import sqlite3
from datetime import datetime, date

DB_NAME = "absensi.db"

# =========================
# CONNECTION
# =========================
def get_conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# =========================
# INIT DB
# =========================
def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS students (
        npm TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        kelas TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        npm TEXT NOT NULL,
        type TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (npm) REFERENCES students(npm)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# STUDENTS
# =========================
def add_student(npm, name, kelas=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO students (npm, name, kelas) VALUES (?, ?, ?)",
        (npm, name, kelas),
    )
    conn.commit()
    conn.close()


def list_students():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT npm, name, kelas FROM students ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return rows


def npm_exists(npm):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT 1 FROM students WHERE npm = ?", (npm,))
    exists = c.fetchone() is not None
    conn.close()
    return exists


def delete_student_and_attendance(npm):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM attendance WHERE npm = ?", (npm,))
    c.execute("DELETE FROM students WHERE npm = ?", (npm,))
    conn.commit()
    conn.close()


# =========================
# ATTENDANCE
# =========================
def add_attendance(npm, att_type, latitude=None, longitude=None):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO attendance (npm, type, timestamp, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            npm,
            att_type,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            latitude,
            longitude,
        ),
    )

    conn.commit()
    conn.close()


def already_marked_today(npm, att_type):
    today = date.today().strftime("%Y-%m-%d")
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT 1 FROM attendance
        WHERE npm = ?
        AND type = ?
        AND timestamp LIKE ?
        """,
        (npm, att_type, f"{today}%"),
    )

    exists = c.fetchone() is not None
    conn.close()
    return exists


def already_marked_recent(npm, minutes=1):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT timestamp FROM attendance
        WHERE npm = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (npm,),
    )

    row = c.fetchone()
    conn.close()

    if not row:
        return False

    last_time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
    diff = datetime.now() - last_time
    return diff.total_seconds() < minutes * 60


def list_attendance(limit=100):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        """
        SELECT a.timestamp, a.npm, s.name, a.type
        FROM attendance a
        JOIN students s ON a.npm = s.npm
        ORDER BY a.timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = c.fetchall()
    conn.close()
    return rows
