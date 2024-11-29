import json
import os
import logging
import time
from datetime import datetime
from typing import Dict, List, Any
import cProfile
import pstats
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from analysis.signal_generator import SignalGenerator, SignalThresholds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TwitterTrendParser:
    def __init__(self, data_dir: str, max_tweets: int = 1000):
        """Initialize the parser with configurable parameters."""
        self.data_dir = data_dir
        self.max_tweets = max_tweets
        self.analyzer = SentimentIntensityAnalyzer()
        self.signal_generator = SignalGenerator()
        self.crypto_keywords = {
            'btc', 'eth', 'bitcoin', 'ethereum', 'crypto', 'blockchain',
            'defi', 'nft', 'altcoin', 'token'
        }

    def _extract_tweet_data(self, tweet_entry: Dict) -> Dict[str, Any]:
        """Extract relevant data from a tweet entry."""
        try:
            tweet = tweet_entry['content']['itemContent']['tweet_results']['result']['legacy']
            return {
                'text': tweet['full_text'],
                'created_at': tweet['created_at'],
                'favorites': tweet['favorite_count'],
                'retweets': tweet['retweet_count']
            }
        except KeyError as e:
            logger.warning(f"Failed to extract tweet data: {e}")
            return None

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of a single tweet."""
        try:
            return self.analyzer.polarity_scores(text)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {'compound': 0.0, 'neg': 0.0, 'neu': 0.0, 'pos': 0.0}

    def _detect_crypto_mentions(self, text: str) -> List[str]:
        """Detect cryptocurrency mentions in text."""
        text_lower = text.lower()
        return [keyword for keyword in self.crypto_keywords if keyword in text_lower]

    def _calculate_engagement_score(self, favorites: int, retweets: int) -> float:
        """Calculate engagement score for a tweet."""
        return (favorites * 1.0 + retweets * 2.0) / 3.0

    def process_tweets(self, input_file: str) -> Dict[str, Any]:
        """Process tweets with performance monitoring."""
        start_time = time.time()
        logger.info(f"Starting tweet processing from {input_file}")

        try:
            # Load and parse JSON
            load_start = time.time()
            with open(input_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            logger.info(f"JSON loading took {time.time() - load_start:.2f} seconds")

            # Extract tweets
            extract_start = time.time()
            entries = raw_data['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries']
            tweets = []
            for entry in entries[:self.max_tweets]:
                tweet_data = self._extract_tweet_data(entry)
                if tweet_data:
                    tweets.append(tweet_data)
            logger.info(f"Tweet extraction took {time.time() - extract_start:.2f} seconds")

            # Process tweets in parallel
            process_start = time.time()
            results = []
            with ThreadPoolExecutor(max_workers=4) as executor:
                for i, tweet in enumerate(tweets):
                    if i % 100 == 0:
                        logger.info(f"Processing tweet {i}/{len(tweets)}")
                    
                    sentiment = self._analyze_sentiment(tweet['text'])
                    crypto_mentions = self._detect_crypto_mentions(tweet['text'])
                    engagement = self._calculate_engagement_score(
                        tweet['favorites'],
                        tweet['retweets']
                    )
                    
                    results.append({
                        'text': tweet['text'],
                        'created_at': tweet['created_at'],
                        'sentiment': sentiment,
                        'crypto_mentions': crypto_mentions,
                        'engagement_score': engagement
                    })
            
            logger.info(f"Tweet processing took {time.time() - process_start:.2f} seconds")

            # Aggregate results
            agg_start = time.time()
            aggregated_data = {
                'total_tweets': len(results),
                'average_sentiment': sum(r['sentiment']['compound'] for r in results) / len(results),
                'crypto_mentions': {},
                'timestamp': datetime.now().isoformat()
            }

            for result in results:
                for coin in result['crypto_mentions']:
                    if coin not in aggregated_data['crypto_mentions']:
                        aggregated_data['crypto_mentions'][coin] = {
                            'mentions': 0,
                            'avg_sentiment': 0.0,
                            'total_engagement': 0.0
                        }
                    
                    coin_data = aggregated_data['crypto_mentions'][coin]
                    coin_data['mentions'] += 1
                    coin_data['avg_sentiment'] += result['sentiment']['compound']
                    coin_data['total_engagement'] += result['engagement_score']

            # Calculate averages
            for coin_data in aggregated_data['crypto_mentions'].values():
                if coin_data['mentions'] > 0:
                    coin_data['avg_sentiment'] /= coin_data['mentions']

            # Generate trading signals
            signal_start = time.time()
            coin_data = []
            for coin, data in aggregated_data['crypto_mentions'].items():
                if data['mentions'] >= 5:  # Minimum mention threshold
                    coin_data.append({
                        'coin': coin,
                        'sentiment': {
                            'compound': data['avg_sentiment'],
                            'pos': max(0, data['avg_sentiment']),
                            'neg': max(0, -data['avg_sentiment']),
                            'neu': 1 - abs(data['avg_sentiment'])
                        },
                        'mentions': data['mentions'],
                        'engagement': data['total_engagement']
                    })
            
            signals = self.signal_generator.generate_signals_batch(coin_data)
            aggregated_data['trading_signals'] = signals
            logger.info(f"Signal generation took {time.time() - signal_start:.2f} seconds")

            logger.info(f"Data aggregation took {time.time() - agg_start:.2f} seconds")
            logger.info(f"Total processing time: {time.time() - start_time:.2f} seconds")

            return aggregated_data

        except Exception as e:
            logger.error(f"Error processing tweets: {e}")
            raise

def main():
    """Main function with profiling."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    input_file = os.path.join(data_dir, 'raw', 'twitter_trends_sample.json')
    output_file = os.path.join(data_dir, 'processed', 'trend_analysis.json')

    # Create processed directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Initialize parser with smaller tweet limit for testing
    parser = TwitterTrendParser(data_dir, max_tweets=100)

    # Run with profiling
    profiler = cProfile.Profile()
    profiler.enable()
    
    try:
        results = parser.process_tweets(input_file)
        
        # Save results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
    
    finally:
        profiler.disable()
        # Print profiling stats
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Print top 20 time-consuming operations

if __name__ == "__main__":
    main()
