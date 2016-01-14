from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import urllib
import sys
import cPickle
import re

def get_bullet_points(soup):

    content = soup.findAll('div', class_="content")
    clean_desc = []

    for text in content[1:]:
        for point in text.findAll('li'):
            point = point.get_text(' ').encode('ascii','ignore')
            clean_desc.append(point.strip())
    return clean_desc

def get_bullet_strings(soup):
    content = soup.findAll('div', class_="content")
    character_list = ['-']
    character = re.compile(r'%s' % '|'.join(character_list), flags=re.IGNORECASE)
    words = ["social media", "views", 'Full-time', 'Mid-Senior level']
    remove = re.compile(r'%s' % '|'.join(words), flags=re.IGNORECASE)
    clean_desc =[]

    for text in content[1:]:
        text = text.get_text(' ').encode('ascii','ignore')
        for point in  text.split('.'):
            if len(character.findall(point)) != 0 :
                if len(remove.findall(point)) == 0:         
                    clean_desc.append(point.strip()) 

    
    return clean_desc

    
'''
>>> exactMatch = re.compile(r'%s' % '|'.join(words), flags=re.IGNORECASE)
>>> print exactMatch.findall("my blue blue cat")
['blue', 'blue']
>>> print len(exactMatch.findall("my blue blue cat"))
'''
'''
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
