#  build devices synchronization statistic

import os
import sys
from datetime import datetime, timedelta
from time import time
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
import auth
import URLs
import crew_utils
from CrewInterface import CrewInterface
import json


start_date = '2019-12-01'
num_of_days = 1
airports = []  # only build stats for this airports
url_main = 'https://admin-su.crewplatform.aero/'
interface = CrewInterface(url_main)

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)


def check_intervals(df, drop_duplicates=True):  # create interval/passengers columns for statistic

    def interval(i):
        if -9 <= i < 30: return 'full'
        if -38 <= i < -9: return 'registration'
        if -4320 <= i < -38: return 'base'
        return 'late_data'

    def passengers(s):
        m = {'full': 'boardedCount', 'registration': 'checkinCount', 'base': 'bookedCount', 'late_data': 'boardedCount'}
        value_to_check = int(s[m[s['interval']]])
        if value_to_check == 0: return 'no_data'
        if s['interval'] == 'late_data': return
        if value_to_check < 0.7 * int(s['bookedCount']): return 'less_than_expected'
        return 'ok'

    df['difference'] = (df['synchronizationDate'] - df['scheduledDepartureDateTime'])/pd.Timedelta(minutes=1)
    df['interval'] = df['difference'].map(lambda i: interval(i))
    df['passengers'] = df.apply(lambda s: passengers(s), axis=1)
    if drop_duplicates:
        df = df.drop_duplicates(['staffId', 'flightNumber', 'scheduledDepartureDateTime', 'interval', 'passengers'])
    interval_type = pd.api.types.CategoricalDtype(categories=['full', 'registration', 'base', 'late_data'], ordered=True)
    passengers_type = pd.api.types.CategoricalDtype(categories=['ok', 'less_than_expected', 'no_data'], ordered=True)
    df['interval'] = df['interval'].astype(interval_type)
    df['passengers'] = df['passengers'].astype(passengers_type)
    return df


def build_stats(interface, df, dates, aggregation='overall', stat_type='common'):
    # aggregation for overall period/hourly/daily
    # type of stats: common/airports/staff_id/CM_FA
    if aggregation == 'overall':
        if stat_type == 'common':
            stats = df.sort_values('interval').\
                drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first').\
                groupby('interval').\
                size()
        if stat_type == 'airports':
            stats = df.sort_values('interval').\
                drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first').\
                groupby(['departureAirport', 'interval']).\
                size()
        if stat_type == 'staff':
            stats = df.sort_values('interval').\
                drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first').\
                groupby(['staffId', 'interval']).\
                size()
        if stat_type == 'CM':
            df = get_crew_roles(interface, df, dates)
            stats = df.sort_values('interval'). \
                drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first'). \
                groupby(['position', 'interval']). \
                size()


    return stats.unstack().fillna(0).astype('int')


def get_crew_roles(interface, df, dates):  # add crew positions in syncs dataframe, this will slow script with 1
    # additional http-requests per every flight in table (about 800 requests for one day)
    t = time()
    check_list = df.drop_duplicates(['flightNumber', 'departureDate'])
    flights = interface.get_flights_table(dates_range=dates)
    print('parsing crew roles for {} flights...'.format(len(flights)))
    crew_list = []
    for i, row in check_list.iterrows():
        date = row['scheduledDepartureDateTime'].strftime('%Y-%m-%d')
        flight_id = flights[(flights['flightNumber'] == row['flightNumber']) &
                            (flights['departureDate'] == row['departureDate'])].index[0]
        crews = interface.get_flight_crews(flight_id)
        crews['scheduledDepartureDateTime'] = row['scheduledDepartureDateTime']
        crews['flightNumber'] = row['flightNumber']
        crew_list.append(crews)
    crews = pd.concat(crew_list, axis=0)
    crews = crews.drop(['name', 'email', 'DT_RowId'], axis=1)
    df = df.merge(crews, how='left', on=['staffId', 'flightNumber', 'scheduledDepartureDateTime'])
    print('crew roles parsing time {} seconds'.format(round(time() - t)))
    return df


df = interface.get_syncs(departure_dates=crew_utils.date_iterator(start_date, num_of_days))
df = check_intervals(df)
df = get_crew_roles(interface, df, crew_utils.date_iterator(start_date, num_of_days))
