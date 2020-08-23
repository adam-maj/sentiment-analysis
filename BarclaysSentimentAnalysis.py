import nltk
import random
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Import the reviews dataset
reviews = pd.read_csv('reviews.csv')

#Change the ratings from 1 to 5 to positive(4, 5) or negative (1, 2, 3)
ratings = ['pos' if reviews.iat[i, 0] > 3 else 'neg' 
           for i in range(len(reviews.index))]

reviews['rating'] = ratings

#Tokenize the words in each review
for i in range(len(reviews.index)):
    reviews.iat[i, 1] = word_tokenize(reviews.iat[i, 1])

#Filter stopwords in each review
stop_words = set(stopwords.words('english'))

for i in range(len(reviews.index)):
    reviews.iat[i, 1] = [w for w in reviews.iat[i, 1] if not w in stop_words]

#Get the dataset into the proper format of a list of tuples for NLTK
dataset = []
for row in reviews.itertuples(index = False):
    dataset.append((getattr(row, 'review'), getattr(row, 'rating')))

#Randomize the orders of the reviews
random.shuffle(dataset)

#Get list of all words used in any review
all_words = []
for i in range(len(reviews.index)):
    for w in reviews.iat[i, 1]:
        all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

#Find the most common words used in all the reviews
word_features = [item[0] for item in all_words.most_common(10000)]

#Find which reviews contain these most common words
def find_features(review):
    words = set(review)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    
    return features

feature_sets = [(find_features(review), rating) for (review, rating) in dataset]

training_set = feature_sets[:1000]
testing_set = feature_sets[1000:]

classifier = nltk.NaiveBayesClassifier.train(training_set)
print('Naive Bayes Accuracy Percent:', (nltk.classify.accuracy(classifier, testing_set)*100))
classifier.show_most_informative_features(10)