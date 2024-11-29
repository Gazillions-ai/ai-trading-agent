import requests
import json
import os

# RapidAPI credentials and endpoint
API_URL = "https://twitter135.p.rapidapi.com/Search/"
API_HEADERS = {
    "x-rapidapi-host": "twitter135.p.rapidapi.com",
    "x-rapidapi-key": "78efa949a9mshdb917f12828cec6p1ed3e9jsn1ebb2af5c03d",  # Replace with your actual RapidAPI key
}

def fetch_twitter_trends(query="crypto"):
    """
    Fetch Twitter trends using search.
    Args:
        query (str): Search query to find trends
    Returns:
        List of trending topics or an error message.
    """
    try:
        # Make the API request with query parameters
        params = {"q": query}
        response = requests.get(API_URL, headers=API_HEADERS, params=params)
        response.raise_for_status()  # Raise an error for HTTP issues
        
        # Parse JSON response
        data = response.json()
        
        # Save data to a JSON file
        os.makedirs("data", exist_ok=True)  # Create 'data' folder if it doesn't exist
        with open("data/twitter_trends.json", "w") as file:
            json.dump(data, file, indent=4)
        
        print("Twitter trends data saved to data/twitter_trends.json")
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Twitter trends: {e}")
        return {}

if __name__ == "__main__":
    print("Fetching Twitter trends...")
    trends = fetch_twitter_trends()
    if trends:
        print("\nTrends data has been saved to data/twitter_trends.json")
