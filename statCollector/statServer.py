import time
import flightStats
import reportStats
from datetime import datetime, timedelta
from DBInterface import DBInterface
from CrewInterface import CrewInterface
import visualization
import pandas as pd

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)
pd.set_option('mode.chained_assignment', None)

url_main = 'https://admin-su.crewplatform.aero/'
DB = DBInterface()


while True:
    start_date = datetime.now()
    table_list = DB.get_list_of_tables()
    interface = CrewInterface(url_main)

    if 'flights' in table_list:
        old_flights = DB.read_table('flights', 'departureDate')
        df_flights = flightStats.update_flights(interface, old_flights)
    else:
        df_flights = flightStats.get_flights_table(interface, start_date + timedelta(days=2), 38, True)

    if 'reports' in table_list:
        old_reports = DB.read_table('reports', 'departureDate')
        df_reports = reportStats.update_reports(interface, old_reports)
    else:
        df_reports = interface.get_reports_table(start_date, -36)

    stats_flights, df_to_check_flights = flightStats.build_stats(df_flights)
    stats_reports = reportStats.build_stats(df_reports, df_flights)
    stats_reports_for_hour = stats_reports[stats_reports['hour'] == stats_reports['hour'].values[-1]]

    DB.write_table('flights', df_flights)
    DB.write_table('reports', df_reports)
    DB.write_table('missing_flights', df_to_check_flights)

    for depth in (7, 9, 14, 21, 30):
        visualization.draw_dashboard(stats_flights, stats_reports, stats_reports_for_hour,
                                     depth=depth, save=True)
    interface.close()
    time.sleep(600)
