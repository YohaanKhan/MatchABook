import sqlite3

def init_db(db_path="matchabook.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            title TEXT,
            selftext TEXT,
            score INTEGER,
            url TEXT,
            created_utc INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id TEXT,
            body TEXT,
            author TEXT,
            score INTEGER,
            created_utc INTEGER,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        )
    """)
    conn.commit()
    return conn, cursor

def insert_post_data(cursor, post_data):
    cursor.execute("""
        INSERT OR REPLACE INTO posts (id, title, selftext, score, url, created_utc)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        post_data["id"],
        post_data["title"],
        post_data["selftext"],
        post_data["score"],
        post_data["url"],
        post_data["created_utc"]
    ))

    for comment in post_data["comments"]:
        cursor.execute("""
            INSERT INTO comments (post_id, body, author, score, created_utc)
            VALUES (?, ?, ?, ?, ?)
        """, (
            post_data["id"],
            comment["body"],
            comment["author"],
            comment["score"],
            comment["created_utc"]
        ))
