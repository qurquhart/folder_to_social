import praw
import re


def reddit_config(key):
    credentials = open("config/reddit.config")
    found = 0
    for line in credentials:
        search = re.findall(f'{key}=(.*)',line)
        if search:
            found += 1
            return(search[0])
    if found == 0:
        return "key not found"


def post_to_reddit(title, file_location):
    posted = False
    reddit = praw.Reddit(client_id=reddit_config("client_id"),
                        client_secret=reddit_config("client_secret"),
                        password=reddit_config("password"),
                        user_agent=reddit_config("user_agent"),
                        username=reddit_config("username"),
                        )

    current_user = reddit.user.me()

    reddit.validate_on_submit = True

    # reddit.subreddit("hexinity").submit("test", selftext="hey look a test")
    reddit.subreddit(reddit_config("subreddit")).submit_image(title, file_location)


    return current_user