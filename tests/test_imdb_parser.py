import pytest
from unittest.mock import patch, Mock
import requests
import imdb_parser


@patch('imdb_parser.requests.get')
def test_fetch_page_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test Content</body></html>"
    mock_get.return_value = mock_response

    soup = imdb_parser.fetch_page("https://example.com")
    assert soup.text == "Test Content"


@patch('imdb_parser.requests.get', side_effect=requests.exceptions.RequestException("Network error"))
def test_fetch_page_exception(mock_get):
    with pytest.raises(requests.exceptions.RequestException):
        imdb_parser.fetch_page("https://example.com")


def test_parse_num_reviews():
    assert imdb_parser.parse_num_reviews("3M") == 3_000_000
    assert imdb_parser.parse_num_reviews("250K") == 250_000
    assert imdb_parser.parse_num_reviews("12345") == 12345
    assert imdb_parser.parse_num_reviews("\xa0(2.5M)") == 2_500_000


def test_parse_num_reviews_invalid_input():
    assert imdb_parser.parse_num_reviews("invalid") == 0


@patch('imdb_parser.fetch_page')
def test_parse_oscar_count_success(mock_fetch_page):
    mock_soup = Mock()
    mock_soup.select_one.return_value.text = "Won 5 Oscars"
    mock_fetch_page.return_value = mock_soup

    oscars = imdb_parser.parse_oscar_count("https://example.com/movie")
    assert oscars == 5


@patch('imdb_parser.fetch_page')
def test_parse_oscar_count_no_oscars(mock_fetch_page):
    mock_soup = Mock()
    mock_soup.select_one.return_value = None
    mock_fetch_page.return_value = mock_soup

    oscars = imdb_parser.parse_oscar_count("https://example.com/movie")
    assert oscars == 0


@patch('imdb_parser.fetch_page')
def test_parse_oscar_count_unexpected_format(mock_fetch_page):
    mock_soup = Mock()
    mock_soup.select_one.return_value.text = "Oscar Nominee"
    mock_fetch_page.return_value = mock_soup

    oscars = imdb_parser.parse_oscar_count("https://example.com/movie")
    assert oscars == 0


@patch('imdb_parser.fetch_page', side_effect=Exception("Network error"))
def test_parse_oscar_count_fetch_error(mock_fetch_page):
    oscars = imdb_parser.parse_oscar_count("https://example.com/movie")
    assert oscars == 0
