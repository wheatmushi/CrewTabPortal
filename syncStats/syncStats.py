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


start_date = '2019-11-24'
num_of_days = 4
is_cm = True  # enable only if different stats for CM and FA required
airports = []  # only build stats for this airports
url_main = 'https://admin-su.crewplatform.aero/'
itf = CrewInterface(url_main)

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
    interval_ordering = ['full', 'registration', 'base', 'late_data']
    passengers_ordering = ['ok', 'less_than_expected', 'no_data']
    df['interval'] = pd.Categorical(df['interval'], categories=interval_ordering, ordered=True)
    df['passengers'] = pd.Categorical(df['passengers'], categories=passengers_ordering, ordered=True)
    df = df.drop_duplicates(['staffId', 'flightNumber', 'scheduledDepartureDateTime', 'interval', 'passengers'])

