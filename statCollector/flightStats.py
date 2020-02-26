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


def get_flights_table(interface):  # NEED TO REPLACE for WITH RANGE OF DATES
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
    stats = pd.DataFrame(df.groupby('departureDate').size(), columns=['flightsCount'])
    stats['dayOfWeek'] = stats.index.dayofweek
    stats.iloc[-1, 0] = stats.iloc[-1, 0] + len(df[(df['departureDate'] == pd.Timestamp(datetime.datetime.now().date())) &
                                                   (df['flightStatusLabel'] == 'SCHEDULED')])  # just prediction for next day
    stats.index = stats.index.strftime('%m-%d')

    # count mean flights amount for every weekday for df range and count difference actual vs mean
    mean_for_month = {}
    ref_df = stats.iloc[:-3, :]
    for i in range(7):
        mean_for_month[i] = round(ref_df[ref_df['dayOfWeek'] == i]['flightsCount'].mean())
    stats['meanForMonth'] = stats['dayOfWeek'].map(mean_for_month)
    stats['vsMonth'] = stats['flightsCount'] - stats['meanForMonth']

    # compare stats for current week vs previous one
    stats['vsWeek'] = 0
    stats = stats.iloc[-7 * int(stats.shape[0]/7):, :]
    for i in range(int(stats.shape[0] / 7) - 1):
        stats.iloc[7 * (i + 1): 7 * (i + 2), 4] = stats['flightsCount'][7 * (i + 1): 7 * (i + 2)].values -\
                                                  stats['flightsCount'][7 * i: 7 * (i + 1)].values
    return stats


def graph(stats, days):
    x = stats.index[-days:]
    y1 = stats['flightsCount'][-days:]
    y2 = stats['vsWeek'][-days:]
    y3 = stats['vsMonth'][-days:]

    color_main = '#6c9bff'
    color_inc = '#98ff88'
    color_exc = '#ff6752'
    colors2 = [color_exc if i < 0 else color_inc for i in y2]
    colors3 = [color_exc if i < 0 else color_inc for i in y3]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10))
    ax2.axhline(0, color='black', linewidth=0.5)
    ax3.axhline(0, color='black', linewidth=0.5)

    rects1 = ax1.bar(x, y1, color=color_main)
    rects2 = ax2.bar(x, y2, color=colors2)
    rects3 = ax3.bar(x, y3, color=colors3)

    def autolabel(axis, rects, diff=()):
        sign = lambda a: -1 if a < 0 else 1
        for i, rect in enumerate(rects):
            height = rect.get_height()
            if len(diff) and diff[i] != 0:
                axis.annotate('{}{}'.format(height, diff[i]),
                              xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, sign(height) * 10),
                              textcoords="offset points", ha='center', va='center')
            else:
                axis.annotate('{}'.format(height), xy=(rect.get_x() + rect.get_width() / 2, height),
                              xytext=(0, sign(height) * 10), textcoords="offset points",
                              ha='center', va='center')
    autolabel(ax1, rects1, y2)
    autolabel(ax2, rects2)
    autolabel(ax3, rects3)
    ax1.margins(y=0.13)
    ax2.margins(y=0.13)
    ax3.margins(y=0.13)
    plt.subplots_adjust(hspace=0.5)


interface = CrewInterface(url_main)
df = get_flights_table(interface)
stats = build_stats(df)

days = 7

stats = stats.iloc[-days:, :]
stats.iloc[-1,0] = stats.iloc[-1,0] - 130
stats.iloc[-1,3] = stats.iloc[-1,3] - 130
stats.iloc[-4,0] = stats.iloc[-4,0] + 58
stats.iloc[-4,3] = stats.iloc[-4,3] + 58



