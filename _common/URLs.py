# URLs for CrewTablet portal

# login
URL_login = 'login'

#  FLIGHT DATA
# get base flight data as raw html BY flight_id (DT_RowId)
URL_flights_base_data = 'core/flights/{flight_id}'
# get flight list filtered BY flight_number & departure_airport & arrival_airport & departure_date (2018-10-2) & length
#URL_flights_list = 'core/flights/filter/ajax?draw=1&columns%5B0%5D%5Bdata%5D=flightNumber&columns%5B0%5D%5Bname%5D=flightNumber&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=departureAirport&columns%5B1%5D%5Bname%5D=departureAirport&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=departureDate&columns%5B2%5D%5Bname%5D=departureDate&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D={departure_date}&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=flightStatusLabel&columns%5B3%5D%5Bname%5D=flightStatusLabel&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=arrivalAirport&columns%5B4%5D%5Bname%5D=arrivalAirport&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=details&columns%5B5%5D%5Bname%5D=details&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=2&order%5B0%5D%5Bdir%5D=desc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1568705987759'
URL_flights_list = 'core/flights/filter/ajax?draw=1&columns[0][data]=flightNumber&columns[0][name]=flightNumber&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]={flight_number}&columns[0][search][regex]=false&columns[1][data]=departureAirport&columns[1][name]=departureAirport&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]={departure_airport}&columns[1][search][regex]=false&columns[2][data]=departureDateStart&columns[2][name]=departureDateStart&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]={departure_date}&columns[2][search][regex]=false&columns[3][data]=departureDateEnd&columns[3][name]=departureDateEnd&columns[3][searchable]=true&columns[3][orderable]=false&columns[3][search][value]={departure_date}&columns[3][search][regex]=false&columns[4][data]=flightStatusLabel&columns[4][name]=flightStatusLabel&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=arrivalAirport&columns[5][name]=arrivalAirport&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]={arrival_airport}&columns[5][search][regex]=false&columns[6][data]=regNumber&columns[6][name]=regNumber&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=equipment&columns[7][name]=equipment&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=paxInfoAvailable&columns[8][name]=paxInfoAvailable&columns[8][searchable]=true&columns[8][orderable]=false&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=details&columns[9][name]=details&columns[9][searchable]=false&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&order[0][column]=2&order[0][dir]=desc&start=0&length={length}&search[value]=&search[regex]=false&_=1599725743660'
# get crew list for flight BY flight_id (DT_RowId) & length
URL_flight_crews = 'core/flights/{flight_id}/crew/ajax?draw=1&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=name&columns%5B1%5D%5Bname%5D=name&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=position&columns%5B2%5D%5Bname%5D=position&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=email&columns%5B3%5D%5Bname%5D=email&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1568721552781'


#  USER DATA
# get list of CrewTab users BY length & search_value & is_enabled
URL_users_list = 'admin/users/ajax?draw=1&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=username&columns%5B1%5D%5Bname%5D=username&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=firstName&columns%5B2%5D%5Bname%5D=firstName&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=lastName&columns%5B3%5D%5Bname%5D=lastName&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=lastUpdate&columns%5B4%5D%5Bname%5D=lastUpdate&columns%5B4%5D%5Bsearchable%5D=false&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=image&columns%5B5%5D%5Bname%5D=image&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=display&columns%5B6%5D%5Bname%5D=display&columns%5B6%5D%5Bsearchable%5D=false&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=delete&columns%5B7%5D%5Bname%5D=delete&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=enabled&columns%5B8%5D%5Bname%5D=enabled&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D={is_enabled}&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D={search_value}&search%5Bregex%5D=false&_=1568721349965'
# enable user BY user_id
URL_users_enable = 'admin/users/{user_id}/toggle_lock'
# get CSRF for user password reset BY user_id
URL_users_reset_password_csrf = 'admin/users/{user_id}/reset_password'
# reset user password (POST)
URL_users_reset_password = 'admin/users/%7Bid%7D/reset_password'

