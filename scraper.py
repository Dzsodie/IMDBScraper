import requests
from bs4 import BeautifulSoup
import json
from rating_adjuster import apply_review_balancer, apply_oscar_bonus

IMDB_TOP_URL = "https://www.imdb.com/chart/top/"

def scrape_top_movies(limit=20):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(IMDB_TOP_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    movies = []

    rows = soup.select('ul.ipc-metadata-list li')[:limit]

    for row in rows:
        title = row.select_one('h3').text.strip()
        rating = float(row.select_one('.ipc-rating-star--imdb').text.split()[0])
        num_reviews_str = row.select_one('.ipc-rating-star--voteCount').text.strip('()').replace(',', '')
        num_reviews = int(num_reviews_str)
        
        # Oscars data isn't directly on this page; placeholder for now.
        num_oscars = 0
        
        movies.append({
            "title": title,
            "rating": rating,
            "num_reviews": num_reviews,
            "num_oscars": num_oscars
        })

    return movies

if __name__ == "__main__":
    movies = scrape_top_movies()
    apply_review_balancer(movies)
    apply_oscar_bonus(movies)
    
    movies.sort(key=lambda m: m['adjusted_rating'], reverse=True)

    with open('output.json', 'w') as f:
        json.dump(movies, f, indent=4)
    print("Results written to output.json")
