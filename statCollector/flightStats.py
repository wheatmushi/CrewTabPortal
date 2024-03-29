# build stats for past and upcoming flights and check if some flights missing

import sys
import os
from datetime import datetime, timedelta
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from crew_utils import date_iterator


def get_flights_table(interface, start_date, num_of_days, filter_numbers=None):
    df = interface.get_flights_table(start_date, num_of_days=-3)
    dates_in_df = set([d.strftime('%Y-%m-%d') for d in list(set(df['departureDateStart']))])
    dates_range = list(date_iterator(start_date, num_of_days=-num_of_days))
    dfs_to_add = []
    for date in set(dates_range).difference(dates_in_df):
        dfs_to_add.append(interface.get_flights_table(date, num_of_days=1))
    df = pd.concat([df] + dfs_to_add, axis=0, sort=False)
    df = df.drop_duplicates()
    df['dayOfWeek'] = df['departureDateStart'].dt.dayofweek
    df['departureDateStart'] = df['departureDateStart'].astype('datetime64')
    df['flightNumber'] = df['flightNumber'].astype('int')
    if filter_numbers:
        df = df[df['flightNumber'] < filter_numbers]
    return df


def build_stats(df):  # build stats for flights compared to month mean and last week amount, return stats DF and
    # df_to_check with excess and missing flights
    df = df[df['flightStatusLabel'] != 'CANCELED']
    stats = pd.DataFrame(df.groupby('departureDateStart').size(), columns=['flightsCount'])
    stats['dayOfWeek'] = stats.index.dayofweek

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
        df_excess['departureDateStart'] = df_excess['departureDateStart'].dt.date
        df_missing['departureDateStart'] = df_missing['departureDateStart'].dt.date
        df_to_check = pd.concat([df_to_check, df_excess, df_missing], axis=0)
    stats['date'] = stats.index.strftime('%m-%d')
    return stats, df_to_check


def update_flights(interface, old_flights, filter_numbers=None):
    start_date = datetime.now() + timedelta(days=2)
    num_of_days = 3
    new_flights = get_flights_table(interface, start_date, num_of_days, filter_numbers=filter_numbers)
    old_flights['departureDateStart'] = old_flights['departureDateStart'].astype('datetime64')
    df_flights = pd.concat([old_flights, new_flights], axis=0, sort=False)
    dates = df_flights['departureDateStart'].drop_duplicates()
    dates = dates.sort_values(ascending=False)[:38]
    df_flights = df_flights[df_flights['departureDateStart'].isin(dates)]
    df_flights = df_flights.drop_duplicates(['flightNumber', 'departureDateStart', 'departureAirport'], keep='last')
    return df_flights


def find_missing(df, day):  # find excess and missing flights for given day and return 2 dataframes
    t_ref = df['departureDateStart'].min() + timedelta(days=day)
    t = t_ref + timedelta(days=7)

    df_new = df[(df['departureDateStart'].between(t, t))]
    df_ref = df[df['departureDateStart'].between(t_ref, t_ref)]

    df_excess = df_new[~df_new['flightNumber'].isin(df_ref['flightNumber'])]
    df_missing = df_ref[~df_ref['flightNumber'].isin(df_new['flightNumber'])]
    if t == df['departureDateStart'].max():
        scheduled = df[(df['departureDateStart'] == pd.Timestamp(datetime.now().date())) &
                       (df['flightStatusLabel'] == 'SCHEDULED')]['flightNumber']
        df_missing = df_missing[~df_missing['flightNumber'].isin(scheduled)]
    df_missing['status'] = 'missing'
    df_excess['status'] = 'excess'
    df_missing['departureDate'] = t
    return df_excess, df_missing


def print_missing(df_to_check, days, to_csv=False):  # write missing/excess flights to .csv and print flights for last few days
    df_to_check = df_to_check.sort_values('departureDateStart', ascending=False)
    if to_csv:
        df_to_check.to_csv('missing_flights_{}.csv'.format(df_to_check['departureDateStart'].max().strftime('%Y-%m-%d')))
    days = sorted(list(set(df_to_check['departureDateStart'].values)), reverse=True)[:days]
    for i in days:
        print(i.astype('datetime64[D]'))
        df_excess = df_to_check[(df_to_check['status'] == 'excess') & (df_to_check['departureDateStart'] == i)]
        df_missing = df_to_check[(df_to_check['status'] == 'missing') & (df_to_check['departureDateStart'] == i)]
        print('Excess flights:', list(df_excess['flightNumber'].values))
        print('Missing flights:', list(df_missing['flightNumber'].values), '\n')
