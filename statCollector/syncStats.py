#  build devices synchronization statistic in two views: amount of syncs in given time intervals
#  and receiving of passengers data

import os
import sys
from time import time
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from crew_utils import date_iterator
from CrewInterface import CrewInterface


start_date = '2019-11-18'
num_of_days = 30
dates = [d for d in date_iterator(start_date, num_of_days)]
airports = ['']  # only build stats for this airports


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)


def check_intervals(dataframe, drop_duplicates=True):  # create interval/passengers columns for statistic

    def interval(s, table):
        duration = table[(table['dep_airport'] == s['departureAirport']) &
                         (table['arr_airport'] == s['arrivalAirport'])]['duration'].min()
        duration = duration if 30 < duration < 1000 else 50
        difference = s['difference']
        if -9 <= difference < duration: return 'full'  # full boarding data
        if -38 <= difference < -9: return 'registration'  # checked in data
        if -4320 <= difference < -38: return 'base'  # booking data
        return 'late_data'  # data received after flight end

    def passengers(s):
        m = {'full': 'boardedCount', 'registration': 'checkinCount', 'base': 'bookedCount', 'late_data': 'boardedCount'}
        value_to_check = int(s[m[s['interval']]])
        if value_to_check == 0: return 'no_data'
        if value_to_check < 0.7 * int(s['bookedCount']): return 'incorrect'
        return 'ok'
    df = dataframe.copy(deep=True)
    routes_table = pd.read_csv(os.path.join('..', '_DB', 'catering', 'afl_routes.csv'), sep=',')
    df['difference'] = (df['synchronizationDate'] - df['scheduledDepartureDateTime'])/pd.Timedelta(minutes=1)
    df['interval'] = df.apply(lambda s: interval(s, routes_table), axis=1)
    df['passengers'] = df.apply(lambda s: passengers(s), axis=1)
    if drop_duplicates:
        df = df.drop_duplicates(['staffId', 'flightNumber', 'scheduledDepartureDateTime', 'interval', 'passengers'])
    interval_type = pd.api.types.CategoricalDtype(categories=['full', 'registration', 'base', 'late_data'], ordered=True)
    passengers_type = pd.api.types.CategoricalDtype(categories=['ok', 'incorrect', 'no_data'], ordered=True)
    df['interval'] = df['interval'].astype(interval_type)
    df['passengers'] = df['passengers'].astype(passengers_type)
    return df


def build_stats(interface, dataframe, dates, kind, index, columns, percent_axis=None):
    # kind: passengers (for passengers data) or interval (for sync intervals)
    # index: rows for stat table (day, hour, departureAirport, staffId, passengers, etc), group by most left first
    # columns: columns for stat table (position, interval, etc), group by most left first
    # percent_axis: 0 for percent count along column, 1 for percent count along row, None for raw numbers
    df = dataframe.copy(deep=True)
    if ('position' in index or 'position' in columns) and 'position' not in df.columns:
        df = get_crew_roles(interface, df, dates)
    df = df[df['position'].isin(('CM', 'FA'))]
    df['day'] = df['scheduledDepartureDateTime'].dt.date
    df['hour'] = df['scheduledDepartureDateTime'].dt.hour

    if kind == 'passengers':
        df = df.sort_values('passengers')
        df = df.drop_duplicates(['staffId', 'flightNumber', 'departureDate', 'interval'], keep='first')
        df_late = df[df['interval'] == 'late_data']

        # add 'fake' no_sync records for reg interval if no reg sync detected but sync presence in late_data interval
        staff_reg = df[df['interval'] == 'registration']['staffId']
        df_add_reg = df_late[~df_late['staffId'].isin(staff_reg)]
        df_add_reg['interval'] = 'registration'
        df_add_reg['passengers'] = 'no_sync'
        df_add_reg[['synchronizationDate', 'lastUpdate', 'deviceId', 'difference']] = 0

        # add 'fake' no_sync records for full interval if no full sync detected but sync presence in late_data interval
        staff_full = df[df['interval'] == 'full']['staffId']
        df_add_full = df_late[~df_late['staffId'].isin(staff_full)]
        df_add_full['interval'] = 'full'
        df_add_full['passengers'] = 'no_sync'
        df_add_full[['synchronizationDate', 'lastUpdate', 'deviceId', 'difference']] = 0

        df = pd.concat([df, df_add_reg, df_add_full], axis=0, sort=False)

    elif kind == 'interval':
        df = df.sort_values('interval')
        df = df[df['scheduledDepartureDateTime'] < pd.Timestamp(time(), unit='s')]
        df = df.drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first')

    stats = df.pivot_table(index=index, columns=columns, aggfunc='size', fill_value=0)
    if type(percent_axis) is int:
        stats_percents = stats.apply(lambda line: round(line / line.sum() * 100, 1), axis=percent_axis)
        if percent_axis == 1:
            stats_percents.columns = ['% ' + c for c in stats_percents.columns]
        elif percent_axis == 0:
            stats_percents.index = ['% ' + c for c in stats_percents.index]
        stats = pd.concat([stats_percents, stats], axis=percent_axis)
    return stats.sort_index(ascending=False)


def get_crew_roles(interface, df, dates):  # add crew positions in syncs dataframe, this will slow script with 1
    # additional http-request per every flight in table (about 800 requests for one day)
    # NEED TO ADD save temp result mechanism for poor internet connection
    t = time()
    check_list = df.drop_duplicates(['flightNumber', 'departureDate'])
    if 'temp_crews.csv' in os.listdir('.'):
        if input('load crew data from temporary file? y/n') == 'y':
            temp_crew_table = pd.read_csv('temp_crews.csv', index_col=0, sep=',')
            check_list = check_list[~((check_list['flightNumber'].isin(temp_crew_table['flightNumber'])) &
                                    (check_list['departureDate'].isin(temp_crew_table['departureDate'])))]
    flights = interface.get_flights_table(dates_range=dates)
    print('parsing crew roles for {} flights...'.format(check_list.shape[0]))
    crew_list = []
    for i, row in check_list.iterrows():
        flight_id = flights[(flights['flightNumber'] == row['flightNumber']) &
                            (flights['departureDate'] == row['departureDate'])].index[0]
        crews = interface.get_flight_crews(flight_id, log=False)
        crews['scheduledDepartureDateTime'] = row['scheduledDepartureDateTime']
        crews['flightNumber'] = row['flightNumber']
        crew_list.append(crews)
        if len(crew_list) % 500 == 0:
            print('completed', len(crew_list), 'flights of', check_list.shape[0])
            temp_crew_table = pd.concat(crew_list, axis=0, sort=False)
            temp_crew_table.to_csv('temp_crews.csv')
    crews = pd.concat(crew_list, axis=0, sort=False)
    crews = crews.drop(['name', 'email', 'DT_RowId'], axis=1)
    df = df.merge(crews, how='left', on=['staffId', 'flightNumber', 'scheduledDepartureDateTime'])
    os.remove('temp_crews.csv')
    print('crew roles parsing time {} seconds'.format(round(time() - t)))
    return df


url_main = 'https://admin-su.crewplatform.aero/'
interface = CrewInterface(url_main)
df = interface.get_syncs(departure_dates=dates, departure_airports=airports)
df = check_intervals(df)
df = get_crew_roles(interface, df, dates)
