import svc
import utility
from sklearn import metrics

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
given a list of words, boardgame training data, and videogame training data,
run a model for each permutation of the list of words
"""
def run_models(bagOfWords,boardgame_training_data,videogame_training_data):

    models_list = list()
    boardComments = getRawComments(utility.load_boardgames(training))
    videoComments = getRawComments(utility.load_videogames(training))
    bagOfWords = ["play", "board", "soul", "people"]  
    perms = utility.permuations(bagOfWords)
    for bag in perms:
        model = svc.getTrainedModel(boardComments, videoComments, bag)
        evaluate_model(model, boardgame_testing_comments, videogame_testing_comments)

"""
given a model, boardgame testing data, and videogame testing data, evaluates the
model
"""
def evaluate_model(model, boardgame_testing_data, videogame_testing_data):
    cleaned_boardgame_comments = svc.getRawComments(boardgame_testing_data)
    cleaned_videogame_comments = svc.getRawComments(videogame_tsting_data)
    features = svc.genFeatures(cleaned_boardgame_comments) + svc.genFeatures(cleaned_videogame_comments)
    actual_labels = svc.genLabels("board", number_of_comments_chosen) + svc.genLabels("video", number_of_comments_chosen)

    classifier_labels = model.predict(features)

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
    
def main():
    run_models(feature_words,boardgame_training_comments,videogame_training_comments)

main()

