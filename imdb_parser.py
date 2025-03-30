import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                  "AppleWebKit/537.36 (KHTML, like Gecko)"
                  "Chrome/123.0.0.0 Safari/537.36"
}

def fetch_page(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def parse_num_reviews(num_reviews_str):
    num_reviews_str = num_reviews_str.replace('\xa0', '').replace('(', '').replace(')', '').strip()
    if 'K' in num_reviews_str:
        return int(float(num_reviews_str.replace('K', '')) * 1_000)
    elif 'M' in num_reviews_str:
        return int(float(num_reviews_str.replace('M', '')) * 1_000_000)
    else:
        return int(num_reviews_str.replace(',', ''))

def parse_oscar_count(movie_url):
    soup = fetch_page(movie_url)
    awards_section = soup.select_one('li[data-testid="award_information"]')
    if awards_section:
        awards_text = awards_section.text
        if "Won" in awards_text and "Oscar" in awards_text:
            try:               
                oscars_won_part = awards_text.split("Won")[1].split("Oscar")[0].strip()
                oscars_won = int(oscars_won_part)
                return oscars_won
            except (IndexError, ValueError):
                return 0  
    return 0
