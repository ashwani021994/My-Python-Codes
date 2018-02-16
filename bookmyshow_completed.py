import json
import selenium
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests


# citylist represents the cities for which we want to find data from bookmyshow
city_df = pd.read_excel("E:/SCRAPING WORK/region_name_and_region_code.xlsx")
citylist = list(set(city_df["REGION_NAME"]))

## empty list named remove citylist will have those citynames added for which browser dont give status code = 200
remove_citylist=[]
## dict_city_data is an empty dictionary that will be used to create a final database at the end
dict_city_data = {}

for city_name in citylist:
    print(city_name)
    try: 
        
               
#       opening the bookmyshow.com/cityname/events solves the problem of cookies 
#       cityname are various cities from citylist
        url_bookmyshow=   "https://in.bookmyshow.com/" + city_name + "/events"
    
#       all those citynames with url_bookmyshow giving status code not equal to 200 are added to remove_citylist
#       this is done to avoid data added by the citynames whose url_bookmyshow dont exist but give response on calling API
#       all the cities whose name is added remove_citylist will be removed from citylist to make a final_citylist whose data will make the database
        r = requests.get(url_bookmyshow)

        
        
#       all those citynames with status code not equal to 200 are added to remove_citylist.
        if r.status_code == 200:
            pass
        else:
            remove_citylist.append(city_name)
            
#       using selenium with google chrome driver
        driver= webdriver.Chrome(executable_path= "C:/Python34/Scripts/chromedriver.exe")
    
#       driver.get is used to load the required url in chrome browser window


        driver.get(url_bookmyshow)
        
        
#       time.sleep here provides a 3 seconds pause before executing the next command
        time.sleep(3)
    
#       calling the api since our region is now stored in cookies using above code
        url_api=   "https://in.bookmyshow.com/serv/getData?cmd=QUICKBOOK&type=SP"
        driver.get(url_api)
        time.sleep(1)
        
#       the json response recieved using API is inside the pre tag, when the response page is inspected,hence getting the data using pre tag
        json_response_As_selenium_object = driver.find_element_by_tag_name('pre')
    
#       note: json_response_as_selenium_object is as name suggests a selenium object ,so below json_response_As_selenium_object.text gives us a string object
    
#       using json.loads(), string data is converted to json format or in other words as a dictionary
        json_data = json.loads(json_response_As_selenium_object.text)
        
#       creating a dynamic dictionary for each city i.e each city has json data associated with it
        dict_city_data[city_name] = json_data
        
        driver.close()

    
    except  Exception as e:
        print(e)
        pass    


# final_citylist comprises of citynames whose url_bookmyshow was a relevant address i.e gave a status code of 200
final_citylist = set(citylist) - set(remove_citylist)


# values from different dictionaries will be added to these empty list to form a final database
event_name_list=[]
event_global_status_list = []
venue_name_list = []
venue_latitude_list = []
venue_longitude_list =[]
venue_address_list = []
venue_region_code_list = []
show_date_code_list= []
show_date_full_list = [] 

#  looping over citynames in final_citylist
for cityname in list(final_citylist):
    
#   deriving data from dictionary of corresponding cityname
    for i in dict_city_data[cityname]['data']['BookMyShow']['arrEvent']:
        
#       for an event that is taking place on multiple days ,each day is a different entry.
        for x in i['arrDates']:
            show_date_code_list.append(x['ShowDateCode'])
            show_date_full_list.append(x['ShowDateDisplay'])
            event_name_list.append(i["EventTitle"])
            event_global_status_list.append(i['EventIsGlobal'])
            venue_name_list.append(i["arrVenues"][0]["VenueName"])
            venue_latitude_list.append(i["arrVenues"][0]['VenueLatitude'])
            venue_longitude_list.append(i["arrVenues"][0]['VenueLongitude'])
            venue_address_list.append(i["arrVenues"][0]['VenueAddress'])
            venue_region_code_list.append(i["arrVenues"][0]['RegionCode'])


# creating adictionary named dict_all_data that contains all the data from all cities and this dictionary will be converted to dataframe             
dict_all_data = {"event_name_list":event_name_list,"event_venue_name_list":venue_name_list,"event_global_status_list":event_global_status_list,"venue_latitude":venue_latitude_list,"venue_longitude":venue_longitude_list,"event_date_full": show_date_full_list,"venue_region_code":venue_region_code_list,"venue_date_code":show_date_code_list,"venue_address":venue_address_list}

# dataframe containing all data named df_all_data
df_all_data  = pd.DataFrame(dict_all_data)

## this step converts dataframe to excel ,bookmyshow_new.xlsx is the file name in 'E' drive  
df_all_data.to_excel("E:/bookmyshow_SPORTS.xlsx")

print("program completed")
