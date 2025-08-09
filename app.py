import os
import random
import json
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# We need to explicitly import our custom modules to use their functions.
from news_fetcher import fetch_stellar_news
from poem_generator import generate_stellar_poem
from image_fetcher import fetch_random_apod_image

load_dotenv() # loads variables from .env

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # Enable CORS for the app

# --- Application Routes ---

@app.route('/')
def home():
    """
    Renders the homepage with dynamic content.
    The homepage focuses on the APOD, and provides links to other pages.
    """
    try:
        # Load static data from files within the route function to prevent startup crashes.
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

        # Fetch a fresh APOD image and select a new poem/constellation for the main page.
        apod_data = fetch_random_apod_image()
        # Fallback if the APOD API call fails
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
    """
    Renders the dedicated news page with fresh articles.
    """
    try:
        # Fetch news every time the page is visited.
        news_articles = fetch_stellar_news()
        # Fallback if the News API call fails
        if not news_articles:
            news_articles = [{"title": "News Feed Currently Unavailable", "url": "#", "description": "Could not fetch news articles. Please check the News API key.", "urlToImage": "https://placehold.co/600x400/0d1117/c5c6c7?text=News+Not+Available", "source": {"name": "StellarFeed"}}]
            
        return render_template('news.html', news=news_articles)
        
    except Exception as e:
        print(f"Error on news page: {e}")
        return render_template('error.html', error=str(e))


@app.route('/poems')
def poems_page():
    """
    Renders the poems page with a dynamic poem from the Gemini API
    and the rest from the static JSON file.
    """
    try:
        # Load static data from file within the route function.
        try:
            with open('data/poems.json', 'r') as f:
                static_poems = json.load(f)
        except FileNotFoundError:
            static_poems = [{"text": "A cosmic journey begins with a single star.", "author": "Anonymous"}]

        # Generate a new poem with the Gemini API on every visit.
        poem_topics = [
            "celestial bodies, the night sky, and wonder",
            "the vastness of space",
          
