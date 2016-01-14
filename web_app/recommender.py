from bs4 import BeautifulSoup
import requests
from time import sleep
import os
from selenium import webdriver
import sys
import cPickle as pickle
from scipy.spatial.distance import cosine
from sklearn.preprocessing import normalize
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel


class user_recommendations(object):

    def __init__(self, url='https://www.linkedin.com/in/iplaton'):
        self.url = url

    def profile_html(self):
        '''
        Purpose: Extracts the html source from the users linkedin
        Input: linkedin url as a string
        Output: HTML of the whole site

        '''
        headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
        browser = webdriver.Chrome("/Applications/chromedriver")
        browser.set_page_load_timeout(5)
        browser.get(self.url)
        html = browser.page_source
        browser.quit()
        return html

    def profile_skills(self):
        '''
        Purpose: Filters the html and obtains the endoresed and non endorsed skills
        Input: html source of the users website
        Output: String
        '''
        html = self.profile_html()
        soup = BeautifulSoup(html, "html.parser")
        skills = soup.findAll('span', class_="wrap")
        skills = (" ").join([skill.text.encode('ascii', 'ignore') for skill in  skills])
        return skills

    def vectorize(self):
        '''
        Purpose: Using already fitted tfidf vectorizer the string is vectorized
        Output: Sparse Matrix
        '''
        skills = self.profile_skills()
        vectorizer = pickle.load(open('web_app/models/vectorizer.pkl', 'r'))
        vectorized_skills = vectorizer.transform([skills])
        matrix_skills = normalize(vectorized_skills, norm='l1', axis=1).toarray()
        return matrix_skills

    def cosine_similarity(self):
        '''
        Purpose: Calculate the cosine similarity between the user's linkedin skills
        and the job postings
        Output: df with the table sorted by cosine similarity
        '''
        df = pickle.load(open('web_app/models/df.pkl', 'r'))
        vectorized_df = pickle.load(open('web_app/models/vectorized_df.pkl', 'r'))
        df_matrix = normalize(vectorized_df, norm='l1', axis=1).toarray()

        matrix_skills = self.vectorize()
        df['cosine_similarity'] = [cosine(x, matrix_skills) for x in df_matrix]
        df.sort_values('cosine_similarity', axis= 0)
        return df
