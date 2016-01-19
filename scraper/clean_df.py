import re
from geopy.geocoders import Nominatim



def cleaning_string(city):
	'''

	'''

	city = city.replace('Metro', '')
	city = city.replace('Area', '')
	city = city.replace('Bay', '')
	city = city.replace('Greater', '')
	city = city.replace('(HQ)', '')
	city = city.replace('L5-', '')
	city = city.replace('- CNVR  60606', '')
	city = city.replace('San Francisco / ','')
	city = city.replace('North America','')
	city = city.replace('US','')
	city = city.replace('DC','')
	city = city.replace('Downtown','')
	city = city.replace('Manhattan','NYC')
	city = city.replace('-',' ')
	city = city.strip()
	city = city.split('/')[0]
	return city

def featurizing_locations(scraped_city):
    geolocator = Nominatim()
    city = cleaning_string(scraped_city)
    
    try:
        located_address = geolocator.geocode(city)
        full_address = located_address.address
        location = (located_address[1])
    except:
        full_address = city
        location = None
    return full_address, scraped_city, location

    


	
