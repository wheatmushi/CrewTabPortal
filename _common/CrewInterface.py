# interface for CrewTab portal access: flights, syncs, reports, users
import json
from bs4 import BeautifulSoup
from datetime import datetime
from time import time
import pandas as pd
import URLs
import auth
import crew_utils


class CrewInterface:
    def __init__(self, url_main):
        self.url_main = url_main
        self.session = auth.SessionCrewTabPortal(url_main)
        self.session.authentication()

    def get_flight_info(self, flight_id, all_info=False):
        # get flight information about times of dep/arr and booked/checked in/boarded passengers
        # if not all_info then returns only scheduled departure/arrival times
        r = self.session.get(URLs.URL_flights_base_data.format(flight_id=flight_id))
        soup = BeautifulSoup(r.content, 'html.parser')
        tables = soup.find_all('table')
        base_head = [cell.text for cell in tables[0].find_all('th')]
        base_content = [cell.text.replace('\n', '').strip() for cell in tables[0].find_all('td')]
        base_info = {base_head[i]: base_content[i] for i in range(len(base_head))}
        base_info['Flight Number'] = base_info['Flight Number'].replace('SU', '')
        for i in ['Scheduled Departure', 'Estimated Departure', 'Scheduled Arrival']:
            base_info[i] = datetime.strptime(base_info[i], '%d/%b/%Y %H:%M:%S %Z')
        base_info['Duration'] = int(
            (base_info['Scheduled Arrival'] - base_info['Scheduled Departure']).total_seconds() // 60)
        pass_head = [cell.text for cell in tables[1].find_all('th')][1:]
        pass_content = [cell.text.replace('\n', '').strip() for cell in tables[1].find_all('td')]
        pass_info = {pass_head[i]: {pass_content[j * 4]: pass_content[j * 4 + i + 1] for j in range(3)} for i in
                     range(3)}
        if all_info:
            return base_info, pass_info
        else:
            return base_info['Scheduled Departure'], base_info['Scheduled Arrival']

    def get_flights_table(self, dates_range, flight_numbers=None, length=1100, id_only=False):
        # get flight table for range of dates OR one flight DB ID
        print('parsing flight table...')
        flights = []
        if type(dates_range) is str:
            dates_range = (dates_range,)
        if flight_numbers and type(flight_numbers) is str:
            flight_numbers = (flight_numbers,)
        for d in dates_range:
            f = self.session.get(URLs.URL_flights_list.format(flight_number='', departure_date=d, length=length))
            f = json.loads(f.content)['data']
            flights.append(pd.DataFrame(data=f))
        flights = pd.concat(flights, axis=0, sort=False)
        flights = crew_utils.dtrowid_to_index(flights)
        flights = flights.drop('details', axis=1)
        if flight_numbers:
            flights = flights[flights['flightNumber'].isin(flight_numbers)]
        if flights.empty:
            print('no flights found!!')
        if id_only:
            return flights.index[0]
        return flights

    def get_portal_users(self, is_enabled=False, search_value=''):  # get all CrewTab users (or enabled only)
        print('parsing full crew list...')
        is_enabled = '1' if is_enabled else '0'
        r = self.session.get(URLs.URL_users_list.format(length=10, search_value='', is_enabled=False))
        total = json.loads(r.content)['recordsTotal']
        r = self.session.get(URLs.URL_users_list.format(length=total, search_value=search_value, is_enabled=is_enabled))
        full_table = json.loads(r.content)['data']
        full_table = pd.DataFrame(data=full_table)
        full_table = crew_utils.dtrowid_to_index(full_table)
        full_table['enabled'] = full_table['enabled'].map(lambda s: BeautifulSoup(s, 'html.parser').text)
        full_table = full_table.drop(['image', 'display', 'delete'], axis=1)
        return full_table

    def get_flight_crews(self, flight_id, log=True):  # get crews for particular flight by flight DB ID
        if log:
            print('parsing data for flight ID', flight_id)
        r = self.session.get(URLs.URL_flight_crews.format(flight_id=flight_id, length=30))
        r = json.loads(r.content)['data']
        crews = pd.DataFrame(data=r)
        return crews

    def close(self):
        self.session.close()

    def get_syncs(self, departure_dates=('',), staff_id='', flight_number='', departure_airports=('',), length=20000):
        # load user's synchronizations from server
        t = time()
        syncs = []
        if flight_number:
            flight_number = '0'*(4-len(flight_number)) + flight_number
        for date in departure_dates:
            for airport in departure_airports:
                print('parsing flight status syncs for {}...'.format(date))
                r = self.session.get(URLs.URL_monitor_syncs.format(departure_date=date, flight_number=flight_number,
                                                                   departure_airport=airport, staff_id=staff_id,
                                                                   length=length))
                r = json.loads(r.content)['data']
                syncs.append(pd.DataFrame(data=r))
        syncs = pd.concat(syncs, axis=0, sort=False)
        syncs = crew_utils.dtrowid_to_index(syncs)
        syncs['lastUpdate'] = syncs['lastUpdate'].astype('datetime64')
        syncs['scheduledDepartureDateTime'] = syncs['scheduledDepartureDateTime'].astype('datetime64')
        syncs['synchronizationDate'] = syncs['synchronizationDate'].astype('datetime64')
        print('syncs parsing time {} seconds'.format(round(time() - t)))
        return syncs

    def get_reports_table(self, url_params):
        # load crew reports records, all parameters in url_params dict (start/end dates, form id, staff id, flight num,
        # tail number, dep/arr airport, length of list
        if 'admin-fv' in self.url_main:
            url = URLs.URL_monitor_reports_FV
        if 'admin-su' in self.url_main:
            url = URLs.URL_monitor_reports_SU
        url = url.format(**url_params)
        reports = self.session.get(url)
        reports = pd.DataFrame(data=json.loads(reports.content)['data'])
        #reports = reports.drop(['DT_RowId', 'checkbox', 'download', 'tag'], axis=1, errors='ignore')
        #reports['id'] = reports['id'].map(lambda x: x.replace(',', '')).astype('int')
        #reports = reports.set_index('id')
        reports['lastUpdate'] = reports['lastUpdate'].astype('datetime64')
        return reports
