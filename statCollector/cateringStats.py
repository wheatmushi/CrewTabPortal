import os
import pandas as pd
import sys
from math import isnan
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)

departure_airport = 'SVO'
date_start = '2021-01-01'
date_end = '2021-02-15'


def check_missing_catering_sessions(itf, date_start, date_end):
    cat_sessions = itf.get_catering_closed_sessions(departure_airport='', date_start=date_start, date_end=date_end)
    flights_by_range = pd.read_csv('/Volumes/data/code/SITA_PycharmProjects/CrewTabPortal/_DB/catering/afl_routes.csv',
                                   index_col=0)
    flights_by_range['fl_num'] = flights_by_range['fl_num'].apply(lambda s: '0'*(4-len(str(s))) + str(s))
    flights_by_range = flights_by_range.drop_duplicates(['dep_airport', 'arr_airport'])
    flights = itf.get_flights_table(start_date=date_start, end_date=date_end, filter_status='SCHEDULED')
    flights = flights.merge(flights_by_range, left_on=['departureAirport', 'arrivalAirport'],
                            right_on=['dep_airport', 'arr_airport'], how='left')
    flights = flights.merge(cat_sessions, how='left',
                            left_on=['flightNumber', 'departureDateStart', 'departureAirport'],
                            right_on=['flightNumber', 'earliestLocalDepartureDate', 'departureAirport'])
    flights = flights[['flightNumber', 'departureAirport', 'departureDateStart', 'flightStatusLabel', 'paxInfoAvailable',
                       'menu', 'amountOfCrewOperated', 'amountOfOrders', 'amountOfOrdersServed']]
    flights['catering_done'] = flights['amountOfOrders'].apply(lambda s: False if isnan(s) else True)

    stats = pd.DataFrame(flights.groupby('catering_done').size(), columns=['amount'])
    stats['catering done, %'] = stats['amount'] / stats['amount'].sum() * 100
    stats = stats.round(0).astype('int')
    return stats


url = 'https://admin-su.crewplatform.aero/'
itf = CrewInterface(url)
stats = check_missing_catering_sessions(itf, date_start, date_end)
