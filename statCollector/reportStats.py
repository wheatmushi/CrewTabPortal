#  load records for crew reports and build statistic for app usage

import os
import json
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
import auth
import URLs
from CrewInterface import CrewInterface


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)

start_date = '2019-10-01'
num_of_days = 86
params = {"form_id": '51',
          "staff_id": '',
          "flight_number": '',
          "dep_airport": '',
          "arr_airport": '',
          "reg_number": ''}

url_main = 'https://admin-su.crewplatform.aero/'
url_main = 'https://admin-fv.crewplatform.aero/'

interface = CrewInterface(url_main)
reports = interface.get_reports_table(start_date, num_of_days, params)
grp = reports.groupby([reports['lastUpdate'].dt.day, reports['lastUpdate'].dt.hour]).size()
grp.to_csv('reports_by_hour_{}.csv'.format(start_date))
