from bs4 import BeautifulSoup
import cPickle
import pymongo
from langdetect import detect # filter out german, french spanish
from desc_cleaner import get_bullet_points, get_bullet_strings
from clean_df import featurizing_locations

'''

'''


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
    '''
    Purpose: Extracting the sources of the company logos
    Input: html beatiful soup
    Output: String
    '''

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
    '''
    '''
    try:
        return soup.find('span', class_="company").text.encode('ascii', 'ignore')
    except:
        print "\n*****************"
        print "Check get_company"
        return

def get_title(soup):
    '''
    '''
    try:
        return soup.find('h1', class_="title", itemprop="title").text.encode('ascii', 'ignore')
    except:
        print "\n*****************"
        print "Check get_title"
        return

def get_location(soup):
    '''
    '''
    try:
        soup_address = soup.find('span', itemprop="address").text
    except:
        print "\n*****************"
        print "Check get_location"
        return None, None, None
    
    full_address, address, location = featurizing_locations(soup_address)
    return full_address, address, location

def get_company_link(soup):
    '''
    '''

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
    job_post_link = get_post_link(soup)
    company_link = get_company_link(soup)
    full_address, scraped_address, location = get_location(soup)
    return company, title, logo, description, job_post_link, \
            company_link, full_address, scraped_address, location

def not_in_database(company, title, scraped_address, coll):
    '''
    '''
    if coll.find({'company' : company, 'title' : title, 'scraped_address' : scraped_address}).count() < 1:
        return True
    else:
        return False

def main():
    '''
    Purpose: Loop through all of the files in the directory, where I have all
    of my html files stored.
    Every loop checks one job posting and updates the mongodb with all the data needed
    '''
    
    cli = pymongo.MongoClient()
    db = cli.project
    coll = db.Linkedin

    global count
    count = 0
    countries = cPickle.load(open('data/countries.p', 'rb'))
    jobs = ['Data Scientist', 'Data Science']
    #countries = ['ch', 'es']

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
                company, title, logo, description, job_post_link, \
                company_link, full_address, scraped_address, location = big_df(soup)

                job_post = {'company': company,
                            'title' : title, 
                            'logo' : logo,
                            'description' : description,
                            'job_post_link' : job_post_link,
                            'company_link' : company_link, 
                            'full_address' : full_address, 
                            'scraped_address' : scraped_address, 
                            'location' :  location,
                            'country' :country
                            }

                if not_in_database(company, title, scraped_address, coll):
                    print "Insert made"
                    coll.insert_one(job_post)

    cli.close()

if __name__ == '__main__':
    main()
