import pickle as p
from textblob.classifiers import NaiveBayesClassifier

classifier_f = open("naivebayes.pickle", "rb")
cl = p.load(classifier_f)
classifier_f.close()
print(cl.classify("This is an amazing library!"))