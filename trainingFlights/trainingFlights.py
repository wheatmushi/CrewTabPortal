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
num_of_days = -3

url_main = 'https://admin-su.crewplatform.aero/'
interface = CrewInterface(url_main)

full_crew_table = interface.get_portal_users(is_enabled=True)
flights_table = interface.get_flights_table(start_date, num_of_days, flights)

txt = open('training_flights_' + datetime.strftime(datetime.now(), '%Y_%m_%d') + '.txt', 'w')
for idx, flight in flights_table.iterrows():
    crews = interface.get_flight_crews(idx)
    if not crews.empty:
        crews = crews[crews['staffId'].isin(full_crew_table['staffId'])]  # filter only enabled user for every flight
        txt.write('SU' + flight['flightNumber'] + '  ' + flight['arrivalAirport'] + '  ' + str(flight['departureDate'])
                  + '\n')
        for i, crew in crews.iterrows():
            txt.write(' '*(6-len(crew['staffId'])) + crew['staffId'] + '  ' + crew['name'] + '\n')
    txt.write('\n')

txt.close()
interface.close()
