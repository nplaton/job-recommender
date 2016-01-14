from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import urllib
import sys
import cPickle


def bullet_points(soup):
    return '*****'
'''
    content = soup.findAll('div', class_="content")
    for description in content[1:]:
        for bullet_points in description.findAll('li'):
            clean_desc.append(('').join(bullet_points.text.strip().encode('ascii','ignore')))
    return clean_desc

class CleaningJobPost(object):

    def __init__(self, soup):
        self.soup = soup

    def bullet(self):
        content = self.soup.findAll('div', class_="content")
        clean_desc =[]
        for description in content[1:]:
            for bullet_points in description.findAll('li'):
                clean_desc.append(('').join(bullet_points.text.strip().encode('ascii','ignore')))
        return clean_desc
'''
