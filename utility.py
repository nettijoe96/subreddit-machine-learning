#import nltk
#nltk.download("stopwords")
#nltk.download('words')

import nltk.corpus as corpus
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
import itertools
import string
import pickle

BOARDGAMES_PICKLE_FILE = "boardgames.pickle"
VIDEOGAMES_PICKLE_FILE = "videogames.pickle"
READ_MODE = "rb"

"""
Load boardgames files into memory
given number n, return a list of the n stored boardgame comments
optionally, take a start index to read boardgames from. 0 by default.
"""
def load_boardgames(num_comments, start_index=0):
    return __load_pickled_data(num_comments, BOARDGAMES_PICKLE_FILE, start_index)
    
"""
Load videogames files into memory
given number n, return a list of the first n stored videogames comments
optionally, take a start index to read videogames from. 0 by default.
"""
def load_videogames(num_comments, start_index=0):
    return __load_pickled_data(num_comments, VIDEOGAMES_PICKLE_FILE, start_index)
    
    
"""
Load pickled data into memory
"""
def __load_pickled_data(num_items, pickle_file_name, start_index=0):
    pickle_file = open(pickle_file_name, READ_MODE)
    data_items = pickle.load(pickle_file)
    
    num_items_loaded = len(data_items)
    
    if(num_items_loaded < num_items):
    
        error_message = "{} items requested, only {} items available".format(
            num_items, num_items_loaded)
            
        raise ValueError(error_message)
    
    output = data_items[start_index:start_index+num_items]
    
    return output

"""
given a list of elements, return a list for each possible subset for a set of 
those elements
"""
def subsets(elements):
    sets = []
    for i in range(1, len(elements)+1):
        sets += list(itertools.combinations(elements, i)) 

    lsts = []
    for s in sets:
        lst = []
        for e in s:
            lst += [e] 
        lsts += [lst] 

    return lsts


"""
given a list of words to check against and a list of words to evaluate, tell 
whether the list being evaluated contains either a number or an element in the
first list
"""
def allEnglishWordsOrNumbers(englishDict, words):
    for word in words:
        if not isEnglishWord(englishDict, word) and not is_number(word):
            return False
        
    return True

"""
given a list of words to check against and a list of words to evaluate, return 
the number of matching words per total words (should be 1 or less)
"""
def avgNonEnglishWordsOrNumbers(englishDict, words):
    num = 0
    for word in words:
        if not isEnglishWord(englishDict, word) and not is_number(word):
            num += 1
        
    if num == 0:
        return 0
    else:
        return num/len(words)


"""
uses nltk words to create an english dictionary dict datastructure
@return dict structure
"""
def makeEnglishDict():
    english_vocab = set(w.lower() for w in corpus.words.words())
    englishDict = {}
    for word in english_vocab:
        englishDict[word] = True
    return englishDict 



"""
checks if english word is in the english dictionary
"""
def isEnglishWord(englishDict, word):
    return word.lower() in englishDict


"""
checks if str is a number
"""
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


"""
returns raw comments from comment list
"""
def getRawComments(comments):
    raw = []
    for comment in comments:
        raw += [cleanComment(comment.body)] 
    return raw


"""
cleans comment: tokenizes, removes punctuation, removes stopwords
@param: comment 
@return: cleaned word list
"""
def cleanComment(comment: str):
    comment = comment.translate(str.maketrans('', '', string.punctuation))
    comment = comment.lower() # lower case
    comment = comment.replace('\"', "")
    comment = comment.replace("\n", "")
    comment = comment.replace("\n", "")
    words = comment.split(" ") 
    stopWords = corpus.stopwords.words('english')
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
    


"""
returns stemmed word list
"""
def stem_cleaned_comment(words):
    stemmer = SnowballStemmer("english")
    #applies the porter stemmer's stem function to the full list of words
    stemmed_comments = list(map(stemmer.stem,words))
    return stemmed_comments



"""
calculates word frequencies for comments
@param: comment objs
@param: cleaningoperation
@return: freq dict
"""
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
 

