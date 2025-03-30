from imdb_parser import fetch_page, parse_num_reviews, parse_oscar_count
from rating_adjuster import apply_review_balancer, apply_oscar_bonus
from utils.logging_config import setup_logging
from utils.cache_utils import load_cache, save_cache
import logging
import json
import os

setup_logging()

IMDB_TOP_URL = "https://www.imdb.com/chart/top/"

def scrape_top_movies(limit=20):
    try:
        soup = fetch_page(IMDB_TOP_URL)
        rows = soup.select('ul.ipc-metadata-list li')[:limit]
    except Exception as e:
        logging.error(f"Failed to scrape IMDb top page: {e}")
        return []

    cache = load_cache()
    movies = []

    for index, row in enumerate(rows, start=1):
        try:
            title_tag = row.select_one('h3')
            title = title_tag.text.strip()
            
            if title in cache:
                logging.info(f"Loaded '{title}' from cache.")
                movie = cache[title]
            else:
                logging.info(f"Fetching details for '{title}' from IMDb.")
                rating_tag = row.select_one('.ipc-rating-star--imdb')
                rating = float(rating_tag.text.split()[0])

                reviews_tag = row.select_one('.ipc-rating-star--voteCount')
                num_reviews = parse_num_reviews(reviews_tag.text)

                movie_page_path = row.select_one('a.ipc-title-link-wrapper')['href']
                movie_url = f"https://www.imdb.com{movie_page_path}"
                num_oscars = parse_oscar_count(movie_url)

                movie = {
                    "title": title,
                    "rating": rating,
                    "num_reviews": num_reviews,
                    "num_oscars": num_oscars
                }
                cache[title] = movie

            movies.append(movie)
        except Exception as e:
            logging.error(f"Error processing movie '{title}': {e}")

    save_cache(cache)
    return movies

def save_movies(movies, filename='output.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(movies, f, indent=4)
        logging.info(f"Results successfully written to '{filename}'.")
    except Exception as e:
        logging.error(f"Failed to save movies to '{filename}': {e}")

if __name__ == "__main__":
    movies = scrape_top_movies()
    if movies:
        apply_review_balancer(movies)
        apply_oscar_bonus(movies)
        movies.sort(key=lambda m: m['adjusted_rating'], reverse=True)
        save_movies(movies)
    else:
        logging.warning("No movies to process.")
