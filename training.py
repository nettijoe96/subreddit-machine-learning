from sklearn import svm
from sklearn import ensemble
import utility


training = 350

#if a feature is used, it is True
numberOfWordsFeature = True
stemmedBagOfWordsFeature = True
wordsInDictionaryFeature = False
englishDict = utility.makeEnglishDict()


"""
train a model and print the featues
@param: model: an already created model (svc or forest)
@param: features: list of features lists
@param: labels: list of labels
@param: bagOfWords
@param: return model after fitted
"""
def trainModel(model, features, labels, bagOfWords):
    printFeatures()
    model = model.fit(features,labels)
    return model


"""
prints active features
"""
def printFeatures():
    print("features for the model:")
    print("numberOfWordsFeature: ", numberOfWordsFeature)
    print("stemmedBagOfWordsFeature: ", stemmedBagOfWordsFeature)
    print("wordsInDictionaryFeature: ", wordsInDictionaryFeature)



"""
generates num labels all of same kind
@param: label
@param: num
@return list of labels
"""
def genLabels(label, num):
    return [label for i in range(0, num)] 


"""
generates features for comments
@param: raw comments (already cleaned)
@param: bagOfWords (stemmed)
@return list of feature lists
"""
def genFeatures(comments, stemmedBagOfWords):
    samples = []
    for c in comments:
        samples += [commentToFeatures(c, stemmedBagOfWords)] 
    return samples 


"""
gets a single comment's features
@param: words of comment (unstemmed but cleaned)
@param: bagOfWords (stemmed)
@return feature list
"""
def commentToFeatures(words, bagOfWords):
    features = []
    if wordsInDictionaryFeature:
        features += [utility.avgNonEnglishWordsOrNumbers(englishDict, words)]    #for average option
        #features += [int(utility.allEnglishWordsOrNumbers(englishDict, words))] #for binary option
    if numberOfWordsFeature:
       features += [len(words)]
    if stemmedBagOfWordsFeature:
       stemmedComment = utility.stem_cleaned_comment(words) 
       for stem in bagOfWords:
           features += [int(isWordInComment(stemmedComment, stem))]
    return features


"""
checks if word is in comment
"""
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

