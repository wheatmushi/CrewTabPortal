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

    def write_table(self, table_name, dataframe, if_exists='replace', index=True):
        dataframe.to_sql(name=table_name, con=self.connection, if_exists=if_exists, index=index)
        self.connection.commit()

    def read_table(self, table_name, order_by, index_col='DT_RowId'):
        sql_req = 'SELECT * FROM {} ORDER BY {} DESC'.format(table_name, order_by)
        dataframe = pd.read_sql(sql_req, self.connection, index_col=index_col)
        return dataframe
