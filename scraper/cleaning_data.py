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
from langdetect import detect
from desc_cleaner import get_bullet_points, get_bullet_strings


def get_description(soup):
    global count
    text = get_bullet_points(soup)
    if text == []:
        text = get_bullet_strings(soup)
    '''
    if job_description == []:
        count+=1
        if count > 4:
            raise ValueError('Check get_description\n')
            print "\n*****************"
    '''
    text = " ".join(text)

    return text

def get_logo(soup):
    try:
        return str(soup.find('img', class_="logo lazy-load lazy-load-loaded")['src'])
    except:
        pass
    try:
        return str(soup.find('img', class_="logo")['src'])
    except:
        pass
    try:
        url = soup.find('img', class_="company-logo")['src']
        base = 'https://www.linkedin.com'
        return base + str(url)
    except:
        return None

    return logo

def get_post_link(soup):
    '''
    Purpose: Extracting the job post link that I hard coded in scraper.py
    Input: html (soup)
    Output: string (job post link)
    '''
    try:
        return soup.find('h1', class_="my-job-link", itemprop="mine").text.encode('ascii', 'ignore')
    except:
        return

def get_company(soup):
    try:
        return soup.find('span', class_="company").text.encode('ascii', 'ignore')
    except:
        print "\n*****************"
        print "Check get_company"
        return

def get_title(soup):
    try:
        return soup.find('h1', class_="title", itemprop="title").text.encode('ascii', 'ignore')
    except:
        print "\n*****************"
        print "Check get_title"
        return

def get_location(soup):
    try:
        return soup.find('span', itemprop="address").text.encode('ascii', 'ignore')

    except:
        print "\n*****************"
        print "Check get_location"
        return

def get_company_link(soup):

    try:
        return soup.find('a', class_="company")['href']
    except:
        print "\n*****************"
        print "Check get_company_link"
        return

def big_df(soup):
    '''
    Purpose: Obtains information such as job title, location, image url... and
    then puts it in a pandas Dataframe
    Input: soup
    Ouput: Pandas Dataframe
    '''
    description = get_description(soup)
    logo = get_logo(soup)
    title = get_title(soup)
    company = get_company(soup)
    location = get_location(soup)
    job_post_link = get_post_link(soup)
    company_link = get_company_link(soup)

    return location, company, title, logo, description, job_post_link, company_link

def main():
    '''
    Purpose: Loop through all of the files in the directory, where I have all
    of my html files stored.
    All the data is consolidated in a pandas Dataframe and written to disk
    '''
    global count
    count = 0
    countries = cPickle.load(open('data/countries.p', 'rb'))
    #countries = ['ch', 'es']
    jobs = ['Data Scientist', 'Data Science']

    all_locations = []
    all_companies = []
    all_titles = []
    all_logos = []
    all_descriptions = []
    all_job_links = []
    all_logo_links = []
    all_company_links = []


    for job in jobs:
        for country in countries:
            for i in xrange(100000):
                filename = 'data/html_data/linkedin_' + str.replace(job, ' ', '_')\
                 + '_' +  country + '_' + str(i) + '.html'
                try:
                    html = urllib.urlopen(filename)
                    soup = BeautifulSoup(html, "html.parser")
                except:
                    break
                #print filename

                location, company, title, logo, description, \
                job_post_link, company_link= big_df(soup)

                all_locations.append(location)
                all_companies.append(company)
                all_titles.append(title)
                all_logos.append(logo)
                all_descriptions.append(description)
                all_job_links.append(job_post_link)
                all_company_links.append(company_link)
         

    df = pd.DataFrame({'job_title' : all_titles, 'job_description' : all_descriptions, \
    'company' : all_companies, 'location' : all_locations, 'job_link' : all_job_links, \
    'logo' : all_logos, 'company_link' : all_company_links})


    df.to_csv('data/all_df')


if __name__ == '__main__':
    main()
