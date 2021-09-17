import sys
import os
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface


sim_connections_location = '/Volumes/data/downloads/User Connections.csv'
start_date = '2021-08-17'
end_date = '2021-09-17'

url_a = 'https://admin-su.crewplatform.aero/'
url_r = 'https://admin-fv.crewplatform.aero/'

def airline_splitter(df, split=True):  # split SU and FV SIMs (mark A or R and create 2 DataFrames)
    led_mask = '(+32)077000505'
    with open(r'/Volumes/data/code/SITA/ICC_connections/fv_vko_numbers.csv', 'r') as vko:
        vko_nums = ['(+32)0' + line.split(',')[0][2:] for line in vko.readlines()]
    df['airline'] = df['Device'].apply(lambda s: 'R' if led_mask in s else 'A')
    df['airline'] = df.apply(lambda r: 'R' if r['Device'] in vko_nums else r['airline'], axis=1)
    if split:
        df_A = df[df['airline'] == 'A']
        df_R = df[df['airline'] == 'R']
        return df_A, df_R
    else:
        return df


def prepare_data(df):
    df['Start Time'] = df['Start Time'].astype('datetime64')
    df['End Time'] = df['End Time'].astype('datetime64')
    df['date'] = df['Start Time'].dt.date
    df['data_used'] = df['Tx Bytes'] + df['Rx Bytes']
    df_a, df_r = airline_splitter(df)
    return df_a, df_r


def get_app_usage_data(url, start_date, end_date, check_catering=False):
    # get stats for app <-> server syncs and catering usage
    itf = CrewInterface(url)
    syncs = itf.get_syncs(start_date=start_date, end_date=end_date)
    syncs['date'] = syncs['synchronizationDate'].dt.date
    if check_catering:
        catering = itf.get_catering_closed_sessions(start_date=start_date, end_date=end_date)
        catering['allServed'] = catering.apply(lambda row: True if row['amountOfOrders'] == row['amountOfOrdersServed']
                                                                   and row['amountOfOrders'] != 0 else False, axis=1)
        return syncs, catering
    else:
        return syncs


def create_report(df_a, df_r, syncs_a, syncs_r, catering_a):
    report = pd.DataFrame(df_a.groupby('date')['Device'].nunique())
    report.columns = ['SU SIM used']
    report['SU unique sync staff IDs'] = syncs_a.groupby('date')['staffId'].nunique()
    report['SU catering sessions'] = catering_a.groupby('earliestLocalDepartureDate').size()
    report['SU catering all served'] = catering_a[catering_a['allServed']].groupby('earliestLocalDepartureDate').size()

    report['FV SIM used'] = df_r.groupby('date')['Device'].nunique()
    report['FV unique sync staff IDs'] = syncs_r.groupby('date')['staffId'].nunique()
    report['FV 4G data used'] = df_r.groupby('date')['data_used'].sum() / 10 ** 9
    report['SU 4G data used'] = df_a.groupby('date')['data_used'].sum() / 10 ** 9
    return report


df = pd.read_csv(sim_connections_location)
df_a, df_r = prepare_data(df)
syncs_a, catering_a = get_app_usage_data(url_a, start_date, end_date, check_catering=True)
syncs_r = get_app_usage_data(url_r, start_date, end_date)
report = create_report(df_a, df_r, syncs_a, syncs_r, catering_a)
report.to_excel('SU and FV device usage.xlsx')
