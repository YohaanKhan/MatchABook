def fetch_subreddit_data(reddit, subreddit_name="suggestmeabook", limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []

    for submission in subreddit.hot(limit=limit):
        submission.comments.replace_more(limit=0)
        post_data = {
            "id": submission.id,
            "title": submission.title,
            "selftext": submission.selftext,
            "score": submission.score,
            "url": submission.url,
            "created_utc": submission.created_utc,
            "comments": []
        }

        for comment in submission.comments:
            post_data["comments"].append({
                "body": comment.body,
                "author": str(comment.author),
                "score": comment.score,
                "created_utc": comment.created_utc
            })

        posts.append(post_data)

    return posts
