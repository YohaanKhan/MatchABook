from dotenv import load_dotenv
import os
import praw
import sqlite3

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

#print(reddit.read_only) # To verify if the above connection is working or not - desired output: False

subreddit = reddit.subreddit("suggestmeabook")

#print(subreddit.display_name)
#print(subreddit.title)
#print(subreddit.description)

conn = sqlite3.connect("matchabook.db")
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


for submission in subreddit.hot(limit=10):
   
    post_data = {
        "id": submission.id,
        "title": submission.title,
        "selftext": submission.selftext,
        "score": submission.score,
        "url": submission.url,
        "created_utc": submission.created_utc,
        "comments": []
    }

    print("POST:", post_data["title"])
    print("COMMENTS:", len(post_data["comments"]))

    submission.comments.replace_more(limit=0)

    for top_comment in submission.comments:
        post_data["comments"].append({
            "body": top_comment.body,
            "author": str(top_comment.author),
            "score": top_comment.score,
            "created_utc": top_comment.created_utc
        })

    
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

conn.commit()
conn.close()


