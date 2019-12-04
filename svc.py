from sklearn import svm
import utility

training = 350

boardComments = utility.load_boardgames(training)
videoComments = utility.load_videogames(training)

bagOfWords = ["people", "game"]

comments = boardComments + videoComments
X = []
Y = []

for c in boardComments:
    Y += ["board"]
for c in videoComments:
    Y += ["video"]

for c in comments:
   cleaned = utility.cleanComment(c.body)
   features = []
   for word in bagOfWords:
       if word in cleaned:
           features += [1]
       else:
           features += [0]
   X += [features]

model = svm.SVC(gamma="auto");
model.fit(X,Y)



