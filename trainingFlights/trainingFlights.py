#  load enabled staff ids for catering training flights
#  flights to load staff in list 'flights', dates in 'dates'

import os
import sys
from datetime import datetime, timedelta
sys.path.insert(1, os.path.join('..', '_common'))
import auth
import URLs
from CrewInterface import CrewInterface


flights = ['0100', '0102', '0110', '0106', '0200', '0204', '0260', '0208', '0290', '0292']
start_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
num_of_days = -1
check_passengers = True  # if True +1 http-request and http-page processing, will slow down script

url_main = 'https://admin-su-qa.crewplatform.aero/'
interface = CrewInterface(url_main)

full_crew_table = interface.get_portal_users(is_enabled=True)
flights_table = interface.get_flights_table(start_date, num_of_days)

txt = open('training_flights_' + datetime.strftime(datetime.now(), '%Y_%m_%d') + '.txt', 'w')
for idx, flight in flights_table.iterrows():
    if check_passengers:
        info, passengers = interface.get_flight_info(idx, all_info=True)
        if sum([int(i) for i in passengers['Boarded'].values()]) == 0:
            continue
    crews = interface.get_flight_crews(idx)
    if not crews.empty:
        crews = crews[crews['staffId'].isin(full_crew_table['staffId'])]  # filter only enabled user for every flight
        txt.write('SU' + str(flight['flightNumber']) + '  ' + flight['departureAirport'] + '  '
                  + flight['arrivalAirport'] + '  ' + str(flight['departureDate']) + '\n')
        for i, crew in crews.iterrows():
            txt.write(' '*(6-len(crew['staffId'])) + str(crew['staffId']) + '  ' +
                      crew['position'] + '  ' + crew['name'] + '\n')
    txt.write('\n')

txt.close()
interface.close()


