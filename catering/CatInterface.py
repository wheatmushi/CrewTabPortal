# interface for operating with CrewTab portal Catering section

import json
import os
import sys
from bs4 import BeautifulSoup
sys.path.insert(1, os.path.join('..', '_common'))

import URLs
import auth


class CatInterface:
    def __init__(self, url_main, lineitems=False):
        self.url_main = url_main
        self.session = auth.SessionCrewTabPortal(url_main)
        self.session.authentication()
        if lineitems:
            self.default_cats = self.get_default_cats()

    def get_cat_ids(self, search_value, exactly=False, top=False, key='name_en', just_id=False):  # get top-lvl category ID
        cat_list = self.session.get(URLs.URL_catering_categories.format(length=1000, search_value=search_value).
                                    replace('+', '%2B'))
        cat_list = json.loads(cat_list.content)['data']
        if top:
            cat_list = [c for c in cat_list if c['parentCategory'] == '-']
        cat_dict = {}
        for cat in cat_list:
            pos = cat['position']
            row_id = cat['DT_RowId'].replace(',', '')
            name = BeautifulSoup(cat['name'], 'html.parser').text.split('\n')
            name_en = name[0].replace('English: ', '')
            name_ru = name[1].replace('Russian: ', '')
            if exactly is False or exactly is True and (search_value in (name_ru, name_en)):
                if key == 'name_en':
                    cat_dict[name_en] = (row_id, pos, name_ru)
                elif key == 'row_id':
                    cat_dict[row_id] = (name_en, pos, name_ru)
        if len(cat_dict) == 0:
            print('no cats found!!')
        if len(cat_dict) > 1 and exactly is True:
            print('wow even more than one cat found!!')
        if len(cat_dict) == 1 and just_id and key == 'row_id':
            return cat_dict.popitem()[0]
        return cat_dict

    def get_subcat_ids(self, parent_cat_id, search_value='', exactly=False, key='row_id'):  # get sub-categories IDs
        subcat_list = self.session.get(URLs.URL_catering_subcategories.format(parent_category_id=parent_cat_id,
                                                                              length=100, search_value=search_value))
        subcat_list = json.loads(subcat_list.content)['data']
        subcat_dict = {}
        for cat in subcat_list:
            pos = cat['position']
            row_id = cat['DT_RowId'].replace(',', '')
            name = BeautifulSoup(cat['name'], 'html.parser').text.split('\n')
            name_en = name[0].replace('English: ', '')
            name_ru = name[1].replace('Russian: ', '')
            if exactly is False or exactly is True and (search_value in (name_ru, name_en)):
                if key == 'row_id':
                    subcat_dict[row_id] = (pos, name_en, name_ru)
                elif key == 'name_en':
                    subcat_dict[name_en] = (pos, row_id, name_ru)
        if len(subcat_dict) == 0:
            print('no subcats found!!')
        return subcat_dict

    def get_default_cats(self):  # get IDs for wines, beverages, tea, coffee, 2-6_morn, 2-6_lunch, 6h+ cats
        default_cats = ['Wine & Champagne', 'Beverages', 'Tea', 'Coffee']
        base_menus = ['2-6hr. Breakfast', '2-6hr. Lunch', '6+ hours']
        default_cats = {cat: self.get_cat_ids(cat, exactly=True)[cat][0] for cat in default_cats}
        default_cats = {'Common': default_cats}
        for menu in base_menus:
            row_id = self.get_cat_ids(menu, exactly=True)[menu][0]
            cats = self.get_subcat_ids(row_id, key='name_en')
            default_cats[menu] = {name: c[1] for name, c in cats.items()}
        return default_cats

    def get_items_in_subcat(self, subcat_id, search_value='', by='pos'):
        items_list = self.session.get(URLs.URL_catering_items_in_cat.format(category_id=subcat_id,
                                                                            length=100, search_value=search_value))
        items_list = json.loads(items_list.content)['data']
        items_dict = {}
        for item in items_list:
            pos = item['position']
            row_id = item['DT_RowId'].replace(',', '')
            name = BeautifulSoup(item['name_translations'], 'html.parser').text.split('\n')
            name_en = name[0].replace('English: ', '').casefold()
            name_ru = name[1].replace('Russian: ', '').casefold()
            if search_value.casefold() in name_ru or search_value.casefold() in name_en:
                if by == 'pos':
                    items_dict[pos] = (row_id, name_en, name_ru)
                elif by == 'id':
                    items_dict[row_id] = (pos, name_en, name_ru)
        if len(items_dict) == 0:
            print('no items found in subcat {}!!'.format(subcat_id))
        return items_dict

    def get_lineitems(self, search_value):  # returns line items with 'search_value' in name
        lineitems_list = self.session.get(URLs.URL_catering_lineitems.format(length=5000, search_value=search_value))
        lineitems_list = json.loads(lineitems_list.content)['data']
        print('from filtered {} first 5 lineitems: {}'.format(len(lineitems_list),
                                                              ', '.join([item['name'] for item in lineitems_list[:5]])))
        return [item['DT_RowId'].replace(',', '') for item in lineitems_list]

    def create_cat(self, data, position, name_en, name_ru, parent_cat_id='', parent_cat_name='', confirm=True):
        if parent_cat_id == '':
            print('creating top-level cat with name {} / {} in position {}'.format(name_en, name_ru, position))
        else:
            print('creating subcat {} / {} in cat {} {}'.format(name_en, name_ru, parent_cat_id, parent_cat_name))
        if confirm is False or input('ok? y/n') == 'y':
            csrf = self.session.get_csrf(URLs.URL_catering_create_category)
            data['_csrf'] = csrf
            return self.session.post(URLs.URL_catering_create_category, data=data)

    def modify_item(self, subcat_id, data, file, action, item_id='', confirm=True):  # create or modify item with prepared data
        print('{} item {} in cat {}'.format(action, data['name[1].value'], subcat_id))
        if confirm is False or input('ok? y/n') == 'y':
            if action == 'creating':
                url_1 = url_2 = URLs.URL_catering_create_item
            elif action == 'modifying':
                url_1 = URLs.URL_catering_edit_item.format(item_id=item_id)
                url_2 = URLs.URL_catering_update_item
            else:
                print('incorrect action for creating/modifying item')
                return 0
            csrf = self.session.get_csrf(url_1)
            data['_csrf'] = csrf
            return self.session.post(url_2, data=data, files=file)

    def create_lineitem(self, name, data):
        csrf = self.session.get_csrf(URLs.URL_catering_create_lineitem)
        print('creating lineitem {}'.format(name))
        data['_csrf'] = csrf
        return self.session.post(URLs.URL_catering_create_lineitem, data=data)

    def delete_cat(self, cat_id, cat_name, confirm=True):
        if self.get_items_in_subcat(cat_id):
            print('trying to delete cat {} but category not empty!'.format(cat_name))
            return 0
        else:
            print('deleting category {}'.format(cat_name))
            if confirm is False or input('ok? y/n') == 'y':
                self.session.get(URLs.URL_catering_delete_category_confirm.format(category_id=cat_id))

    def delete_item(self, item_id, confirm=True):
        print('deleting item {}'.format(item_id))
        if confirm is False or input('ok? y/n') == 'y':
            self.session.get(URLs.URL_catering_delete_item_confirm.format(item_id=item_id))

    def delete_lineitems(self, search_value, confirm=True):
        lineitems = self.get_lineitems(search_value)
        if confirm is False or input('delete this line items? y/n') == 'y':
            for item in lineitems:
                self.session.get(URLs.URL_catering_delete_lineitem_confirm.format(lineitem_id=item))

    def edit_allergens(self, name, item_id):
        name_to_num = {'nuts': 4, 'gluten': 5, 'lactose': 6, 'fish': 8, 'eggs': 22, 'milk': 25, 'mustard': 28,
                       'clams': 31, 'soy': 34, 'cereals': 37, 'sesame': 40, 'celery': 43, 'shrimps': 46,
                       'sesame oil': 49, 'anchovies': 52, 'wheat flour': 55, 'salmon': 58, 'oysters': 61,
                       'sour cream': 64}
        print('modifying allergen: {}'.format(name))
        csrf = self.session.get_csrf(URLs.URL_catering_item.format(item_id=item_id))
        data = {'_csrf': csrf, 'cateringItemId': item_id, 'allergenId': name_to_num[name.casefold()],
                'cateringAllergensTable_length': 10}
        p = self.session.post(URLs.URL_catering_edit_allergens.format(item_id=item_id), data=data)
        if 'Update successful' not in str(p.content):
            print('allergen', name, 'was not added to item', item_id)
        return p

    def get_item(self, search_value, exactly=True):
        items = self.session.get(URLs.URl_catering_items.format(search_value=search_value, length=30))
        items = json.loads(items.content)['data']
        items = [i for i in items if search_value in i['description_translations']]
        if len(items) == 0:
            print('no items found')
            return None
        elif len(items) > 1:
            print('more than one item found')
            return None
        else:
            return items[0]['DT_RowId'].replace(',', '')

    def get_allergens(self, item_id, search_value='', length=20):
        allergens = self.session.get(URLs.URL_catering_allergens.format(item_id=item_id, search_value=search_value, length=length))
        allergens = json.loads(allergens.content)['data']
        allergens = [BeautifulSoup(a['name_translations'], 'html.parser').text.split()[1].casefold() for a in allergens]
        return allergens

    def delete_whole_menu(self, search_value):  # recursively delete top level category with all content
        parent_cat = self.get_cat_ids(search_value, exactly=True)
        parent_cat_name = list(parent_cat.keys())[0]
        parent_cat_id = parent_cat[parent_cat_name][0]
        print('we\'re about to delete whole {} {} menu'.format(parent_cat_id, parent_cat_name))
        if input('ok? y/n') == 'y':
            subcat_ids = self.get_subcat_ids(parent_cat_id)
            for subcat_id, subcat in subcat_ids.items():
                items = self.get_items_in_subcat(subcat_id, by='id')
                for item_id, item in items.items():
                    print("deleting", item[2])
                    self.delete_item(item_id, confirm=False)
                self.delete_cat(subcat_id, subcat[1], confirm=False)
            self.delete_cat(parent_cat_id, parent_cat_name, confirm=False)