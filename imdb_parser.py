import requests
from bs4 import BeautifulSoup
import logging

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}

def fetch_page(url):
    try:
        logging.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        logging.info(f"Successfully fetched URL: {url}")
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        raise

def parse_num_reviews(num_reviews_str):
    try:
        num_reviews_str = num_reviews_str.replace('\xa0', '').replace('(', '').replace(')', '').strip()
        if 'K' in num_reviews_str:
            return int(float(num_reviews_str.replace('K', '')) * 1_000)
        elif 'M' in num_reviews_str:
            return int(float(num_reviews_str.replace('M', '')) * 1_000_000)
        else:
            return int(num_reviews_str.replace(',', ''))
    except ValueError as e:
        logging.error(f"Failed to parse number of reviews '{num_reviews_str}': {e}")
        return 0

def parse_oscar_count(movie_url):
    try:
        soup = fetch_page(movie_url)
        awards_section = soup.select_one('li[data-testid="award_information"]')
        if awards_section:
            awards_text = awards_section.text
            if "Won" in awards_text and "Oscar" in awards_text:
                try:
                    oscars_won_part = awards_text.split("Won")[1].split("Oscar")[0].strip()
                    oscars_won = int(oscars_won_part)
                    logging.info(f"Parsed {oscars_won} Oscars for URL: {movie_url}")
                    return oscars_won
                except (IndexError, ValueError) as e:
                    logging.warning(f"Unexpected Oscar format at URL {movie_url}: {e}")
                    return 0
        logging.info(f"No Oscars found for URL: {movie_url}")
        return 0
    except Exception as e:
        logging.error(f"Failed to parse Oscar count for {movie_url}: {e}")
        return 0