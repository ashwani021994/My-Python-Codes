import requests
import pandas as pd
citieslist = pd.read_excel("E:\project\states and cities edited and cleaned.xlsx")
dict_lat={"latitude":[],"longitude":[]}
for i,rows in citieslist.iterrows():
    try:
        a = ("+"+ str(rows["Cities"])+",+"+ str(rows["States"]))
        link = str('https://maps.googleapis.com/maps/api/geocode/json?address=' + a)

        response = requests.get(link)
        resp_json_payload = response.json()

        latitude=(resp_json_payload['results'][0]['geometry']['location']['lat'])
        longitude = (resp_json_payload['results'][0]['geometry']['location']['lng'])
        dict_lat["latitude"].append(latitude)
        dict_lat["longitude"].append(longitude)
        print(i)
    
    except:
        dict_lat["latitude"].append("error")
        dict_lat["longitude"].append("error")
        print(i)
        continue
