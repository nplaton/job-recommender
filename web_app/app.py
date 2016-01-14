from flask import Flask, render_template, request
import random
import requests
from  recommender import user_recommendations
import pickle


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/linkedin_input')
def linkedin_input():
    return render_template('input.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    url = str(request.form['url'])
    recommendation = user_recommendations(url)
    df = recommendation.cosine_similarity()
    return render_template('recommendations.html', df = df.iloc[:20])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
