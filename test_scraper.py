import pytest
from unittest.mock import patch, Mock
from scraper import scrape_top_movies, parse_num_reviews


# Unit tests for parse_num_reviews
def test_parse_num_reviews_millions():
    assert parse_num_reviews("3M") == 3_000_000

def test_parse_num_reviews_thousands():
    assert parse_num_reviews("250K") == 250_000

def test_parse_num_reviews_plain_number():
    assert parse_num_reviews("12345") == 12345

def test_parse_num_reviews_with_brackets():
    assert parse_num_reviews("(1.2M)") == 1_200_000

def test_parse_num_reviews_with_special_chars():
    assert parse_num_reviews("\xa0(3M)") == 3_000_000


# Mock HTML response for scraper tests
MOCK_HTML = """
<html>
<body>
<ul class="ipc-metadata-list">
    <li>
        <h3>Movie Title 1</h3>
        <span class="ipc-rating-star--imdb">9.2 (1M)</span>
        <span class="ipc-rating-star--voteCount">(1.1M)</span>
    </li>
    <li>
        <h3>Movie Title 2</h3>
        <span class="ipc-rating-star--imdb">8.8 (500K)</span>
        <span class="ipc-rating-star--voteCount">(500K)</span>
    </li>
</ul>
</body>
</html>
"""

# Unit test for scrape_top_movies
@patch('scraper.requests.get')
def test_scrape_top_movies(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = MOCK_HTML
    mock_get.return_value = mock_response

    movies = scrape_top_movies(limit=2)

    assert len(movies) == 2

    assert movies[0]['title'] == 'Movie Title 1'
    assert movies[0]['rating'] == 9.2
    assert movies[0]['num_reviews'] == 1_100_000
    assert movies[0]['num_oscars'] == 0

    assert movies[1]['title'] == 'Movie Title 2'
    assert movies[1]['rating'] == 8.8
    assert movies[1]['num_reviews'] == 500_000
    assert movies[1]['num_oscars'] == 0


def test_scrape_top_movies_http_error():
    with patch('scraper.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        mock_get.return_value = mock_response

        with pytest.raises(Exception) as exc_info:
            scrape_top_movies()

        assert "HTTP Error" in str(exc_info.value)