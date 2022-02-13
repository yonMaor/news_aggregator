from database_api import DatabaseAPI
from news_aggregator import NewsAggregator
from user import User
from notifier import Notifier
import datetime as dt

import utils
import time

LOOP_INTERVAL = 60
database = DatabaseAPI('News_Aggregator_Database.db')

date_started = '20:47, 02.10.22'
utils.populate_user_database(database)
url = 'https://www.ynetnews.com/category/3089'
ynet_scrapper = NewsAggregator(url, 'ynet', database)
last_added_article = database.query_database(
    query_text='SELECT date_time FROM article ORDER BY date_time DESC LIMIT 1')
if len(last_added_article) == 0:
    last_added_article = 2202120816
else:
    last_added_article = last_added_article[0][0]

while True:
    time_now = dt.datetime.now()
    delta = dt.timedelta(0, LOOP_INTERVAL)
    time_now_with_delta = time_now + delta
    time_now_with_delta = int(time_now_with_delta.strftime('%y%m%d%H%M'))
    ynet_scrapper.get_news_articles(last_added_article)
    users_to_email = database.query_database(query_text='SELECT * FROM user WHERE next_update<?',
                                             query_data=(time_now_with_delta,))

    for user_tuple in users_to_email:
        user_obj = User('database', LOOP_INTERVAL, user=user_tuple)
        user_obj.set_next_update_time(time_now_with_delta, database)
        article_list = database.query_database(
            query_text='SELECT * FROM article WHERE date_time BETWEEN ? AND ? AND category=?',
            query_data=(user_obj.last_update, user_obj.next_update, user_obj.category))
        if len(article_list) != 0:
            notif = Notifier(user_obj, article_list)
            notif.send_email()

    time.sleep(LOOP_INTERVAL)
