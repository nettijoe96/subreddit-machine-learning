import time
import praw
import config

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret, password=config.password,
                     user_agent=config.user_agent, username=config.username)

subreddit = reddit.subreddit('funny')
hot_python = subreddit.hot()
subIds = []
for s in hot_python:
    subIds += [s]

for subId in subIds:
    submission = reddit.submission(id=subId)
    submission.comments.replace_more(limit=None)
    for c in submission.comments.list():
        print(c.body)
        

