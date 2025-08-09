import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from news_fetcher import fetch_stellar_news
from image_fetcher import fetch_random_apod_image
from poem_generator import generate_stellar_poem
import random
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for the app

# Load static poems and constellations from JSON files.
with open('data/poems.json', 'r') as f:
    static_poems = json.load(f)
with open('data/constellations.json', 'r') as f:
    constellations = json.load(f)


# --- Application Routes ---

@app.route('/')
def home():
    """
    Renders the homepage with dynamic content from various APIs.
    """
    try:
        # Fetch the Astronomy Picture of the Day.
        apod = fetch_random_apod_image()
        if not apod:
            # Fallback to a placeholder if the API fails.
            apod = {
                "title": "CosmicPlaceholder",
                "url": "https://placehold.co/1200x675/0d1117/c5c6c7?text=Image+Not+Available",
                "explanation": "Could not fetch the Astronomy Picture of the Day. Please check the NASA API."
            }

        # Select a random static poem.
        poem = random.choice(static_poems)

        # Select a random constellation.
        constellation = random.choice(constellations)

        # Render the index.html template with the fetched data.
        return render_template('index.html', apod=apod, poem=poem, constellation=constellation)

    except Exception as e:
        print(f"An error occurred on the home page: {e}")
        return render_template('error.html', error=str(e))


@app.route('/news')
def news_page():
    """
    Renders the news page with the latest articles.
    """
    try:
        # Fetch the latest news articles.
        news_articles = fetch_stellar_news()
        if not news_articles:
            # Fallback if the news API fails.
            news_articles = []
            
        # Render the news.html template with the articles.
        return render_template('news.html', news=news_articles)
        
    except Exception as e:
        print(f"An error occurred on the news page: {e}")
        return render_template('error.html', error=str(e))


@app.route('/poems')
def poems_page():
    """
    Renders the poems page with a dynamically generated poem and static ones.
    """
    try:
        # Generate a new poem using the Gemini API.
        generated_poem = generate_stellar_poem("celestial bodies and the vastness of space")
        
        # Combine the generated poem with the static poems.
        all_poems = [{"text": generated_poem, "author": "Gemini AI"}] + static_poems
        
        # Render the poems.html template.
        return render_template('poems.html', poems=all_poems)
        
    except Exception as e:
        print(f"An error occurred on the poems page: {e}")
        return render_template('error.html', error=str(e))


@app.route('/about')
def about_page():
    """
    Renders the About page.
    """
    return render_template('about.html')


# A simple API endpoint for a constellation, if needed by a front-end script
@app.route('/api/constellation')
def get_constellation():
    """
    Returns a random constellation as JSON.
    """
    constellation = random.choice(constellations)
    return jsonify(constellation)


if __name__ == '__main__':
    app.run(debug=True)
