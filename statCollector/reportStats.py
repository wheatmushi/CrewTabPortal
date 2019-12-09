import os
import json
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
import auth
import URLs
from CrewInterface import CrewInterface


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)

start_date = '2019-12-02'
end_date = '2019-12-09'
form_id = 51

url_main = 'https://admin-su.crewplatform.aero/'
url_main = 'https://admin-fv.crewplatform.aero/'

interface = CrewInterface(url_main)

params = {'start_date': '2019-12-02',
          "end_date": '2019-12-09',
          "form_id": '51',
          "staff_id": '',
          "flight_number": '',
          "dep_airport": '',
          "arr_airport": '',
          "reg_number": '',
          "length": 10000}

reports = interface.get_reports_table(params)
grp = reports.groupby([reports['lastUpdate'].dt.day, reports['lastUpdate'].dt.hour]).size()
grp.to_csv('reports_by_hour.csv')
