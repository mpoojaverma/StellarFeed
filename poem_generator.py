import requests
import json
import os

# This script generates a space-themed poem using a placeholder API call.
# In a real application, you would replace this with a call to a
# generative AI model API, such as the Google Gemini API.

# A brief explanation of the code:
# 1. The function `generate_stellar_poem` takes a topic (e.g., "nebula").
# 2. It constructs a prompt for the AI model to generate a short poem.
# 3. It makes a POST request to a placeholder API endpoint.
# 4. It handles potential errors and returns the generated poem text.

def generate_stellar_poem(topic):
    """
    Generates a short, space-themed poem using a placeholder API call.
    
    Args:
        topic (str): The subject of the poem (e.g., "stars", "black holes").
    
    Returns:
        str: The generated poem text, or an error message if generation fails.
    """
    # This is a placeholder for a real API endpoint.
    # For a real application, you would use an endpoint like:
    # "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
    # and provide a real API key.
    api_url = "https://placeholder-api.example.com/generate-poem"
    
    # This is the prompt that would be sent to a real generative AI model.
    # It tells the model what kind of text to create.
    prompt = f"Write a short, descriptive poem about {topic}."

    # In a real-world scenario, you would also need to provide an API key.
    # api_key = "YOUR_API_KEY"

    # The payload to send to the API.
    # The 'prompt' is the key piece of information for the AI model.
    payload = {
        "model": "text-davinci-003", # This is a placeholder model name.
        "prompt": prompt,
        "max_tokens": 100,
    }

    print(f"Generating a poem about: {topic}...")

    try:
        # We are mocking a response here to make the script runnable.
        # This will simulate a successful API call.
        
        # In a real implementation, you would use:
        # response = requests.post(api_url, json=payload, headers={"Authorization": f"Bearer {api_key}"})
        # response.raise_for_status()

        # Mocked response for demonstration purposes.
        mock_response = {
            "choices": [
                {
                    "text": (
                        f"A cosmic waltz, a silent gleam,\n"
                        f"Where {topic} in darkness dream.\n"
                        f"A whispered tale of light and dust,\n"
                        f"In timeless starlight, we place our trust."
                    )
                }
            ]
        }
        
        # Extract the generated text from the mocked response.
        poem_text = mock_response["choices"][0]["text"]
        return poem_text

    except requests.exceptions.RequestException as e:
        # Handle potential request errors.
        print(f"Error calling the generative AI API: {e}")
        return "Failed to generate a poem. Please check your network connection."
    except KeyError:
        # Handle errors if the response format is unexpected.
        print("Error: Unexpected response format from the API.")
        return "Failed to generate a poem due to an API error."

# This section of the code will run when you execute the script directly.
if __name__ == "__main__":
    # Test the function with a few different topics.
    print("--- Poem about Stars ---")
    stars_poem = generate_stellar_poem("stars")
    print(stars_poem)

    print("\n--- Poem about a Black Hole ---")
    black_hole_poem = generate_stellar_poem("a black hole")
    print(black_hole_poem)

    print("\n--- Poem about a Nebula ---")
    nebula_poem = generate_stellar_poem("a nebula")
    print(nebula_poem)

