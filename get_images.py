import requests
import os
import time
import secret_keys

API_KEY = secret_keys.API_KEY  # Replace 'YOUR_API_KEY' with your actual API key

# Define the base URL for Google Street View Static API
base_url = "https://maps.googleapis.com/maps/api/streetview"

# Define the image size
image_size = "640x640"

# Define the heading angles for rotation (0, 90, 180, 270)
heading_angles = [0, 90, 180, 270]

# Function to fetch images for a given location and heading
def fetch_images(latitude, longitude, index):
    # Create a directory for the images if it doesn't exist
    directory = f"data/{index}"
    if os.path.exists(directory):
        print("Directory for data already exists... exiting images fetch")
        return
    os.makedirs(directory)

    loc_file = f"{directory}/loc.txt"
    with open(loc_file, "w") as loc:
        loc.write(f"Latitude: {latitude}\nLongitude: {longitude}\n")

    # Construct the URL for the Street View image
    for angle in heading_angles:
        image_url = f"{base_url}?size={image_size}&location={latitude},{longitude}&heading={angle}&key={API_KEY}"
        filename = f"{directory}/image_{angle}.jpg"

        # Fetch the image and save it
        response = requests.get(image_url)
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")

        # Sleep for a short time to avoid rate limiting
        time.sleep(0.5)

# Function to search for points of interest (POIs) in San Francisco
def search_for_pois():
    pois = []
    page_token = None

    # Fetch POIs using the Nearby Search API until 25 valid points are found
    while len(pois) < 25:
        # Construct the URL for the Nearby Search API request
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=37.7749,-122.4194&radius=5000&type=point_of_interest&key={API_KEY}"

        # Add page token if available
        if page_token:
            url += f"&pagetoken={page_token}"

        # Send request to the Nearby Search API
        response = requests.get(url)
        data = response.json()

        # Extract POI coordinates from the response
        for result in data.get("results", []):
            location = result.get("geometry", {}).get("location")
            if location:
                pois.append((location["lat"], location["lng"]))

        # Update page token for the next page of results
        page_token = data.get("next_page_token")

        # Sleep for a short time to avoid rate limiting
        time.sleep(1)

    return pois[:25]  # Return the first 25 POIs

# Main function to download images for 25 points in San Francisco
def download_images():
    # Search for points of interest (POIs) in San Francisco
    points = search_for_pois()

    # Fetch images for each point
    for i, (latitude, longitude) in enumerate(points, start=1):
        print(f"Fetching images for point {i}/{len(points)}...")
        fetch_images(latitude, longitude, i)

