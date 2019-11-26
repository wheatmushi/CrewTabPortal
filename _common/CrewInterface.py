# interface for CrewTab portal access
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import URLs
import auth


class CrewInterface:
    def __init__(self, url_main):
        self.url_main = url_main
        self.session = auth.SessionCrewTabPortal(url_main)
        self.session.authentication()

    def get_flight_info(self, flight_id, all_info=False):  # get flight information about times of dep/arr and passengers
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

    def get_flights_table(self, dates_range, flight_numbers=None, length=1100):  # get flight table for range of dates
        flights = []
        if not hasattr(dates_range, '__iter__'):
            dates_range = (dates_range,)
        if not flight_numbers:
            flight_numbers = ('',)
        elif not hasattr(flight_numbers, '__iter__'):
            flight_numbers = (flight_numbers,)
        for d in dates_range:
            f = self.session.get(URLs.URL_flights_list.format(flight_number='', departure_date=d, length=length))
            f = json.loads(f.content)['data']
            flights.append(pd.DataFrame(data=f))
        flights = pd.concat(flights, axis=0, sort=False)
        flights = self.dtrowid_to_index(flights)
        flights = flights.drop('details', axis=1)
        flights = flights[flights['flightNumber'].isin(flight_numbers)]
        if flights.empty:
            print('no flights found!!')
        return flights

    def get_portal_users(self, is_enabled=False, search_value=''):
        print('parsing full crew list...')
        is_enabled = '1' if is_enabled else '0'
        r = self.session.get(URLs.URL_users_list.format(length=10, search_value='', is_enabled=False))
        total = json.loads(r.content)['recordsTotal']
        r = self.session.get(URLs.URL_users_list.format(length=total, search_value=search_value, is_enabled=is_enabled))
        full_table = json.loads(r.content)['data']
        full_table = pd.DataFrame(data=full_table)
        full_table = self.dtrowid_to_index(full_table)
        full_table['enabled'] = full_table['enabled'].map(lambda s: BeautifulSoup(s, 'html.parser').text)
        full_table = full_table.drop(['image', 'display', 'delete'], axis=1)
        return full_table

    def get_flight_crews(self, flight_id):  # get crews for particular flight
        print('parsing data for flight ID', flight_id)
        r = self.session.get(URLs.URL_flight_crews.format(flight_id=flight_id, length=30))
        r = json.loads(r.content)['data']
        crews = pd.DataFrame(data=r)
        return crews

    def dtrowid_to_index(self, df):  # just fix pd.Dataframe indexes to original DB IDs
        df['DT_RowId'] = df['DT_RowId'].map(lambda s: s.replace(',', ''))
        df['DT_RowId'] = df['DT_RowId'].astype('int')
        df = df.set_index('DT_RowId')
        return df

    def close(self):
        self.session.close()
