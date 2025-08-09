import requests
import json
import os

# This script is a news fetching module for the StellarFeed project.
# It retrieves recent news articles related to astronomy and space exploration
# from a popular news API.

# A brief explanation of the code:
# 1. It defines the base URL for the NewsAPI.
# 2. It requires an API key, which you can get for free from NewsAPI.org.
# 3. The function `fetch_stellar_news` makes an HTTP GET request to the API.
# 4. It searches for keywords like "astronomy" and "space exploration".
# 5. It handles potential errors and returns a list of news articles.

def fetch_stellar_news():
    """
    Fetches the latest news articles related to astronomy and space.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents a news article.
              Returns an empty list if an error occurs.
    """
    # Replace 'YOUR_API_KEY' with your actual API key from newsapi.org.
    # It's a good practice to store this in an environment variable, but for
    # this example, we'll keep it here for clarity.
    api_key = "YOUR_API_KEY"

    # The API endpoint for fetching top headlines. We can use the 'everything'
    # endpoint for more specific searches.
    api_url = "https://newsapi.org/v2/everything"
    
    # Check if the API key has been provided.
    if api_key == "YOUR_API_KEY" or not api_key:
        print("Error: API key is missing. Please sign up for a key at newsapi.org and update the script.")
        return []

    # Define the search parameters.
    # 'q' is the query for the search.
    # 'sortBy' determines the order of the results.
    # 'language' filters results by language.
    params = {
        "q": "astronomy OR 'space exploration'",  # Search for articles with these keywords
        "sortBy": "publishedAt",                 # Sort by the most recent articles
        "language": "en",                        # Fetch articles in English
        "apiKey": api_key                        # Your API key
    }

    try:
        # Make the request to the NewsAPI.
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response.
        data = response.json()
        
        # Check if the request was successful and if there are articles.
        if data["status"] == "ok" and data["articles"]:
            print(f"Successfully fetched {len(data['articles'])} news articles.")
            # Return the list of articles.
            return data["articles"]
        else:
            print("No articles found or API status is not 'ok'.")
            print(f"API Response: {data.get('message', 'No message available.')}")
            return []

    except requests.exceptions.RequestException as e:
        # Handle potential request errors (e.g., network issues).
        print(f"Error fetching data from NewsAPI: {e}")
        return []
    except json.JSONDecodeError:
        # Handle JSON parsing errors.
        print("Error decoding JSON response from NewsAPI.")
        return []

# The code below is an example of how to use the function.
if __name__ == "__main__":
    news_articles = fetch_stellar_news()
    if news_articles:
        print("\n--- Stellar News Headlines ---")
        # Print the title and URL of the first 5 articles.
        for i, article in enumerate(news_articles[:5]):
            print(f"\n{i+1}. {article.get('title', 'No Title')}")
            print(f"   Source: {article.get('source', {}).get('name', 'N/A')}")
            print(f"   URL: {article.get('url', 'N/A')}")
    else:
        print("\nCould not fetch stellar news today. Please try again later.")
