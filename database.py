import sqlite3

def create_database():

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (

       id INTEGER PRIMARY KEY AUTOINCREMENT,

filename TEXT,

name TEXT,

email TEXT,

phone TEXT,

score REAL,

rating TEXT,

status TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_result(
    filename,
    name,
    email,
    phone,
    score,
    rating
):

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO candidates
        (
            filename,
            name,
            email,
            phone,
            score,
            rating,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            filename,
            name,
            email,
            phone,
            score,
            rating,
            "Review"
        )
    )

    conn.commit()
    conn.close()

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO candidates
        (filename, score, rating)
        VALUES (?, ?, ?)
        """,
        (filename, score, rating)
    )

    conn.commit()
    conn.close()

def get_all_results():

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM candidates ORDER BY id DESC"
    )

    results = cursor.fetchall()

    conn.close()

    return results

def get_statistics():

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*), MAX(score), AVG(score) FROM candidates"
    )

    stats = cursor.fetchone()

    conn.close()

    return stats

def get_top_candidates():

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT filename, score, rating
        FROM candidates
        ORDER BY score DESC
        LIMIT 5
        """
    )

    candidates = cursor.fetchall()

    conn.close()

    return candidates

def get_chart_data():

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT filename, score FROM candidates"
    )

    data = cursor.fetchall()

    conn.close()

    return data

def update_status(candidate_id, status):

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE candidates
        SET status = ?
        WHERE id = ?
        """,
        (status, candidate_id)
    )

    conn.commit()
    conn.close()

def search_candidates(keyword):

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM candidates
        WHERE
        name LIKE ?
        OR email LIKE ?
        OR filename LIKE ?
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    results = cursor.fetchall()

    conn.close()

    return results

def get_candidate_by_id(candidate_id):

    conn = sqlite3.connect("resume_data.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    )

    candidate = cursor.fetchone()

    conn.close()

    return candidate