#  CATERING DATA
# get list of categories BY length & search_value
URL_catering_categories = 'core/catering/ajax/categories?draw=1&columns[0][data]=name&columns[0][name]=name&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=image&columns[1][name]=image&columns[1][searchable]=false&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=parentCategory&columns[2][name]=parentCategory&columns[2][searchable]=false&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=subcategories&columns[3][name]=subcategories&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=backgroundColor&columns[4][name]=backgroundColor&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=foregroundColor&columns[5][name]=foregroundColor&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=multipleChoice&columns[6][name]=multipleChoice&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=position&columns[7][name]=position&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=lastUpdate&columns[8][name]=lastUpdate&columns[8][searchable]=false&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=details&columns[9][name]=details&columns[9][searchable]=false&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]={search_value}&search[regex]=false&_=1553694425077'
# get list of SUBcategories BY parent_category_id & length & search_value
URL_catering_subcategories = 'core/catering/ajax/category/subcategories/{parent_category_id}?draw=1&columns[0][data]=name&columns[0][name]=name&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=image&columns[1][name]=image&columns[1][searchable]=false&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=parentCategory&columns[2][name]=parentCategory&columns[2][searchable]=false&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=subcategories&columns[3][name]=subcategories&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=backgroundColor&columns[4][name]=backgroundColor&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=foregroundColor&columns[5][name]=foregroundColor&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=multipleChoice&columns[6][name]=multipleChoice&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=position&columns[7][name]=position&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=lastUpdate&columns[8][name]=lastUpdate&columns[8][searchable]=false&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=details&columns[9][name]=details&columns[9][searchable]=false&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]={search_value}&search[regex]=false&_=1553695423178'
# get list of line items BY length & search_value
URL_catering_lineitems = 'core/catering/line_items/ajax?draw=2&columns[0][data]=name&columns[0][name]=name&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=displayOrder&columns[1][name]=displayOrder&columns[1][searchable]=false&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=flightNumbers&columns[2][name]=flightNumbers&columns[2][searchable]=false&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=departureAirports&columns[3][name]=departureAirports&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=arrivalAirports&columns[4][name]=arrivalAirports&columns[4][searchable]=false&columns[4][orderable]=false&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=itemCategories&columns[5][name]=itemCategories&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=display&columns[6][name]=display&columns[6][searchable]=false&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]={search_value}&search[regex]=false&_=1553776137482'
# get list of items BY length & search_value
URL_catering_items = 'core/catering/items/ajax?draw=16&columns[0][data]=name_translations&columns[0][name]=name_translations&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=description_translations&columns[1][name]=description_translations&columns[1][searchable]=false&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=shortName&columns[2][name]=shortName&columns[2][searchable]=false&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=image&columns[3][name]=image&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=category&columns[4][name]=category&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=position&columns[5][name]=position&columns[5][searchable]=false&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=validityStart&columns[6][name]=validityStart&columns[6][searchable]=false&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=validityEnd&columns[7][name]=validityEnd&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=display&columns[8][name]=display&columns[8][searchable]=false&columns[8][orderable]=false&columns[8][search][value]=&columns[8][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]={search_value}&search[regex]=false&_=1614860624446'
# get list of items in category BY category_id & length & search_value
URL_catering_items_in_cat = 'core/catering/ajax/category/items/{category_id}?draw=7&columns%5B0%5D%5Bdata%5D=name_translations&columns%5B0%5D%5Bname%5D=name_translations&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=description_translations&columns%5B1%5D%5Bname%5D=description_translations&columns%5B1%5D%5Bsearchable%5D=false&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=shortName&columns%5B2%5D%5Bname%5D=shortName&columns%5B2%5D%5Bsearchable%5D=false&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=image&columns%5B3%5D%5Bname%5D=image&columns%5B3%5D%5Bsearchable%5D=false&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=category&columns%5B4%5D%5Bname%5D=category&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=position&columns%5B5%5D%5Bname%5D=position&columns%5B5%5D%5Bsearchable%5D=false&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=validityStart&columns%5B6%5D%5Bname%5D=validityStart&columns%5B6%5D%5Bsearchable%5D=false&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=validityEnd&columns%5B7%5D%5Bname%5D=validityEnd&columns%5B7%5D%5Bsearchable%5D=false&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=display&columns%5B8%5D%5Bname%5D=display&columns%5B8%5D%5Bsearchable%5D=false&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D={search_value}&search%5Bregex%5D=false&_=1590751268918'
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
# edit item options (POST)
URL_catering_add_options = 'core/catering/items/%7BidItem%7D/options/%7BidOption%7D'

# confirm delete item BY item_id
URL_catering_delete_item_confirm = 'core/catering/items/delete_confirmed/{item_id}'
# confirm line item deletion BY lineitem_id
URL_catering_delete_lineitem_confirm = 'core/catering/line_items/delete_confirm/{lineitem_id}'
# confirm delete category BY category_id
URL_catering_delete_category_confirm = 'core/catering/categories/delete_confirmed/{category_id}'
# confirm delete option BY option_id
URL_catering_delete_option = 'core/catering/items/option/delete_confirmed/{option_id}'

# CATERING STATS
# get list of catering closed sessions BY flight_number & departure_airport & date_start & date_end & length
get_catering_closed_sessions = 'core/catering/sessions/ajax?draw=2&columns[0][data]=flightNumber&columns[0][name]=flightNumber&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]={flight_number}&columns[0][search][regex]=false&columns[1][data]=departureAirport&columns[1][name]=departureAirport&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]={departure_airport}&columns[1][search][regex]=false&columns[2][data]=arrivalAirport&columns[2][name]=arrivalAirport&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=earliestLocalDepartureDate&columns[3][name]=earliestLocalDepartureDate&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]={date_start}&columns[3][search][regex]=false&columns[4][data]=latestLocalDepartureDate&columns[4][name]=latestLocalDepartureDate&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]={date_end}&columns[4][search][regex]=false&columns[5][data]=aircraftType&columns[5][name]=aircraftType&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=amountOfCrewOperated&columns[6][name]=amountOfCrewOperated&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=amountOfOrders&columns[7][name]=amountOfOrders&columns[7][searchable]=false&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=amountOfOrdersServed&columns[8][name]=amountOfOrdersServed&columns[8][searchable]=false&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=display&columns[9][name]=display&columns[9][searchable]=false&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={length}&search[value]=&search[regex]=false&_=1613643937998'


