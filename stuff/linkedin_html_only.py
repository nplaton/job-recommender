from bs4 import BeautifulSoup
import requests
from time import sleep
import os
from selenium import webdriver
import sys

def scrapying_selenium(url):
    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    browser = webdriver.Chrome("/Applications/chromedriver")
    browser.set_page_load_timeout(5)
    browser.get(url)#Connects to Website
    html = browser.page_source
    browser.quit()
    return html

def scraping_linkedin(job, country = 'us'):

    if job is None:
        print 'Please insert a job'
        return

    zip_url = 'https://www.linkedin.com/jobs/search?keywords=' + job + '&locationId=' + country + ':0&start=0'
    html = scrapying_selenium(zip_url)
    # Scraping number of pages to loop through
    soup = BeautifulSoup(html, "html.parser")
    job_numbers = soup.find('div', class_="results-context").text
    job_numbers = job_numbers.split(' ')

    # When the total is larger than 1000 the comma in the string cannot be transformed to int
    try:
        job_numbers = "".join(job_numbers[0].split(','))
    except:
        pass

    jobs_total = int(job_numbers)
    total_pages = jobs_total/25


    #Loop that iterates through every page
    for page in xrange(total_pages):

        #defining the url for every page
        url = 'https://www.linkedin.com/jobs/search?keywords=' + job + '&locationId=' + country + ':0&start=' + str(page*25)
        print 'Scraping page %d of %d pages' %(page, total_pages)

        html = scrapying_selenium(url)
        soup = BeautifulSoup(html, "html.parser")

        # Extracting every job description link of the current page in indeed
        links = soup.findAll('a', class_="job-title-link")
        links = [line.get('href') for line in links]
        job_links = [link for link in links if 'jobs2' in link]

        #Scraping html sources
        for count, url in enumerate(job_links):
            try:
                source = scrapying_selenium(url).encode('utf-8')
            except:
                continue

            html = url.encode('utf-8') + '\n\n' + source
            filename = 'data/html_data/linkedin_' + country + '_' + str(page*25 + count) + '.html'

            with open(filename, 'w') as f:
                f.write(html)
                f.close()

    return

if __name__ == '__main__':
    job = sys.argv[1:][:-1]
    country = sys.argv[1:][2]
    job = '"' + '+'.join(job) + '"'
    data = scraping_linkedin(job, country)
