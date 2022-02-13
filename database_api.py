import sqlite3 as sl
from sqlite3 import Error


# TODO: make sure that articles and users are unique, do this by hashing all of the user personal data with sha1
class DatabaseAPI():
    # Handles all communications with the database
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        if self.conn is not None:
            self.create_table(self.create_user_table_query())
            self.create_table(self.create_news_table_query())
        else:
            print("Error! cannot create the database connection.")

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sl.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_query):
        try:
            cur = self.conn.cursor()
            cur.execute(create_table_query)
        except Error as e:
            print(e)

    def create_user_table_query(self):
        query = '''
                    CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT,
                        category TEXT,
                        timing TEXT,
                        timing_day TEXT,
                        timing_hour TEXT,
                        last_update INTEGER,
                        next_update INTEGER
                    );
        '''
        return query

    def create_news_table_query(self):
        query = '''
                    CREATE TABLE IF NOT EXISTS article (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        URL TEXT,
                        category TEXT,
                        article_text TEXT,
                        date_time INTEGER,
                        source TEXT
                    );
        '''
        return query

    def get_user(self, user_email):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM USER WHERE email=?', (user_email,))
        rows = cur.fetchall()
        return rows

    def get_news_article(self, article_title):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM NEWS_ARTICLE WHERE title=?', (article_title,))
        rows = cur.fetchall()
        return rows

    def add_user(self, user):
        sql_query = '''INSERT INTO user (name, email, category, timing, timing_day, timing_hour, next_update) values(?, ?, ?, ?, ?, ?, ?)'''
        data = (
            user.name, user.email, user.category, user.timing, user.timing_day, user.timing_hour, user.next_update)
        user_rows = self.query_database(query_text='SELECT * FROM USER WHERE email=?', query_data=(user.email,))
        if len(user_rows) != 0:
            print('User already exists - new row was not inserted')
            return 0

        cur = self.conn.cursor()
        cur.execute(sql_query, data)
        self.conn.commit()
        return cur.lastrowid

    def add_news_article(self, article):
        sql_query = '''INSERT INTO article (title, URL, category, article_text, date_time, source) VALUES(?, ?, ?, ?, ?, ?)'''
        data = (article.title, article.URL, article.category, article.text, article.date_time, article.source)
        cur = self.conn.cursor()
        cur.execute(sql_query, data)
        self.conn.commit()
        return cur.lastrowid

    def get_latest_news_article(self):
        latest_id = self.conn.execute(''' SELECT last_insert_rowid() ''')
        return latest_id

    def query_database(self, **kwargs):
        cur = self.conn.cursor()
        if len(kwargs) == 1:
            cur.execute(kwargs['query_text'])
        if len(kwargs) == 2:
            cur.execute(kwargs['query_text'], kwargs['query_data'])
        rows = cur.fetchall()
        return rows

    def update_database(self, **kwargs):
        cur = self.conn.cursor()
        if len(kwargs) == 1:
            cur.execute(kwargs['query_text'])
        if len(kwargs) == 2:
            cur.execute(kwargs['query_text'], kwargs['query_data'])
        self.conn.commit()
        rows = cur.fetchall()
        return rows
