import os
import pandas as pd
from datetime import datetime
from time import time
sys.path.insert(1, os.path.join('..', '_common'))
import crew_utils
from CrewInterface import CrewInterface

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)


def check_sync_intervals(row, max_delay):  # filter user syncs by DCS timings for boarded/checkin
    if row['diff'] < -120:
        return 'late_data'
    elif -max_delay < row['diff'] < 9:
        return 'boarded'
    elif 9 < row['diff'] < 38:
        return 'check in'
    elif 38 < row['diff']:
        return 'booked'


def get_crew_list(interface, start_date, end_date, departure_airport, filter_scheduled=True):  # return full crew roster
    # for all flights for given airport/dates
    t = time()
    df_flights = interface.get_flights_table(start_date=start_date, end_date=end_date,
                                             departure_airport=departure_airport)
    if filter_scheduled:
        if set(df_flights['flightStatusLabel'].values) == {'SCHEDULED'}:
            print('only scheduled flights found for {}'.format(departure_airport))
        else:
            df_flights = df_flights[df_flights['flightStatusLabel'] != 'SCHEDULED']
    full_crew_list = []
    for flight_id in df_flights.index.values:
        crew = interface.get_flight_crews(flight_id, log=False)
        crew['flightNumber'] = df_flights.loc[flight_id]['flightNumber']
        crew['departureDate'] = df_flights.loc[flight_id]['departureDateStart']
        full_crew_list.append(crew)
    full_crew_list = pd.concat(full_crew_list, axis=0, sort=False)
    full_crew_list = full_crew_list.drop(['email', 'DT_RowId'], axis=1)
    print('{} crews parsing time {} seconds'.format(departure_airport, round(time() - t)))
    return full_crew_list


def get_sync_table(interface, departure_airport, start_date, end_date, max_delay):
    # return table with syncs/crew for one airport
    df_syncs = interface.get_syncs(departure_dates=crew_utils.date_iterator(start_date, end_date=end_date),
                                   departure_airports=(departure_airport,))
    df_syncs['diff'] = (df_syncs['scheduledDepartureDateTime'] - df_syncs['synchronizationDate']).astype('timedelta64[m]')
    df_syncs['interval'] = df_syncs.apply(lambda row: check_sync_intervals(row, max_delay), axis=1)
    df_crews = get_crew_list(itf, start_date, end_date, departure_airport)
    df = df_syncs.merge(df_crews, left_on=['staffId','flightNumber', 'departureDate'],
                        right_on=['staffId', 'flightNumber', 'departureDate'])

    interval_ranged = pd.api.types.CategoricalDtype(categories=['boarded', 'check in', 'booked', 'late_data'], ordered=True)
    df['interval'] = df['interval'].astype(interval_ranged)
    df['boardedCount'] = df['boardedCount'].astype('int')
    df = df.sort_values(['interval', 'boardedCount'], ascending=[True, False])
    return df.drop_duplicates(['staffId', 'flightNumber', 'departureDate'])


air1 = ['JFK']  # airport list for 1st set of parameters
air2 = ['LED']  # airport list for 2nd set of parameters
sd1 = '2021-02-01'  # start date for stat gathering 1st set
sd2 = '2021-02-01'  # start date for stat gathering 2nd set
ed1 = '2021-02-03'  # end date for stat gathering 1st set
ed2 = '2021-02-03'  # end date for stat gathering 2nd set
delay1 = 180  # max minutes for departure delay, must be less then flight duration, 1st set
delay2 = 60   # max minutes for departure delay, must be less then flight duration, 2nd set

url = 'https://admin-su.crewplatform.aero/'
itf = CrewInterface(url)

table = []
iterator = crew_utils.packer(4, air1, sd1, ed1, delay1, air2, sd2, ed2, delay2)

for param_list in iterator:
    for airport, start_date, end_date, delay in param_list:
        t = get_sync_table(itf, airport, start_date, end_date, delay)
        table.append(t)
df = pd.concat(table, axis=0, sort=False)
df.to_csv('sync_history_{}.csv'.format(datetime.now().strftime('%Y%m%d_%H%M')), index=False)

stats = df.groupby(['departureAirport', 'interval', 'position']).size()
stats = stats.reindex(pd.MultiIndex.from_product([stats.index.levels[0],
                                                  ['boarded', 'booked', 'check in', 'late data'], ['CM', 'FA']],
                                                 names=['airport', 'interval', 'position']), fill_value=0)

stats.name = 'count'
stats = stats.reset_index()
stats = pd.pivot_table(data=stats, values='count', index='airport', columns=['position', 'interval'])

stats_cm = stats[['CM']]
stats_fa = stats[['FA']]
stats_cm_p = stats_cm.copy(deep=True)
stats_fa_p = stats_fa.copy(deep=True)

stats_cm_p = stats_cm_p.apply(lambda r: r/r.sum(), axis=1)*100
stats_fa_p = stats_fa_p.apply(lambda r: r/r.sum(), axis=1)*100
stats_cm_p.columns.set_levels(['boarded, %', 'booked, %', 'check in, %', 'late data, %'], level=1, inplace=True)
stats_fa_p.columns.set_levels(['boarded, %', 'booked, %', 'check in, %', 'late data, %'], level=1, inplace=True)

stats_cm.loc['total/mean'] = stats_cm.apply(pd.np.sum)
stats_fa.loc['total/mean'] = stats_fa.apply(pd.np.sum)
stats_cm_p.loc['total/mean'] = stats_cm_p.apply(pd.np.mean)
stats_fa_p.loc['total/mean'] = stats_fa_p.apply(pd.np.mean)

stats = pd.concat([stats_cm, stats_cm_p, stats_fa, stats_fa_p], axis=1)
stats = stats.round(0).astype('int')
stats.to_csv('sync_stats_{}.csv'.format(datetime.now().strftime('%Y%m%d_%H%M')))
