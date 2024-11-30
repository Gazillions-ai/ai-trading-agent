import requests

class CoinGeckoAPI:
    BASE_URL = "https://api.coingecko.com/api/v3"

    @staticmethod
    def get_trending_coins():
        """
        Fetches the top 7 trending cryptocurrencies on CoinGecko.
        Returns a list of trending coins with details like name, symbol, and market cap rank.
        """
        endpoint = f"{CoinGeckoAPI.BASE_URL}/search/trending"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            coins = data.get("coins", [])
            return [{"name": coin["item"]["name"],
                     "symbol": coin["item"]["symbol"],
                     "market_cap_rank": coin["item"]["market_cap_rank"]}
                    for coin in coins]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching trending coins: {e}")
            return []

# Example usage
if __name__ == "__main__":
    api = CoinGeckoAPI()
    trending_coins = api.get_trending_coins()
    print("Trending Coins:", trending_coins)


class SolanaTrackerAPI:
    BASE_URL = "https://solanatracker.io/api"

    @staticmethod
    def get_recent_tokens():
        """
        Fetches recently created tokens from Solana Tracker.
        Returns a list of tokens with details like name, symbol, and creation date.
        """
        endpoint = f"{SolanaTrackerAPI.BASE_URL}/recent_tokens"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            tokens = data.get("tokens", [])
            return [{"name": token["name"],
                     "symbol": token["symbol"],
                     "created_at": token["created_at"]}
                    for token in tokens]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching recent tokens from Solana Tracker: {e}")
            return []

# Example usage
if __name__ == "__main__":
    # CoinGecko API Example
    coingecko_api = CoinGeckoAPI()
    trending_coins = coingecko_api.get_trending_coins()
    print("Trending Coins from CoinGecko:", trending_coins)

    # Solana Tracker API Example
    solana_api = SolanaTrackerAPI()
    recent_tokens = solana_api.get_recent_tokens()
    print("Recent Tokens from Solana Tracker:", recent_tokens)
