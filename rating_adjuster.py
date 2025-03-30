import logging

def apply_review_balancer(movies):
    try:
        if not movies:
            logging.warning("No movies provided to apply_review_balancer.")
            return

        max_reviews = max(movie.get('num_reviews', 0) for movie in movies)
        logging.info(f"Maximum number of reviews found: {max_reviews}")

        for movie in movies:
            try:
                reviews = movie.get('num_reviews', 0)
                rating = movie.get('rating', 0)

                diff = max_reviews - reviews
                penalty = (diff // 100000) * 0.1

                movie['adjusted_rating'] = round(rating - penalty, 2)

                logging.info(f"'{movie['title']}' adjusted rating after review penalty: {movie['adjusted_rating']}")

            except Exception as e:
                logging.error(f"Failed to adjust rating for movie '{movie.get('title', 'Unknown')}': {e}")

    except Exception as e:
        logging.error(f"Error in apply_review_balancer: {e}")

def apply_oscar_bonus(movies):
    if not movies:
        logging.warning("No movies provided to apply_oscar_bonus.")
        return

    for movie in movies:
        try:
            oscars = movie.get('num_oscars', 0)
            adjusted_rating = movie.get('adjusted_rating', movie.get('rating', 0))

            bonus = 0.0
            if 1 <= oscars <= 2:
                bonus = 0.3
            elif 3 <= oscars <= 5:
                bonus = 0.5
            elif 6 <= oscars <= 10:
                bonus = 1.0
            elif oscars > 10:
                bonus = 1.5

            movie['adjusted_rating'] = round(adjusted_rating + bonus, 2)

            logging.info(f"'{movie['title']}' adjusted rating after Oscar bonus: {movie['adjusted_rating']} (Oscars: {oscars})")

        except Exception as e:
            logging.error(f"Failed to apply Oscar bonus for movie '{movie.get('title', 'Unknown')}': {e}")