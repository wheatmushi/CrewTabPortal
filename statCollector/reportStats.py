#  load records for crew reports and build statistic for app usage

import sys
import os
import pandas as pd
sys.path.insert(1, os.path.join('..', '_common'))
from CrewInterface import CrewInterface
from datetime import datetime, timedelta


pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 30)

start_date = datetime.now()
num_of_days = 35
params = {"form_id": '51',
          "staff_id": '',
          "flight_number": '',
          "dep_airport": '',
          "arr_airport": '',
          "reg_number": ''}

url_main = 'https://admin-su.crewplatform.aero/'

''''
interface = CrewInterface(url_main)
reports = interface.get_reports_table(start_date, num_of_days, params)
grp = reports.groupby([reports['lastUpdate'].dt.day, reports['lastUpdate'].dt.hour]).size()
grp.to_csv('reports_by_hour_{}.csv'.format(start_date))
'''