import time
import praw
import config
import pickle

DATA_FILE_NAME = "reddit_comments_list.pickle"
#write binary mode
WRITE_MODE = "wb"

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret, password=config.password,
                     user_agent=config.user_agent, username=config.username)

subreddit = reddit.subreddit('funny')
hot_python = subreddit.hot()
subIds = []
for s in hot_python:
    subIds += [s]

full_comment_list = list()

for subId in subIds:
    submission = reddit.submission(id=subId)
    submission.comments.replace_more(limit=None)
    comment_list = submission.comments.list()
    for c in comment_list:
        print(c.body)
    
    full_comment_list = full_comment_list + comment_list
    
#create/identify the file to write reddit data to
reddit_data_file = open(DATA_FILE_NAME,WRITE_MODE)
    
pickle.dump(full_comment_list,reddit_data_file)
        

