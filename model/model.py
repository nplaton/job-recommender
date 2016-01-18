import requests
import pandas as pd
import numpy as np
import pickle
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import re
import pymongo
from collections import defaultdict


def load_clean_df():
    '''
    Purpose: Data is loaded from a csv file
    Output: DataFrame that had been merged and cleaned
    '''
    cli = pymongo.MongoClient()
    db = cli.project
    coll = db.Linkedin

    cursor = coll.find()

    df = pd.DataFrame(list(cursor))
    df.to_pickle('web_app/models/df.pkl')
    return df

def tokenizer(description):
    '''
    Purpose: Tokenize, stem  and remove stopwords from descriptions
    Input: string
    Output: List of string of words
    '''
    description = re.findall(r'\w+', description.lower())

    stp = set(stopwords.words('english'))
    desc_stop = [word for word in description if word not in stp]

    snowball = SnowballStemmer('english')
    clean_description = " ".join([str(snowball.stem(word)) for word in desc_stop])

    return clean_description


def vectorize(stemmed_description):
    '''
    Purpose: The clean and stemmed Job Descriptions without stop words is now
    vectorized. The vectorized matrix and the fitted tfidf vectorizer are pickled
    Input: Dataframe
    Ouput:DataFrame
    '''
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    vectorizer = vectorizer.fit(stemmed_description)
    pickle.dump(vectorizer, open('web_app/models/vectorizer.pkl', 'wb'))
    vectorized_df = vectorizer.transform(df['description'])
    pickle.dump(vectorized_df, open('web_app/models/vectorized_df.pkl', 'wb'))
    return vectorizer, vectorized_df 

if __name__ == '__main__':

    df = load_clean_df()
    vectorizer, vectorized_df = vectorize(df['description'])
