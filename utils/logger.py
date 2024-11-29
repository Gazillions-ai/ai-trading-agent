"""Logging configuration for the AI Trading Agent."""

import logging
import sys
from datetime import datetime
import os
from functools import wraps
import time
from typing import Callable, Any

def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """Set up a logger with the specified configuration."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add formatters to handlers
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    
    return logger

def log_execution_time(logger: logging.Logger) -> Callable:
    """Decorator to log function execution time."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            logger.debug(
                f"Function {func.__name__} took {end_time - start_time:.2f} seconds to execute"
            )
            return result
        return wrapper
    return decorator

def retry_on_error(max_retries: int = 3, delay: int = 5) -> Callable:
    """Decorator to retry function on error with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    
                    wait_time = delay * (2 ** (retries - 1))  # Exponential backoff
                    logging.warning(
                        f"Error in {func.__name__}: {str(e)}. "
                        f"Retrying in {wait_time} seconds... "
                        f"(Attempt {retries + 1}/{max_retries})"
                    )
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator
