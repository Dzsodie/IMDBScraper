import pytest
from rating_adjuster import apply_review_balancer, apply_oscar_bonus
from model.movie import Movie

def test_apply_review_balancer():
    movies = [
        Movie("Movie A", rating=9.0, num_reviews=2500000, num_oscars=0),
        Movie("Movie B", rating=8.5, num_reviews=1500000, num_oscars=0),
        Movie("Movie C", rating=9.5, num_reviews=2500000, num_oscars=0),
    ]

    apply_review_balancer(movies)

    assert movies[0].adjusted_rating == 9.0  # No penalty
    assert movies[1].adjusted_rating == 7.5  # 1M diff penalty
    assert movies[2].adjusted_rating == 9.5  # No penalty

def test_apply_oscar_bonus():
    movies = [
        Movie("Movie A", rating=8.0, num_reviews=0, num_oscars=0, adjusted_rating=8.0),
        Movie("Movie B", rating=8.0, num_reviews=0, num_oscars=2, adjusted_rating=8.0),
        Movie("Movie C", rating=8.0, num_reviews=0, num_oscars=4, adjusted_rating=8.0),
        Movie("Movie D", rating=8.0, num_reviews=0, num_oscars=7, adjusted_rating=8.0),
        Movie("Movie E", rating=8.0, num_reviews=0, num_oscars=12, adjusted_rating=8.0),
    ]

    apply_oscar_bonus(movies)

    assert movies[0].adjusted_rating == 8.0  # No Oscars
    assert movies[1].adjusted_rating == 8.3  # 2 Oscars
    assert movies[2].adjusted_rating == 8.5  # 4 Oscars
    assert movies[3].adjusted_rating == 9.0  # 7 Oscars
    assert movies[4].adjusted_rating == 9.5  # 12 Oscars

def test_integration_review_and_oscar_bonus():
    movies = [
        Movie("Movie A", rating=9.0, num_reviews=2000000, num_oscars=3),
        Movie("Movie B", rating=8.5, num_reviews=1500000, num_oscars=1),
        Movie("Movie C", rating=9.5, num_reviews=2500000, num_oscars=0),
    ]

    apply_review_balancer(movies)
    apply_oscar_bonus(movies)

    assert movies[0].adjusted_rating == 9.0  # -0.5 penalty, +0.5 bonus
    assert movies[1].adjusted_rating == 7.8  # -1.0 penalty, +0.3 bonus
    assert movies[2].adjusted_rating == 9.5  # No penalty, no bonus
