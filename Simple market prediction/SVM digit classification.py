## Digit prediction using SVM
## [insert description here]

## Import required libraries
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

## Import datasets
digits = datasets.load_digits()

## Specify classifier
#SVM selected. Gamma and C value defined [to research]
clf = svm.SVC(gamma=0.000001, C=100)

## Load and train model
# X is multidimensional coordinate data, y is classifying label
X,y = digits.data[:-10], digits.target[:-10]
clf.fit(X,y)

## Output mdoel results
#train and visualist the predicted digit
print(clf.predict(digits.data[-5]))
plt.imshow(digits.images[-5], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()
