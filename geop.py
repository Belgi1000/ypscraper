import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import threading
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="brucy688@gmail.com")

main_list = []

def extract(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup.find_all('div', class_ = 'listing__content__wrap--flexed jsGoToMp')

def transform(articles):
    for item in articles:
        name = item.find('a', class_ ='listing__name--link listing__link jsListingName').text
        try:
            street = item.find('span', {'itemprop':'streetAddress'}).text
        except:
            street = ''
        try:
            city = item.find('span', {'itemprop':'addressLocality'}).text
        except:
            city = ''
        try:   
            province = item.find('span', {'itemprop':'addressRegion'}).text
        except:
            province = ''
        try:
            postCode = item.find('span', {'itemprop':'postalCode'}).text
        except:
            postCode = ''
        try:
            phone = item.find('li', class_ = 'mlr__submenu__item').text.strip()
        except:
            phone = ''
        try:
            
            def search_geo():
                global location
                location = geolocator.geocode(street + ' ' + city)
            print(street + ' ' + city)
            thread = threading.Thread(target=search_geo)
            thread.start()
            thread.join()
            slatitude = location.latitude
        except:
            slatitude = ''
        try:
            thread = threading.Thread(target=search_geo)
            thread.start()
            thread.join()
            slongitude = location.longitude
        except:
            slongitude = ''

        business = {
            'name': name,
            'street': street,
            'city': city,
            'province': province,
            'postCode': postCode,
            'phone': phone,
            'slongitude': slongitude,
            'slatitude': slatitude
        }
        main_list.append(business)
    return

def load():
    df = pd.DataFrame(main_list)
    df.to_csv('repairshopsbc', index=False)

for x in range(1,2):
    print(f'Getting page {x}')
    articles = extract(f'https://www.yellowpages.ca/search/si/{x}/car+repair/British+Columbia+BC')
    transform(articles)
    time.sleep(5)

load()
print('Saved to CSV')