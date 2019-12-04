from sklearn import svm
import utility


training = 350

#if a feature is used, it is True
numberOfWordsFeature = False
bagOfWordsFeature = True
bagOfWords = ["people", "game"]


def main():
    boardComments = getRawComments(utility.load_boardgames(training))
    videoComments = getRawComments(utility.load_videogames(training))
    features = genFeatures(boardComments) + genFeatures(videoComments)
    labels = genLabels("board", len(boardComments)) + genLabels("video", len(videoComments))
    model = createModel(features, labels)     


def getRawComments(comments):
    raw = []
    for comment in comments:
        raw += [utility.cleanComment(comment.body)] 
    return raw


def genLabels(label, num):
    return [label for i in range(0, num)] 


def genFeatures(comments):
    samples = []
    for c in comments:
        samples += [commentToFeatures(c)] 
    return samples 


def commentToFeatures(comment):
    features = []
    if numberOfWordsFeature: #TODO: make numberOfWords function
        pass
    if bagOfWordsFeature:
       for word in bagOfWords:
           features += [int(isWordInComment(comment, word))]
    return features


def isWordInComment(comment, word):
    return word in comment


"""
creates the svc model. 

@param X: a list of features lists where each feature list is a sample
@param Y: labels for each sample

"""
def createModel(X, Y):
    model = svm.SVC(gamma="auto");
    model.fit(X,Y)
    return model


main()
