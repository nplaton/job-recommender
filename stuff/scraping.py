from bs4 import BeautifulSoup
import re
import requests
from time import sleep
from nltk.corpus import stopwords
import pandas as pd
import os
import numpy as np


def get_url(job, city, state):

    query_job = job.split()
    query_job = "+".join(query_job)

    query_city = city.split()
    query_city = "+".join(query_city)

    url = 'http://www.indeed.com/jobs?q=' + query_job + '&l=' + query_city + '%2C+' + state

    return url
def request_site(website):
    try:
        site = requests.get(website).text #Connects to Website
    except:
        return 'Data Extraction Failed'

    return BeautifulSoup(site, "html.parser")

def cleaning_site(website):
    try:
        site = requests.get(website).text #Connects to Website
    except:
        return 'Data Extraction Failed'

    soup = BeautifulSoup(site, "html.parser")
    for row in soup.find_all(['script', 'style']):
        row.extract()

    text = (' ').join([job.text.strip().encode('ascii','ignore') for job in soup.findAll('li')])
    stop_words = set(stopwords.words("english"))
    text = [word for word in text.split() if not word in stop_words]
    text = " ".join([word for word in text])
    return text

'''
def cleaning_site(website):

    soup = request_site(website)
    for row in soup.find_all(['script', 'style']):
        row.extract()

    text = soup.get_text() # Get the text from this
    text = re.sub("[^a-zA-Z.+3]"," ", text)
    text = text.lower()
    text = text.decode('unicode_escape').encode('ascii', 'ignore')


    stop_words = set(stopwords.words("english"))
    text = [word for word in text.split() if not word in stop_words]
    text = " ".join([word for word in text])

    return text
'''
def scraping_indeed(job = None, city = None, state = None):

    if job is None:
        print 'Please insert a job'
        return

    if city is not None:
        indeed_url = get_url(job, city, state)

    else:
        indeed_url = 'http://www.indeed.com/jobs?q=' + job + '&l='

    soup = request_site(indeed_url)

    # Scraping number of pages to loop through

    jobs_numbers = soup.find('div', id='searchCount').text

    jobs_number = jobs_numbers.split('of ')[-1]

    # When the total is larger than 1000 the comma in the string cannot be transformed to int
    try:
        jobs_number = "".join(jobs_number.split(','))
    except:
        pass

    jobs_total = int(jobs_number)
    total_pages = jobs_total/14

    final_descriptions = []
    final_companies    = []
    final_locations    = []
    final_job_titles   = []

    #Loop that iterates through every page
    for page in xrange(1, total_pages + 1):

        #defining the url for every page
        #example of url: http://www.indeed.com/jobs?q=data+scientist&l=Chicago%2C+IL&start=10 (page 2 )
        if page == 1:
            url = indeed_url
        else:
            url = indeed_url + '&start=' + str((page-1)*10)

        print 'Scraping page %d of %d pages' %(page, total_pages+1)
        soup = request_site(url)

        #Scraping job title and cleaning data
        job_titles = soup.findAll('a', rel = 'nofollow', target="_blank")
        #job_titles = job_titles.findAll('a', data-tn-element = "jobTitle")
        job_titles = [job_title.text.strip().encode('ascii','ignore') for job_title in job_titles]

        #Scraping Company Location and cleaning the data
        locations = soup.findAll('span', class_='location')
        locations = [location.text.strip().encode('ascii','ignore') for location in locations]

        # Scraping Company Name and cleaning the data
        companies = soup.findAll('span', class_='company')
        companies = [company.text.strip().encode('ascii','ignore') for company in companies]

        # Extracting every job description link of the current page in indeed
        links = soup.findAll('a', href=True, rel='nofollow', class_="turnstileLink")
        job_links = [line.get('href') for line in links]
        if len(job_links) != len(companies):
            links = soup.findAll('a', href=True, rel='nofollow')
            job_links = [link for link in links if 'clk' in link]

        #ob_links = [link for link in links if 'clk' in link]
        all_urls = []

        #Creating a list containing the job links for the current page in indeed
        for link in job_links:
            all_urls.append('http://www.indeed.com' + link)

        #Scraping and cleaning data from the job descriptions links
        job_descriptions =  []
        for url in all_urls:
            job_descriptions.append(cleaning_site(url))

        if len(job_links) != len(companies):
            print "companies and links do not match"
            continue

        print
        final_descriptions.extend(job_descriptions)
        final_companies.extend(companies)
        final_locations.extend(locations)
        final_job_titles.extend(job_titles)


        sleep(1)
        if page == 60:
            break

    data = pd.DataFrame({'job_title' : final_job_titles, 'job_description' : final_descriptions, 'company' : final_companies, 'location' : final_locations })
    return data

if __name__ == '__main__':
    data = scraping_indeed('data scientist')
    data.to_csv('data/jobs_data')
