import sys
import os
import pandas as pd
from datetime import datetime, timedelta
import flightStats
# import reportStats
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface
import visualization


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)
pd.set_option('mode.chained_assignment', None)


url_main = 'https://admin-su.crewplatform.aero/'
num_of_days = 35
start_date = datetime.now() + timedelta(days=2)

path_to_DB = os.path.join('..', '_DB', 'flights', 'flights_DB.csv')
filter_numbers = True


interface = CrewInterface(url_main)
df_flights = flightStats.get_flights_table(interface, start_date, num_of_days, path_to_DB, filter_numbers)
stats_flights, df_to_check_flights = flightStats.build_stats(df_flights)
visualization.bar_graph(stats_flights)
flightStats.print_missing(df_to_check_flights, 3)
