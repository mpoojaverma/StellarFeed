import requests
import json
import os

# This script fetches news articles using a secure environment variable for the API key.
# It is a crucial step to fix the server crash.

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
    
    # Check if the API key has been provided.
    if not api_key:
        print("Error: News API key is missing. Please set 'NEWS_API_KEY' in your Vercel environment variables.")
        return []

    params = {
        "q": "astronomy OR 'space exploration'",
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": api_key
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        data = response.json()
        
        if data["status"] == "ok" and data["articles"]:
            print(f"Successfully fetched {len(data['articles'])} news articles.")
            return data["articles"]
        else:
            print("No articles found or API status is not 'ok'.")
            print(f"API Response: {data.get('message', 'No message available.')}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from NewsAPI: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON response from NewsAPI.")
        return []

if __name__ == "__main__":
    # Note: This will fail if the environment variable is not set locally.
    news_articles = fetch_stellar_news()
    if news_articles:
        print("\n--- Stellar News Headlines ---")
        for i, article in enumerate(news_articles[:5]):
            print(f"\n{i+1}. {article.get('title', 'No Title')}")
            print(f"   Source: {article.get('source', {}).get('name', 'N/A')}")
            print(f"   URL: {article.get('url', 'N/A')}")
    else:
        print("\nCould not fetch stellar news today.")
