import sys
import os
import time
import flightStats
import reportStats
from datetime import datetime, timedelta
sys.path.insert(1, os.path.join('..', '_common'))
import DBinterface
import CrewInterface
import visualization


url_main = 'https://admin-su.crewplatform.aero/'


while True:
    start_date = datetime.now()
    table_list = DBinterface.get_list_of_tables()
    interface = CrewInterface(url_main, login='test', password='test')

    if 'flights' in table_list:
        old_flights = DBinterface.read_table('flights', 'departureDate', '*')
        df_flights = flightStats.update_flights(old_flights)
    else:
        df_flights = flightStats.get_flights_table(interface, start_date + timedelta(days=2), 35, True)

    if 'reports' in table_list:
        old_reports = DBinterface.read_table('reports', 'departureDate', '*')
        df_reports = reportStats.update_reports(old_reports)
    else:
        df_reports = interface.get_reports_table(start_date, -35)

    DBinterface.write_table('flights', df_flights)
    DBinterface.write_table('reports', df_reports)

    stats_flights = flightStats.build_stats(df_flights)
    stats_reports = reportStats.build_stats(df_reports)
    stats_reports_for_hour = stats_reports[stats_reports['hour'] == stats_reports['hour'].values[-1]]

    for depth in (7, 9, 14, 21, 30):
        visualization.draw_dashboard(stats_flights, stats_reports, stats_reports_for_hour,
                                     depth=depth, save=True)

    time.sleep(10)
