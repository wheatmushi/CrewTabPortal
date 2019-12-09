#  build two separate statistic table for SUcrew synchs
#  for all airports and all staffIDs with collecting data over range of days

import auth
import os
from datetime import datetime, timedelta
import json
from time import sleep, time

start_time = time()
#os.environ['url_main'] = 'https://admin-su.crewplatform.aero/'
#url_main = os.environ.get('url_main')
start_date = '2019-11-24'
num_of_days = 4
is_cm = True  # enable only if different stats for CM and FA required,
# this will slow script with +2 http-request per flight in fl_list

url_fl_list = 'core/flights/filter/ajax?draw=1&columns%5B0%5D%5Bdata%5D=flightNumber&columns%5B0%5D%5Bname%5D=flightNumber&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=departureAirport&columns%5B1%5D%5Bname%5D=departureAirport&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=departureDate&columns%5B2%5D%5Bname%5D=departureDate&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D={departure_date}&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=flightStatusLabel&columns%5B3%5D%5Bname%5D=flightStatusLabel&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=arrivalAirport&columns%5B4%5D%5Bname%5D=arrivalAirport&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=details&columns%5B5%5D%5Bname%5D=details&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=2&order%5B0%5D%5Bdir%5D=desc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1568705987759'
url_fl_crw = 'core/flights/{flight_id}/crew/ajax?draw=1&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=name&columns%5B1%5D%5Bname%5D=name&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=position&columns%5B2%5D%5Bname%5D=position&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=email&columns%5B3%5D%5Bname%5D=email&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1568721552781'


def date_iter(start_date, num_of_days):  # iterate over days end generate new str with date
    for i in range(0,num_of_days):
        cur_date = datetime.strptime(start_date, '%Y-%m-%d')
        date = '{:%Y-%m-%d}'.format(cur_date + timedelta(days=i))
        yield date


def time_converter(d):  # convert str_dates to datetime obj for synch json-s
    str_time_to_date = lambda s: datetime.strptime(s[:-4], '%d/%b/%Y %H:%M:%S')
    d['scheduledDepartureDateTime'] = str_time_to_date(d['scheduledDepartureDateTime'])
    d['synchronizationDate'] = str_time_to_date(d['synchronizationDate'])
    d['lastUpdate'] = str_time_to_date(d['lastUpdate'])
    return d


def check_synch_interval(synch_for_fl):  # check intervals for synchronizations
    def is_in_interval(synch_for_fl, t1, t2):
        synch_for_fl = [synch for synch in synch_for_fl if
                        synch['scheduledDepartureDateTime'] - timedelta(minutes=t1) < synch['synchronizationDate'] and
                        synch['synchronizationDate'] < synch['scheduledDepartureDateTime'] + timedelta(minutes=t2)]
        return True if synch_for_fl else False

    if not synch_for_fl:
        return 'no_records'
    elif is_in_interval(synch_for_fl, 9, 120):  # synched in dept-9 < x < dept+30 mins
        return 'full'
    elif is_in_interval(synch_for_fl, 38, -9):  # synched in dept-38 < x < dept-9 mins
        return 'registration'
    elif is_in_interval(synch_for_fl, 4320, -38):  # synched in dept-3days < x < dept-38mins
        return 'base'
    else:
        return 'late_data'


def get_fl_id(session, flight, date):
    print('parsing data for flight ' + flight + '  ' + date)
    url_fl_filtered = url_fl_list.format(flight_number=flight, departure_date=date, length=10)
    r = session.get(url_fl_filtered, timeout=10)
    r = json.loads(r.content)
    if r['data']:
        fl_id = r['data'][0]['DT_RowId'].replace(',', '')
        arr_arpt = r['data'][0]['arrivalAirport'].replace(',', '')
        return fl_id, arr_arpt
    else:
        return None, None


def get_fl_crw(session, fl_id):
    url_crw = url_fl_crw.format(flight_id=fl_id, length=30)
    r = session.get(url_crw, timeout=10)
    r = json.loads(r.content)
    return r['data']


def build_stats(session, fl_list, synch_list_tc, stats_for_airport, stats_for_staffid, date, is_cm):
    for flight in fl_list:
        if is_cm:
            fl_id = get_fl_id(session, flight[0], date)
            crew_list = get_fl_crw(session, fl_id[0])
            crew_list = {crw['staffId']: crw['position'] for crw in crew_list}
        synch_for_fl = [s for s in synch_list_tc if s['flightNumber'] == flight[0]]
        synch_for_fl_for_stf = {}
        for synch in synch_for_fl:
            staffid = synch['staffId']
            if staffid in synch_for_fl_for_stf.keys():
                synch_for_fl_for_stf[staffid] = synch_for_fl_for_stf[staffid] + [synch]
            else:
                synch_for_fl_for_stf[staffid] = [synch]

        for staffid in synch_for_fl_for_stf:
            interval = check_synch_interval(synch_for_fl_for_stf[staffid])
            if not is_cm or staffid not in crew_list.keys():
                break
            stats_overall[interval] = stats_overall[interval] + 1
            airport = flight[1]

            if airport in stats_for_airport.keys():
                stats_for_airport[airport][interval] = stats_for_airport[airport][interval] + 1
            else:
                stats_for_airport[airport] = {'base': 0, 'registration': 0, 'full': 0, 'no_records': 0, 'late_data': 0}
                stats_for_airport[airport][interval] = stats_for_airport[airport][interval] + 1

            if staffid in stats_for_staffid.keys():
                stats_for_staffid[staffid][interval] = stats_for_staffid[staffid][interval] + 1
            else:
                stats_for_staffid[staffid] = {'position': 'none', 'base': 0, 'registration': 0,
                                              'full': 0, 'no_records': 0, 'late_data': 0}
                stats_for_staffid[staffid][interval] = stats_for_staffid[staffid][interval] + 1
                if is_cm:
                    if staffid in crew_list.keys():
                        stats_for_staffid[staffid]['position'] = crew_list[staffid]
    return stats_for_airport, stats_for_staffid


