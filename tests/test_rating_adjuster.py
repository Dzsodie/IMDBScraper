import pytest
from rating_adjuster import apply_review_balancer, apply_oscar_bonus


def test_apply_review_balancer():
    movies = [
        {"title": "Movie A", "rating": 9.0, "num_reviews": 2500000},
        {"title": "Movie B", "rating": 8.5, "num_reviews": 1500000},
        {"title": "Movie C", "rating": 9.5, "num_reviews": 2500000},
    ]

    apply_review_balancer(movies)

    assert movies[0]['adjusted_rating'] == 9.0  # No penalty, equal max reviews
    assert movies[1]['adjusted_rating'] == 7.5  # Penalty: 1M diff = 1.0 deduction
    assert movies[2]['adjusted_rating'] == 9.5  # No penalty, max reviews


def test_apply_oscar_bonus():
    movies = [
        {"title": "Movie A", "adjusted_rating": 8.0, "num_oscars": 0},
        {"title": "Movie B", "adjusted_rating": 8.0, "num_oscars": 2},
        {"title": "Movie C", "adjusted_rating": 8.0, "num_oscars": 4},
        {"title": "Movie D", "adjusted_rating": 8.0, "num_oscars": 7},
        {"title": "Movie E", "adjusted_rating": 8.0, "num_oscars": 12},
    ]

    apply_oscar_bonus(movies)

    assert movies[0]['adjusted_rating'] == 8.0  # No Oscars, no bonus
    assert movies[1]['adjusted_rating'] == 8.3  # 2 Oscars, +0.3
    assert movies[2]['adjusted_rating'] == 8.5  # 4 Oscars, +0.5
    assert movies[3]['adjusted_rating'] == 9.0  # 7 Oscars, +1.0
    assert movies[4]['adjusted_rating'] == 9.5  # 12 Oscars, +1.5


def test_integration_review_and_oscar_bonus():
    movies = [
        {"title": "Movie A", "rating": 9.0, "num_reviews": 2000000, "num_oscars": 3},
        {"title": "Movie B", "rating": 8.5, "num_reviews": 1500000, "num_oscars": 1},
        {"title": "Movie C", "rating": 9.5, "num_reviews": 2500000, "num_oscars": 0},
    ]

    apply_review_balancer(movies)
    apply_oscar_bonus(movies)

    assert movies[0]['adjusted_rating'] == 9.0  # -0.5 penalty, +0.5 bonus
    assert movies[1]['adjusted_rating'] == 7.8  # -1.0 penalty, +0.3 bonus
    assert movies[2]['adjusted_rating'] == 9.5  # No penalty, no bonus
