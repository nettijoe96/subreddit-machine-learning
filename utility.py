#import nltk
#nltk.download("stopwords")
from nltk.corpus import stopwords
import string
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
    


#class CommentFeatures:
    


def cleanComment(comment: str):
    comment = comment.translate(str.maketrans('', '', string.punctuation))
    comment = comment.lower() # lower case
    comment = comment.replace('\"', "")
    comment = comment.replace("\n", "")
    comment = comment.replace("\n", "")
    words = comment.split(" ") 
    stopWords = stopwords.words('english')
    for sw in stopWords:
        try: 
            i = words.index(sw)
            while True:
                words.pop(i)
                i = words.index(sw)
        except ValueError:
            continue 
    for i in range(len(words)-1, -1, -1):   #remove empty space
        if words[i] == "":
            words.pop(i)

    return words


#note - code here duplicated in bag_of_words() now. If this function is changed,
#consider refactoring
def wordFreq(commentObjs):
    freqDict = {}
    for commentObj in commentObjs:
        commentWords = cleanComment(commentObj.body)
        for word in commentWords:
            if word in freqDict:
                freqDict[word] += 1
            else:
                freqDict[word] = 1
    return freqDict
    
    
#note - code here duplicated in wordFreq() now. If this function is changed,
#consider refactoring
"""
Given a comment, return a bag of words (a dictionary with words as keys and 
their frequencies in the comment represented as integer values)
"""
def bag_of_words(commentObj):
    commentWords = cleanComment(commentObj.body)
        for word in commentWords:
            if word in freqDict:
                freqDict[word] += 1
            else:
                freqDict[word] = 1
    return freqDict
 

