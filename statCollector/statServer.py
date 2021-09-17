import time
import flightStats
import reportStats
from datetime import datetime, timedelta, timezone
from DBInterface import DBInterface
from CrewInterface import CrewInterface
import visualization
import pandas as pd

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)
pd.set_option('mode.chained_assignment', None)

url_su = 'https://admin-su.crewplatform.aero/'
url_fv = 'https://admin-fv.crewplatform.aero/'
DB = DBInterface()


while True:
    start_date = datetime.now(timezone.utc)
    table_list = DB.get_list_of_tables()
    interface_su = CrewInterface(url_su)
    interface_fv = CrewInterface(url_fv)

    if 'flights_su' in table_list:
        old_flights_su = DB.read_table('flights_su', 'departureDate')
        df_flights_su = flightStats.update_flights(interface_su, old_flights_su, filter_numbers=3000)
    else:
        df_flights_su = flightStats.get_flights_table(interface_su, start_date + timedelta(days=2), 38, filter_numbers=3000)

    if 'reports_su' in table_list:
        old_reports_su = DB.read_table('reports_su', 'departureDate')
        df_reports_su = reportStats.update_reports(interface_su, old_reports_su, report='purser')
    else:
        df_reports_su = interface_su.get_reports_table(start_date, -36, report='purser')

    if 'flights_fv' in table_list:
        old_flights_fv = DB.read_table('flights_fv', 'departureDate')
        df_flights_fv = flightStats.update_flights(interface_fv, old_flights_fv)
    else:
        df_flights_fv = flightStats.get_flights_table(interface_fv, start_date + timedelta(days=2), 38)

    if 'reports_fv' in table_list:
        old_reports_fv = DB.read_table('reports_fv', 'departureDate')
        df_reports_fv = reportStats.update_reports(interface_fv, old_reports_fv, report='otchet_sb')
    else:
        df_reports_fv = interface_fv.get_reports_table(start_date, -36, report='otchet_sb')

    stats_flights_su, df_to_check_flights_su = flightStats.build_stats(df_flights_su)
    stats_flights_fv, df_to_check_flights_fv = flightStats.build_stats(df_flights_fv)
    stats_reports_su = reportStats.build_stats(df_reports_su, df_flights_su)
    stats_reports_fv = reportStats.build_stats(df_reports_fv, df_flights_fv)
    stats_reports_for_hour_su = stats_reports_su[stats_reports_su['hour'] == start_date.hour]
    stats_reports_for_hour_fv = stats_reports_fv[stats_reports_fv['hour'] == start_date.hour]

    DB.write_table('flights_su', df_flights_su)
    DB.write_table('flights_fv', df_flights_fv)
    DB.write_table('reports_su', df_reports_su)
    DB.write_table('reports_fv', df_reports_fv)
    DB.write_table('missing_flights_su', df_to_check_flights_su)
    DB.write_table('missing_flights_fv', df_to_check_flights_fv)
    DB.write_table('monitor_timestamps', pd.DataFrame(data=[start_date], columns=['timestamp']),
                   if_exists='append', index=False)

    for depth in (7, 9, 14, 21, 30):
        visualization.plot_dashboard_imgs(stats_flights_su, stats_reports_for_hour_su, depth=depth, airline='su')
    for depth in (7, 9, 14, 21, 30):
        visualization.plot_dashboard_imgs(stats_flights_fv, stats_reports_for_hour_fv, depth=depth, airline='fv')

    interface_su.close()
    interface_fv.close()
    time.sleep(600)
