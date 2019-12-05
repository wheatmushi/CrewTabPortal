# URLs for CrewTablet portal

# login
URL_login = 'login'

#  FLIGHT DATA
# get base flight data as raw html BY flight_id (DT_RowId)
URL_flights_base_data = 'core/flights/{flight_id}'
# get flight list filtered BY flight_number & departure_date (2018-10-2) & length
URL_flights_list = 'core/flights/filter/ajax?draw=1&columns%5B0%5D%5Bdata%5D=flightNumber&columns%5B0%5D%5Bname%5D=flightNumber&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=departureAirport&columns%5B1%5D%5Bname%5D=departureAirport&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=departureDate&columns%5B2%5D%5Bname%5D=departureDate&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D={departure_date}&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=flightStatusLabel&columns%5B3%5D%5Bname%5D=flightStatusLabel&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=arrivalAirport&columns%5B4%5D%5Bname%5D=arrivalAirport&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=details&columns%5B5%5D%5Bname%5D=details&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=2&order%5B0%5D%5Bdir%5D=desc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1568705987759'
# get crew list for flight BY flight_id (DT_RowId) & length
URL_flight_crews = 'core/flights/{flight_id}/crew/ajax?draw=1&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=name&columns%5B1%5D%5Bname%5D=name&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=position&columns%5B2%5D%5Bname%5D=position&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=email&columns%5B3%5D%5Bname%5D=email&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1568721552781'


#  USER DATA
# get list of CrewTab users BY length & search_value & is_enabled
URL_users_list = 'admin/users/ajax?draw=1&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=username&columns%5B1%5D%5Bname%5D=username&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=firstName&columns%5B2%5D%5Bname%5D=firstName&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=lastName&columns%5B3%5D%5Bname%5D=lastName&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=lastUpdate&columns%5B4%5D%5Bname%5D=lastUpdate&columns%5B4%5D%5Bsearchable%5D=false&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=image&columns%5B5%5D%5Bname%5D=image&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=display&columns%5B6%5D%5Bname%5D=display&columns%5B6%5D%5Bsearchable%5D=false&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=delete&columns%5B7%5D%5Bname%5D=delete&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=enabled&columns%5B8%5D%5Bname%5D=enabled&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D={is_enabled}&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D={search_value}&search%5Bregex%5D=false&_=1568721349965'


