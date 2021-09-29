#  use stats modules to draw standalone dashboard
import sys
import os
import pandas as pd
from datetime import datetime, timedelta, timezone
import flightStats
import reportStats
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface
import visualization


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)
pd.set_option('mode.chained_assignment', None)


url_main = 'https://admin-su.crewplatform.aero/'
num_of_days = 15
start_date = datetime.now(timezone.utc)


interface = CrewInterface(url_main)
df_flights = flightStats.get_flights_table(interface, start_date + timedelta(days=2), num_of_days)
df_reports = interface.get_reports_table(start_date, -num_of_days)

stats_flights, df_to_check_flights = flightStats.build_stats(df_flights)
stats_reports = reportStats.build_stats(df_reports, df_flights)
stats_reports_for_hour = stats_reports[stats_reports['hour'] == start_date.hour]

visualization.draw_dashboard(stats_flights, stats_reports, stats_reports_for_hour)
flightStats.print_missing(df_to_check_flights, 3)
