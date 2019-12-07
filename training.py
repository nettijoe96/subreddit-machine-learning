from sklearn import svm
from sklearn import ensemble
import utility


training = 350

#if a feature is used, it is True
numberOfWordsFeature = True
unstemmedBagOfWordsFeature = False
stemmedBagOfWordsFeature = True
wordsInDictionaryFeature = False
englishDict = utility.makeEnglishDict()


def trainModel(model, features, labels, bagOfWords):
    printFeatures()
    model = model.fit(features,labels)
    return model


def printFeatures():
    print("features for the model:")
    print("numberOfWordsFeature: ", numberOfWordsFeature)
    print("unstemmedBagOfWordsFeature: ", unstemmedBagOfWordsFeature)
    print("stemmedBagOfWordsFeature: ", stemmedBagOfWordsFeature)
    print("wordsInDictionaryFeature: ", wordsInDictionaryFeature)


def genLabels(label, num):
    return [label for i in range(0, num)] 


def genFeatures(comments, bagOfWords):
    samples = []
    for c in comments:
        samples += [commentToFeatures(c, bagOfWords)] 
    return samples 


def commentToFeatures(words, bagOfWords):
    features = []
    if wordsInDictionaryFeature:
        features += [utility.avgNonEnglishWordsOrNumbers(englishDict, words)]
        #features += [int(utility.allEnglishWordsOrNumbers(englishDict, words))]
    if numberOfWordsFeature:
       features += [len(words)]
    if unstemmedBagOfWordsFeature:
       unstemmedComment = words 
       unstemmedBagOfWords = bagOfWords #right now bag of words is stemmed
       for stem in unstemmedBagOfWords:
           features += [int(isWordInComment(unstemmedComment, stem))]
    if stemmedBagOfWordsFeature:
       stemmedComment = utility.stem_cleaned_comment(words) 
       #stemmedBagOfWords = utility.stem_cleaned_comment(bagOfWords)  //TODO: this may cause issues elsewhere
       for stem in bagOfWords:
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
    
"""
creates the random forest model. 

"""
def newRandomForestModel():
    model = ensemble.RandomForestClassifier(n_estimators= 1000, random_state = 1);
    return model

