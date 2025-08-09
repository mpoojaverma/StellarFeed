import os
import random
import json
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

from news_fetcher import fetch_stellar_news
from poem_generator import generate_stellar_poem
from image_fetcher import fetch_random_apod_image

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

try:
    with open('data/poems.json', 'r') as f:
        static_poems = json.load(f)
except FileNotFoundError:
    static_poems = [{"text": "A cosmic journey begins with a single star.", "author": "Anonymous"}]

try:
    with open('data/constellations.json', 'r') as f:
        constellations = json.load(f)
except FileNotFoundError:
    constellations = [{"name": "Orion", "desc": "The Hunter of the night sky."}]


@app.route('/')
def home():
    try:
        apod_data = fetch_random_apod_image()
        if apod_data is None:
            apod_data = {
                "title": "APOD Currently Unavailable",
                "url": "https://placehold.co/1200x675/0d1117/c5c6c7?text=Image+Not+Available",
                "explanation": "Could not fetch the Astronomy Picture of the Day. Please check the NASA API key."
            }

        poem_of_day = random.choice(static_poems)
        constellation_of_day = random.choice(constellations)
        
        return render_template('index.html', apod=apod_data, poem=poem_of_day, constellation=constellation_of_day)

    except Exception as e:
        print(f"Error on home page: {e}")
        return render_template('error.html', error=str(e))


@app.route('/news')
def news_page():
    try:
        news_articles = fetch_stellar_news()
        if not news_articles:
            news_articles = [{"title": "News Feed Currently Unavailable", "url": "#", "description": "Could not fetch news articles. Please check the News API key.", "urlToImage": "https://placehold.co/600x400/0d1117/c5c6c7?text=News+Not+Available", "source": {"name": "StellarFeed"}}]
            
        return render_template('news.html', news=news_articles)
        
    except Exception as e:
        print(f"Error on news page: {e}")
        return render_template('error.html', error=str(e))


@app.route('/poems')
def poems_page():
    try:
        generated_poem_text = generate_stellar_poem("celestial bodies, the night sky, and wonder")
        if not generated_poem_text:
            generated_poem = {"text": "A whisper from the stars, a story untold.", "author": "StellarFeed AI"}
        else:
            generated_poem = {"text": generated_poem_text, "author": "Gemini AI"}
        
        all_poems = [generated_poem] + static_poems
        
        return render_template('poems.html', poems=all_poems)
        
    except Exception as e:
        print(f"Error on poems page: {e}")
        return render_template('error.html', error=str(e))


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "favicon.ico", mimetype="image/vnd.microsoft.icon")


if __name__ == "__main__":
    app.run(debug=True)
