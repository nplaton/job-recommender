from flask import Flask, render_template, request, redirect, url_for
from flask.ext.paginate import Pagination
import random
import requests
from  recommender import user_recommendations
import pickle
import pandas as pd
import json
from geopy.distance import vincenty


app = Flask(__name__)
app.config.from_object(__name__)
DF = None

def init_filters(df):
	global ALL_LOCATIONS, CITIES_LOCATION, ALL_COUNTRIES
	ALL_LOCATIONS = [] 
	CITIES_LOCATION = pickle.load(open('web_app/models/city_location_dict.pkl', 'r'))
	all_cities = CITIES_LOCATION.keys()
	ALL_COUNTRIES = list(df.country.unique())
	ALL_LOCATIONS.extend(all_cities + ALL_COUNTRIES)

	country = pd.DataFrame({'name' : ALL_LOCATIONS})
	country['id'] = country.index
	country_json = json.dumps([{"id": id, "name": name} for id, name in\
	zip(country['id'], country['name'])])
	return country_json

def find_distance(location):
	global CITIES_LOCATION, DF_FILTERED
	lat_long = CITIES_LOCATION[location]
	DF_FILTERED['dist_diff'] = DF.location.apply(lambda x: (vincenty(x, lat_long).miles))
	DF_FILTERED = DF_FILTERED[DF_FILTERED['dist_diff']<=8]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/linkedin_input')
def linkedin_input():
	try:
		return render_template('input.html')

	except ValueError: 
		return render_template('input.html', cat=cat, msg='Oops! Please enter a Linkedin profile url ', form_action=form_action)
    

@app.route('/filter', methods=['POST', 'GET'])
def filter():
	global DF, ALL_LOCATIONS, DF_FILTERED, ALL_COUNTRIES, PAGES
	DF_FILTERED = DF
	PAGES = DF_FILTERED.shape[0]
	location = str(request.form['location'])

	try:
		if location in ALL_COUNTRIES:
			DF_FILTERED = DF[DF['country'] == location]
		else:
			find_distance(location)
		return redirect(url_for('recommendations'))
	
	except:
		return redirect(url_for('recommendations'))

@app.route('/recommendations', methods=['POST', 'GET'])
def recommendations():
	global DF, DF_FILTERED, COUNTRIES, PAGES

	try:
		if request.method == 'POST' and request.form['url'] is not None:
			url = str(request.form['url'])
			recommendation = user_recommendations(url)
			DF = recommendation.cosine_similarity()
			DF_FILTERED = DF
			page = 1
			COUNTRIES = init_filters(DF)
		else:
			page = int(request.args.get('page', 1))

		
		PAGES = DF_FILTERED.shape[0]
		i_end = page * 10
		i_start = i_end - 10
		df_subset = DF_FILTERED[i_start:i_end]
		pagination = Pagination(page = page, total = PAGES, css_framework = 'foundation')
		return render_template('search.html', df = df_subset, pagination= pagination, countries = COUNTRIES)
	
	except ValueError: 
		return render_template('input.html', msg='Oops! Please enter a Linkedin profile url')		

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8003, debug=True)
