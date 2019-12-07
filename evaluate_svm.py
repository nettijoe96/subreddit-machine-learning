import svc
import utility

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

conf = confusion_matrix("board",actual_labels, classifier_labels)
print(conf)

