import requests
from bs4 import BeautifulSoup


class Scraper:
    #Base class for aggregators
    def __init__(self, URL, scraper_type):
        #Args:
        #   string URL: url for the we page to be scraped
        #   string scraper_type: 'main_news_page' or 'new_article'
        self.URL = URL
        self.scrapper_type = scraper_type

    def get_soup(self):
        # Returns the html page in beautiful soup format
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def seperate_date_time(self, time):
        # Separates a date time string to date and time
        time_list = time.split(', ')
        return time_list[1], time_list[0]
