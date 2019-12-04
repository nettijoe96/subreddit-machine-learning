#import nltk
#nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
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
    

def stem_cleaned_comment(words):
    stemmer = PorterStemmer()
    #applies the porter stemmer's stem function to the full list of words
    stemmed_comment = list(map(stemmer.stem,words))
    return stemmed_comments


def wordFreq(commentObjs, cleaningOperation=cleanComment):
    freqDict = {}
    for commentObj in commentObjs:
        comment_words = bag_of_words(commentObj, cleaningOperation)
        for word in comment_words.keys():
            if word in freqDict:
                freqDict[word] += comment_words[word]
            else:
                freqDict[word] = comment_words[word]
    return freqDict
    
    
"""
Given a comment and a cleaning operation, return a bag of words (a dictionary 
with words as keys and their frequencies in the comment represented as integer 
values)

cleaning_operation is expected to take string values and output the cleaned data
as a list of tokenized words.
"""
def bag_of_words(comment_obj, cleaning_operation=cleanComment):
    freqDict = {}
    commentWords = cleaning_operation(comment_obj.body)
    for word in commentWords:
        if word in freqDict:
            freqDict[word] += 1
        else:
            freqDict[word] = 1
    return freqDict
 

