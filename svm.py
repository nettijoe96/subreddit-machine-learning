import sklearn
import utility
import operator

training = 350
dev = 175
testing = 175


#some rudimentary feature selection stuff is below


boardComments = utility.load_boardgames(training)
boardDict = utility.wordFreq(boardComments)
boardTup = sorted(boardDict.items(), key=operator.itemgetter(1), reverse=1)
#for i in range(0, 50):
#    print(boardTup[i][0], boardTup[i][1])

print()

videoComments = utility.load_videogames(training)
videoDict = utility.wordFreq(videoComments)
videoTup = sorted(videoDict.items(), key=operator.itemgetter(1), reverse=1)
#for i in range(0, 50):
#    print(videoTup[i][0], videoTup[i][1])



print("top boardgames words that are different from videogames")
diff = 20
boardDiff = []
for i in range(0, 50):
    word = boardTup[i][0]  
    boardVal = boardTup[i][1]
    videoVal = 0
    if word in videoDict:
        videoVal = videoDict[word]
    wordDiff = boardVal - videoVal
    if wordDiff >= diff:
        boardDiff += [(word, wordDiff)]

for w in boardDiff:
    print(w)


print("top videogame words that are different from boardgames\n")
videoDiff = []
diff = 20
for i in range(0, 50):
    word = videoTup[i][0]  
    videoVal = videoTup[i][1]
    boardVal = 0
    if word in boardDict:
        boardVal = boardDict[word]
    wordDiff = videoVal - boardVal
    if wordDiff >= diff:
        videoDiff += [(word, wordDiff)]

for w in videoDiff:
    print(w)