#  CATERING DATA
# get list of categories BY length & search_value
URL_catering_categories = 'core/catering/ajax/categories?draw=1&columns[0][data]=name&columns[0][name]=name&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=image&columns[1][name]=image&columns[1][searchable]=false&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=parentCategory&columns[2][name]=parentCategory&columns[2][searchable]=false&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=subcategories&columns[3][name]=subcategories&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=backgroundColor&columns[4][name]=backgroundColor&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=foregroundColor&columns[5][name]=foregroundColor&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=multipleChoice&columns[6][name]=multipleChoice&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=position&columns[7][name]=position&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=lastUpdate&columns[8][name]=lastUpdate&columns[8][searchable]=false&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=details&columns[9][name]=details&columns[9][searchable]=false&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]={search_value}&search[regex]=false&_=1553694425077'
# get list of SUBcategories BY parent_category_id & length & search_value
URL_catering_subcategories = 'core/catering/ajax/category/subcategories/{parent_category_id}?draw=1&columns[0][data]=name&columns[0][name]=name&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=image&columns[1][name]=image&columns[1][searchable]=false&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=parentCategory&columns[2][name]=parentCategory&columns[2][searchable]=false&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=subcategories&columns[3][name]=subcategories&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=backgroundColor&columns[4][name]=backgroundColor&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=foregroundColor&columns[5][name]=foregroundColor&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=multipleChoice&columns[6][name]=multipleChoice&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=position&columns[7][name]=position&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=lastUpdate&columns[8][name]=lastUpdate&columns[8][searchable]=false&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=details&columns[9][name]=details&columns[9][searchable]=false&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]={search_value}&search[regex]=false&_=1553695423178'
# get list of line items BY length & search_value
URL_catering_lineitems = 'core/catering/line_items/ajax?draw=2&columns[0][data]=name&columns[0][name]=name&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=displayOrder&columns[1][name]=displayOrder&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=flightNumbers&columns[2][name]=flightNumbers&columns[2][searchable]=false&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=departureAirports&columns[3][name]=departureAirports&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=arrivalAirports&columns[4][name]=arrivalAirports&columns[4][searchable]=false&columns[4][orderable]=false&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=itemCategories&columns[5][name]=itemCategories&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=display&columns[6][name]=display&columns[6][searchable]=false&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]={search_value}&search[regex]=false&_=1553776137482'
# get list of items BY length and search_value
URL_catering_items = 'core/catering/items/ajax?draw=1&columns%5B0%5D%5Bdata%5D=name_translations&columns%5B0%5D%5Bname%5D=name_translations&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=description_translations&columns%5B1%5D%5Bname%5D=description_translations&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=shortName&columns%5B2%5D%5Bname%5D=shortName&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=image&columns%5B3%5D%5Bname%5D=image&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=category&columns%5B4%5D%5Bname%5D=category&columns%5B4%5D%5Bsearchable%5D=false&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=allergens&columns%5B5%5D%5Bname%5D=allergens&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=limitedQuantity&columns%5B6%5D%5Bname%5D=limitedQuantity&columns%5B6%5D%5Bsearchable%5D=false&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=availableOnAllFlights&columns%5B7%5D%5Bname%5D=availableOnAllFlights&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=gmPreparationRequired&columns%5B8%5D%5Bname%5D=gmPreparationRequired&columns%5B8%5D%5Bsearchable%5D=false&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=displayOnBeverageSummary&columns%5B9%5D%5Bname%5D=displayOnBeverageSummary&columns%5B9%5D%5Bsearchable%5D=false&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=showInHistory&columns%5B10%5D%5Bname%5D=showInHistory&columns%5B10%5D%5Bsearchable%5D=false&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=color&columns%5B11%5D%5Bname%5D=color&columns%5B11%5D%5Bsearchable%5D=false&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=position&columns%5B12%5D%5Bname%5D=position&columns%5B12%5D%5Bsearchable%5D=false&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=display&columns%5B13%5D%5Bname%5D=display&columns%5B13%5D%5Bsearchable%5D=false&columns%5B13%5D%5Borderable%5D=false&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D={search_value}&search%5Bregex%5D=false&_=1569323243758'
# get list of items in category BY category_id & length & search_value
URL_catering_items_in_cat = 'core/catering/ajax/category/items/{category_id}?draw=1&columns%5B0%5D%5Bdata%5D=name_translations&columns%5B0%5D%5Bname%5D=name_translations&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=description_translations&columns%5B1%5D%5Bname%5D=description_translations&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=shortName&columns%5B2%5D%5Bname%5D=shortName&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=image&columns%5B3%5D%5Bname%5D=image&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=category&columns%5B4%5D%5Bname%5D=category&columns%5B4%5D%5Bsearchable%5D=false&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=allergens&columns%5B5%5D%5Bname%5D=allergens&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=limitedQuantity&columns%5B6%5D%5Bname%5D=limitedQuantity&columns%5B6%5D%5Bsearchable%5D=false&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=availableOnAllFlights&columns%5B7%5D%5Bname%5D=availableOnAllFlights&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=gmPreparationRequired&columns%5B8%5D%5Bname%5D=gmPreparationRequired&columns%5B8%5D%5Bsearchable%5D=false&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=displayOnBeverageSummary&columns%5B9%5D%5Bname%5D=displayOnBeverageSummary&columns%5B9%5D%5Bsearchable%5D=false&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=showInHistory&columns%5B10%5D%5Bname%5D=showInHistory&columns%5B10%5D%5Bsearchable%5D=false&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=color&columns%5B11%5D%5Bname%5D=color&columns%5B11%5D%5Bsearchable%5D=false&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=position&columns%5B12%5D%5Bname%5D=position&columns%5B12%5D%5Bsearchable%5D=false&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=display&columns%5B13%5D%5Bname%5D=display&columns%5B13%5D%5Bsearchable%5D=false&columns%5B13%5D%5Borderable%5D=false&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D={search_value}&search%5Bregex%5D=false&_=1569675124394'
# get list of allergens for one item BY item_id & search_value & length
URL_catering_allergens = 'core/catering/items/allergens/{item_id}?draw=1&columns%5B0%5D%5Bdata%5D=name_translations&columns%5B0%5D%5Bname%5D=name_translations&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=image&columns%5B1%5D%5Bname%5D=image&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=display&columns%5B2%5D%5Bname%5D=display&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=20&search%5Bvalue%5D={search_value}&search%5Bregex%5D=false&_=1573130514047'

