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
num_of_days = 4
is_cm = True  # enable only if different stats for CM and FA required
airports = []  # only build stats for this airports
url_main = 'https://admin-su.crewplatform.aero/'
interface = CrewInterface(url_main)

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)


def check_intervals(df):  # create interval/passengers columns for statistic

    def interval(i):
        if -9 <= i < 30: return 'full'
        if -38 <= i < -9: return 'registration'
        if -4320 <= i < -38: return 'base'
        return 'late_data'

    def passengers(s):
        m = {'full': 'boardedCount', 'registration': 'checkinCount', 'base': 'bookedCount', 'late_data': 'boardedCount'}
        value_to_check = int(s[m[s['interval']]])
        if value_to_check == 0: return 'no_data'
        if value_to_check < 0.7 * int(s['bookedCount']): return 'less_than_expected'
        return 'ok'

    df['difference'] = (df['synchronizationDate'] - df['scheduledDepartureDateTime'])/pd.Timedelta(minutes=1)
    df['interval'] = df['difference'].map(lambda i: interval(i))
    df['passengers'] = df.apply(lambda s: passengers(s), axis=1)
    df = df.drop_duplicates(['staffId', 'flightNumber', 'scheduledDepartureDateTime', 'interval', 'passengers'])
    interval_ordering = ['full', 'registration', 'base', 'late_data']
    passengers_ordering = ['ok', 'less_than_expected', 'no_data']
    df['interval'] = pd.Categorical(df['interval'], categories=interval_ordering, ordered=True)
    df['passengers'] = pd.Categorical(df['passengers'], categories=passengers_ordering, ordered=True)
    return df


def build_stats(df, stat_type):
    if stat_type == 'overall':
        stats = df.sort_values('interval').\
            drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first').\
            groupby('interval').\
            size()
    if stat_type == 'airports':
        stats = df.sort_values('interval').\
            drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first').\
            groupby(['departureAirport', 'interval']).\
            size()
        stats = stats.unstack().fillna(0).astype('int')
    if stat_type == 'staff':
        stats = df.sort_values('interval').\
            drop_duplicates(['staffId', 'flightNumber', 'departureDate'], keep='first').\
            groupby(['staffId', 'interval']).\
            size()
        stats = stats.unstack().fillna(0).astype('int')


def get_crew_roles(interface, df):  # build crew positions table for all flights in df, use carefully as it add 2
    # additional http-requests for every flight in table
    df['position'] = ''
    check_list = df.drop_duplicates(['flightNumber', 'departureDate'])
    crew_list = []
    for i, row in check_list.iterrows():
        date = row['scheduledDepartureDateTime'].strftime('%Y-%m-%d')
        #
        flight_id = interface.get_flights_table(dates_range=date, flight_numbers=row['flightNumber'], id_only=True)
        # need to replace flight_id with one http-request with all ids for this dates
        crews = interface.get_flight_crews(flight_id)
        crews['scheduledDepartureDateTime'] = row['scheduledDepartureDateTime']
        crews['flightNumber'] = row['flightNumber']
        crew_list.append(crews)
    crews = pd.concat(crew_list, axis=0)
    # pd.merge(df, crews)




df = pd.read_csv('db.csv', sep=';', index_col=0, dtype='object')
df['scheduledDepartureDateTime'] = df['scheduledDepartureDateTime'].astype('datetime64')

