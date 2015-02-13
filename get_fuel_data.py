from BeautifulSoup import BeautifulSoup
from prettytable import PrettyTable
import re
import requests
from urllib import unquote


CITY_ID_URL = 'http://www.mypetrolprice.com/petrol-price-in-india.aspx'
FUEL_DATA_URL = 'http://www.mypetrolprice.com/{city_id}/Petrol-price-in-Agartala?FuelType={fuel_type_id}'
FUEL_TYPE_IDS = [('Petrol', 0), ('Diesel', 1), ('AutoGas', 2), ('CNG', 3)]

def find_city_ids(url=CITY_ID_URL):
    '''
    This functions yields a tuple containing
    city name and id.
    '''
    content = requests.get(url).content
    soup = BeautifulSoup(content)
    middle_section = soup.find(id='middle_section')
    cities = middle_section.findAll('li')
    for city in cities:
        href = city.find('a').get('href')
        yield process_city_url(href)

def process_city_url(url):
    '''
    Process city url and return a tuple containing
    city id and its name.
    '''
    id, rest = url.split('/', 1)
    name = unquote(rest.rsplit('-', 1)[-1])
    return name, int(id)

def extract_price(s):
    try:
        return re.search(r'\d+(?:\.\d+)?', s).group()
    except Exception as e:
        return 'NULL'
    

def get_all_city_data(url=FUEL_DATA_URL):
    
    table = PrettyTable(['City'] + [fuel_name for fuel_name, _ in FUEL_TYPE_IDS])
    table.align["City"] = "l"

    for city_name, city_id in sorted(find_city_ids(), key=lambda x: x[0].lower()):
        city_data = [city_name]
        for fuel_name, fuel_type_id in FUEL_TYPE_IDS:
            current_url = url.format(**locals())
            try:
                content = requests.get(current_url).content
                soup = BeautifulSoup(requests.get(current_url).content)
                price_td = soup.find(id='BC_GridView1').find('td')
                price_string = price_td.find('span').getString()
                price = extract_price(price_string)
                city_data.append(price)

            except Exception as e:
                print e
                print city_name, city_id, fuel_name, fuel_type_id
        table.add_row(city_data)
        
    return table


data = get_all_city_data()
print data
