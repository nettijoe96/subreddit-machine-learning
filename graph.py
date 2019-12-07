from matplotlib import pyplot as plt
import pickle
import evaluate

filenameSVC = "confMatrixFile.pickle"
filenameForest = "confMatrixFile_Forest.pickle"

def extractData(filename):
    f = open(filename, "rb")
    lstConfMatrix = pickle.load(f)
    recallB = []
    precisionB = []
    recallV = []
    precisionV = []
    for m in lstConfMatrix:
        recallB += [evaluate.calcRecall(m[0][0])]
        precisionB += [evaluate.calcPrecision(m[0][0])]
        recallV += [evaluate.calcRecall(m[0][1])]
        precisionV += [evaluate.calcPrecision(m[0][1])]
    
    highestDiff = len(lstConfMatrix)
    x = [i for i in range(1, highestDiff+1)]

    return recallB, precisionB, recallV, precisionV, x



forestRecallB, forestPrecisionB, forestRecallV, forestPrecisionV, x = extractData(filenameForest)
svcRecallB, svcPrecisionB, svcRecallV, svcPrecisionV, x = extractData(filenameSVC)

print("max forestRecallB", max(forestRecallB), forestRecallB.index(max(forestRecallB)))
print("max forestPrecisionB", max(forestPrecisionB), forestPrecisionB.index(max(forestPrecisionB)))
print("max forestRecallV", max(forestRecallV), forestRecallV.index(max(forestRecallV)))
print("max forestPrecisionV", max(forestPrecisionV), forestPrecisionV.index(max(forestPrecisionV)))

print("max svcRecallB", max(svcRecallB), svcRecallB.index(max(svcRecallB)))
print("max svcPrecisonB", max(svcPrecisionB), svcPrecisionB.index(max(svcPrecisionB)))
print("max svcRecallV", max(svcRecallV), svcRecallV.index(max(svcRecallV)))
print("max svcPrecisionV", max(svcPrecisionV), svcPrecisionV.index(max(svcPrecisionV)))

plt.plot( x, forestRecallB, marker='o', markerfacecolor='green', markersize=5, color='green', linewidth=2, label="Forest r/boardgames")
plt.plot( x, forestRecallV, marker='o', markerfacecolor='#4ac901', markersize=5, color='#4ac901', linewidth=2, label="Forest r/videogames")
plt.plot( x, svcRecallB, marker='o', markerfacecolor='#9c0a00', markersize=5, color='#9c0a00', linewidth=2, label="SVC r/boardgames")
plt.plot( x, svcRecallV, marker='o', markerfacecolor='red', markersize=5, color='red', linewidth=2, label="SVC r/videogames")
plt.title("Recall for Forest and SVC")
plt.legend()
plt.ylabel("recall")
plt.xlabel("min. word difference in bag of words")
plt.show()


plt.plot( x, forestPrecisionB, marker='o', markerfacecolor='green', markersize=5, color='green', linewidth=2, label="Forest r/boardgames")
plt.plot( x, forestPrecisionV, marker='o', markerfacecolor='#4ac901', markersize=5, color='#4ac901', linewidth=2, label="Forest r/videogames")
plt.plot( x, svcPrecisionB, marker='o', markerfacecolor='#9c0a00', markersize=5, color='#9c0a00', linewidth=2, label="SVC r/boardgames")
plt.plot( x, svcPrecisionV, marker='o', markerfacecolor='red', markersize=5, color='red', linewidth=2, label="SVC r/videogames")
plt.title("Precision for Forest and SVC")
plt.legend()
plt.ylabel("precision")
plt.xlabel("min. word difference in bag of words")
plt.show()


#9c0a00
