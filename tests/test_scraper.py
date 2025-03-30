import pytest
from unittest.mock import patch, Mock, mock_open
import scraper

@patch('scraper.fetch_page')
def test_scrape_top_movies_success(mock_fetch_page):
    mock_soup = Mock()
    mock_fetch_page.return_value = mock_soup

    mock_row = Mock()
    mock_row.select_one.side_effect = [
        Mock(text='Movie Title 1'),
        Mock(text='9.2 (1M)'),
        Mock(text='(1M)'),
        {'href': '/title/tt0111161/'}
    ]

    mock_soup.select.return_value = [mock_row]

    with patch('scraper.parse_num_reviews', return_value=1000000) as mock_reviews, \
         patch('scraper.parse_oscar_count', return_value=2) as mock_oscars:

        movies = scraper.scrape_top_movies(limit=1)

        assert len(movies) == 1
        assert movies[0]['title'] == 'Movie Title 1'
        assert movies[0]['rating'] == 9.2
        assert movies[0]['num_reviews'] == 1000000
        assert movies[0]['num_oscars'] == 2

@patch('scraper.fetch_page', side_effect=Exception("Network error"))
def test_scrape_top_movies_network_error(mock_fetch_page):
    movies = scraper.scrape_top_movies()
    assert movies == []

@patch('os.path.exists', return_value=True)
@patch('builtins.open', new_callable=mock_open)
def test_save_movies(mock_file, mock_exists):
    movies = [{'title': 'Test Movie', 'rating': 9.0, 'num_reviews': 1000, 'num_oscars': 0}]

    scraper.save_movies(movies, filename='output.json')

    mock_file.assert_called_with('output.json', 'w')
    handle = mock_file()
    handle.write.assert_called()

@patch('os.path.exists', return_value=True)
@patch('builtins.open', side_effect=Exception("Disk error"))
def test_save_movies_exception(mock_file, mock_exists):
    movies = [{'title': 'Test Movie', 'rating': 9.0, 'num_reviews': 1000, 'num_oscars': 0}]

    scraper.save_movies(movies, filename='output.json')
    # Ensure exception handled gracefully without crashing
