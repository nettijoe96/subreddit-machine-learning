from sklearn import svm
from sklearn import ensemble
import utility


training = 350

#if a feature is used, it is True
numberOfWordsFeature = True
unstemmedBagOfWordsFeature = False
stemmedBagOfWordsFeature = True

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
           features += [int(unstemmedComment.count(stem))]
    if stemmedBagOfWordsFeature:
       stemmedComment = utility.stem_cleaned_comment(words) 
       stemmedBagOfWords = utility.stem_cleaned_comment(bagOfWords)
       for stem in stemmedBagOfWords:
           features += [int(stemmedComment.count(stem))]
    return features


def isWordInComment(comment, word):
    return word in comment


"""
creates the svc model. 

"""
def newSVCModel():
    model = svm.SVC(gamma="auto");
    return model
    
"""
creates the random forest model. 

"""
def newRandomForestModel():
    model = ensemble.RandomForestClassifier(n_estimators= 1000, random_state = 1);
    return model

