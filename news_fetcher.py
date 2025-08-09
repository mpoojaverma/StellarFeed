import requests
import json
import os

# This script fetches news articles using a secure environment variable for the API key.
# This is a crucial step to fix the 500 error from a missing key.

def fetch_stellar_news():
    """
    Fetches the latest news articles related to astronomy and space,
    using an API key from the environment variables.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents a news article.
              Returns an empty list if an error occurs.
    """
    # Fetch the API key from the environment variable.
    # YOU MUST set 'NEWS_API_KEY' in your Vercel project settings.
    api_key = os.environ.get('NEWS_API_KEY')
    api_url = "https://newsapi.org/v2/everything"
    
    if not api_key:
        print("Error: News API key is missing from environment variables. Check Vercel settings.")
        return []

    params = {
        "q": "astronomy OR 'space exploration' OR nasa",
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": 12, # Fetch more articles for a dynamic page
        "apiKey": api_key
    }

    try:
        response = requests.get(api_url, params=params, timeout=8)
        response.raise_for_status()

        data = response.json()
        
        if data["status"] == "ok" and data["articles"]:
            return data["articles"]
        else:
            print(f"NewsAPI returned an error: {data.get('message')}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NewsAPI: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON response from NewsAPI.")
        return []
        
# A fallback for local testing if the API key is not set.
if __name__ == "__main__":
    if 'NEWS_API_KEY' not in os.environ:
        print("NEWS_API_KEY not set locally. Using a placeholder.")
        # This placeholder will fail on a real API call but allows the script to run locally
        # without crashing, so you can test other parts of your code.
        os.environ['NEWS_API_KEY'] = 'placeholder'
    news_articles = fetch_stellar_news()
    print(f"Fetched {len(news_articles)} articles.")
