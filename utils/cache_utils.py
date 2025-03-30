import json
import os
import logging

CACHE_FILE = 'cache/movie_cache.json'

def load_cache():
    if not os.path.exists(CACHE_FILE):
        logging.info("Cache file not found, initializing empty cache.")
        return {}
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            logging.info("Successfully loaded cache.")
            return cache
    except Exception as e:
        logging.error(f"Error loading cache: {e}")
        return {}

def save_cache(cache):
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=4)
        logging.info("Successfully saved cache.")
    except Exception as e:
        logging.error(f"Error saving cache: {e}")
