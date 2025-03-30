import logging
from model.movie import Movie

def apply_review_balancer(movies: list[Movie]):
    try:
        if not movies:
            logging.warning("No movies provided to apply_review_balancer.")
            return

        max_reviews = max(movie.num_reviews for movie in movies)
        logging.info(f"Maximum number of reviews found: {max_reviews}")

        for movie in movies:
            diff = max_reviews - movie.num_reviews
            penalty = (diff // 100000) * 0.1
            movie.adjusted_rating = round(movie.rating - penalty, 2)
            logging.info(f"'{movie.title}' adjusted rating after review penalty: {movie.adjusted_rating}")

    except Exception as e:
        logging.error(f"Error in apply_review_balancer: {e}")

def apply_oscar_bonus(movies: list[Movie]):
    if not movies:
        logging.warning("No movies provided to apply_oscar_bonus.")
        return

    for movie in movies:
        bonus = 0.0
        if 1 <= movie.num_oscars <= 2:
            bonus = 0.3
        elif 3 <= movie.num_oscars <= 5:
            bonus = 0.5
        elif 6 <= movie.num_oscars <= 10:
            bonus = 1.0
        elif movie.num_oscars > 10:
            bonus = 1.5

        movie.adjusted_rating = round((movie.adjusted_rating or movie.rating) + bonus, 2)
        logging.info(f"'{movie.title}' adjusted rating after Oscar bonus: {movie.adjusted_rating} (Oscars: {movie.num_oscars})")
