import requests
import json
import os

# Base URL for CoinGecko API
COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

def fetch_trending_coins():
    """
    Fetch trending coins from CoinGecko API.
    Save the data to a local JSON file.
    """
    try:
        # Endpoint for trending coins
        endpoint = f"{COINGECKO_API_URL}/search/trending"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Save data to a JSON file in the data folder
        os.makedirs("data", exist_ok=True)  # Create a 'data' folder if it doesn't exist
        with open("data/trending_coins.json", "w") as file:
            json.dump(data, file, indent=4)
        
        print("Trending coins data saved to data/trending_coins.json")
        return data['coins']
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching trending coins: {e}")
        return []

def main():
    # Fetch and save trending coins
    fetch_trending_coins()

if __name__ == "__main__":
    main()
