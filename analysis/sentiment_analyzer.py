from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from typing import Dict, List, Union
from functools import lru_cache
import concurrent.futures

class AdvancedSentimentAnalyzer:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        """Initialize the sentiment analyzer with FinBERT model."""
        self.model_name = "ProsusAI/finbert"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name).to(device)
        self.device = device
        self.labels = ["negative", "neutral", "positive"]
        self.batch_size = 32  # Adjust based on your GPU memory

    @lru_cache(maxsize=1000)
    def _cached_analyze(self, text: str) -> Dict[str, Union[float, str]]:
        """Cached version of single text analysis."""
        return self._analyze_single(text)

    def _analyze_single(self, text: str) -> Dict[str, Union[float, str]]:
        """Analyze a single text."""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            scores = torch.nn.functional.softmax(outputs.logits, dim=1)
            
        scores = scores.cpu().numpy()[0]
        label_idx = np.argmax(scores)
        
        return {
            "label": self.labels[label_idx],
            "confidence": float(scores[label_idx]),
            "scores": {
                "negative": float(scores[0]),
                "neutral": float(scores[1]),
                "positive": float(scores[2]),
                "compound": float((scores[2] - scores[0]) / (1e-6 + np.sum(scores)))
            }
        }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Union[float, str]]]:
        """Analyze sentiment for a batch of texts efficiently."""
        results = []
        
        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            
            # Try to get cached results first
            batch_results = []
            uncached_texts = []
            uncached_indices = []
            
            for idx, text in enumerate(batch_texts):
                cached_result = self._cached_analyze(text)
                if cached_result is not None:
                    batch_results.append(cached_result)
                else:
                    uncached_texts.append(text)
                    uncached_indices.append(idx)
            
            # Process uncached texts in parallel
            if uncached_texts:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(self._analyze_single, text) for text in uncached_texts]
                    for idx, future in zip(uncached_indices, futures):
                        batch_results.insert(idx, future.result())
            
            results.extend(batch_results)
        
        return results

    def analyze_text(self, text: str) -> Dict[str, Union[float, str]]:
        """Analyze a single text with caching."""
        return self._cached_analyze(text)
