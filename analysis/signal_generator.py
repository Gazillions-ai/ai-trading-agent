"""Advanced trading signal generation module combining sentiment and technical analysis."""

import numpy as np
from datetime import datetime
from typing import Dict, List, Any
import logging
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SignalType(Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    NEUTRAL = "NEUTRAL"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"

@dataclass
class SignalThresholds:
    """Thresholds for signal generation."""
    STRONG_BUY: float = 0.8
    BUY: float = 0.5
    NEUTRAL: float = 0.0
    SELL: float = -0.5
    STRONG_SELL: float = -0.8
    MIN_MENTIONS: int = 5
    MIN_ENGAGEMENT: float = 100.0

class SignalGenerator:
    """Generate trading signals based on sentiment and technical analysis."""
    
    def __init__(self, thresholds: SignalThresholds = SignalThresholds()):
        """Initialize signal generator with configurable thresholds."""
        self.thresholds = thresholds
    
    def _calculate_sentiment_score(self, sentiment_data: Dict[str, Any]) -> float:
        """Calculate weighted sentiment score."""
        try:
            compound_score = sentiment_data.get('compound', 0)
            pos_score = sentiment_data.get('pos', 0)
            neg_score = sentiment_data.get('neg', 0)
            
            # Weight recent sentiment more heavily
            weighted_score = (
                compound_score * 0.5 +
                (pos_score - neg_score) * 0.3 +
                (1 if compound_score > 0 else -1) * 0.2
            )
            
            return max(-1.0, min(1.0, weighted_score))
        except Exception as e:
            logger.error(f"Error calculating sentiment score: {e}")
            return 0.0

    def _calculate_engagement_impact(self, engagement_score: float) -> float:
        """Calculate normalized engagement impact."""
        try:
            # Normalize engagement using log scale to handle outliers
            normalized = np.log1p(max(0, engagement_score)) / np.log1p(self.thresholds.MIN_ENGAGEMENT)
            return min(1.0, normalized)
        except Exception as e:
            logger.error(f"Error calculating engagement impact: {e}")
            return 0.0

    def _calculate_mention_confidence(self, mention_count: int) -> float:
        """Calculate confidence based on mention count."""
        try:
            # Logarithmic scaling for mention confidence
            base_confidence = np.log1p(mention_count) / np.log1p(self.thresholds.MIN_MENTIONS)
            return min(1.0, max(0.0, base_confidence))
        except Exception as e:
            logger.error(f"Error calculating mention confidence: {e}")
            return 0.0

    def generate_signal(self, 
                       coin: str,
                       sentiment_data: Dict[str, Any],
                       mention_count: int,
                       engagement_score: float) -> Dict[str, Any]:
        """Generate trading signal for a coin based on various metrics."""
        try:
            # Calculate component scores
            sentiment_score = self._calculate_sentiment_score(sentiment_data)
            engagement_impact = self._calculate_engagement_impact(engagement_score)
            confidence = self._calculate_mention_confidence(mention_count)
            
            # Calculate final signal strength
            signal_strength = (
                sentiment_score * 0.5 +
                engagement_impact * 0.3 +
                confidence * 0.2
            )
            
            # Determine signal type
            signal_type = SignalType.NEUTRAL
            if signal_strength >= self.thresholds.STRONG_BUY:
                signal_type = SignalType.STRONG_BUY
            elif signal_strength >= self.thresholds.BUY:
                signal_type = SignalType.BUY
            elif signal_strength <= self.thresholds.STRONG_SELL:
                signal_type = SignalType.STRONG_SELL
            elif signal_strength <= self.thresholds.SELL:
                signal_type = SignalType.SELL
            
            return {
                'coin': coin,
                'signal_type': signal_type.value,
                'signal_strength': signal_strength,
                'confidence': confidence,
                'metrics': {
                    'sentiment_score': sentiment_score,
                    'engagement_impact': engagement_impact,
                    'mention_count': mention_count,
                    'raw_sentiment': sentiment_data
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating signal for {coin}: {e}")
            return None

    def generate_signals_batch(self, 
                             coin_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate signals for multiple coins."""
        signals = []
        
        for data in coin_data:
            try:
                signal = self.generate_signal(
                    coin=data['coin'],
                    sentiment_data=data['sentiment'],
                    mention_count=data['mentions'],
                    engagement_score=data['engagement']
                )
                if signal:
                    signals.append(signal)
            except Exception as e:
                logger.error(f"Error processing coin data: {e}")
                continue
        
        # Sort signals by absolute strength
        return sorted(
            signals,
            key=lambda x: abs(x['signal_strength']),
            reverse=True
        )

def main():
    """Test signal generation with sample data."""
    # Sample data
    sample_data = [{
        'coin': 'BTC',
        'sentiment': {
            'compound': 0.8,
            'pos': 0.6,
            'neg': 0.1,
            'neu': 0.3
        },
        'mentions': 10,
        'engagement': 500.0
    }]
    
    # Generate signals
    generator = SignalGenerator()
    signals = generator.generate_signals_batch(sample_data)
    
    # Print results
    for signal in signals:
        print(f"\nSignal for {signal['coin']}:")
        print(f"Type: {signal['signal_type']}")
        print(f"Strength: {signal['signal_strength']:.3f}")
        print(f"Confidence: {signal['confidence']:.3f}")
        print("Metrics:", signal['metrics'])

if __name__ == "__main__":
    main()
