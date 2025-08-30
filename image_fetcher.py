import requests
import datetime
import random
import json
import os

# This script fetches a random Astronomy Picture of the Day (APOD)
# from the NASA API. It uses a publicly available demo key, so no
# manual setup is required to get started.


def fetch_random_apod_image():
    """
    Fetches a random Astronomy Picture of the Day from the NASA API
    using a demo API key.
    
    Returns:
        dict: A dictionary containing the image's title, URL, and explanation,
              or None if an error occurs or no image is found.
    """
    # Using the NASA DEMO_KEY.
    api_key = "DEMO_KEY"

    # The NASA APOD API endpoint.
    api_url = "https://api.nasa.gov/planetary/apod"

    # Define the date range to fetch from. NASA's API has data from 1995.
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date.today()

    # Calculate the number of days in the range to pick a random day.
    days_in_range = (end_date - start_date).days

    # Loop a few times to increase the chance of finding an image,
    # as some dates might feature a video or other non-image media.
    for _ in range(5):
        # Generate a random date within the specified range.
        random_day = start_date + datetime.timedelta(days=random.randint(0, days_in_range))
        formatted_date = random_day.strftime("%Y-%m-%d")

        # Set up the parameters for the API call.
        params = {
            "api_key": api_key,
            "date": formatted_date
        }

        try:
            # Make the HTTP GET request to the NASA API.
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            # Parse the JSON response from the API.
            data = response.json()

            # The API returns different media types. We only want images.
            if "url" in data and "image" in data.get("media_type", ""):
                print(f"Successfully fetched image for date: {formatted_date}")
                
                # Create a dictionary with the image data we need.
                image_info = {
                    "title": data.get("title", "No Title"),
                    "url": data.get("url"),
                    "explanation": data.get("explanation", "No explanation available.")
                }
                return image_info
            else:
                # If it's not an image, we print a message and the loop will continue.
                print(f"Skipping media type: {data.get('media_type', 'N/A')} for date: {formatted_date}")

        except requests.exceptions.RequestException as e:
            # Catch and handle any errors related to the API request itself.
            print(f"Error fetching data from NASA API: {e}")
        except json.JSONDecodeError:
            # Catch and handle errors if the response is not valid JSON.
            print(f"Error decoding JSON response for date: {formatted_date}")
    
    # If the loop completes without finding an image, return None.
    print("Could not find a valid image after multiple attempts.")
    return None


if __name__ == "__main__":
    image_data = fetch_random_apod_image()
    if image_data:
        print("\n--- Stellar Image of the Day ---")
        print(f"Title: {image_data['title']}")
        print(f"URL: {image_data['url']}")
        print("\nExplanation:")
        print(image_data['explanation'])
    else:
        print("\nCould not fetch a stellar image today. Please try again later.")
