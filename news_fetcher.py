import requests
import json
import os

def fetch_stellar_news():
    api_key = os.environ.get('NEWS_API_KEY')
    api_url = "https://newsapi.org/v2/everything"
    
    if not api_key:
        return []

    params = {
        "q": "astronomy OR 'space exploration' OR nasa",
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 12,
        "apiKey": api_key
    }

    try:
        response = requests.get(api_url, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "ok" and data["articles"]:
            return data["articles"]
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NewsAPI: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON response from NewsAPI.")
        return []
        
if __name__ == "__main__":
    if 'NEWS_API_KEY' not in os.environ:
        os.environ['NEWS_API_KEY'] = 'placeholder'
    news_articles = fetch_stellar_news()
    print(f"Fetched {len(news_articles)} articles.")
