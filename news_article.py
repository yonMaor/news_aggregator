from scraper import Scraper
import random


class NewsArticle(Scraper):
    # Handles scraping specific news stories
    def __init__(self, url, title, date_time, categories, source):
        super().__init__(url, 'news_article')
        self.title = title
        self.text = self.get_news_article()
        self.category = self.get_article_type(categories)
        self.date_time = date_time
        self.title = title
        self.source = source

    def get_news_article(self):
        # Returns data from the news article
        soup = self.get_soup()
        article_text = ""
        for wrapper in soup.find_all('div', class_='public-DraftStyleDefault-block public-DraftStyleDefault-ltr'):
            article_text += wrapper.text
        return article_text

    def get_article_type(self, categories):
        # Finds the type of article according to known categories
        article_type = []
        for key in categories.key_words:
            word_list = categories.key_words[key]
            word_list = [' {0} '.format(elem) for elem in word_list]
            if any(x in self.text for x in word_list):
                article_type.append(key)
        if len(article_type) > 1:
            article_type = random.choice(article_type)
        if len(article_type) == 0:
            article_type = random.choice(list(categories.key_words.keys()))
        return article_type
