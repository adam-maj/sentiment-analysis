import nltk
import pandas as pd

#Get the dataset and split the reviews(X) and ratings(Y)
dataset = pd.read_csv('reviews.csv')
X = dataset.iloc[:, 1]
Y = dataset.iloc[:, 0]

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Tokenize the reviews
for i in range(len(X.index)):
    X.iat[i] = word_tokenize(X.iat[i])

#Filter stopwords   
stop_words = set(stopwords.words('english'))

for i in range(len(X.index)):
    X.iat[i] = [w for w in X.iat[i] if not w in stop_words]


#Part of Speech Tagging
tagged_reviews = pd.DataFrame(columns = ['Reviews'])

for i in range(len(X.index)):
    tagged = nltk.pos_tag(X.iat[i])
    tagged_reviews = tagged_reviews.append({'Reviews': tagged}, ignore_index = True)

#Stemming
from nltk.stem import PorterStemmer

ps = PorterStemmer()

for i in range(len(X.index)):
    stemmed_words = []
    for w in X.iat[i]:
        stemmed_words.append(ps.stem(w))
    X.iat[i] = stemmed_words
    