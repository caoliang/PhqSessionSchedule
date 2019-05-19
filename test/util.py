import requests
import json

def get(url):
    resp = requests.get(url)
    if resp.ok:
        return resp.json()

def construct_city_dct():
    with open("current.city.list.json", mode="r", encoding="UTF-8") as city_file:
            city_data = city_file.read()

    city_json = json.loads(city_data)
    city_dct = {}

    for city_item in city_json:
            city_name = city_item["name"].lower()
            city_dct[city_name] = city_item

    return city_dct

def get_weather_status(city_name, city_dct):
    city_name = city_name.lower()
    if city_name in city_dct:
        city_id = city_dct[city_name]["id"] #refering to global coindct
        print("Found city {} with id {}".format(city_name, city_id))

        url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID=e8deaf57951576d5ac2aa6efdc22ff48"
    else:
        print("Cannot not find city id at {}".format(city_name))
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID=e8deaf57951576d5ac2aa6efdc22ff48"

    data = get(url)

    #parse the weather info from the resp
    weather_status = data["weather"][0]["description"]
    print("Found weather status: {}".format(weather_status))
    return weather_status

