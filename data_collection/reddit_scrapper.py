from data_collection.reddit_client import get_reddit_instance
from data_collection.fetch_posts import fetch_subreddit_data
from utils.db_handler import init_db, insert_post_data

def run_scraper():
    reddit = get_reddit_instance()
    posts = fetch_subreddit_data(reddit)

    conn, cursor = init_db()

    for post in posts:
        insert_post_data(cursor, post)

    conn.commit()
    conn.close()



