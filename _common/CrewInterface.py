# interface for CrewTab portal access: flights, syncs, reports, users
import json
from bs4 import BeautifulSoup
from datetime import datetime
from time import time
import pandas as pd
import URLs
import auth
import crew_utils


def timer(method_to_decorate):
    def wrapper(*args, **kwargs):
        name = method_to_decorate.__name__.replace('get_', '')
        print('parsing {}...'.format(name))
        t = time()
        result = method_to_decorate(*args, **kwargs)
        t = round(time() - t)
        print('{} parsing time {} seconds'.format(name, t))
        return result
    return wrapper


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
        for i in ['Scheduled Departure (UTC)', 'Estimated Departure (UTC)', 'Scheduled Arrival (UTC)']:
            try:
                base_info[i] = datetime.strptime(base_info[i], '%d%b%Y %H:%M %Z')
            except:
                base_info[i] = None
        base_info['Duration'] = int(
            (base_info['Scheduled Arrival (UTC)'] - base_info['Scheduled Departure (UTC)']).total_seconds() // 60)
        pass_head = [cell.text for cell in tables[1].find_all('th')][1:]
        pass_content = [cell.text.replace('\n', '').strip() for cell in tables[1].find_all('td')]
        pass_info = {pass_head[i]: {pass_content[j * 4]: pass_content[j * 4 + i + 1] for j in range(3)} for i in
                     range(3)}
        if all_info:
            return base_info, pass_info
        else:
            return base_info['Scheduled Departure (UTC)'], base_info['Scheduled Arrival (UTC)']

    @timer
    def get_flights_table(self, start_date, end_date=None, num_of_days=None, flight_numbers='', departure_airport='',
                          arrival_airport='', length=2000, id_only=False, filter_status=False):
        # get flight table for range of dates OR one flight DB ID
        if departure_airport and departure_airport.upper() != 'SVO':
            f = self.session.get(URLs.URL_flights_list.format(flight_number=flight_numbers,
                                                              departure_airport=departure_airport,
                                                              arrival_airport=arrival_airport,
                                                              departure_date='',
                                                              length=length))
            f = json.loads(f.content)['data']
            flights = pd.DataFrame(data=f)
        else:
            flights = []
            dates_range = crew_utils.date_iterator(start_date, end_date=end_date, num_of_days=num_of_days)
            if flight_numbers and type(flight_numbers) is str:
                flight_numbers = (flight_numbers,)
            for d in dates_range:
                f = self.session.get(URLs.URL_flights_list.format(flight_number='', departure_airport=departure_airport,
                                                                  arrival_airport=arrival_airport, departure_date=d,
                                                                  length=length))
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
        if filter_status:
            flights = flights[flights['flightStatusLabel'] != filter_status]
        flights['departureDateStart'] = flights['departureDateStart'].astype('datetime64')
        flights = flights[flights['departureDateStart'].isin(list(crew_utils.date_iterator(start_date,
                                                                                           end_date=end_date,
                                                                                           num_of_days=num_of_days)))]
        flights['paxInfoAvailable'] = flights['paxInfoAvailable'].replace(
            {'<i class="fa fa-ban"></i><span class="hidden">false</span>': False,
             '<i class="fa fa-check"></i><span class="hidden">true</span>': True})
        #flights['flightNumber'] = flights['flightNumber'].astype('int')
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

    @timer
    def get_syncs(self, departure_dates=(), start_date=None, end_date=None,
                  staff_id='', flight_number='', departure_airports=(), length=25000):
        # load user's app<->server synchronizations
        # lastUpdate == Last DCS call, synchronizationDate == Sync Timestamp
        syncs = []
        if not departure_dates and not departure_airports and not (start_date and end_date):
            print('no date or airport given for sync filter, please add params')
            return
        if not departure_dates:
            departure_dates = crew_utils.date_iterator(start_date, end_date=end_date)
        if flight_number:
            flight_number = '0'*(4-len(flight_number)) + flight_number

        if departure_airports:
            for date in departure_dates:
                for airport in departure_airports:
                    print('parsing flight status syncs for {}...'.format(date))
                    r = self.session.get(URLs.URL_monitor_syncs.format(departure_date=date, flight_number=flight_number,
                                                                       departure_airport=airport, staff_id=staff_id,
                                                                       sort='asc', length=length))
                    r = json.loads(r.content)['data']
                    syncs.append(pd.DataFrame(data=r))

        else:  # too much results will be returned if no filtering for airports given
            if not departure_dates:
                departure_dates = ('',)
            for date in departure_dates:
                print('parsing flight status syncs for {}...'.format(date))
                asc = self.session.get(URLs.URL_monitor_syncs.format(departure_date=date, flight_number=flight_number,
                                                                     departure_airport='', staff_id=staff_id,
                                                                     sort='asc', length=length))
                asc = json.loads(asc.content)['data']
                syncs.append(pd.DataFrame(data=asc))
                desc = self.session.get(URLs.URL_monitor_syncs.format(departure_date=date, flight_number=flight_number,
                                                                      departure_airport='', staff_id=staff_id,
                                                                      sort='desc', length=length))
                desc = json.loads(desc.content)['data']
                syncs.append(pd.DataFrame(data=desc))

        syncs = pd.concat(syncs, axis=0, sort=False)
        syncs = syncs.drop_duplicates()
        syncs = crew_utils.dtrowid_to_index(syncs)
        syncs['lastUpdate'] = syncs['lastUpdate'].astype('datetime64')
        syncs['departureDate'] = syncs['departureDate'].astype('datetime64')
        syncs['scheduledDepartureDateTime'] = syncs['scheduledDepartureDateTime'].astype('datetime64')
        syncs['synchronizationDate'] = syncs['synchronizationDate'].astype('datetime64')
        return syncs

    @timer
    def get_reports_table(self, start_date, num_of_days, report='purser'):
        # load crew reports records, all parameters in url_params dict (start/end dates, form id, staff id, flight num,
        # tail number, dep/arr airport, length of list
        if type(start_date) is datetime:
            start_date = start_date.strftime('%Y-%m-%d')

        form_id = {'purser': '51', 'otchet_sb': '32'}

        url_params = {"staff_id": '',
                      "flight_number": '',
                      "departure_airport": '',
                      "arrival_airport": '',
                      "reg_number": '',
                      "length": 10000,
                      "form_id": form_id[report]}

        reports_table = []
        dates_range = crew_utils.date_iterator(start_date, num_of_days=num_of_days)
        for date in dates_range:
            url_params['start_date'] = url_params['end_date'] = date
            url = URLs.URL_monitor_reports.format(**url_params)
            reports = self.session.get(url)
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

    @timer
    def get_catering_closed_sessions(self, flight_number='', departure_airport='', start_date='', end_date=''):
        # load catering sessions statistic for given airport/dates/flight

        def get_one(self, flight_number=flight_number, departure_airport=departure_airport,
                    start_date=start_date, end_date=end_date, length=1000):
            r = self.session.get(URLs.get_catering_closed_sessions.format(flight_number=flight_number,
                                                                          departure_airport=departure_airport,
                                                                          start_date=start_date,
                                                                          end_date=end_date,
                                                                          length=length))
            r = json.loads(r.content)['data']
            return r

        if departure_airport and departure_airport.upper() != 'SVO':
            cat_sessions = get_one(self, departure_airport=departure_airport, start_date=start_date, end_date=end_date)
            cat_sessions = pd.DataFrame(data=cat_sessions)
        else:
            cat_sessions = []
            dates_range = crew_utils.date_iterator(start_date, end_date=end_date)
            for d in dates_range:
                sessions = get_one(self, departure_airport=departure_airport, start_date=d, end_date=d)
                cat_sessions.append(pd.DataFrame(data=sessions))
            cat_sessions = pd.concat(cat_sessions, axis=0, sort=False)

        cat_sessions = cat_sessions.drop('display', axis=1)
        cat_sessions = crew_utils.dtrowid_to_index(cat_sessions)
        cat_sessions['earliestLocalDepartureDate'] = cat_sessions['earliestLocalDepartureDate'].astype('datetime64')
        cat_sessions['latestLocalDepartureDate'] = cat_sessions['latestLocalDepartureDate'].astype('datetime64')
        cat_sessions['amountOfOrders'] = cat_sessions['amountOfOrders'].astype('int')
        cat_sessions['amountOfCrewOperated'] = cat_sessions['amountOfCrewOperated'].astype('int')
        cat_sessions['amountOfOrdersServed'] = cat_sessions['amountOfOrdersServed'].astype('int')
        return cat_sessions
