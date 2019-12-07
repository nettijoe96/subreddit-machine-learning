import svc
import utility
from sklearn import metrics

"""
given a label to evaluate, list of actual labels and a list of labels applied by 
a classifier, return a tuple of (true positives, true negatives, false 
positives, and false negatives) for the label classification is being evaluated
for
"""
def confusion_matrix(evaluation_label, actual_labels, classifier_labels):
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



number_of_comments_chosen = 150
number_of_comments_skipped = 350
boardgame_comments = utility.load_boardgames(number_of_comments_chosen,
    number_of_comments_skipped)
videogame_comments = utility.load_videogames(number_of_comments_chosen,
    number_of_comments_skipped)

model = svc.getTrainedModel()

cleaned_boardgame_comments = svc.getRawComments(boardgame_comments)
cleaned_videogame_comments = svc.getRawComments(videogame_comments)
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

#binary_actual_labels()

#precision = metrics.precision_score(actual_labels,classifier_labels, ["board","video"], pos_label = 0, average = None)
#recall = metrics.recall_score(actual_labels,classifier_labels, ["board","video"], pos_label = 0, average = None)

print("board recall " + str(board_recall))
print("board precision " + str(board_precision))
print("video recall " + str(video_recall))
print("video precision " + str(video_precision))

