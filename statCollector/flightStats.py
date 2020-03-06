# build stats for past and upcoming flights and check if some flights missing

import sys
import os
from datetime import datetime, timedelta
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from crew_utils import date_iterator
from CrewInterface import CrewInterface
import visualization as viz

start_date_ = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
start_date = datetime.now() + timedelta(days=2)
num_of_days = 35
dates_range = list(date_iterator(start_date_, -num_of_days))
path_to_DB = os.path.join('..', '_DB', 'flights', 'flights_DB.csv')
url_main = 'https://admin-su.crewplatform.aero/'
filter_numbers = True

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)


def get_flights_table(interface):  # NEED TO REPLACE for WITH RANGE OF DATES
    df = interface.get_flights_table(start_date_, -3)
    if os.path.exists(path_to_DB):
        df_local = pd.read_csv(path_to_DB, index_col=0, parse_dates='departureDate')
        df = pd.concat([df, df_local], axis=0, sort=False)

    dates_in_df = set([d.strftime('%Y-%m-%d') for d in list(set(df['departureDate']))])
    dfs_to_add = []
    for date in set(dates_range).difference(dates_in_df):
        dfs_to_add.append(interface.get_flights_table(date, 1))
    df = pd.concat([df] + dfs_to_add, axis=0, sort=False)
    df = df.drop_duplicates()
    df['dayOfWeek'] = df['departureDate'].dt.dayofweek
    df['flightNumber'] = df['flightNumber'].astype('int')
    if filter_numbers:
        df = df[df['flightNumber'] < 3000]
    return df


def build_stats(df, days=7):
    stats = pd.DataFrame(df.groupby('departureDate').size(), columns=['flightsCount'])
    stats['dayOfWeek'] = stats.index.dayofweek
    stats.iloc[-1, 0] = stats.iloc[-1, 0] + len(df[(df['departureDate'] == pd.Timestamp(datetime.now().date())) &
                                                   (df['flightStatusLabel'] == 'SCHEDULED')])  # just prediction for next day
    stats.index = stats.index.strftime('%m-%d')

    # count mean flights amount for every weekday for df range and count difference actual vs mean
    mean_for_month = {}
    ref_df = stats.iloc[:-3, :]
    for i in range(7):
        mean_for_month[i] = int(round(ref_df[ref_df['dayOfWeek'] == i]['flightsCount'].mean()))
    stats['meanForMonth'] = stats['dayOfWeek'].map(mean_for_month)
    stats['vsMonth'] = stats['flightsCount'] - stats['meanForMonth']

    # compare stats for current week vs previous one
    #stats['vsWeek'] = 0
    stats['vsWeek +'] = 0
    stats['vsWeek -'] = 0
    #stats = stats.iloc[-7 * int(stats.shape[0]/7):, :]
    '''
    for i in range(int(stats.shape[0] / 7) - 1):
        stats.iloc[7 * (i + 1): 7 * (i + 2), 4] = stats['flightsCount'][7 * (i + 1): 7 * (i + 2)].values -\
                                                  stats['flightsCount'][7 * i: 7 * (i + 1)].value
    '''
    for day in range(stats.shape[0]-7):
        df_excess, df_missing = find_missing(df, day)
        stats.iloc[day+7, 4] = df_excess.shape[0]
        stats.iloc[day+7, 5] = df_missing.shape[0]
    return stats


def find_missing(df, day):
    t_ref = df['departureDate'].min() + timedelta(days=day)
    t = t_ref + timedelta(days=7)

    df_new = df[(df['departureDate'].between(t, t))]
    df_ref = df[df['departureDate'].between(t_ref, t_ref)]

    df_excess = df_new[~df_new['flightNumber'].isin(df_ref['flightNumber'])]
    df_missing = df_ref[~df_ref['flightNumber'].isin(df_new['flightNumber'])]
    if t == df['departureDate'].max():
        scheduled = df[(df['departureDate'] == pd.Timestamp(datetime.now().date())) &
                       (df['flightStatusLabel'] == 'SCHEDULED')]['flightNumber']
        df_missing = df_missing[~df_missing['flightNumber'].isin(scheduled)]
    return df_excess, df_missing

'''
ref = df_ref['flightNumber']
new = df_new['flightNumber']
ref = set(ref.values)
new = set(new.values)
new.difference(ref)
'''




interface = CrewInterface(url_main)
df = get_flights_table(interface)
stats = build_stats(df)
viz.bar_graph(stats)




