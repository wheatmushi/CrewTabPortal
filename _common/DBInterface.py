import sqlite3
import pandas as pd


class DBInterface:
    def __init__(self):
        self.connection = sqlite3.connect('../_DB/CrewTabSQL.sqlite')

    def create_table(self, table_name, dataframe):
        dataframe.to_sql(name=table_name, con=self.connection)

    def update_table(self, table_name, dataframe):
        p2 =

    def read_table(self, table_name):
        dataframe = pd.read_sql('select * from {}'.format(table_name), self.connection)
        return dataframe


