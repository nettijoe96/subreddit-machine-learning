import pickle

BOARDGAMES_PICKLE_FILE = "boardgames.pickle"
VIDEOGAMES_PICKLE_FILE = "videogames.pickle"
READ_MODE = "rb"

"""
Load boardgames files into memory

given number n, return a list of the first n stored boardgame comments
"""
def load_boardgames(num_comments):
    return __load_pickled_data(num_comments, BOARDGAMES_PICKLE_FILE)
    
"""
Load videogames files into memory

given number n, return a list of the first n stored videogames comments
"""
def load_videogames(num_comments):
    return __load_pickled_data(num_comments, VIDEOGAMES_PICKLE_FILE)
    
    
"""
Load pickled data into memory
"""
def __load_pickled_data(num_items, pickle_file_name):
    pickle_file = open(pickle_file_name, READ_MODE)
    data_items = pickle.load(pickle_file)
    
    num_items_loaded = len(data_items)
    
    if(num_items_loaded < num_items):
    
        error_message = "{} items requested, only {} items available".format(
            num_items, num_items_loaded)
            
        raise ValueError(error_message)
    
    output = data_items[0:num_items]
    
    return output
    