# build stats for past and upcoming flights and check if some flights missing

import sys
import os
from datetime import datetime, timedelta
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from crew_utils import date_iterator


def get_flights_table(interface, start_date, num_of_days, path_to_DB, filter_numbers):  # NEED TO REPLACE for WITH RANGE OF DATES
    df = interface.get_flights_table(start_date, -3)
    if os.path.exists(path_to_DB):
        df_local = pd.read_csv(path_to_DB, index_col=0, parse_dates='departureDate')
        df = pd.concat([df, df_local], axis=0, sort=False)

    dates_in_df = set([d.strftime('%Y-%m-%d') for d in list(set(df['departureDate']))])
    dates_range = list(date_iterator(start_date, -num_of_days))
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


def build_stats(df):  # build stats for flights compared to month mean and last week amount, return stats DF and
    # df_to_check with excess and missing flights
    df = df[df['flightStatusLabel'] != 'CANCELED']
    stats = pd.DataFrame(df.groupby('departureDate').size(), columns=['flightsCount'])
    stats['dayOfWeek'] = stats.index.dayofweek
    stats.iloc[-1, 0] = stats.iloc[-1, 0] + len(df[(df['departureDate'] == pd.Timestamp(datetime.now().date())) &
                                                   (df['flightStatusLabel'] == 'SCHEDULED')]) - 20  # just prediction for next day

    # count mean flights amount for every weekday for df range and count difference actual vs mean
    mean_for_month = {}
    ref_df = stats.iloc[:-3, :]
    for i in range(7):
        mean_for_month[i] = int(round(ref_df[ref_df['dayOfWeek'] == i]['flightsCount'].mean()))
    stats['meanForMonth'] = stats['dayOfWeek'].map(mean_for_month)
    stats['vsMonth'] = stats['flightsCount'] - stats['meanForMonth']

    # compare stats for current week vs previous one
    stats['vsWeek +'] = 0
    stats['vsWeek -'] = 0
    df_to_check = pd.DataFrame()
    for day in range(stats.shape[0]-7):
        df_excess, df_missing = find_missing(df, day)
        stats.iloc[day+7, 4] = df_excess.shape[0]
        stats.iloc[day+7, 5] = -df_missing.shape[0]
        df_to_check = pd.concat([df_to_check, df_excess, df_missing], axis=0)
    stats.index = stats.index.strftime('%m-%d')
    return stats, df_to_check


def find_missing(df, day):  # find excess and missing flights for given day and return 2 dataframes
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
    df_missing['status'] = 'missing'
    df_excess['status'] = 'excess'
    df_missing['departureDate'] = t
    return df_excess, df_missing


def print_missing(df_to_check, days, to_csv=False):  # write missing/excess flights to .csv and print flights for last few days
    df_to_check = df_to_check.sort_values('departureDate', ascending=False)
    if to_csv:
        df_to_check.to_csv('missing_flights_{}.csv'.format(df_to_check['departureDate'].max().strftime('%Y-%m-%d')))
    days = sorted(list(set(df_to_check['departureDate'].values)), reverse=True)[:days]
    for i in days:
        print(i.astype('datetime64[D]'))
        df_excess = df_to_check[(df_to_check['status'] == 'excess') & (df_to_check['departureDate'] == i)]
        df_missing = df_to_check[(df_to_check['status'] == 'missing') & (df_to_check['departureDate'] == i)]
        print('Excess flights:', list(df_excess['flightNumber'].values))
        print('Missing flights:', list(df_missing['flightNumber'].values), '\n')
