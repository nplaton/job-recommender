from bs4 import BeautifulSoup
import re
import requests
from time import sleep
from nltk.corpus import stopwords
import pandas as pd
import os
import numpy as np
import urllib
from selenium import webdriver
import sys
import cPickle


def cleaning_description(soup):
    '''
    Purpose: Cleaning the description of all job descriptions, filters it by Extracting
    only the data in bulletpoints
    Input: html (soup)
    Ouput: string
    '''
    job_descriptions = soup.findAll('div', class_="content")
    clean_site = []
    for job_description in job_descriptions[1:]:
        for job in job_description.findAll('li'):
            clean_site.append(('').join(job.text.strip().encode('ascii','ignore')))

    stop_words = set(stopwords.words("english"))
    text = [word for word in clean_site if not word in stop_words]
    return " ".join([word for word in text])

def image_url_(soup):
    try:
        image_url = str(soup.find('img', class_="logo lazy-load lazy-load-loaded")['src'])
    except:
        pass
    try:
        image_url = str(soup.find('img', class_="logo")['src'])
    except:
        pass
    try:
        url = soup.find('img', class_="company-logo")['src']
        base = 'https://www.linkedin.com'
        image_url = base + str(url)
    except:
        image_url = None

    return image_url

def job_post_link_(soup):
    '''
    Purpose: Extracting the job post link that I hard coded in scraper.py
    Input: html (soup)
    Output: string (job post link)
    '''

    try:
        return str(soup.find('h1', class_="my-job-link", itemprop="mine").text)
    except:
        return None

def big_df(soup):
    '''
    Purpose: Obtains information such as job title, location, image url... and
    then puts it in a pandas Dataframe
    Input: soup
    Ouput: Pandas Dataframe
    '''
    description = cleaning_description(soup)

    image_url = image_url_(soup)

    title = soup.find('h1', class_="title", itemprop="title")
    #title = title.get_text.strip().encode('ascii','ignore')
    title = title.get_text()
    print title

    company = soup.find('span', itemprop="name", class_="company")
    #company = company.get_text.strip().encode('ascii','ignore')
    company = company.get_text()

    print company

    location = soup.find('span', itemprop="address")
    #location = location.get_text.strip().encode('ascii','ignore')
    location = location.get_text()

    print location

    job_post_link = job_post_link_(soup)

    return location, company, title, image_url, description, job_post_link

def main():
    '''
    Purpose: Loop through all of the files in the directory, where I have all
    of my html files stored.
    All the data is consolidated in a pandas Dataframe and written to disk
    '''

    countries = cPickle.load(open('data/countries.p', 'rb'))
    countries = ['ch', 'es']
    jobs = ['Data Scientist', 'Data Science']

    all_locations = []
    all_companies = []
    all_titles = []
    all_image_url = []
    all_descriptions = []
    all_job_post_link = []

    for job in jobs:
        for country in countries:
            for i in xrange(100000):
                filename = 'data/html_data/linkedin_' + str.replace(job, ' ', '_') + '_' +  country + '_' + str(i) + '.html'
                try:
                    html = urllib.urlopen(filename)
                    soup = BeautifulSoup(html, "html.parser")
                except:
                    break

                print filename
                location, company, title, image_url, description, \
                job_post_link = big_df(soup)

                all_locations.append(location)
                all_companies.append(company)
                all_titles.append(title)
                all_image_url.append(image_url)
                all_descriptions.append(description)
                all_job_post_link.append(job_post_link)


    data = pd.DataFrame({'job_title' : all_titles, 'job_description' : all_descriptions, \
    'company' : all_companies, 'location' : all_locations, 'job_links' : all_job_post_link})
    data.to_csv('data/all_df')
    return

if __name__ == '__main__':
    main()
