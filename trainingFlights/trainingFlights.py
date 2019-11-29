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
dates = [datetime.strftime(datetime.now() + timedelta(days=d), '%Y-%m-%d') for d in range(-3, 0)]

url_main = 'https://admin-su.crewplatform.aero/'
itf = CrewInterface(url_main)

full_crew_table = itf.get_portal_users(is_enabled=True)
flights_table = itf.get_flights_table(dates, flights)

txt = open('training_flights_' + datetime.strftime(datetime.now(), '%Y_%m_%d') + '.txt', 'w')
for idx, flight in flights_table.iterrows():
    crews = itf.get_flight_crews(idx)
    if not crews.empty:
        crews = crews[crews['staffId'].isin(full_crew_table['staffId'])]  # filter only enabled user for every flight
        txt.write('SU' + flight['flightNumber'] + '  ' + flight['arrivalAirport'] + '  ' + flight['departureDate'] + '\n')
        for i, crew in crews.iterrows():
            txt.write(' '*(6-len(crew['staffId'])) + crew['staffId'] + '  ' + crew['name'] + '\n')
    txt.write('\n')

txt.close()
itf.close()
