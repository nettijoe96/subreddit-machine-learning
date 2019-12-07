from sklearn import svm
import utility


training = 350

#if a feature is used, it is True
numberOfWordsFeature = True
unstemmedBagOfWordsFeature = False
stemmedBagOfWordsFeature = True
wordsInDictionary = False
englishDict = utility.makeEnglishDict()


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
    if wordsInDictionary:
        features += [int(allEnglishWordsOrNumbers(words))]
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


def allEnglishWordsOrNumbers(words):
    for word in words:
        if not utility.isEnglishWord(englishDict, word) and not utility.is_number(word):
            return False
        
    return True


"""
creates the svc model. 

"""
def newSVCModel():
    model = svm.SVC(gamma="auto");
    return model

