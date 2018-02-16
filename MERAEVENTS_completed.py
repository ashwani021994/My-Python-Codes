
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import json
import requests
import pandas as pd



# please enter category id 
# id =  1    : category - entertainment ,id =  9    : category - sports
category_id = 1
# empty lists to which data will be added for making final database
titlelist= []
venuelist =[]
latitudelist = []
longitudelist = []
startdatelist = []
enddatelist = []
citylist = []

# starting with page_no = 1 ,this variable will be incremented by one to get next pages
page_no = 1

# while True loop executes infinitely until a 'break' command is given.A 'break' command will be executed only if the page don't have any data.
while True :
    
#   printing the page_no just for reference  
    print("scraping page no :",page_no)
    
#   using try and except for catching errors that might come .
    try:
        
#       url is made such that each change in page_no changes the whole url
        url=   "https://www.meraevents.com/api/event/list?countryId=14&categoryId=" + str(category_id) + "&day=6&page=" + str(page_no) + "&limit=12"
    
#       adding headers to avoid being blocked by page
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url,headers=hdr)
        
#       urlopen() opens the file and read() gives the response body as string
        page_response = urlopen(req).read()
    
#       parsing the page_response using beautifulsoup which is imported as soup
        page_html = soup(page_response,"html.parser")

        
#       converting page_html which is a beautifulsoup object to json type or in other words as a dictionary named as dict_content
        dict_content = json.loads(str(page_html))
        
#       the below if and else statements executes the 'break'command if no data is present on the page
#       it can be seen by visiting the api link that pages with no data available have value inside dict_content["response"]["total"] == 0
        if dict_content["response"]["total"] == 0:
            print( "data not available  on page_no",page_no)
            break
        else:
            pass
        
#       increasing the page_no by 1 so as to go to next page
        page_no += 1
    
#       value corresponding to key:'eventList' inside dictionary dict_content["response"] is a list 
        event_details_list = (dict_content["response"]["eventList"])

#       iterating over different elements in the list named event_details_list.Each element of this list is a dictionary with keys and values.
        for eventname in event_details_list:

#           finding various values associated with different keys and adding them to respective list
            titlelist.append(eventname["title"])
            venuelist.append(eventname["venueName"])
            citylist.append(eventname["cityName"])
            latitudelist.append(eventname["latitude"])
            longitudelist.append(eventname["longitude"])
            startdatelist.append(eventname["startDate"])
            enddatelist.append(eventname["endDate"])
            
            
        
    except Exception as e:
        print(e)
        pass
      
        
#   dict_full_data is a dictionary containing all the data and this dictionary will be used to make a dataframe
dict_full_data = {"title" : titlelist,"venuename":venuelist,"cityname":citylist,"latitude":latitudelist,"longitude":longitudelist,"startdate":startdatelist,"enddate":enddatelist}

# df_full_data is a dataframe made using dict_full_data dictionary
df_full_data = pd.DataFrame(dict_full_data)

print(df_full_data)


df_full_data.to_excel("E:/meraevents_new.xlsx")

print("program completed")
