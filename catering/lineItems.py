import json
import os
import pandas as pd
import sys
sys.path.insert(1, os.path.join('..', '_common'))

from CatInterface import CatInterface


def filter_line_items(session, string):  # returns line items with 'string' in name
    items_list = session.get(URLs.URL_catering_lineitems.format(length=500, search_value=string))
    items_list = json.loads(items_list.content)['data']
    print([item['name'] for item in items_list])
    return [item['DT_RowId'] for item in items_list]


def del_line_items(session, string):  # delete line items with 'string' in name
    items = filter_line_items(session, string)
    items = [i.replace(',', '') for i in items]
    h = input('delete this line items? y/n')
    if h == 'y':
        for s in items:
            session.get(URLs.URL_catering_delete_lineitem.format(lineitem_id=s))
            session.get(URLs.URL_catering_delete_lineitem_confirm.format(lineitem_id=s))


def create_line_items_ind(session, fl_num, dep_airport, arr_airport, morning, duration, sub_menu_ids):
    def create_one_item(counter, line1, line2, line3):
        csrf = session.getCSRF(URLs.URL_catering_create_lineitem)
        print(dep_airport.upper() + '-' + arr_airport.upper() + '-' + fl_num + '-' + str(counter))
        content = {'name': dep_airport.upper() + '-' + arr_airport.upper() + '-' + str(fl_num) + '-' + str(counter),
                   'displayOrder': counter, 'flightNumbers': fl_num,
                   'departureAirports': dep_airport, 'arrivalAirports': arr_airport,
                   'itemCategories[0].displayOrder': 0, 'itemCategories[0].categoryId': line1,
                   'itemCategories[1].displayOrder': 1, 'itemCategories[1].categoryId': line2,
                   'itemCategories[2].displayOrder': 2, 'itemCategories[2].categoryId': line3,
                   '_csrf': csrf}
        session.post(URLs.URL_catering_create_lineitem, content)

    fl_num = '0' * (4 - len(str(fl_num))) + str(fl_num)

    if duration == '6hrs_plus':
        for counter, category in enumerate(sorted(list(sub_menu_ids.keys())), 501):
            id, name = sub_menu_ids[category]
            if 'Dessert' in name:
                create_one_item(counter, id, '121', '122')  # dessert tea coffee
            elif ('2nd round' in name) or ('Second round' in name):
                create_one_item(counter, id, '131', '122')  # 2nd_round beverages coffee
            else:
                create_one_item(counter, id, '94', '131')  # xxx wine beverages

    elif duration == '2-6hrs' and morning == 1:
        for counter, category in enumerate(sorted(list(sub_menu_ids.keys())), 501):
            if len(sub_menu_ids) == 2 and counter == 501:
                create_one_item(500, '94', '131', '121')  # wine beverages tea
            id, name = sub_menu_ids[category]
            if 'Dessert' in name:
                continue
            else:
                create_one_item(counter, id, '94', '131')  # xxx wine beverages
            if len(sub_menu_ids) == 2 and counter == 502:
                create_one_item(counter + 1, '121', '122', '133')  # tea coffee beverages

    elif duration == '2-6hrs' and morning == 0:
        for counter, category in enumerate(sorted(list(sub_menu_ids.keys())), 501):
            if len(sub_menu_ids) == 2 and counter == 501:
                create_one_item(500, '94', '131', '121')  # wine beverages tea
            id, name = sub_menu_ids[category]
            if 'Dessert' in name:
                create_one_item(counter, id, '121', '122')  # dessert tea coffee
            else:
                create_one_item(counter, id, '94', '131')  # xxx wine beverages
            if len(sub_menu_ids) == 2 and counter == 502:
                create_one_item(counter + 1, '121', '122', '133')  # tea coffee beverages


def create_line_items_base(session, fl_num, dep_airport, arr_airport, morning, duration):
    def create_one_item(counter, line1, line2, line3):
        csrf = session.getCSRF(URLs.URL_catering_create_lineitem)
        print(dep_airport.upper() + '-' + arr_airport.upper() + '-' + fl_num + '-' + str(counter))
        content = {'name': dep_airport.upper() + '-' + arr_airport.upper() + '-' + str(fl_num) + '-' + str(counter),
                   'displayOrder': counter, 'flightNumbers': fl_num,
                   'departureAirports': dep_airport, 'arrivalAirports': arr_airport,
                   'itemCategories[0].displayOrder': 0, 'itemCategories[0].categoryId': line1,
                   'itemCategories[1].displayOrder': 1, 'itemCategories[1].categoryId': line2,
                   'itemCategories[2].displayOrder': 2, 'itemCategories[2].categoryId': line3,
                   '_csrf': csrf}
        session.post(URLs.URL_catering_create_lineitem, content)

    fl_num = '0' * (4 - len(str(fl_num))) + str(fl_num)

    if arr_airport == 'DEL':  # Delhi menu
        create_one_item(300,  '98',  '94', '131')  # appetizer wine beverages
        create_one_item(301,  '99',  '94', '131')  # cold_starter wine beverages
        create_one_item(302, '101',  '94', '131')  # main_delhi wine beverages
        create_one_item(303, '361', '121', '122')  # dessert tea coffee
        create_one_item(304, '101',  '94', '131')  # main_delhi wine beverages (2nd round)

    elif duration == '6hrs_plus':
        for id in range(112, 117):
            create_one_item(id-12, str(id), '94', '131')  # xxx wine beverages
        create_one_item(105, '117', '121', '122')  # dessert tea coffee
        create_one_item(106, '118', '131', '122')  # 2nd_round beverages coffee

    elif duration == '2-6hrs' and morning == 1:  # 2-6hrs breakfast
        create_one_item(200,  '94', '131', '121')  # wine beverages tea
        create_one_item(201,  '93',  '94', '131')  # cold_starter wine beverages
        create_one_item(202,  '92',  '94', '131')  # main_course wine beverages
        create_one_item(203, '374', '121', '122')  # dessert tea coffee

    elif duration == '2-6hrs' and morning == 0:
        create_one_item(300,  '98',  '94', '131')  # appetizer wine beverages
        create_one_item(301,  '99',  '94', '131')  # cold_starter wine beverages
        create_one_item(302, '100',  '94', '131')  # main_course wine beverages
        create_one_item(303, '361', '121', '122')  # dessert tea coffee


def create_items_by_table(session, dataframe):  # generate bunch of flight's LI from pandas DF with flight settings
    data = dataframe[dataframe['individual menu'] == 1].values
    for row in data:
        sub_menu_ids = utils.get_subcatgegories_ids(session, utils.get_category_id(session, row[1]))
        create_line_items_ind(session, row[0], row[1], row[2], row[7], row[12], sub_menu_ids)

    data_base = dataframe[dataframe['individual menu'] == 0].values
    for row in data_base:
        create_line_items_base(session, row[0], row[1], row[2], row[7], row[12])


df = pd.read_csv('/Volumes/data/code/SITA_PycharmProjects/catering/AFL_routes_2019_05_27.csv')
session = auth.SessionCrewTabPortal('https://admin-su-qa.crewplatform.aero/')
session.authentication()

itf = CatInterface('https://admin-su-qa.crewplatform.aero/')