def prcnt(airport_data):  # create percentage for raw numbers
    s = sum(list(airport_data.values()))
    airport_data_p = {key + '_p': round(value/s*100) for (key,value) in airport_data.items()}
    airport_data.update(airport_data_p)
    airport_data['all_flights'] = s
    return airport_data


def airport_table_builder(stats_for_airport):
    filename = 'stats_for_airport_' + start_date + '_plus_' + str(num_of_days) + '_days.csv'
    csv = open(os.path.join('output', filename), 'w')
    head = 'airport;all flights x crews;full data;full data %;registration data;registration data %;' \
           'base data;base data %;no records at all;no records at all %;data received later;data received later%\n'
    line = '{airport};{all_flights};{full};{full_p};{registration};{registration_p};{base};{base_p};' \
           '{no_records};{no_records_p};{late_data};{late_data_p}\n'
    csv.write(head)
    for airport in stats_for_airport.keys():
        csv.write(line.format(airport=airport, **prcnt(stats_for_airport[airport])))
    csv.close()
    return filename


def staffid_table_builder(stats_for_staffid):
    filename = 'stats_for_staffid_' + start_date + '_plus_' + str(num_of_days) + '_days.csv'
    csv = open(os.path.join('output', filename), 'w')
    head = 'staffid;position;all flights;full data;full data %;registration data;registration data %;' \
           'base data;base data %;no records at all;no records at all %;data received later;data received later%\n'
    line = '{staffid};{position};{all_flights};{full};{full_p};{registration};{registration_p};' \
           '{base};{base_p};{no_records};{no_records_p};{late_data};{late_data_p}\n'
    csv.write(head)
    for staffid in stats_for_staffid.keys():
        position = stats_for_staffid[staffid].pop('position')
        csv.write(line.format(staffid=staffid, position=position, **prcnt(stats_for_staffid[staffid])))
    csv.close()
    return filename

url_main = 'https://admin-fv.crewplatform.aero/'
session = auth.SessionCrewTabPortal(url_main)
session.authentication()

stats_overall = {'base': 0, 'registration': 0, 'full': 0, 'no_records': 0, 'late_data': 0}
stats_for_airport = {}  # {'SVO': {'base': 12, 'full': 34}, 'AER': {'base': 3, 'full': 0}}
stats_for_staffid = {}

for date in date_iter(start_date, num_of_days):
    print('loading data for ' + date)
    url_synch_with_date = 'core/monitoring/ajax/flight_status_monitor/search?draw=4&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=flightNumber&columns%5B1%5D%5Bname%5D=flightNumber&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=departureAirport&columns%5B2%5D%5Bname%5D=departureAirport&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=arrivalAirport&columns%5B3%5D%5Bname%5D=arrivalAirport&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=departureDate&columns%5B4%5D%5Bname%5D=departureDate&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D={date}&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=scheduledDepartureDateTime&columns%5B5%5D%5Bname%5D=scheduledDepartureDateTime&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=synchronizationDate&columns%5B6%5D%5Bname%5D=synchronizationDate&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=lastUpdate&columns%5B7%5D%5Bname%5D=lastUpdate&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=deviceId&columns%5B8%5D%5Bname%5D=deviceId&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=bookedCount&columns%5B9%5D%5Bname%5D=bookedCount&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=checkinCount&columns%5B10%5D%5Bname%5D=checkinCount&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=boardedCount&columns%5B11%5D%5Bname%5D=boardedCount&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=7&order%5B0%5D%5Bdir%5D=desc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1574845825249'
    url_synch_with_date = url_synch_with_date.format(date=date)
    url_fl_with_date = 'core/flights/filter/ajax?draw=1&columns%5B0%5D%5Bdata%5D=flightNumber&columns%5B0%5D%5Bname%5D=flightNumber&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=departureAirport&columns%5B1%5D%5Bname%5D=departureAirport&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=departureDate&columns%5B2%5D%5Bname%5D=departureDate&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D={departure_date}&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=flightStatusLabel&columns%5B3%5D%5Bname%5D=flightStatusLabel&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=arrivalAirport&columns%5B4%5D%5Bname%5D=arrivalAirport&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=details&columns%5B5%5D%5Bname%5D=details&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=2&order%5B0%5D%5Bdir%5D=desc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1568705987759'
    url_fl_with_date = url_fl_with_date.format(flight_number='', departure_date=date, length=1000)

    # to load full statistic for all flights (please don't use with is_cm == True flag, you'll regret so)
    fl_list = session.get(url_fl_with_date)
    fl_list = json.loads(fl_list.content)['data']
    fl_list = [(flight['flightNumber'], flight['departureAirport']) for flight in fl_list]

    #fl_list = [('0103', 'JFK'), ('0101', 'JFK'), ('0123', 'JFK')]
    #fl_list = [('0107', 'LAX')]

    synch_list = session.get(url_synch_with_date, timeout=10)
    synch_list = json.loads(synch_list.content)['data']
    synch_list_tc = [time_converter(line) for line in synch_list]

    stats_for_airport, stats_for_staffid = \
        build_stats(session, fl_list, synch_list_tc, stats_for_airport, stats_for_staffid, date, is_cm)

airport_table_path = airport_table_builder(stats_for_airport)
staffid_table_path = staffid_table_builder(stats_for_staffid)
print('\nwork is done, see detailed stats in:\n{}\n{}\n\nstats overall:'.format(airport_table_path, staffid_table_path))
print(stats_overall)
print('running time:', (time()-start_time)/60, 'min')
