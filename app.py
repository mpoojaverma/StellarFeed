import os
import random
import json
from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# We need to explicitly import our custom modules to use their functions.
from news_fetcher import fetch_stellar_news
from poem_generator import generate_stellar_poem
from image_fetcher import fetch_random_apod_image

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# --- API Endpoints for React Frontend ---
# These routes will not render a template, they will return JSON data.

@app.route('/api/apod')
def get_apod():
    apod_data = fetch_random_apod_image()
    if apod_data is None:
        return jsonify({
            "title": "APOD Currently Unavailable",
            "url": "https://placehold.co/1200x675/0d1117/c5c6c7?text=Image+Not+Available",
            "explanation": "Could not fetch APOD. Please check the NASA API key."
        }), 500
    return jsonify(apod_data)

@app.route('/api/news')
def get_news():
    news_articles = fetch_stellar_news()
    if not news_articles:
        return jsonify([{"title": "News Feed Currently Unavailable", "url": "#", "description": "Could not fetch news.", "urlToImage": "https://placehold.co/600x400/0d1117/c5c6c7?text=News+Not+Available", "source": {"name": "StellarFeed"}}]), 500
    return jsonify(news_articles)

@app.route('/api/poems')
def get_poems():
    try:
        with open('data/poems.json', 'r') as f:
            static_poems = json.load(f)
    except FileNotFoundError:
        static_poems = [{"text": "A cosmic journey begins with a single star.", "author": "Anonymous"}]

    generated_poems = []
    poem_topics = ["celestial bodies", "the night sky", "the vastness of space"]
    for topic in poem_topics:
        generated_poem_text = generate_stellar_poem(topic)
        if generated_poem_text:
            generated_poems.append({"text": generated_poem_text, "author": "Gemini AI"})
    
    all_poems = generated_poems + static_poems
    if not all_poems:
        return jsonify([{"text": "No poems available.", "author": "StellarFeed"}]), 500
    return jsonify(all_poems)

@app.route('/api/constellation')
def get_constellation():
    try:
        with open('data/constellations.json', 'r') as f:
            constellations = json.load(f)
    except FileNotFoundError:
        constellations = [{"name": "Orion", "desc": "The Hunter of the night sky."}]
    
    constellation = random.choice(constellations)
    return jsonify(constellation)

# --- Route for Serving the React Application ---
@app.route('/')
def serve_react_app():
    # This route serves your single React index.html file.
    return send_from_directory('static', 'index.html')

# --- Fallback Route for React Router ---
@app.route('/<path:path>')
def serve_react_routes(path):
    # This is a crucial fallback route that allows React Router to handle
    # all other URLs like /news, /poems, etc.
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
