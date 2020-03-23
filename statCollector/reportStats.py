#  load records for crew reports and build statistic for app usage

import sys
import os
import numpy as np
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))


def build_stats(df_reports, df_flights=None):
    stats = pd.DataFrame(df_reports.groupby([df_reports['lastUpdate'].dt.date,
                                             df_reports['lastUpdate'].dt.dayofweek,
                                             df_reports['lastUpdate'].dt.hour]).size())
    stats_by_departure = pd.DataFrame(df_reports.groupby([df_reports['departureDate'].dt.date]).size())

    stats.columns = ['reportsCount']
    stats.index.names = ['date', 'dayOfWeek', 'hour']
    stats['cumulative24hrs'] = stats.rolling(24).sum()  # cumulative amount for last 24 hours
    stats['cumulativeSince0'] = stats['reportsCount'].groupby('date').cumsum()  # cumulative amount since 0:00 UTC
    stats = stats.reset_index((1, 2))
    # stats = stats.iloc[:-1, :]  # remove current hour with incomplete stats
    stats['byDepartureDate'] = stats_by_departure[0]

    # count mean flights amount for every hour for df range and count difference actual vs mean
    mean_for_month = int(stats.iloc[24:-24, 3].mean())
    stats['vsMonth'] = stats['cumulative24hrs'] - mean_for_month

    # compare today and yesterday stats
    stats['vsYesterday'] = np.append(np.zeros(24),
                                     stats['cumulative24hrs'][24:].values - stats['cumulative24hrs'][:-24].values)
    stats['vsMonth %'] = stats['vsMonth'] / mean_for_month * 100
    stats['vsYesterday %'] = np.append(np.zeros(24),
                                       stats['vsYesterday'][24:].values / stats['cumulative24hrs'][:-24].values * 100)
    stats = stats.round(pd.Series([1, 1], index=['vsMonth %', 'vsYesterday %']))
    if not df_flights.empty:
        dates = list(set(df_reports['departureDate']))
        flights_vs_reports = {}
        df_reports['flightNumber'] = df_reports['flightNumber'].astype('int')
        for d in dates:
            reports_for_d = df_reports[df_reports['departureDate'] == d]['flightNumber']
            flights_for_d = df_flights[(df_flights['departureDate'] == d) &
                                       (df_flights['flightStatusLabel'] != 'CANCELED')]['flightNumber']
            flights_vs_reports[d] = len(set(flights_for_d.values).difference(reports_for_d.values))
        stats['vsFlights'] = -stats.index.to_series().map(flights_vs_reports)

    stats.index = [i.strftime('%m-%d') for i in stats.index.values]
    stats[['reportsCount', 'vsMonth', 'vsYesterday', 'byDepartureDate']] =\
        stats[['reportsCount', 'vsMonth', 'vsYesterday', 'byDepartureDate']].fillna(0)
    stats[['reportsCount', 'vsMonth', 'vsYesterday', 'byDepartureDate']] =\
        stats[['reportsCount', 'vsMonth', 'vsYesterday', 'byDepartureDate']].astype('int')
    return stats
