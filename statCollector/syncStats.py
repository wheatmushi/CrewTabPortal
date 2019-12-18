#  build devices synchronization statistic

import os
import sys
from time import time
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from crew_utils import date_iterator
from CrewInterface import CrewInterface


start_date = '2019-12-02'
num_of_days = 2
airports = []  # only build stats for this airports


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)


def check_intervals(dataframe, drop_duplicates=True):  # create interval/passengers columns for statistic

    def interval(s, table):
        duration = table[(table['dep_airport'] == s['departureAirport']) &
                         (table['arr_airport'] == s['arrivalAirport'])]['duration'].min()
        duration = duration if 30 < duration < 1000 else 50
        difference = s['difference']
        if -9 <= difference < duration: return 'full'
        if -38 <= difference < -9: return 'registration'
        if -4320 <= difference < -38: return 'base'
        return 'late_data'

    def passengers(s):
        m = {'full': 'boardedCount', 'registration': 'checkinCount', 'base': 'bookedCount', 'late_data': 'boardedCount'}
        value_to_check = int(s[m[s['interval']]])
        if value_to_check == 0: return 'no_data'
        if value_to_check < 0.7 * int(s['bookedCount']): return 'incorrect'
        return 'ok'
    df = dataframe.copy()
    flights_table = pd.read_csv(os.path.join('..', '_DB', 'catering', 'afl_routes.csv'), sep=',')
    df['difference'] = (df['synchronizationDate'] - df['scheduledDepartureDateTime'])/pd.Timedelta(minutes=1)
    #df['interval'] = df['difference'].map(lambda i: interval(i))
    df['interval'] = df.apply(lambda s: interval(s, flights_table), axis=1)
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
    df = dataframe.copy()
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
    if percent_axis:
        stats = stats.apply(lambda line: round(line / line.sum() * 100, 1), axis=percent_axis)
    return stats


def get_crew_roles(interface, df, dates):  # add crew positions in syncs dataframe, this will slow script with 1
    # additional http-request per every flight in table (about 800 requests for one day)
    t = time()
    check_list = df.drop_duplicates(['flightNumber', 'departureDate'])
    flights = interface.get_flights_table(dates_range=dates)
    print('parsing crew roles for {} flights...'.format(check_list.shape[0]))
    crew_list = []
    for i, row in check_list.iterrows():
        date = row['scheduledDepartureDateTime'].strftime('%Y-%m-%d')
        flight_id = flights[(flights['flightNumber'] == row['flightNumber']) &
                            (flights['departureDate'] == row['departureDate'])].index[0]
        crews = interface.get_flight_crews(flight_id, log=False)
        crews['scheduledDepartureDateTime'] = row['scheduledDepartureDateTime']
        crews['flightNumber'] = row['flightNumber']
        crew_list.append(crews)
        if len(crew_list) % 100 == 0:
            print('completed', len(crew_list), 'flights of', check_list.shape[0])
    crews = pd.concat(crew_list, axis=0, sort=False)
    crews = crews.drop(['name', 'email', 'DT_RowId'], axis=1)
    df = df.merge(crews, how='left', on=['staffId', 'flightNumber', 'scheduledDepartureDateTime'])
    print('crew roles parsing time {} seconds'.format(round(time() - t)))
    return df


url_main = 'https://admin-su.crewplatform.aero/'
interface = CrewInterface(url_main)
df = interface.get_syncs(departure_dates=date_iterator(start_date, num_of_days))
df = check_intervals(df)
df = get_crew_roles(interface, df, date_iterator(start_date, num_of_days))
