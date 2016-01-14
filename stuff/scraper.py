from bs4 import BeautifulSoup
import requests
from time import sleep
import os
from selenium import webdriver
import sys

def scrapying_selenium(url):
    '''
    Purpose: Requesting access to Linkedin, waiting until javascript loads and then
    getting the html of the whole pages
    Input: string
    Output: html
    '''

    headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
    browser = webdriver.Chrome("/Applications/chromedriver")
    browser.set_page_load_timeout(5)
    browser.get(url)#Connects to Website
    html = browser.page_source
    browser.quit()
    return html

def page_count(soup):
    '''
    Purpose: Obtaining the number of jobs that the search engine has found, subsequently
    find the total number of pages to iterate
    Input: html (soup)
    Ouput: int (number of pages)
    '''
    total_jobs = soup.find('div', class_="results-context").text
    total_jobs = total_jobs.split(' ')

    try:
        total_jobs = "".join(total_jobs[0].split(','))
    except:
        return None

    total_pages = int(total_jobs)/25
    return total_pages

def scraping_linkedin(job='\"Data+Scientist\"', country = 'us'):
    '''
    Purpose:
        - Loop through all of the pages that contain job posting matching our query parameters
            - Loop through all the job postings in every page and save the html into disk
    '''

    url = 'https://www.linkedin.com/jobs/search?keywords=' + job + '&locationId=' + country + ':0&start=0'
    html = scrapying_selenium(url)
    soup = BeautifulSoup(html, "html.parser")
    total_pages = page_count(soup)

    if total_pages is None:
        return

    for page in xrange(total_pages):
        '''
        Purpose:
            - iterating through Linkedin job post search engine
            - Scrape the 25 urls for every iteration and storing them in a list

        '''

        start = str(page*25)
        url = 'https://www.linkedin.com/jobs/search?keywords=' + job + '&locationId=' + country + ':0&start=' + start
        print 'Scraping page %d of %d pages' %(page, total_pages)

    if page != 1:
        html = scrapying_selenium(url)
        soup = BeautifulSoup(html, "html.parser")
        links = soup.findAll('a', class_="job-title-link")

            if links == []:
                return

        links = [line.get('href') for line in links]
        job_links = [link for link in links if 'jobs2' in link]

        #Scraping html sources
        for count, url in enumerate(job_links):
            '''
            Purpose:
                - get the html of the 25 job posts of each page
                - Save the html file to disk
                - NO cleaning is done, the whole file is saved untouched
            '''
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
    '''
    Loop through all the countries and two jobs
    '''

    countries = ['af','ax','al','dz','as','ad','ao','ai','aq','ag','ar','am','aw','au','at','az','bs',
    'bh','bd','bb','by','be','bz','bj','bm','bt','bo','ba','bw','bv','br','io','bn','bg','bf','bi','kh',
    'cm','ca','cv','ky','cf','td','cl','cn','cx','cc','co','km','cg','cd','ck','cr','ci','hr','cu','cy',
    'cz','dk','dj','dm','do','ec','eg','sv','gq','er','ee','et','fk','fo','fj','fi','fr','gf','pf','tf',
    'ga','gm','ge','de','gh','gi','gr','gl','gd','gp','gu','gt','gn','gw','gy','ht','hm','va','hn','hk',
    'hu','is','in','id','ir','iq','ie','il','it','jm','jp','jo','kz','ke','ki','kp','kr','kw','kg','la',
    'lv','lb','ls','lr','ly','li','lt','lu','mo','mk','mg','mw','my','mv','ml','mt','mh','mq','mr','mu',
    'yt','mx','fm','md','mc','mn','ms','ma','mz','mm','na','nr','np','nl','an','nc','nz','ni','ne','ng',
    'nu','nf','mp','no','om','pk','pw','ps','pa','pg','py','pe','ph','pn','pl','pt','pr','qa','re','ro',
    'ru','rw','sh','kn','lc','pm','vc','ws','sm','st','sa','sn','cs','sc','sl','sg','sk','si','sb','so',
    'za','gs','es','lk','sd','sr','sj','sz','se','ch','sy','tw','tj','tz','th','tl','tg','tk','to','tt',
    'tn','tr','tm','tc','tv','ug','ua','ae','gb','us','um','uy','uz','vu','ve','vn','vg','vi','wf','eh',
    'ye','zm','zw']

    jobs = ['\"Data+Scientist\"', '\"Data+Science\"']
    data = scraping_linkedin()

    '''
    for job in jobs:
        for country in countries:
            data = scraping_linkedin(job, country)

    '''