# get one item BY item_id
URL_catering_item = 'core/catering/items/display/{item_id}'

# create new line item (POST)
URL_catering_create_lineitem = 'core/catering/line_items/create'
# create new item (POST)
URL_catering_create_item = 'core/catering/items/add'
# create new category (POST)
URL_catering_create_category = 'core/catering/categories/add'

# delete line item BY lineitem_id
URL_catering_delete_lineitem = 'core/catering/line_items/delete/{lineitem_id}'
# delete item BY item_id
URL_catering_delete_item = 'core/catering/items/delete_confirmed/{item_id}'

# edit item (POST)
URL_catering_update_item = 'core/catering/items/update'
# edit item (get csrf) BY item_id
URL_catering_edit_item = 'core/catering/items/edit/{item_id}'
# edit item allergens BY item_id (POST)
URL_catering_edit_allergens = 'core/catering/items/related_allergens/{item_id}'

# confirm delete item BY item_id
URL_catering_delete_item_confirm = 'core/catering/items/delete_confirmed/{item_id}'
# confirm line item deletion BY lineitem_id
URL_catering_delete_lineitem_confirm = 'core/catering/line_items/delete_confirm/{lineitem_id}'
# confirm delete category BY category_id
URL_catering_delete_category_confirm = 'core/catering/categories/delete_confirmed/{category_id}'


#  MONITORING DATA
# user syncs from flight status monitor BY staff_id & departure_airport & flight_number & departure_date & length
URL_monitor_syncs = 'core/monitoring/ajax/flight_status_monitor/search?draw=1&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D={staff_id}&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=flightNumber&columns%5B1%5D%5Bname%5D=flightNumber&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=departureAirport&columns%5B2%5D%5Bname%5D=departureAirport&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D={departure_airport}&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=arrivalAirport&columns%5B3%5D%5Bname%5D=arrivalAirport&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=departureDate&columns%5B4%5D%5Bname%5D=departureDate&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D={departure_date}&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=scheduledDepartureDateTime&columns%5B5%5D%5Bname%5D=scheduledDepartureDateTime&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=synchronizationDate&columns%5B6%5D%5Bname%5D=synchronizationDate&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=lastUpdate&columns%5B7%5D%5Bname%5D=lastUpdate&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=deviceId&columns%5B8%5D%5Bname%5D=deviceId&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=bookedCount&columns%5B9%5D%5Bname%5D=bookedCount&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=checkinCount&columns%5B10%5D%5Bname%5D=checkinCount&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=boardedCount&columns%5B11%5D%5Bname%5D=boardedCount&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1575543569584'

'''
admin/users/ajax
admin/users/create
admin/users/{}
admin/users/{}/delete
admin/users/{}/edit
admin/users/{}/reset_password

core/monitoring/manifests
core/monitoring/flight_status_monitor
core/monitoring/ajax/manifests       
core/monitoring/manifest/download/{}
core/monitoring/ajax/flight_status_monitor/search
'''
