# IMDB Scraper

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Made with Python](https://img.shields.io/badge/Made%20with-Python%203.13.2-blue?style=for-the-badge&logo=python)
![pytest](https://img.shields.io/badge/Tests-pytest%208.3.5-brightgreen?style=for-the-badge&logo=pytest)
![BeautifulSoup4](https://img.shields.io/badge/Scraping-BeautifulSoup4-orange?style=for-the-badge&logo=python)
![requests](https://img.shields.io/badge/HTTP-requests%20library-red?style=for-the-badge&logo=python)
![JSON](https://img.shields.io/badge/Output-JSON%20format-yellowgreen?style=for-the-badge&logo=json)

A Python-based solution that scraps data from IMDB and creates a curated rating for the top 20 movies. This solution is created for interview challenge purpose, it uses BeautifulSoup4 scraper and Python's requests library. It writes the 20 top movies with rating into a json file.

### Features
- scraper to call to IMDB and get raw data
- rating adjuster to curate data scraped from IMDB
- result written to `output.json`
- simple caching to reduce scraping time

### Prerequisites
1. Make sure Python 3.8+ is installed.
    ```bash
    python3 --version
    ```
2. Install dependencies of Requests and BeautifySoup4 by running this command.  
    ```bash
    pip3 install -r requirements.txt
    ```

### Steps to Run the Application Locally
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/Dzsodie/IMDBScraper.git
    cd IMDBScarper
    ```
2. Use the following command while in the directory of the IMDBScraper
    ```bash
    python3 scraper.py
    ```

### Run tests
1. Use the following command while in the directory of the IMDBScraper
    ```bash
    python3 -m pytest
    ```
2. Running specific test file use this command
    ```bash
    python3 -m pytest tests/test_scraper.py
    ```
    
### Logging
    Logs are saved to `app.log` file. Log level can be adjusted in `logging_config.py`

### Further enhancements
- log aggregation
- config file for different settings
- persistency in DB

### License
    This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.