import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    cats INTEGER DEFAULT 0,
    referrals INTEGER DEFAULT 0,
    ref_by INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    item TEXT,
    price INTEGER
)
""")

conn.commit()


def add_user(user_id, username, ref_by=None):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user is None:
        cursor.execute("""
        INSERT INTO users (user_id, username, ref_by)
        VALUES (?, ?, ?)
        """, (user_id, username, ref_by))

        if ref_by:
            cursor.execute("""
            UPDATE users
            SET referrals = referrals + 1,
                cats = cats + 1
            WHERE user_id = ?
            """, (ref_by,))

        conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()


def top_users():
    cursor.execute("""
    SELECT username, referrals
    FROM users
    ORDER BY referrals DESC
    LIMIT 10
    """)
    return cursor.fetchall()


def buy_item(user_id, item, price):
    cursor.execute("""
    UPDATE users
    SET cats = cats - ?
    WHERE user_id = ?
    """, (price, user_id))

    cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    cursor.execute("""
    INSERT INTO purchases (user_id, username, item, price)
    VALUES (?, ?, ?, ?)
    """, (user_id, user[0], item, price))

    conn.commit()
