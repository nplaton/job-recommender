from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import urllib
import sys
import cPickle

class Cleaning(object):

    def __init__(self, soup):
        self.soup = soup

    def bullets(self, soup):
        content = self.soup.findAll('div', class_="content")
        clean_desc =[]
        for description in content[1:]:
            for bullet_points in description.findAll('li').text:
                clean_desc.append(('').join(bullet_points.text.strip().encode('ascii','ignore')))

        return clean_desc
                #bullet_points.strip().encode('ascii','ignore')
