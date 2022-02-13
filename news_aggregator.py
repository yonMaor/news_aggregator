from scraper import Scraper
from news_article import NewsArticle
import datetime as dt
from categories import Categories


class NewsAggregator(Scraper):
    # Handles scrapping the general breaking news page

    def __init__(self, url, news_source, database):
        super().__init__(url, 'main_news_page')
        self.database = database
        self.categories = Categories()
        self.news_source = news_source

    def get_news_articles(self, last_date_time):
        # Finds new news articles that have been published after last_date_time
        soup = self.get_soup()
        for wrapper in soup.find_all('div', class_='textDiv'):
            breaking_news_item = wrapper.find('div', class_='slotTitle')
            link = breaking_news_item.find('a')['href']
            title = breaking_news_item.text.strip()
            date_time = wrapper.find('span', class_='dateView').text.strip()
            date_time = dt.datetime.strptime(date_time, '%H:%M, %m.%d.%y')
            date_time = int(date_time.strftime('%y%m%d%H%M'))
            article_is_new = self.compare_date_time(date_time, last_date_time)
            if article_is_new:  # Article hasn't been added yet
                article = NewsArticle(link, title, date_time, self.categories, self.news_source)
                self.database.add_news_article(article)
            else:
                break

    def compare_date_time(self, date_time, last_date_time):
        # Compares two points in time, returns true of date_time is closer than last_date
        if date_time > last_date_time:
            return True
        return False
