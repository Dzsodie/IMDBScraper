from imdb_parser import fetch_page, parse_num_reviews, parse_oscar_count
from rating_adjuster import apply_review_balancer, apply_oscar_bonus
import json

IMDB_TOP_URL = "https://www.imdb.com/chart/top/"

def scrape_top_movies(limit=20):
    soup = fetch_page(IMDB_TOP_URL)
    rows = soup.select('ul.ipc-metadata-list li')[:limit]

    movies = []
    for row in rows:
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

    return movies

def save_movies(movies, filename='output.json'):
    with open(filename, 'w') as f:
        json.dump(movies, f, indent=4)

if __name__ == "__main__":
    movies = scrape_top_movies()
    apply_review_balancer(movies)
    apply_oscar_bonus(movies)
    movies.sort(key=lambda m: m['adjusted_rating'], reverse=True)
    save_movies(movies)
    print("Results written to output.json")
