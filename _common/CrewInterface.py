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
    def __init__(self, url_main, login=None, password=None):
        self.url_main = url_main
        self.session = auth.SessionCrewTabPortal(url_main)
        self.session.authentication(login, password)

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

    def get_flights_table(self, start_date, num_of_days, flight_numbers=None, length=1100, id_only=False):
        # get flight table for range of dates OR one flight DB ID
        print('parsing flight table...')
        flights = []
        dates_range = crew_utils.date_iterator(start_date, num_of_days)
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
        flights['departureDate'] = flights['departureDate'].astype('datetime64')
        flights['flightNumber'] = flights['flightNumber'].astype('int')
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
        print('closing CrewInterface session...')
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

    def get_reports_table(self, start_date, num_of_days, url_params='purser'):
        # load crew reports records, all parameters in url_params dict (start/end dates, form id, staff id, flight num,
        # tail number, dep/arr airport, length of list
        print('parsing reports table...')
        if type(start_date) is datetime:
            start_date = start_date.strftime('%Y-%m-%d')
        if 'admin-fv' in self.url_main:
            url = URLs.URL_monitor_reports_FV
        if 'admin-su' in self.url_main:
            url = URLs.URL_monitor_reports_SU
        
        if url_params == 'purser':
            url_params = {"form_id": '51',
                          "staff_id": '',
                          "flight_number": '',
                          "dep_airport": '',
                          "arr_airport": '',
                          "reg_number": ''}
        elif url_params == 'otchet_sb':
            url_params = {"form_id": '32',
                          "staff_id": '',
                          "flight_number": '',
                          "dep_airport": '',
                          "arr_airport": '',
                          "reg_number": ''}
        
        url_params['length'] = 10000
        reports_table = []
        dates_range = crew_utils.date_iterator(start_date, num_of_days)
        for date in dates_range:
            url_params['start_date'] = url_params['end_date'] = date
            url_temp = url.format(**url_params)
            reports = self.session.get(url_temp)
            reports = json.loads(reports.content)['data']
            reports_table.append(pd.DataFrame(data=reports))
        reports_table = pd.concat(reports_table, axis=0, sort=False)
        reports_table = crew_utils.dtrowid_to_index(reports_table)
        reports_table = reports_table.drop(['manualProcessingProcessedDate', 'download', 'manualProcessingStaffId', 'id'],
                               axis=1, errors='ignore')
        reports_table['lastUpdate'] = reports_table['lastUpdate'].astype('datetime64')
        reports_table['departureDate'] = reports_table['departureDate'].astype('datetime64')
        reports_table['lastUpdateEnd'] = reports_table['lastUpdateEnd'].astype('datetime64')
        reports_table['flightNumber'] = reports_table['flightNumber'].astype('int')
        return reports_table
    
    def activate_all_users(self):
        user_table = self.get_portal_users()
        user_table = user_table[user_table['enabled'] == 'false']
        users_to_activate = user_table.index.values
        print('start activation of {} users'.format(len(users_to_activate)))
        activated = []
        not_activated = []
        for user_id in users_to_activate:
            r = self.activate_user(user_id)
            if r: 
                activated.append(user_id)
            else: 
                not_activated.append(user_id)
        return activated, not_activated
    
    def activate_user(self, user_id, password='su'):
        self.session.get(URLs.URL_users_enable.format(user_id=user_id))
        upd = self.reset_user_password(user_id, password)
        if 'Update successful' in str(upd):
            print('password update for {} successful'.format(user_id))
            return True
        else:
            print('password update for {} FAILED'.format(user_id))
            return False

    def reset_user_password(self, user_id, password='su'):
        csrf = self.session.get_csrf(URLs.URL_users_reset_password_csrf.format(user_id=user_id))
        data = {'id': user_id, 'token': '', 'credentials': password,
                'credentialsConfirmation': password, 'save': '', '_csrf': csrf}
        p = self.session.post(URLs.URL_users_reset_password, data=data)
        return p.content
