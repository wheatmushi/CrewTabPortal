import URLs
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import itertools

name_to_position = {'AAQ (ret)': 10, 'AER (ret)': 11, 'AGP (ret)': 12, 'VLC (ret)': 12, 'ALC (ret)': 12, 'ARN (ret)': 13, 'ASF (ret)': 13, 'BKK (ret)': 14, 'HKT (ret)': 14, 'CAN (ret)': 15, 'CEK (ret)': 16, 'CMB (ret)': 16, 'CMN (ret)': 16, 'DEL (ret)': 17, 'DUS (ret)': 18, 'DXB (ret)': 19, 'DWC (ret)': 19, 'EVN (ret)': 20, 'HAN (ret)': 21, 'HAV (ret)': 22, 'VRA (ret)': 22, 'HKG (ret)': 23, 'IAD (ret)': 24, 'ICN (ret)': 25, 'IKT (ret)': 26, 'JFK (ret)': 27, 'KHV (ret)': 28, 'KRR (ret)': 29, 'LAX (ret)': 30, 'LIS (ret)': 31, 'MAD (ret)': 32, 'MIA (ret)': 33, 'MLE (ret)': 34, 'MRV (ret)': 34, 'NRT (ret)': 35, 'PEE (ret)': 36, 'PEK (ret)': 37, 'PKC (ret)': 38, 'PMI (ret)': 38, 'PRG (ret)': 39, 'PVG (ret)': 40, 'SEZ (ret)': 40, 'SGN (ret)': 41, 'SIP (ret)': 42, 'STW (ret)': 43, 'SVX (ret)': 44, 'TFS (ret)': 45, 'TLV (ret)': 46, 'UFA (ret)': 47, 'ULN (ret)': 48, 'UUS (ret)': 49, 'VVO (ret)': 50, 'YKS (ret)': 51, 'TST (ret)': 999, 'AGP  VLC  ALC (ret)': 12, 'BKK  HKT (ret)': 14, 'DXB  DWC (ret)': 19, 'HAV  VRA (ret)': 22, '2-6hr. Breakfast': 2, '2-6hr. Lunch': 3, '6+ hours': 4}


def table_2_dict(table, D, drop_t=(0, None), drop_l=(0, None)):
    # return dict for 1D and 2D html tables (you could drop some columns/rows)
    table = table.find_all('tr')
    head = table[0].find_all('th')[drop_t[0]:drop_t[1]]
    head = [f.text for f in head]
    table = [[s.text.replace('\n', '').strip() for s in f.find_all('td')] for f in table[1:]]
    if D == 1:
        return {head[i].replace(' ', ''): [s[drop_t[0] + i] for s in table] for i in range(len(head))}
    if D == 2:
        return {(head[1+i] + r[0]).replace(' ', ''): r[1+i]
                for r in table[drop_l[0]:drop_l[1]] for i in range(len(head)-1)}


def get_flight_info(session, flight_id, passengers=False):
    r = session.get(URLs.URL_flights_base_data.format(flight_id=flight_id))
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
    if passengers:
        return base_info, pass_info
    else:
        return base_info['Scheduled Departure'], base_info['Scheduled Arrival']


def acc_auth():  # just draft
    session = requests.session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    params = ('__EVENTTARGET', '__EVENTARGUMENT', '__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION')
    r = session.get('https://acc.mobility.sita.aero/admin/Login.aspx?chcode=8301')
    soup = BeautifulSoup(r.content, 'html.parser')


def date_iterator(start_date, end_date=None, num_of_days=None):  # iterate over days end generate new str with date
    if type(start_date) is not datetime:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        if type(end_date) is not datetime:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        while start_date != end_date:
            yield '{:%Y-%m-%d}'.format(start_date)
            start_date += timedelta(days=1)
        return 0
    for i in range(min(num_of_days, 0), max(num_of_days, 1)):
        date = '{:%Y-%m-%d}'.format(start_date + timedelta(days=i))
        yield date


def dtrowid_to_index(df):  # just change pd.Dataframe indexes to original DB IDs
    df['DT_RowId'] = df['DT_RowId'].map(lambda s: s.replace(',', ''))
    df['DT_RowId'] = df['DT_RowId'].astype('int')
    df = df.set_index('DT_RowId')
    return df


def packer(amount, *args):
    full_list = []
    if len(args) % amount != 0:
        print('WARNING: wrong amount of arguments!!!')
        return None
    else:
        while args:
            list1 = args[0]
            it = itertools.product(list1, (args[1],), (args[2],), (args[3],))
            full_list.append(it)
            args = args[4:]
    return full_list
