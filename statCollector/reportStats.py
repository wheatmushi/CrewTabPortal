#  load records for crew reports and build statistic for app usage

import sys
import os
import numpy as np
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface
from datetime import datetime, timedelta


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)

start_date = datetime.now()
num_of_days = 35
params = {"form_id": '51',
          "staff_id": '',
          "flight_number": '',
          "dep_airport": '',
          "arr_airport": '',
          "reg_number": ''}

url_main = 'https://admin-su.crewplatform.aero/'


interface = CrewInterface(url_main)
reports = interface.get_reports_table(start_date, -num_of_days, params)
reports['lastUpdate'] = reports['lastUpdate'] + timedelta(minutes=180)
reports['hour'] = reports['lastUpdate'].dt.hour
reports['dayOfWeek'] = reports['lastUpdate'].dt.dayofweek
reports['postingDate'] = reports['lastUpdate'].dt.date

grp = reports.groupby([reports['lastUpdate'].dt.day, reports['lastUpdate'].dt.hour]).size()
grp.to_csv('reports_by_hour_{}.csv'.format(start_date))


def build_stats(df):
    stats = pd.DataFrame(df.groupby([df['lastUpdate'].dt.date,
                                     df['lastUpdate'].dt.dayofweek,
                                     df['lastUpdate'].dt.hour]).size())
    stats.columns = ['reportsCount']
    stats.index.names = ['date', 'dayOfWeek', 'hour']
    #stats = stats.groupby('date').cumsum()
    stats = stats.rolling(24).sum()  # cumulative amount for last 24 hours
    stats = stats.reset_index((1, 2))
    stats = stats.iloc[:-1, :]  # remove last hour with incomplete stats

    # count mean flights amount for every hour for df range and count difference actual vs mean
    mean_for_month = int(stats.iloc[24:-24, 2].mean())
    stats['vsMonth'] = stats['reportsCount'] - mean_for_month

    # compare today and yesterday stats
    stats['vsYesterday'] = np.append(np.zeros(24),
                                     stats['reportsCount'][24:].values - stats['reportsCount'][:-24].values)
    stats['vsMonth %'] = stats['vsMonth'] / mean_for_month * 100
    stats['vsYesterday %'] = np.append(np.zeros(24),
                                       stats['vsYesterday'][24:].values / stats['reportsCount'][:-24].values * 100)
    stats = stats.round(pd.Series([0, 1], index=['vsMonth %', 'vsYesterday %']))

    # table for last week
    df_daily = pd.DataFrame()
    last_days = sorted(sorted(list(set(stats.index.values)), reverse=True)[:7])
    for d in last_days[:-1]:
        df_daily[d] = stats.loc[d, 'reportsCount'].values
    last_day_values = stats.loc[last_days[-1], 'reportsCount'].values
    df_daily[last_days[-1]] = np.append(last_day_values, np.zeros(24 - len(last_day_values)))
    return stats, df_daily

