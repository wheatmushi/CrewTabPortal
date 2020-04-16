import sqlite3
import pandas as pd


class DBInterface:
    def __init__(self):
        self.connection = sqlite3.connect('../_DB/CrewTabSQL.sqlite')
        self.cursor = self.connection.cursor()
        
    def get_list_of_tables(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = self.cursor.fetchall()
        return [i for t in res for i in t]

    def write_table(self, table_name, dataframe):
        dataframe.to_sql(name=table_name, con=self.connection, if_exists='replace')
        self.connection.commit()

    def read_table(self, table_name, order_by, depth):
        sql_req = 'SELECT * FROM {} ORDER BY {} DESC limit {}'.format(table_name, order_by, depth)
        dataframe = pd.read_sql(sql_req, self.connection)
        return dataframe


conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

stats_flights.to_sql('stats_flights', con=conn, if_exists='replace')
conn.commit()

q = pd.read_sql('SELECT * FROM stats_flights ORDER BY departureDate DESC limit 10',
                con=conn, index_col='departureDate')
