import requests
import json
import os

# The Gemini API is used to generate a unique poem on each request.
# This script is a crucial part of making the website interactive.

def generate_stellar_poem(topic):
    """
    Generates a short, space-themed poem using the Gemini API.
    
    Args:
        topic (str): The subject of the poem (e.g., "stars", "black holes").
    
    Returns:
        str: The generated poem text, or an error message if generation fails.
    """
    # API key is intentionally left blank here. Vercel will provide it in the runtime
    # environment when deploying, or you can get a key from AI Studio and add it
    # as an environment variable in Vercel settings.
    api_key = ""  
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    # This is the prompt that will be sent to the generative AI model.
    prompt = f"Write a short, descriptive poem about {topic} in the style of a thoughtful observer."

    # The payload to send to the API.
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        # Make the HTTP POST request to the Gemini API.
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response.
        data = response.json()
        
        # Extract the generated text from the response.
        generated_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        if generated_text:
            return generated_text.strip()
        else:
            print("Error: Empty response from the Gemini API.")
            return "Failed to generate a poem. The API returned an empty response."

    except requests.exceptions.RequestException as e:
        # Handle potential request errors.
        print(f"Error calling the Gemini API: {e}")
        return "Failed to generate a poem. Please check your network connection."
    except KeyError:
        # Handle errors if the response format is unexpected.
        print("Error: Unexpected response format from the API.")
        return "Failed to generate a poem due to an API error."

# This section of the code will run when you execute the script directly.
if __name__ == "__main__":
    # Test the function with a specific topic.
    print("--- Generating a poem about celestial bodies ---")
    poem_text = generate_stellar_poem("celestial bodies and the vastness of space")
    print(poem_text)
