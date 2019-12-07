from sklearn import svm
import utility


training = 350

#if a feature is used, it is True
numberOfWordsFeature = True
unstemmedBagOfWordsFeature = False
stemmedBagOfWordsFeature = True


def main():
    boardComments = getRawComments(utility.load_boardgames(training))
    videoComments = getRawComments(utility.load_videogames(training))
    labels = genLabels("board", len(boardComments)) + genLabels("video", len(videoComments))
    bagOfWords = ["play", "board", "soul", "people"]  
    perms = utility.permuations(bagOfWords)       #get permuations of bag of words
    for bag in perms:
        svc = newSVCModel()
        features = genFeatures(boardComments, bag) + genFeatures(videoComments, bag)
        model = trainModel(svc, features, labels, bag)


def trainModel(model, features, labels, bagOfWords):
    model = model.fit(features,labels)
    return model


def genLabels(label, num):
    return [label for i in range(0, num)] 


def genFeatures(comments, bagOfWords):
    samples = []
    for c in comments:
        samples += [commentToFeatures(c, bagOfWords)] 
    return samples 


def commentToFeatures(words, bagOfWords):
    features = []
    if numberOfWordsFeature:
       features += [len(words)]
    if unstemmedBagOfWordsFeature:
       unstemmedComment = utility.stem_cleaned_comment(words) 
       unstemmedBagOfWords = utility.stem_cleaned_comment(bagOfWords)
       for stem in stemmedBagOfWords:
           features += [int(isWordInComment(unstemmedComment, stem))]
    if stemmedBagOfWordsFeature:
       stemmedComment = utility.stem_cleaned_comment(words) 
       stemmedBagOfWords = utility.stem_cleaned_comment(bagOfWords)
       for stem in stemmedBagOfWords:
           features += [int(isWordInComment(stemmedComment, stem))]
    return features


def isWordInComment(comment, word):
    return word in comment


"""
creates the svc model. 

"""
def newSVCModel():
    model = svm.SVC(gamma="auto");
    return model


main()
