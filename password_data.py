import psycopg2
import psycopg2.extras
import numpy as np
import pandas as pd
from collections import defaultdict



class PasswordData:

    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def setUp(self):
        with self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            setup_queries = open('schema.sql', 'r').read()
            cursor.execute(setup_queries)
        self.conn.commit()

    def check_connectivity(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM college LIMIT 1")
        records = cursor.fetchall()
        return len(records) == 1

    def query_with_params(self, query, params):
        self.cursor.execute(query, params)
        rst = self.cursor.fetchall()
        return rst

    def print_records(self, records):
        for record in records:
            print(record)

    def commit_execute(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def execute_many(self, query, params):
        self.cursor.executemany(query, params)
        self.conn.commit()

    def select_recent(self, url):
        query = """
        SELECT password
        FROM website
        WHERE url=%(url)s
        """
        params = {'url':url}
        query_result = self.query_with_params(query, params)
        return query_result


    def update_password(self, url):
        if not url:
            print('url is required')
            return

        query = "UPDATE website SET password = '' WHERE url=%(url)s;"
        params = {'url':url}
        self.commit_execute(query, params)
        query_result = self.select_recent(url)
        print("Website: {} successfully updated with Password: {}".format(url, query_result[0][0]))

    def new_password(self, url, name):
        if not url:
            print('url is required')
            return

        if name:
            query = "INSERT INTO website(url,name) VALUES(%(url)s,%(name)s);"
            params = {'url':url, 'name':name}
        else:
            query = "INSERT INTO website(url) VALUES(%(url)s);"
            params = {'url':url}
        self.commit_execute(query, params)
        query_result = self.select_recent(url)
        print("Website: {} successfully inserted with Password: {}".format(url, query_result[0][0]))

    def see_password_website(self, url):
        query = """
        SELECT *
        FROM website
        WHERE url = %(url)s;
        """
        params = {'url':url}
        query_result = self.query_with_params(query, params)
        print(query_result)

    def see_password_company(self, name):
        query = """
        SELECT *
        FROM website
        WHERE name = %(name)s;
        """
        params = {'name':name}
        query_result = self.query_with_params(query, params)
        result_pd = pd.DataFrame(query_result, columns=['Website', 'Company Name', 'Password'])
        print(result_pd)

    def see_old_password(self, url):
        query = """
        SELECT *
        FROM old_passwords
        WHERE url = %(url)s
        ORDER BY last_used DESC;
        """
        params = {'url':url}
        query_result = self.query_with_params(query, params)
        result_pd = pd.DataFrame(query_result, columns=['Website', 'Day Created', 'Password'])
        print(result_pd)
