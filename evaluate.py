import training
import utility
from sklearn import metrics
import data_exploration
import pickle


confMatrixFile = "confMatrixFile.pickle"

feature_words = [
    "people",
    "work",
    "would",
    "make",
    "abuse",
    "think",
    "time",
    "know",
    "person",
    "use",
    "comment",
    "say",
    "read",
    "post",
    "remove",
    "support",
    "jr",
    "someone",
    "accuse",
    "victoria",
    "kind",
    "made",
    "design",
    "see",
    "victim",
    "statement",
    "believe",
    "relationship",
    "response",
    "game",
    "play",
    "soul",
    "2",
    "3",
    "fun"]   
number_of_testing_comments = 150
number_of_training_comments = 350
boardgame_training_comments = utility.load_boardgames(number_of_training_comments)
videogame_training_comments = utility.load_videogames(number_of_training_comments)
boardgame_testing_comments = utility.load_boardgames(number_of_testing_comments,
    number_of_training_comments)
videogame_testing_comments = utility.load_videogames(number_of_testing_comments,
    number_of_training_comments)
    
"""
given a label to evaluate, list of actual labels and a list of labels applied by 
a classifier, return a tuple of (true positives, true negatives, false 
positives, and false negatives) for the label classification is being evaluated
for
"""
def confusion_matrix(evaluation_label, actual_labels, classifier_labels):

    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0
    
    number_of_samples = len(actual_labels)
    
    for i in range(0,number_of_samples):
        actual_label = actual_labels[i]
        classifier_label = classifier_labels[i]
        #positive
        if(evaluation_label == classifier_label):
            if(evaluation_label == actual_label): true_positives += 1
            else: false_positives += 1
        #negative
        else:
            if(evaluation_label != actual_label): true_negatives += 1
            else: false_negatives += 1
    
    return (true_positives,true_negatives,false_positives,false_negatives)
    


"""
"""
def getWordsFromDiff(minDiff, sortedDiffList):
    for i in range(0, len(sortedDiffList)):
        if sortedDiffList[i][1] < minDiff:
            return sortedDiffList[0:i]

    return sortedDiffList[0:len(sortedDiffList)]

"""
given a list of words, boardgame training data, and videogame training data,
run a model for each permutation of the list of words
"""
def run_models(bagOfWords,boardgame_training_data,videogame_training_data):
    models_list = list()
    boardComments = utility.getRawComments(boardgame_training_data)
    videoComments = utility.getRawComments(videogame_training_data)
    labels = training.genLabels("board", len(boardComments)) + training.genLabels("video", len(videoComments))
    minDiff = 1
    sortedDiffList = data_exploration.getWordDiffs(minDiff)
    topDiff = sortedDiffList[0][1]
    lstConfMatrices = []
    confMatrix = ()
    prevBagOfWords = []
    for d in range(0, topDiff):
        shortenedDiffList = getWordsFromDiff(d, sortedDiffList)
        bagOfWords = [shortenedDiffList[i][0] for i in range(0, len(shortenedDiffList))]
        if bagOfWords == prevBagOfWords:
            lstConfMatrices +=  [confMatrix]
        else:
            svc_model = training.newSVCModel()
            features = training.genFeatures(boardComments, bagOfWords) + training.genFeatures(videoComments, bagOfWords)
            model = training.trainModel(svc_model, features, labels, bagOfWords)
            confMatrix = [evaluate_model(model, boardgame_testing_comments, videogame_testing_comments, bagOfWords)]
            lstConfMatrices += [confMatrix] 
        saveConfMatrices(lstConfMatrices, confMatrixFile)

    #**old stuff**
    #perms = utility.subsets(bagOfWords)       #get permuations of bag of words
    #print(len(perms))
    #for bag in perms:
    #    svc_model = svc.newSVCModel()
    #    features = svc.genFeatures(boardComments, bag) + svc.genFeatures(videoComments, bag)
    #    model = svc.trainModel(svc_model, features, labels, bag)
    #    evaluate_model(model, boardgame_testing_comments, videogame_testing_comments, bag)


def saveConfMatrices(lstConfMatrices, filename):
    f = open(filename, "wb")
    pickle.dump(lstConfMatrices, f)     

        
"""
given a model, boardgame testing data, and videogame testing data, evaluates the
model
"""
def evaluate_model(model, boardgame_testing_data, videogame_testing_data, bag_of_words_words):
    cleaned_boardgame_comments = utility.getRawComments(boardgame_testing_data)
    cleaned_videogame_comments = utility.getRawComments(videogame_testing_data)
    features = training.genFeatures(cleaned_boardgame_comments, bag_of_words_words) + training.genFeatures(cleaned_videogame_comments, bag_of_words_words)
    actual_labels = training.genLabels("board", number_of_testing_comments) + training.genLabels("video", number_of_testing_comments)

    classifier_labels = model.predict(features)
    
    print("words in the bag of words: " + str(bag_of_words_words))
    print("num of classified labels: " + str(len(classifier_labels)))
    print("num of actual labels: " + str(len(actual_labels)))

    video_conf = confusion_matrix("video",actual_labels, classifier_labels)
    board_conf = confusion_matrix("board",actual_labels, classifier_labels)

    video_recall = video_conf[0]/(video_conf[0] + video_conf[3])
    video_precision = video_conf[0]/(video_conf[0] + video_conf[2])

    board_recall = board_conf[0]/(board_conf[0] + board_conf[3])
    board_precision = board_conf[0]/(board_conf[0] + board_conf[2])

    print("board recall " + str(board_recall))
    print("board precision " + str(board_precision))
    print("video recall " + str(video_recall))
    print("video precision " + str(video_precision))
    
    return (board_conf, video_conf)


def calcRecall(confMatrix):
    return confMatrix[0]/(confMatrix[0] + confMatrix[3])
    
def calcPrecision(confMatrix):
    return confMatrix[0]/(confMatrix[0] + confMatrix[2])


def main():
    run_models(feature_words,boardgame_training_comments,videogame_training_comments)


if __name__ == "__main__":
    main()

