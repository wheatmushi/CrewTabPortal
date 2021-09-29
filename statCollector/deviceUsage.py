#  create report for device usage:
#  SIMs connection sessions (to be loaded manually), app<->server syncs, catering orders

import sys
import os
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface

pd.set_option('display.width', 320)
pd.set_option('display.max_columns',30)

sim_connections_location = '/Volumes/data/downloads/User Connections.csv'
start_date = '2021-09-17'
end_date = '2021-09-20'

url_su = 'https://admin-su.crewplatform.aero/'
url_fv = 'https://admin-fv.crewplatform.aero/'


def airline_splitter(df, split=True):  # split SU and FV SIMs (mark SU or FV and create 2 DataFrames)
    led_mask = '(+32)077000505'
    with open(r'/Volumes/data/code/SITA/ICC_connections/fv_vko_numbers.csv', 'r') as vko:
        vko_nums = ['(+32)0' + line.split(',')[0][2:] for line in vko.readlines()]
    df['airline'] = df['Device'].apply(lambda s: 'FV' if led_mask in s else 'SU')
    df['airline'] = df.apply(lambda r: 'FV' if r['Device'] in vko_nums else r['airline'], axis=1)
    if split:
        df_su = df[df['airline'] == 'SU']
        df_fv = df[df['airline'] == 'FV']
        return df_su, df_fv
    else:
        return df


def prepare_data(df):
    df['Start Time'] = df['Start Time'].astype('datetime64')
    df['End Time'] = df['End Time'].astype('datetime64')
    df['date'] = df['Start Time'].dt.date
    df['data_used'] = df['Tx Bytes'] + df['Rx Bytes']
    df_su, df_fv = airline_splitter(df)
    return df_su, df_fv


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


def create_report(df_su, df_fv, syncs_su, syncs_fv, catering_su):
    report = pd.DataFrame(df_su.groupby('date')['Device'].nunique())
    report.columns = ['SU SIM used']
    report['SU unique sync staff IDs'] = syncs_su.groupby('date')['staffId'].nunique()
    report['SU catering sessions'] = catering_su.groupby('earliestLocalDepartureDate').size()
    report['SU catering all served'] = catering_su[catering_su['allServed']].groupby('earliestLocalDepartureDate').size()

    report['FV SIM used'] = df_fv.groupby('date')['Device'].nunique()
    report['FV unique sync staff IDs'] = syncs_fv.groupby('date')['staffId'].nunique()
    report['FV 4G data used'] = df_fv.groupby('date')['data_used'].sum() / 10 ** 9
    report['SU 4G data used'] = df_fv.groupby('date')['data_used'].sum() / 10 ** 9
    return report


df = pd.read_csv(sim_connections_location)
df_su, df_fv = prepare_data(df)
syncs_su, catering_su = get_app_usage_data(url_su, start_date, end_date, check_catering=True)
syncs_fv = get_app_usage_data(url_fv, start_date, end_date)
report = create_report(df_su, df_fv, syncs_su, syncs_fv, catering_su)
report.to_excel('SU and FV device usage.xlsx')
