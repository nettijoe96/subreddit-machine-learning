from matplotlib import pyplot as plt
import pickle
import evaluate

filename = "confMatrixFile.pickle"
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

plt.plot( x, recallB, marker='o', markerfacecolor='red', markersize=6, color='red', linewidth=2, label="h1")
plt.plot( x, recallV, marker='o', markerfacecolor='blue', markersize=6, color='blue', linewidth=2, label="h1")
plt.show()

plt.plot( x, precisionB, marker='o', markerfacecolor='red', markersize=6, color='red', linewidth=2, label="h1")
plt.plot( x, precisionV, marker='o', markerfacecolor='blue', markersize=6, color='blue', linewidth=2, label="h1")
plt.show()

