import training
import utility
from sklearn import metrics
from sklearn.model_selection import learning_curve
import data_exploration
import pickle
import numpy as np
from matplotlib import pyplot as plt

confMatrixFile = "confMatrixFile.pickle"

#number of comments used in each phase
number_of_testing_comments = 150
number_of_development_comments = 150
number_of_training_comments = 350

boardgame_training_comments = utility.load_boardgames(number_of_training_comments)
videogame_training_comments = utility.load_videogames(number_of_training_comments)
boardgame_development_comments = utility.load_boardgames(number_of_development_comments,
    number_of_training_comments)
videogame_development_comments = utility.load_videogames(number_of_development_comments,
    number_of_training_comments)
boardgame_testing_comments = utility.load_boardgames(number_of_testing_comments, number_of_training_comments + number_of_development_comments)
videogame_testing_comments = utility.load_videogames(number_of_testing_comments, number_of_training_comments + number_of_development_comments)

#the optimal thresholds for bag of words differences gathered from experiment
optimalMinDiffSVC = 27     
optimalMinDiffForest = 3   

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
given a minimum difference in word counts and a list of tuples containing 
(string, difference in count) sorted from highest to lowest difference, return 
an array of strings with a difference in word count over the min
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
def run_models(model, bagOfWords,boardgame_training_data,videogame_training_data):
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
            features = training.genFeatures(boardComments, bagOfWords) + training.genFeatures(videoComments, bagOfWords)
            model = training.trainModel(model, features, labels, bagOfWords)
            confMatrix = [evaluate_model(model, boardgame_development_comments, videogame_development_comments, bagOfWords)]
            lstConfMatrices += [confMatrix] 
        saveConfMatrices(lstConfMatrices, confMatrixFile)

"""
parameters:
    model: the sklearn model being trained
    optimalMinDiff: the minimum difference between number of occurences in the 
        two training sets a word must have to be included in the model's bag of 
        words features.
    boardgame_training_data: a list of comments used to train the model (labeled
        as class "board" for boardgame)
    videogame_training_data: a list of comments used to train the model (labeled
        as class "video" for videogame)
    boardgame_eval_comments: a list of comments used to evaluate the model 
        (labeled as class "board" for boardgame)
    videogame_eval_comments: a list of comments used to evaluate the model 
        (labeled as class "video" for videogame)
        
given the previously listed parameter: clean and process the input data, extract 
its features, and use it to train and evaluate the input model.
"""
def run_model(model, optimalMinDiff, boardgame_training_data, videogame_training_data, boardgame_eval_comments, videogame_eval_comments):
    models_list = list()
    boardComments = utility.getRawComments(boardgame_training_data)
    videoComments = utility.getRawComments(videogame_training_data)
    labels = training.genLabels("board", len(boardComments)) + training.genLabels("video", len(videoComments))
    sortedDiffList = data_exploration.getWordDiffs(optimalMinDiff)
    shortenedDiffList = getWordsFromDiff(optimalMinDiff, sortedDiffList)
    bagOfWords = [shortenedDiffList[i][0] for i in range(0, len(shortenedDiffList))]

    features = training.genFeatures(boardComments, bagOfWords) + training.genFeatures(videoComments, bagOfWords)

    train_sizes, train_scores, test_scores = learning_curve(model, features, labels, train_sizes=[256, 361,466], cv=3)
    #graph_learning_curve(train_sizes, train_scores, test_scores) //uncomment if you want learning curve

    model = training.trainModel(model, features, labels, bagOfWords)
    evaluate_model(model, boardgame_eval_comments, videogame_eval_comments, bagOfWords)


"""
given a list of raining set sizes, a list of training scores, and a list of
lists of test scores, output a graph comparing the score on the training
data to the score on the test data
"""
def graph_learning_curve(train_sizes, train_scores, test_scores):
    plt.title("learning curve")
    plt.xlabel("size of training set")
    plt.ylabel("score")
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1,
                         color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")
    plt.show()

"""
given a list of confusion matrices and a filename, pickle the configuration
matrices and write them to the specified file to be loaded later
"""
def saveConfMatrices(lstConfMatrices, filename):
    f = open(filename, "wb")
    pickle.dump(lstConfMatrices, f)     

        
"""
given a model, boardgame development data, and videogame development data, evaluates the
model
"""
def evaluate_model(model, boardgame_eval_data, videogame_eval_data, bag_of_words_words):
    cleaned_boardgame_comments = utility.getRawComments(boardgame_eval_data)
    cleaned_videogame_comments = utility.getRawComments(videogame_eval_data)
    features = training.genFeatures(cleaned_boardgame_comments, bag_of_words_words) + training.genFeatures(cleaned_videogame_comments, bag_of_words_words)
    actual_labels = training.genLabels("board", len(boardgame_eval_data)) + training.genLabels("video", len(videogame_eval_data))

    classifier_labels = model.predict(features)
    
    #print("words in the bag of words: " + str(bag_of_words_words))
    #print("num of classified labels: " + str(len(classifier_labels)))
    #print("num of actual labels: " + str(len(actual_labels)))

    video_conf = confusion_matrix("video",actual_labels, classifier_labels)
    board_conf = confusion_matrix("board",actual_labels, classifier_labels)
   

    video_recall = video_conf[0]/(video_conf[0] + video_conf[3])
    video_precision = video_conf[0]/(video_conf[0] + video_conf[2])

    board_recall = board_conf[0]/(board_conf[0] + board_conf[3])
    board_precision = board_conf[0]/(board_conf[0] + board_conf[2])
    accuracy = calcAccuracy(board_conf)
    
    print("results: ")
    print("boardgame recall: " + str(board_recall))
    print("boardgame precision: " + str(board_precision))
    print("videogame recall: " + str(video_recall))
    print("videogame precision: " + str(video_precision))
    print("accuracy: " + str(accuracy))
    
    return (board_conf, video_conf)

"""
give a confusion matrix, calculate recall
"""
def calcRecall(confMatrix):
    return confMatrix[0]/(confMatrix[0] + confMatrix[3])
 
"""
give a confusion matrix, calculate precision
""" 
def calcPrecision(confMatrix):
    return confMatrix[0]/(confMatrix[0] + confMatrix[2])

"""
give a confusion matrix, calculate accuracy
"""
def calcAccuracy(confMatrix):
    return (confMatrix[0] + confMatrix[1])/(confMatrix[0] + confMatrix[1] + confMatrix[2] + confMatrix[3])

"""
provides the user options to run a random forest or support vector model on 
either the training or test data

prints precision and recall for the boardgame class and the videogame class, and
prints overall accuracy (valid for both classes)
"""
def main():
    commentType = input("evaluation on dev or test comments?\n")
    if commentType != "dev" and commentType != "test":
        print("enter either dev or test")
        return
    else:
        if commentType == "dev":
            commentsb = boardgame_development_comments    
            commentsv = videogame_development_comments    
        else:
            commentsb = boardgame_testing_comments    
            commentsv = videogame_testing_comments    

    modelName = input("svc or forest?\n").lower()
    if modelName != "svc" and modelName != "forest":
        print("not an appropriate model. Either svc or forest")
    elif modelName == "svc":
        model = training.newSVCModel()
        run_model(model, optimalMinDiffSVC, boardgame_training_comments,videogame_training_comments, commentsb, commentsv)
    elif modelName == "forest":
        model = training.newRandomForestModel()
        run_model(model, optimalMinDiffForest, boardgame_training_comments,videogame_training_comments, commentsb, commentsv)

    #run_models(model, feature_words,boardgame_training_comments,videogame_training_comments)


if __name__ == "__main__":
    main()

