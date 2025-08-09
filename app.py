import os
import random
import json
from flask import Flask, render_template, send_from_directory
import requests
from dotenv import load_dotenv

load_dotenv() # loads variables from .env

app = Flask(__name__, static_folder="static", template_folder="templates")

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY") # optional, fallback provided in code

# --- Utilities / API wrappers ---

def fetch_apod():
    """Fetch NASA APOD (Astronomy Picture of the Day)."""
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("APOD fetch error:", e)
        # fallback local placeholder
        return {
            "title": "APOD currently unavailable",
            "url": "/static/images/apod-placeholder.jpg",
            "explanation": "Could not fetch APOD. Try again later."
        }

def fetch_space_news(limit=6):
    """
    Fetch space/astronomy news.
    Priority:
      1) If NEWS_API_KEY is provided -> use NewsAPI (newsapi.org) for 'space OR astronomy' query
      2) Otherwise fallback to Spaceflight News API (no key)
    """
    # Try NewsAPI.org if key available
    if NEWS_API_KEY:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "space OR astronomy OR nasa OR satellite OR rocket OR astrophysics",
            "language": "en",
            "pageSize": limit,
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY
        }
        try:
            r = requests.get(url, params=params, timeout=8)
            r.raise_for_status()
            data = r.json()
            return data.get("articles", [])[:limit]
        except Exception as e:
            print("NewsAPI fetch error:", e)

    # Fallback to Spaceflight News API (no key)
    try:
        r = requests.get(f"https://api.spaceflightnewsapi.net/v3/articles?_limit={limit}&_sort=publishedAt:desc", timeout=8)
        r.raise_for_status()
        data = r.json()
        # normalize to common fields used in templates (title, url, summary, image, publishedAt, source)
        normalized = []
        for item in data:
            normalized.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "description": item.get("summary") or item.get("newsSite"),
                "urlToImage": item.get("imageUrl"),
                "publishedAt": item.get("publishedAt"),
                "source": item.get("newsSite") or "Spaceflight News"
            })
        return normalized
    except Exception as e:
        print("SpaceflightNews fetch error:", e)
        return []

def load_poems():
    """Load local poems/quotes from data/poems.json (returns list)."""
    try:
        with open("data/poems.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Poems load error:", e)
        # fallback tiny list
        return [
            {"text": "I have loved the stars too fondly to be fearful of the night.", "author": "Sarah Williams"},
            {"text": "The cosmos is within us. We are made of star-stuff.", "author": "Carl Sagan"}
        ]

def load_constellations():
    """Load local constellations from data/constellations.json (returns list)."""
    try:
        with open("data/constellations.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Constellations load error:", e)
        return [
            {"name": "Orion", "desc": "The Hunter — bright belt of three stars, visible during winter nights."},
            {"name": "Cassiopeia", "desc": "W-shaped constellation, easy to spot near Polaris."}
        ]

# --- Routes ---

@app.route("/")
def index():
    apod = fetch_apod()
    news = fetch_space_news(8)
    poems = load_poems()
    poem_of_day = random.choice(poems) if poems else None
    constellations = load_constellations()
    constellation = random.choice(constellations)

    return render_template("index.html",
                           apod=apod,
                           news=news,
                           poem=poem_of_day,
                           constellation=constellation)

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/news")
def news_page():
    news = fetch_space_news(20) # Fetch more articles for a dedicated page
    return render_template("news.html", news=news)
    
@app.route("/poems")
def poems_page():
    poems = load_poems()
    return render_template("poems.html", poems=poems)


# Serve a simple robots.txt or favicon optionally
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "favicon.ico", mimetype="image/vnd.microsoft.icon")


if __name__ == "__main__":
    app.run(debug=True)

