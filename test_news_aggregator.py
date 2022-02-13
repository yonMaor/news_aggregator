import unittest
from news_aggregator import NewsAggregator
from database_api import DatabaseAPI


class TestNewsAggregator(unittest.TestCase):
    def test_compare_date_time(self):
        database = DatabaseAPI('test_db')
        news_aggregator = NewsAggregator('3089.html', 'ynet', database)
        self.assertTrue(news_aggregator.compare_date_time(2, 1))
        self.assertFalse(news_aggregator.compare_date_time(1, 2))

