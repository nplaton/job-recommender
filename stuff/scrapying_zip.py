from bs4 import BeautifulSoup
import re
import requests
from time import sleep
from nltk.corpus import stopwords
import pandas as pd
import os
import numpy as np
from pymongo import MongoClient


def cleaning_site(website):
    try:
        site = requests.get(website).text #Connects to Website
    except:
        return 'Data Extraction Failed'

    soup = BeautifulSoup(site, "html.parser") # Get the html from the site
    job_descriptions = soup.findAll('div', itemprop="description")
    descriptions = [job.text.strip().encode('ascii','ignore') for job in job_descriptions]
    return descriptions

def init_mongo_client():
    # Initiate Mongo client
    client = MongoClient()

    # Access database created for these articles
    db = client.job_descriptions

    # Access collection created for these articles
    job_posting = db.zip_jobs

    # Access articles collection in db and return collection pointer.
    return job_posting

def get_url(job, city, state):

    query_job = job.split()
    query_job = "+".join(query_job)

    query_city = city.split()
    query_city = "+".join(query_city)

    url = 'https://www.ziprecruiter.com/candidate/search?search=' + query_job + '&location=' + query_city + '%2C+' + state

    return url


def scraping_zip    (coll, job = None, city = None, state = None):

    if job is None:
        print 'Please insert a job'
        return

    if city is not None:
        zip_url = get_url(job, city, state)

    else:
        query_job = job.split()
        query_job = "+".join(query_job)
        zip_url = 'https://www.ziprecruiter.com/candidate/search?sort=quick-apply&search=' + query_job + '&location='

    site = requests.get(zip_url).text
    soup = BeautifulSoup(site, "html.parser")

    # Scraping number of pages to loop through

    job_numbers = soup.find('h1', class_='headline')
    job_numbers = [i.strip().encode('ascii','ignore') for i in job_numbers]
    job_numbers = job_numbers[0].split(" ")[0]

    # When the total is larger than 1000 the comma in the string cannot be transformed to int
    try:
        job_numbers = "".join(job_numbers.split(','))
    except:
        pass

    jobs_total = int(job_numbers)
    total_pages = jobs_total/20
    print 'Total number of jobs', jobs_total

    final_descriptions = []
    final_companies    = []
    final_cities       = []
    final_states       = []
    final_job_titles   = []

    #Loop that iterates through every page
    for page in xrange(1, total_pages + 1):

        #defining the url for every page
        #example of url: https://www.ziprecruiter.com/candidate/..
        # ..search?sort=quick-apply&search=Data+Scientist&page=2&location= (page 2 )
        url = zip_url
        if page == 1:
            pass
        else:
            url_break = zip_url.split('&location')
            url = url_break[0] + '&page=' + str(page) + '&location' + url_break[1]

        print 'Scraping page %d of %d pages' %(page, total_pages+1)

        site = requests.get(url).text
        soup = BeautifulSoup(site, "html.parser")

        #Scraping city and cleaning data
        cities = soup.findAll('span', itemprop="addressLocality")
        cities = [city.text.strip().encode('ascii','ignore') for city in cities]

        #Scraping State and cleaning data
        states = soup.findAll('span', itemprop="addressRegion")
        states = [state.text.strip().encode('ascii','ignore') for state in states]

        #Scraping company and cleaning data
        companies = soup.findAll('span', class_="name", itemprop="name")
        companies = [company.text.strip().encode('ascii','ignore') for company in companies]

        #Scraping job and cleaning data
        titles = soup.findAll('span', class_="just_job_title")
        titles = [title.text.strip().encode('ascii','ignore') for title in titles]

        # Extracting every job description link of the current page in indeed
        links = soup.findAll('a', class_="job_link t_job_link")
        links = [line.get('href') for line in links]
        job_links = [link for link in links if 'clk' in link]

        #Scraping and cleaning data from the job descriptions links
        job_descriptions =  []
        for url in job_links:
            job_descriptions.append(cleaning_site(url))

        final_descriptions.extend(job_descriptions)
        final_companies.extend(companies)
        final_states.extend(states)
        final_cities.extend(cities)
        final_job_titles.extend(titles)
        sleep(1)
        print 'Inserts:', len(states), len(job_descriptions)

        if page == 20:
            break

    data = pd.DataFrame({'job_title' : final_job_titles, 'job_description' : final_descriptions, 'company' : final_companies, 'state' : final_states, 'city' : final_cities })



    return data

if __name__ == '__main__':

    job_posting = init_mongo_client()
    data = scraping_zip(job_posting,'\'data scientist\'')
    data.to_csv('data/zip_data2')
