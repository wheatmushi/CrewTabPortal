# manager script for full menu creation
import os
import CatInterface
import CatClasses


url_main = 'https://admin-su-qa.crewplatform.aero/'


routes_table_path = ''
nonbase_menus_path = '/Volumes/data/wrk/catering menu/внебазовые меню/CSVs_to_load'


def create_non_base_menus():
    done = []
    interface = CatInterface.CatInterface(url_main)
    files = [f for f in os.listdir(nonbase_menus_path) if f.endswith('.csv')]
    files.sort()
    top_cats = interface.get_cat_ids('', top=True)
    for file in files:
        cat_name_en = [i for i in top_cats.keys() if file.split('_')[0] in i][0]
        cat_name_ru = top_cats[cat_name_en][2]
        menu = CatClasses.Menu(nonbase_menus_path,
                               file,
                               interface,
                               name_en=cat_name_en,
                               name_ru=cat_name_ru)
        menu.deploy()
        done.append(file)
    print(done)


def create_base_menu(base_menus_path, filename, position):
    interface = CatInterface.CatInterface(url_main)
    menu = CatClasses.Menu(base_menus_path, filename, interface, position)
    menu.deploy()


def create_lineitems():
    interface = CatInterface.CatInterface(url_main, lineitems=True)
    table = CatClasses.LineItemTable(interface)
    table.deploy()


itf = CatInterface.CatInterface(url_main, lineitems=False)

menu = CatClasses.Menu('/Volumes/data/wrk/catering menu/base catering/2021_02_16/CSV_storage',
                       '2-6hrs Breakfast.csv',
                       itf,
                       name_en='2-6hr. Breakfast',
                       name_ru='2-6 часов Завтрак',
                       img_path='/Volumes/data/wrk/catering menu/base catering/2021_02_16/2-6hrs Breakfast_imgs/JPEG')

menu = CatClasses.Menu('/Volumes/data/wrk/catering menu/base catering/2021_02_16/CSV_storage',
                       '2-6hrs Lunch.csv',
                       itf,
                       name_en='2-6hr. Lunch',
                       name_ru='2-6 часов Обед',
                       img_path='/Volumes/data/wrk/catering menu/base catering/2021_02_16/2-6hrs Lunch_imgs/JPEG')

menu = CatClasses.Menu('/Volumes/data/wrk/catering menu/base catering/2021_02_16/CSV_storage',
                       '6hrs_plus.csv',
                       itf,
                       name_en='6+ hours',
                       name_ru='6+ часов',
                       img_path='/Volumes/data/wrk/catering menu/base catering/2021_02_16/6_plus_imgs_jpg')

menu = CatClasses.Menu('/Volumes/data/wrk/catering menu/внебазовые меню/CSV_storage', 'UUS_1.csv',
                       itf, name_en='UUS (ret)', name_ru='UUS (обр)')
