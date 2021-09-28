# Catering objects description and methods:
# Menu == top-lvl category with sub-categories == serving rounds,
# Item == separate dish, LineItems == links for fast order taking
import pandas as pd
import sys
import os
import csv
import pytz
from datetime import datetime, timedelta
from time import sleep
sys.path.insert(1, os.path.join('..', '_common'))
import crew_utils
import CrewInterface


class Menu:
    def __init__(self, csv_path, filename, interface, new=False, name_en=None, name_ru=None, img_path=None):
        self.new = new
        if name_en:
            self.name_en, self.name_ru = name_en, name_ru
            self.position = self.name_and_position(name_en=name_en)
        else:
            self.name_en, self.name_ru, self.position = self.name_and_position(filename=filename)
        self.csv_storage_path = os.path.join(csv_path, filename)  # here prepared .csv located
        self.interface = interface  # initialized CateringInterface
        self.content = pd.read_csv(self.csv_storage_path, sep='|', dtype=object)
        self.img_path = img_path
        self.menu = [Item(self.content.iloc[i], self.interface, self.img_path) for i in range(self.content.shape[0])]
        self.csv_serving_rounds = set(self.content['subcategory name en'])  # serving rounds expected in .csv
        if new:
            self.create_menu_cat_itself()
        menu_id = self.interface.get_cat_ids(search_value=self.name_en, exactly=True)
        self.category_id = menu_id[self.name_en][0]
        self.server_serving_rounds = self.interface.get_subcat_ids(self.category_id)
        print('menu {} initialized for {} cat'.format(self.name_en, self.category_id))

    def name_and_position(self, filename=None, name_en=None):
        if filename:
            n = filename.split('.')[0].split('_')[0]
            name_en = n
            name_ru = n
            return name_en, name_ru, crew_utils.name_to_position[name_en]
        if name_en:
            return name_en, crew_utils.name_to_position[name_en]

    def create_menu_cat_itself(self):  # create top-lvl category
        data = self.prepare(self.name_en, self.name_ru, self.position)
        self.interface.create_cat(data, self.position, self.name_en, self.name_ru)

    def create_serving_rounds(self):  # check and create (if needed) subcats for different serving rounds
        if not self.server_serving_rounds and self.new:
            if input('create all serving rounds? y/n?') == 'y':
                confirm = False
            else:
                confirm = True
        elif not self.server_serving_rounds:
            print('no serving rounds found on server')
            return 'exit'
        else:
            confirm=True
        server_rounds_names = [s[1] for s in self.server_serving_rounds.values()]
        for s_round in self.csv_serving_rounds:
            if s_round not in server_rounds_names:
                pos = self.content[self.content['subcategory name en'] == s_round]['subcategory position'].iloc[0]
                name_ru = self.content[self.content['subcategory name en'] == s_round]['subcategory name ru'].iloc[0]
                data = self.prepare(s_round, name_ru, pos, self.category_id)
                self.interface.create_cat(data, pos, s_round, name_ru, self.category_id, self.name_en, confirm=confirm)
        self.server_serving_rounds = self.interface.get_subcat_ids(self.category_id)
        return confirm

    def deploy(self):  # just deploy all serving rounds and items from .csv DataFrame on CrewTab portal
        confirm = self.create_serving_rounds()
        if confirm == 'exit':
            return 0
        for subcat_id, subcat in self.server_serving_rounds.items():
            items_ids = self.interface.get_items_in_subcat(subcat_id)
            items_len = len([item for item in self.menu if item.data['subcategory name en'] == subcat[1]])
            if len(items_ids) != items_len:
                print('{} items on server in subcat {} and {} items in menu, continue menu creation?'.
                      format(len(items_ids), subcat[2], items_len))
                if input('y/n?') != 'y':
                    return 0
            for item in self.menu:
                if item.data['subcategory position'] == subcat[0]:
                    item_pos = item.data['item position']
                    if item.check_if_exist(subcat_id, log='not_exist'):
                        item_id = items_ids[item_pos][0]
                        item.modify(subcat_id, item_id, confirm=False)
                    else:
                        item.create(subcat_id, confirm=False)

    def prepare(self, name_en, name_ru, position, parent_cat_id=''):  # prepare category to POST
        data = {'id': '',
                "nameLocalizedValueId": '',
                "name[0].idTranslation": '',
                "name[0].idLanguage": '4',
                "name[0].defaultLanguage": 'true',
                "name[0].languageName": 'English',
                "name[0].value": name_en,
                "name[1].idTranslation": '',
                "name[1].idLanguage": '5',
                "name[1].defaultLanguage": 'false',
                "name[1].languageName": 'Russian',
                "name[1].value": name_ru,
                "name[2].idTranslation": '',
                "name[2].idLanguage": '7',
                "name[2].defaultLanguage": 'false',
                "name[2].languageName": 'French',
                "name[2].value": '',
                "name[3].idTranslation": '',
                "name[3].idLanguage": '8',
                "name[3].defaultLanguage": 'false',
                "name[3].languageName": 'Italian',
                "name[3].value": '',
                "name[4].idTranslation": '',
                "name[4].idLanguage": '10',
                "name[4].defaultLanguage": 'false',
                "name[4].languageName": 'Polish',
                "name[4].value": '',
                "parentCategoryId": parent_cat_id,
                "backgroundColor": '#000000',
                "foregroundColor": '#000000',
                "multipleChoice": 'true',
                "_multipleChoice": 'on',
                "position": position,
                "save": ''}
        return data


