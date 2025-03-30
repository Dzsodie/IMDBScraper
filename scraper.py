from imdb_parser import fetch_page, parse_num_reviews, parse_oscar_count
from rating_adjuster import apply_review_balancer, apply_oscar_bonus
from logging_config import setup_logging
import logging
import json
import os

setup_logging()

IMDB_TOP_URL = "https://www.imdb.com/chart/top/"

def scrape_top_movies(limit=20):
    try:
        logging.info(f"Fetching IMDb Top {limit} movies.")
        soup = fetch_page(IMDB_TOP_URL)
    except Exception as e:
        logging.error(f"Failed to fetch IMDb Top page: {e}")
        return []

    rows = soup.select('ul.ipc-metadata-list li')[:limit]

    movies = []
    for index, row in enumerate(rows, start=1):
        try:
            title_tag = row.select_one('h3')
            title = title_tag.text.strip()

            rating_tag = row.select_one('.ipc-rating-star--imdb')
            rating = float(rating_tag.text.split()[0])

            reviews_tag = row.select_one('.ipc-rating-star--voteCount')
            num_reviews = parse_num_reviews(reviews_tag.text)

            movie_page_path = row.select_one('a.ipc-title-link-wrapper')['href']
            movie_url = f"https://www.imdb.com{movie_page_path}"
            num_oscars = parse_oscar_count(movie_url)

            movies.append({
                "title": title,
                "rating": rating,
                "num_reviews": num_reviews,
                "num_oscars": num_oscars
            })

            logging.info(f"Successfully parsed movie {index}: '{title}'.")

        except Exception as e:
            logging.error(f"Error parsing movie at position {index}: {e}")

    return movies

def save_movies(movies, filename='output.json'):
    try:
        # Clear the file content first if exists
        if os.path.exists(filename):
            open(filename, 'w').close()
            logging.info(f"Cleared existing data in '{filename}'.")

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
