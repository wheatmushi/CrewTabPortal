# build stats for past and upcoming flights and check if some flights missing

import sys
import os
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sys.path.insert(1, os.path.join('..', '_common'))
from crew_utils import date_iterator
from CrewInterface import CrewInterface

start_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')
num_of_days = 35
dates_range = list(date_iterator(start_date, -num_of_days))
path_to_DB = os.path.join('..', '_DB', 'flights', 'flights_DB.csv')
url_main = 'https://admin-su.crewplatform.aero/'
filter_numbers = True

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)

interface = CrewInterface(url_main)


def get_flights_table():
    df = interface.get_flights_table(start_date, -3)
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
    def mean_for_weekday(day):
        s = stats.iloc[:-3, :]
        return round(s[s['dayOfWeek'] == day]['flightsCount'].mean())

    stats = pd.DataFrame(df.groupby('departureDate').size(), columns=['flightsCount'])
    stats['dayOfWeek'] = stats.index.dayofweek
    stats.iloc[-1, 0] = stats.iloc[-1, 0] + len(df[(df['departureDate'] == pd.Timestamp(datetime.datetime.now().date())) &
                                                   (df['flightStatusLabel'] == 'SCHEDULED')])  # just prediction for next day
    stats.index = stats.index.strftime('%m-%d')
    stats['meanForWeekDay'] = stats['dayOfWeek'].apply(lambda day: mean_for_weekday(day))
    stats['difference'] = stats['flightsCount'] - stats['meanForWeekDay']

    x = stats.index[-days:]
    f, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    sns.barplot(x=x, y=stats['flightsCount'][-days:], hue=np.zeros(len(stats['flightsCount'][-days:])), palette='Blues', ax=ax1)
    sns.barplot(x=x, y=stats['difference'][-days:], hue=stats['difference'][-days:], palette="RdBu_r", ax=ax2)

