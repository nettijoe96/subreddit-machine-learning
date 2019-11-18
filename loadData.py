import pickle

BOARDGAMES_PICKLE_FILE = "boardgames.pickle"
VIDEOGAMES_PICKLE_FILE = "videogames.pickle"
READ_MODE = "rb"

"""
Load boardgame files into memory

given number n, return a list of the first n stored boardgame comments
"""
def load_boardgames(num_comments):

    boardgames_file = open(BOARDGAMES_PICKLE_FILE, READ_MODE)
    boardgames_comments = pickle.load(boardgames_file)
    
    num_comments_loaded = len(boardgames_comments)
    
    if(num_comments_loaded < num_comments):
    
        error_message = "{} items requested, only {} items available".format(
            num_comments, num_comments_loaded)
            
        raise ValueError(error_message)
    
    output = boardgames_comments[0:num_comments]
    
    return output
    