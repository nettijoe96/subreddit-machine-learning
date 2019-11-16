import time
import praw
import config
import pickle

boardGamesFile = "boardgames.pickle"
videoGamesFile = "videogames.pickle"
#write binary mode
WRITE_MODE = "wb"

def fetch(subredditName, filename):
    subreddit = reddit.subreddit(subredditName)
    hot_python = subreddit.hot()
    subIds = []
    for s in hot_python:
        subIds += [s]
    
    full_comment_list = list()
    
    for subId in subIds:
        submission = reddit.submission(id=subId)
        submission.comments.replace_more(limit=None)
        comment_list = submission.comments.list()
        full_comment_list = full_comment_list + comment_list
        
    #create/identify the file to write reddit data to
    reddit_data_file = open(filename, WRITE_MODE)
        
    print(len(full_comment_list))
    pickle.dump(full_comment_list,reddit_data_file)
        

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret, password=config.password,
                     user_agent=config.user_agent, username=config.username)

fetch("boardgames", boardGamesFile)
fetch("videogames", videoGamesFile)