class Item:
    def __init__(self, series, interface, img_path=None):
        self.interface = interface
        self.data = series.to_dict()
        full_descr_ru = [self.data['item description ru'], self.data['item calories ru'], self.data['item wines ru']]
        self.data['full description ru'] = ' / '.join([i for i in full_descr_ru if isinstance(i, str)])
        full_descr_en = [self.data['item description en'], self.data['item calories en'], self.data['item wines en']]
        self.data['full description en'] = ' / '.join([i for i in full_descr_en if isinstance(i, str)])
        self.img_path = None
        if img_path:
            img_filename = '{}_{}.jpg'.format(self.data['subcategory position'], self.data['item position'])
            img_path = os.path.join(img_path, img_filename)
            if os.path.isfile(img_path):
                self.img_path = img_path

    def check_if_exist(self, subcat_id, log=None):  # if item for replacement already exist or should be created
        item_position = self.data['item position']
        items_list = self.interface.get_items_in_subcat(subcat_id)
        if item_position in items_list.keys():
            if log and log == 'exist':
                print('item {} already exist'.format(self.data['item name ru']))
            return items_list[item_position]
        else:
            if log and log == 'not_exist':
                print('item {} does not exist'.format(self.data['item name ru']))
            return False

    def modify(self, subcat_id, item_id, confirm=True):  # edit existing item
        item_data, item_file = self.prepare_item(subcat_id, item_id)
        p = self.interface.modify_item(subcat_id, item_data, item_file, 'modifying', item_id, confirm=confirm)
        if isinstance(self.data['item allergens'], str):
            server_allergens = set(self.interface.get_allergens(item_id))
            table_allergens = set(self.data['item allergens'].split(', '))
            for allergen in server_allergens.symmetric_difference(table_allergens):
                self.interface.edit_allergens(allergen, item_id)
        return p

    def create(self, subcat_id, confirm=True):  # create new item
        item_data, item_file = self.prepare_item(subcat_id)
        print(item_data)
        print(item_file)
        p = self.interface.modify_item(subcat_id, item_data, item_file, 'creating', confirm=confirm)
        if isinstance(self.data['item allergens'], str):
            item_id = self.interface.get_items_in_subcat(subcat_id, search_value=self.data['item name en'])
            item_id = list(item_id.values())[0][0]
            for allergen in self.data['item allergens'].split(', '):
                self.interface.edit_allergens(allergen, item_id)
        return p

    def prepare_item(self, subcat_id, item_id=''):  # prepare data for POSTing (creating/modifying) item
        data = {"idItem": item_id,
             "name[0].idTranslation": '',
             "name[0].idLanguage": '4',
             "name[0].defaultLanguage": 'true',
             "name[0].languageName": 'English',
             "name[0].value": self.data['item name en'],  # ENGLISH NAME
             "name[1].idTranslation":'',
             "name[1].idLanguage": '5',
             "name[1].defaultLanguage": 'false',
             "name[1].languageName": 'Russian',
             "name[1].value": self.data['item name ru'],  # RUSSIAN NAME
             "name[2].idTranslation": '',
             "name[2].idLanguage": '7',
             "name[2].defaultLanguage": 'false',
             "name[2].languageName": 'French',
             "name[2].value": '',
             "name[3].idTranslation": '',
             "name[3].idLanguage": '8',
             "name[3].defaultLanguage": 'false',
             "name[3].languageName": 'Italian',
             "name[3].value": '',
             "description[0].idTranslation": '',
             "description[0].idLanguage": '4',
             "description[0].defaultLanguage": 'true',
             "description[0].languageName": 'English',
             "description[0].value": self.data['full description en'],  # ENGLISH DESCRIPTION
             "description[1].idTranslation": '',
             "description[1].idLanguage": '5',
             "description[1].defaultLanguage": 'false',
             "description[1].languageName": 'Russian',
             "description[1].value": self.data['full description ru'],  # RUSSIAN DESCRIPTION
             "description[2].idTranslation": '',
             "description[2].idLanguage": '7',
             "description[2].defaultLanguage": 'false',
             "description[2].languageName": 'French',
             "description[2].value": '',
             "description[3].idTranslation": '',
             "description[3].idLanguage": '8',
             "description[3].defaultLanguage": 'false',
             "description[3].languageName": 'Italian',
             "description[3].value": '',
             "idCategory": subcat_id,  # TARGET CATEGORY
             "shortName": self.data['item short name ru'],  # ITEM SHORT NAME
             "_limitedQuantity": 'on',
             "_availableOnAllFlights": 'on',
             "_gmPreparationRequired": 'on',
             "_displayOnBeverageSummary": 'on',
             "_showInHistory": 'on',
             "color": '#000000',
             "position": self.data['item position'],
             "validityDateStart": '',
             "validityDateEnd": '',
             "nameLocalizedValueId": '',
             "descriptionLocalizedValueId": '',
             "save": ''}
        if self.data['is limited'] == '1':
            data['limitedQuantity'] = 'true'
        if self.data['is for all flights'] == '1':
            data['availableOnAllFlights'] = 'true'
        if self.data['is req GM prep'] == '1':
            data['gmPreparationRequired'] = 'true'
        if self.data['is display beverage'] == '1':
            data['displayOnBeverageSummary'] = 'true'
        if self.data['is show in hist'] == '1':
            data['showInHistory'] = 'true'
        file = None
        if isinstance(self.data['path to image'], str):
            with open(self.data['path to image'], 'rb') as file:
                img = file.read()
            file = {'image': ('image.jpg', img, 'image/jpeg')}
        elif self.img_path:
            with open(self.img_path, 'rb') as file:
                img = file.read()
            file = {'image': ('image.jpg', img, 'image/jpeg')}
        return data, file


