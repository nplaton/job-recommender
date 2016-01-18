from flask import Flask, render_template, request
from flask.ext.paginate import Pagination
import random
import requests
from  recommender import user_recommendations
import pickle


app = Flask(__name__)
app.config.from_object(__name__)
DF = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/linkedin_input')
def linkedin_input():
    return render_template('input.html')

@app.route('/recommendations', methods=['POST', 'GET'])
def recommendations():
	global DF
	if request.method == 'POST':
		url = str(request.form['url'])
		recommendation = user_recommendations(url)
		DF = recommendation.cosine_similarity()
		page = 1
	else:
		page = int(request.args.get('page', 1))
    
	pages = DF.shape[0]
	i_end = page * 10
	i_start = i_end - 10
	df_subset = DF[i_start:i_end]
	pagination = Pagination(page = page, total = pages, css_framework = 'foundation')
	return render_template('search.html', df = df_subset, pagination= pagination)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8095, debug=True)