#  MONITORING DATA
# user syncs from flight status monitor BY staff_id & departure_airport & flight_number & departure_date & length
URL_monitor_syncs = 'core/monitoring/ajax/flight_status_monitor/search?draw=1&columns%5B0%5D%5Bdata%5D=staffId&columns%5B0%5D%5Bname%5D=staffId&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D={staff_id}&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=flightNumber&columns%5B1%5D%5Bname%5D=flightNumber&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=departureAirport&columns%5B2%5D%5Bname%5D=departureAirport&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D={departure_airport}&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=arrivalAirport&columns%5B3%5D%5Bname%5D=arrivalAirport&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=departureDate&columns%5B4%5D%5Bname%5D=departureDate&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D={departure_date}&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=scheduledDepartureDateTime&columns%5B5%5D%5Bname%5D=scheduledDepartureDateTime&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=synchronizationDate&columns%5B6%5D%5Bname%5D=synchronizationDate&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=lastUpdate&columns%5B7%5D%5Bname%5D=lastUpdate&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=deviceId&columns%5B8%5D%5Bname%5D=deviceId&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=bookedCount&columns%5B9%5D%5Bname%5D=bookedCount&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=checkinCount&columns%5B10%5D%5Bname%5D=checkinCount&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=boardedCount&columns%5B11%5D%5Bname%5D=boardedCount&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1575543569584'
# get posted reports records (different URLs for Aeroflot and Rossiya) BY
# start_date & end_date & staff_id & form_id & departure_airport & arrival_airport & flight_number & reg_number & length
URL_monitor_reports_SU = 'core/forms/ajax/search?draw=2&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=id&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=staffId&columns%5B1%5D%5Bname%5D=staffId&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D={staff_id}&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=formTitle&columns%5B2%5D%5Bname%5D=formTitle&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=flightNumber&columns%5B3%5D%5Bname%5D=flightNumber&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=departureAirport&columns%5B4%5D%5Bname%5D=departureAirport&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D={dep_airport}&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=arrivalAirport&columns%5B5%5D%5Bname%5D=arrivalAirport&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D={arr_airport}&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=regNumber&columns%5B6%5D%5Bname%5D=regNumber&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D={reg_number}&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=departureDate&columns%5B7%5D%5Bname%5D=departureDate&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=departureDateEnd&columns%5B8%5D%5Bname%5D=departureDateEnd&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=lastUpdate&columns%5B9%5D%5Bname%5D=lastUpdate&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D={start_date}&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=lastUpdateEnd&columns%5B10%5D%5Bname%5D=lastUpdateEnd&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D={end_date}%2023%3A59%3A59&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=formId&columns%5B11%5D%5Bname%5D=formId&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=false&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D={form_id}&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=manualProcessingProcessedDate&columns%5B12%5D%5Bname%5D=manualProcessingProcessedDate&columns%5B12%5D%5Bsearchable%5D=false&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=manualProcessingStaffId&columns%5B13%5D%5Bname%5D=manualProcessingStaffId&columns%5B13%5D%5Bsearchable%5D=false&columns%5B13%5D%5Borderable%5D=true&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=download&columns%5B14%5D%5Bname%5D=download&columns%5B14%5D%5Bsearchable%5D=false&columns%5B14%5D%5Borderable%5D=false&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=9&order%5B0%5D%5Bdir%5D=desc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1577348010703'
URL_monitor_reports_FV = 'core/forms/ajax/search?draw=2&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=id&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=staffId&columns%5B1%5D%5Bname%5D=staffId&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D={staff_id}&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=formTitle&columns%5B2%5D%5Bname%5D=formTitle&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=flightNumber&columns%5B3%5D%5Bname%5D=flightNumber&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D={flight_number}&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=departureAirport&columns%5B4%5D%5Bname%5D=departureAirport&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D={dep_airport}&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=arrivalAirport&columns%5B5%5D%5Bname%5D=arrivalAirport&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D={arr_airport}&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=regNumber&columns%5B6%5D%5Bname%5D=regNumber&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D={reg_number}&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=departureDate&columns%5B7%5D%5Bname%5D=departureDate&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=departureDateEnd&columns%5B8%5D%5Bname%5D=departureDateEnd&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=lastUpdate&columns%5B9%5D%5Bname%5D=lastUpdate&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D={start_date}&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=lastUpdateEnd&columns%5B10%5D%5Bname%5D=lastUpdateEnd&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=true&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D={end_date}%2023%3A59%3A59&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=formId&columns%5B11%5D%5Bname%5D=formId&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=false&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D={form_id}&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=download&columns%5B12%5D%5Bname%5D=download&columns%5B12%5D%5Bsearchable%5D=false&columns%5B12%5D%5Borderable%5D=false&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=9&order%5B0%5D%5Bdir%5D=desc&start=0&length={length}&search%5Bvalue%5D=&search%5Bregex%5D=false&_=1575885055120'