class LineItemTable:
    def __init__(self, interface, path=os.path.join('..', '_DB', 'catering')):
        self.path = path
        self.interface = interface
        self.table = pd.read_csv(os.path.join(path, 'afl_routes.csv'), sep=',', dtype=object, index_col=0)

    def check_updates(self, start_date, end_date):  # check for new flights on CrewTab portal for last N days and update flights table in DB
        def get_flight_local_time(dep_airport, utc_time, timezones):
            zone = timezones[dep_airport]
            return pytz.utc.localize(utc_time).astimezone(pytz.timezone(zone))

        def separate_menus(row):
            if row['dep_airport'] in airport_with_separate_menu:
                return 'individual'
            elif row['duration'] < 120:
                return 'less 2 hrs'
            elif row['duration'] > 360:
                return '6+ hours'
            elif row['is_morn']:
                return '2-6hr. Breakfast'
            else:
                return '2-6hr. Lunch'
        print('loading fresh flight data... please be patient this operation will take few minutes')

        airport_with_separate_menu = [i.replace(' (ret)', '') for i in crew_utils.name_to_position.keys()]

        with open(os.path.join(self.path, 'iata_to_timezone.csv'), mode='r') as f:
            reader = csv.reader(f, delimiter=',')
            timezones = {rows[0]: rows[1] for rows in reader}

        itf = CrewInterface.CrewInterface(self.interface.url_main)

        flights = itf.get_flights_table(start_date=start_date, end_date=end_date)
        flights = flights.rename(columns=
                                 {'flightNumber': 'fl_num',
                                  'departureAirport': 'dep_airport',
                                  'arrivalAirport': 'arr_airport'})
        flights = flights[flights['fl_num'] < '3000']
        flights = flights[flights.duplicated(subset=['fl_num', 'dep_airport', 'arr_airport'], keep=False)]
        flights = flights.drop_duplicates(['fl_num', 'dep_airport', 'arr_airport'])
        flights['utc_dep_time'], flights['utc_arr_time'] =\
            zip(*flights.apply(lambda r: itf.get_flight_info(r.name), axis=1))
        flights['duration'] = flights.apply(lambda row: (row['utc_arr_time'] - row['utc_dep_time']).seconds // 60, axis=1)
        flights['local_dep_time'] = flights.apply(
            lambda row: get_flight_local_time(row['dep_airport'], row['utc_dep_time'], timezones), axis=1)
        flights['is_morn'] = flights['local_dep_time'].map(lambda t: True if 6 <= t.hour < 10 else False)
        flights['menu'] = flights.apply(lambda row: separate_menus(row), axis=1)
        flights['timezone'] = flights['dep_airport'].map(timezones)
        flights = flights.drop(['departureDateStart', 'flightStatusLabel', 'departureDateEnd', 'regNumber', 'equipment',
                                'paxInfoAvailable'], axis=1)
        flights['fl_num'] = flights['fl_num'].astype('int')

        old_routes_path = os.path.join('..', '_DB', 'catering', 'afl_routes_old.csv')
        new_routes_path = os.path.join('..', '_DB', 'catering', 'afl_routes.csv')
        old_flights = pd.read_csv(new_routes_path, index_col=0, sep=',')
        flights_difference = pd.concat([flights, old_flights], axis=0, sort=False).\
            drop_duplicates(subset=['fl_num', 'dep_airport', 'arr_airport'], keep=False)
        print('{} flights in DB\n{} flights in fresh data\n{} flights to add'.format(old_flights.shape[0],
                                                                                     flights.shape[0],
                                                                                     flights_difference.shape[0]))

        choice = 0
        while choice not in (1, 2, 3):
            choice = int(input('select 1 to replace old flight table with new one,\n'
                               'select 2 to make sum of new and old flights,\n'
                               'select 3 to keep only old flight table'))
        if choice == 1:
            os.rename(new_routes_path, old_routes_path)
            flights.to_csv(new_routes_path, sep=',')
            print('new flight table exported to afl_routes.csv, old flights in afl_routes_old.csv')
            return flights
        elif choice == 2:
            os.rename(new_routes_path, old_routes_path)
            flights_sum = pd.concat([flights, old_flights], axis=0, sort=False). \
                drop_duplicates(subset=['fl_num', 'dep_airport', 'arr_airport'], keep='first')
            flights_sum.to_csv(new_routes_path, sep=',')
            flights.to_csv('afl_routes_new.csv', sep=',')
            print('updated table (both old and new) exported to afl_routes.csv,'
                  ' old flights exported to afl_routes_old.csv,'
                  ' new table exported to afl_routes_new.csv')
            return flights_sum
        else:
            flights.to_csv('afl_routes_new.csv', sep=',')
            print('old flight table still in afl_routes.csv, new flights table in afl_routes.csv')
            return old_flights

    def deploy(self, below=False):  # deploy whole line items table (for many flights maybe)
        if input('update flights table in DB?\ny or n?') == 'y':
            self.table = self.check_updates()
        if below:
            n = self.table[self.table['fl_num'] == below].index[0]
            table = self.table.loc[n:]
        else:
            table = self.table

        for index, row in table.iterrows():
            if row['menu'] != 'less 2 hrs':
                item_set = LineItemSet(row, self.interface)
                item_set.create()


class LineItemSet:
    def __init__(self, line_data, interface):
        self.line_data = line_data
        self.interface = interface
        self.dc = interface.default_cats
        self.item_set = []

    def create(self):  # create all lineitems for one flight
        order = {}
        order['2-6hr. Breakfast'] = ['Tea', 'Cold starter', 'Main course', 'Dessert']
        order['2-6hr. Lunch'] = ['Appetizer', 'Cold starter', 'Main course', 'Dessert']
        order['Delhi'] = ['Appetizer', 'Cold starter', 'Delhi', 'Dessert', 'Delhi']
        order['6+ hours'] = ['Appetizer', 'Cold starters & Sets', 'Salad', 'Soup', 'Main course',
                             'Dessert', '2nd round']
        order['individual'] = ['Appetizer', 'Cold starter', 'Cold starters & Sets', 'Salad', 'Soup', 'Main course',
                               'Dessert', '2nd round']
        key1 = self.line_data['menu']

        if key1 == 'individual':
            airport = self.line_data['dep_airport']
            if airport in ('HKT', 'BKK'):
                airport = 'BKK  HKT (ret)'
            elif airport in ('AGP', 'ALC', 'VLC'):
                airport = 'AGP  VLC  ALC (ret)'
            elif airport in ('DXB', 'DWC'):
                airport = 'DXB  DWC (ret)'
            elif airport in ('HAV', 'VRA'):
                airport = 'HAV  VRA (ret)'
            else:
                airport += ' (ret)'
            menu_id = self.interface.get_cat_ids(search_value=airport, top=True, exactly=True)[airport][0]
            menu = self.interface.get_subcat_ids(menu_id, key='name_en')
            menu = {name: c[1] for name, c in menu.items()}
            for n, r in enumerate(order[key1]):
                if r == 'Dessert' and r in menu.keys():
                    line = (menu[r], self.dc['Common']['Tea'], self.dc['Common']['Coffee'])
                elif r == '2nd round' and r in menu.keys():
                    line = (menu[r], self.dc['Common']['Beverages'], self.dc['Common']['Coffee'])
                elif r in menu.keys():
                    line = (menu[r], self.dc['Common']['Wine & Champagne'], self.dc['Common']['Beverages'])
                else:
                    continue
                self.item_set.append(line)
                lineitem = LineItem(n + 1, self.interface, self.line_data, line)
                lineitem.create()
        else:
            for n, r in enumerate(order[key1]):
                if r == 'Tea':
                    line = (self.dc['Common'][r], self.dc['Common']['Wine & Champagne'], self.dc['Common']['Beverages'])
                elif r == 'Dessert':
                    line = (self.dc[key1][r], self.dc['Common']['Tea'], self.dc['Common']['Coffee'])
                elif r == '2nd round':
                    line = (self.dc[key1][r], self.dc['Common']['Beverages'], self.dc['Common']['Coffee'])
                else:
                    line = (self.dc[key1][r], self.dc['Common']['Wine & Champagne'], self.dc['Common']['Beverages'])
                self.item_set.append(line)
                lineitem = LineItem(n + 1, self.interface, self.line_data, line)
                lineitem.create()


class LineItem:
    def __init__(self, round_num, interface, line_data, line):
        self.round_num = round_num
        self.interface = interface
        self.line_data = line_data
        num = self.line_data['fl_num']
        self.num = '0' * (4 - len(str(num))) + str(num)
        self.name = '-'.join((self.line_data['dep_airport'], self.line_data['arr_airport'],
                              self.num, str(round_num))).upper()
        self.line = line

    def create(self):  # create one lineitem
        data = self.prepare()
        self.interface.create_lineitem(self.name, data)

    def prepare(self):
        return {'name': self.name,
                'displayOrder': self.round_num,
                'flightNumbers': self.num,
                'departureAirports': self.line_data['dep_airport'],
                'arrivalAirports': self.line_data['arr_airport'],
                'itemCategories[0].displayOrder': 0, 'itemCategories[0].categoryId': self.line[0],
                'itemCategories[1].displayOrder': 1, 'itemCategories[1].categoryId': self.line[1],
                'itemCategories[2].displayOrder': 2, 'itemCategories[2].categoryId': self.line[2]}
