import datetime
from requests import get
from json import loads
from terminaltables import AsciiTable

CITIES = []

def get_city ():    
    list_city = []
    url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
    response = (get(url))
    for i in (loads(response.text)):
        city = extract_city(i['stationName'])
        if city in CITIES:
            list_city.append (i['stationName'])          
    return (list_city)

def get_id():
    list_id = []
    url = 'https://api.gios.gov.pl/pjp-api/rest/station/findAll'
    response = (get(url))
    for i in (loads(response.text)):
        city = extract_city(i['stationName'])
        if city in CITIES:
            list_id.append (i['id'])            
    return (list_id)

def extract_city (city_with_adress):
    return city_with_adress.split(',')[0]

def air ():   
    list_id = get_id()
    id_air=[]
    for i in list_id:
        url = "https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/%d" % i
        response = (get(url))
        data = (loads(response.text))
        d = (data ['stIndexLevel'])
        id_air.append (d['indexLevelName'])
    return (id_air)

def main_air(): 
    city = get_city()
    id_air = air()
    rows = []
    for c in city:
        for i in id_air:
            rows.append (f"Indeks jakości powietrza: {c}:\n")
            rows.append (F" - jest {i.upper()}.\n")
            break
    print (' '.join(str(i) for i in rows))

def main_weather ():
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    response = get(url)
    rows = [
        ['Miasto', 'Godzina pomiaru', 'Temperatura st. C', 'Opady %', 'Wiatr km/h']
    ]
    for i in (loads(response.text)):
        if i['stacja'] in CITIES:
            rows.append([
                i['stacja'],
                i['godzina_pomiaru'],
                i['temperatura'],
                i['suma_opadu'],
                i['predkosc_wiatru']
            ])
    table = AsciiTable (rows)
    print (table.table)   

if __name__ == '__main__':
    time = datetime.datetime.now()
    print ("-----------------------------------------------------------")
    print (F"Pogoda z dnia: {time.day}.{time.month}.{time.year} r. Źródło: IMGW")
    print ("-----------------------------------------------------------")
    CITIES = input ("Wybierz miasta: ")
    main_weather()
    main_air()
    
