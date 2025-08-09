import requests
import json
import os

def generate_stellar_poem(topic):
    api_key = os.environ.get('GOOGLE_API_KEY')
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    if not api_key:
        return "A whisper from the stars, a story untold."

    prompt = f"Write a short, descriptive poem about {topic} in a thoughtful and awe-inspiring tone. The poem should be no more than 4-6 lines."

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(api_url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        generated_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        if generated_text:
            return generated_text.strip()
        else:
            return "The cosmos is vast, but our curiosity is infinite."

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "An error occurred while generating a poem."
    except KeyError:
        print("Error: Unexpected response format from the API.")
        return "An error occurred while generating a poem."
