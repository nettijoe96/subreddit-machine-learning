import sklearn
import utility
import operator
import statistics

training = 350
dev = 175
testing = 175


englishDict = utility.makeEnglishDict()

#some rudimentary feature selection stuff is below


def getWordDiffs(minDiff):
    boardComments = utility.load_boardgames(training)
    boardDict = utility.wordFreq(boardComments,cleaning_function)
    boardTup = sorted(boardDict.items(), key=operator.itemgetter(1), reverse=1)
    videoComments = utility.load_videogames(training)
    videoDict = utility.wordFreq(videoComments,cleaning_function)
    videoTup = sorted(videoDict.items(), key=operator.itemgetter(1), reverse=1)
    boardDiff = getBoardDifferences(minDiff, boardTup, videoDict)
    videoDiff = getVideoDifferences(minDiff, videoTup, boardDict)
    #print("avg wordcount in videogames:")
    #print(calc_avg_wordcount(boardComments))
    #print("avg wordcount in boardgames:")
    #print(calc_avg_wordcount(videoComments))
    #print("avg non-english in boardgames:")
    #print(calc_avg_non_english_words(boardComments))
    #print("avg non-english in videogames:")
    #print(calc_avg_non_english_words(videoComments))
    fullDiff = boardDiff + videoDiff
    fullDiffSorted = sorted(fullDiff, key=operator.itemgetter(1), reverse=1)
    return fullDiffSorted


#top boardgames words that are different from videogames
def getBoardDifferences(diff, boardTup, videoDict):
    boardDiff = []
    for i in range(0, len(boardTup)):
        word = boardTup[i][0]  
        boardVal = boardTup[i][1]
        videoVal = 0
        if word in videoDict:
            videoVal = videoDict[word]
        wordDiff = boardVal - videoVal
        if wordDiff >= diff:
            boardDiff += [(word, wordDiff)]
    
    return boardDiff

#top videogame words that are different from boardgames
def getVideoDifferences(diff, videoTup, boardDict):

    videoDiff = []
    for i in range(0, len(videoTup)):
        word = videoTup[i][0]  
        videoVal = videoTup[i][1]
        boardVal = 0
        if word in boardDict:
            boardVal = boardDict[word]
        wordDiff = videoVal - boardVal
        if wordDiff >= diff:
            videoDiff += [(word, wordDiff)]

    return videoDiff

def cleaning_function(comment_text):
    cleaned_tokens = utility.cleanComment(comment_text)
    #return cleaned_tokens
    return utility.stem_cleaned_comment(cleaned_tokens)
    
def calc_avg_wordcount(comments_list):
    comment_bodies = list(map(lambda x: x.body,comments_list))
    tokenized_comments = list(map(utility.cleanComment,comment_bodies))
    wordcounts = list(map(len,tokenized_comments))
    return statistics.mean(wordcounts)
    
def calc_avg_non_english_words(comments_list):
    comment_bodies = list(map(lambda x: x.body,comments_list))
    commments = list(map(utility.cleanComment,comment_bodies))
    avg = sum([utility.avgNonEnglishWordsOrNumbers(englishDict, c) for c in commments])/len(commments)
    return avg 

