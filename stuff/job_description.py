from bs4 import BeautifulSoup
import requests
import re
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import urllib
import sys
import cPickle


def desc_cleaning(soup):
    clean_desc = []
    content = soup.findAll('div', class_="content")

    for description in content[1:]:
        for bullet_points in description.findAll('li').text:
            #clean_desc.append(('').join(bullet_points.text.strip().encode('ascii','ignore')))

    return
            #bullet_points.strip().encode('ascii','ignore')
