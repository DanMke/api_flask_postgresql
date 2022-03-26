import psycopg2
import os
import sys

class Database():
    
    def __init__(self, host=os.environ['POSTGRESQL_ADDRESS'],
                            database=os.environ['POSTGRESQL_DATABASE'],
                            user=os.environ['POSTGRESQL_USERNAME'],
                            password=os.environ['POSTGRESQL_PASSWORD']):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)
        self.cur = self.conn.cursor()

    def query(self, query):
        try:
            self.cur.execute(query)
        except Exception as e:
            self.conn.rollback()
            print(e, file=sys.stderr)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
