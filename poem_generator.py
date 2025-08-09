import requests
import json
import os

# This script is a crucial part of making the website interactive.
# It uses the Gemini API key from the environment variables.

def generate_stellar_poem(topic):
    """
    Generates a short, space-themed poem using the Gemini API.
    
    Args:
        topic (str): The subject of the poem (e.g., "stars", "black holes").
    
    Returns:
        str: The generated poem text, or an error message if generation fails.
    """
    # This line is correct. It fetches the API key from Vercel's environment.
    api_key = os.environ.get('GOOGLE_API_KEY')
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    if not api_key:
        return "Failed to generate a poem. The Google API key is missing from your Vercel environment variables."

    prompt = f"Write a short, descriptive poem about {topic} in the style of a thoughtful observer."

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()

        data = response.json()
        
        generated_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        if generated_text:
            return generated_text.strip()
        else:
            return "Failed to generate a poem. The API returned an empty response."

    except requests.exceptions.RequestException as e:
        print(f"Error calling the Gemini API: {e}")
        return "Failed to generate a poem. Please check your network connection."
    except KeyError:
        print("Error: Unexpected response format from the API.")
        return "Failed to generate a poem due to an API error."

if __name__ == "__main__":
    print("--- Generating a poem about celestial bodies ---")
    poem_text = generate_stellar_poem("celestial bodies and the vastness of space")
    print(poem_text)
