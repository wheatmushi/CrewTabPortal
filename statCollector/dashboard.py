import sys
import os
import pandas as pd
from datetime import datetime, timedelta
import flightStats
import reportStats
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface
import visualization


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)
pd.set_option('mode.chained_assignment', None)


url_main = 'https://admin-su.crewplatform.aero/'
num_of_days = 35
start_date = datetime.now()

path_to_DB = os.path.join('..', '_DB', 'flights', 'flights_DB.csv')
filter_numbers = True
params = {"form_id": '51',
          "staff_id": '',
          "flight_number": '',
          "dep_airport": '',
          "arr_airport": '',
          "reg_number": ''}


interface = CrewInterface(url_main)
df_flights = flightStats.get_flights_table(interface, start_date + timedelta(days=2),
                                           num_of_days, path_to_DB, filter_numbers)
df_reports = interface.get_reports_table(start_date, -num_of_days, params)

stats_flights, df_to_check_flights = flightStats.build_stats(df_flights)
stats_reports = reportStats.build_stats(df_reports, df_flights)
stats_reports_for_hour = stats_reports[stats_reports['hour'] == stats_reports['hour'].values[-1]]

visualization.draw_dashboard(stats_flights, stats_reports, stats_reports_for_hour)
flightStats.print_missing(df_to_check_flights, 3)

from importlib import reload
visualization = reload(visualization)
