number_of_comments_chosen = 150
number_of_comments_skipped = 350
boardgame_comments = utility.load_boardgames(number_of_comments_chosen,
    number_of_comments_skipped)
videogame_comments = utility.load_videogames(number_of_comments_chosen,
    number_of_comments_skipped)
model = None;

"""
given a list of actual labels and a list of labels applied by a classifier, 
return a tuple of (true positives, true negatives, false positives, and false
negatives)
"""
def confusion_matrix(actual_labels, classifier_labels):
    return (0,0,0,0)

