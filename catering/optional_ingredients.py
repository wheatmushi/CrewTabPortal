# tool for optional ingredients addition, add ingredient for all items in categories with related category_name
import CatInterface


url_main = 'https://admin-su-qa.crewplatform.aero/'
itf = CatInterface.CatInterface(url_main, lineitems=False)

category_name = 'Soup'  # text to search in categories names
ingr_name_en = 'separate dressing'
ingr_name_ru = 'заправка отдельно'
ingr_short_name = 'з/о'

cats = list(itf.get_cat_ids(category_name, exactly=True, key='row_id').keys())
while cats:
    c = cats.pop()
    print('modifying category {}'.format(c))
    items = list(itf.get_items_in_subcat(c, search_value='', by='id').keys())
    while items:
        i = items.pop()
        itf.add_option(i, ingr_name_en, ingr_name_ru, ingr_short_name)
