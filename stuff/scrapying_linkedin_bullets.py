from bs4 import BeautifulSoup
import re
import requests
from time import sleep
from nltk.corpus import stopwords
import pandas as pd
import os
import numpy as np
from selenium import webdriver
import sys

def scrapying_selenium(url):
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    browser = webdriver.Chrome("/Applications/chromedriver")
    browser.set_page_load_timeout(5)
    browser.get(url) #Connects to Website
    soup = BeautifulSoup(browser.page_source, "html.parser")# Get the html from the site
    browser.quit()
    return soup

def init_mongo_client():
    # Initiate Mongo client
    client = pymongo.MongoClient()

    # Access database created for these articles
    db = client.job_descriptions

    # Access collection created for these articles
    job_descriptions = db.zip_jobs

    # Access articles collection in db and return collection pointer.
    return db.zip_jobs


def cleaning_site(website):
    try:
        soup = scrapying_selenium(website) #Connects to Website
    except:
        return 'Data Extraction Failed'

    job_descriptions = soup.findAll('div', class_="content")
    clean_site = []
    for job_description in job_descriptions[1:]:
        for job in job_description.findAll('li'):
            clean_site.append(('').join(job.text.strip().encode('ascii','ignore')))
        #clean_text = (' ').join(clean_site)

    stop_words = set(stopwords.words("english"))
    text = [word for word in clean_site if not word in stop_words]
    return " ".join([word for word in text])


def scraping_linkedin(job, country = 'us'):

    if job is None:
        print 'Please insert a job'
        return

    query_job = job.split()
    query_job = "+".join(query_job)
    zip_url = 'https://www.linkedin.com/jobs/search?keywords=' + query_job + '&locationId=' + country + ':0&start=0'
    soup = scrapying_selenium(zip_url)
    # Scraping number of pages to loop through

    job_numbers = soup.find('div', class_="results-context").text
    job_numbers = job_numbers.split(' ')

    # When the total is larger than 1000 the comma in the string cannot be transformed to int
    try:
        job_numbers = "".join(job_numbers[0].split(','))
    except:
        pass

    jobs_total = int(job_numbers)
    print "There are %d Data Science jobs" % jobs_total
    total_pages = jobs_total/25
    final_descriptions = []
    final_companies    = []
    final_titles       = []
    final_locations    = []

    #Loop that iterates through every page
    for page in xrange(total_pages):

        #defining the url for every page
        url = 'https://www.linkedin.com/jobs/search?keywords=' + query_job + '&locationId=' + country + ':0&start=' + str(page*25)
        print 'Scraping page %d of %d pages' %(page, total_pages)

        soup = scrapying_selenium(url)

        #Scraping State and cleaning data
        locations = soup.findAll('span', itemprop="addressLocality")
        locations = [location.text.strip().encode('ascii','ignore') for location in locations]

        #Scraping company and cleaning data
        companies = soup.findAll('span', class_="company-name-text")
        companies = [company.text.strip().encode('ascii','ignore') for company in companies]

        #Scraping job and cleaning data
        titles = soup.findAll('span', class_="job-title-text")
        titles = [title.text.strip().encode('ascii','ignore') for title in titles]

        companies_details = soup.findAll('div', class_="rich-text", itemprop="description")
        comapanies_details = [details.text.strip().encode('ascii','ignore') for details in companies_details]

        # Extracting every job description link of the current page in indeed
        links = soup.findAll('a', class_="job-title-link")
        links = [line.get('href') for line in links]
        job_links = [link for link in links if 'jobs2' in link]

        #Scraping and cleaning data from the job descriptions links
        job_descriptions =  []
        for url in job_links:
            job_descriptions.append(cleaning_site(url))

        final_descriptions.extend(job_descriptions)
        final_companies.extend(companies)
        final_locations.extend(locations)
        final_titles.extend(titles)
        sleep(10)

        if page % 5 == 1:
            data = pd.DataFrame({'job_title' : final_titles, 'job_description' : final_descriptions, 'company' : final_companies, 'location' : final_locations})
            file_name = 'data/jobs_data_linkedin_' + country
            data.to_csv(file_name)

    return data

if __name__ == '__main__':
    job = sys.argv[1:][0]
    country = sys.argv[1:][1]
    data = scraping_linkedin(" ".join(job), country)
