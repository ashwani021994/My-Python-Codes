from bs4 import BeautifulSoup as soup
from requests import get
import requests
import urllib.request as req
import pandas as pd
stateslist = pd.read_excel("E:/project/states list.xlsx",sheetname = "Sheet1")

dict_city = {i:[] for i in stateslist["states"]}


for i in stateslist["states"]:
    link = "https://www.google.co.in/search?q=cities+in+" + i
    




    base_url=link
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Referer': 'https://cssspritegenerator.com',
             'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
             'Accept-Encoding': 'none',
             'Accept-Language': 'en-US,en;q=0.8',
             'Connection': 'keep-alive'}
    page = get(base_url,headers = hdr)


    sauce = soup(page.content,"html.parser")
    yo = sauce.find_all("div",{"class":"kltat"})
    for x in yo :    
        a = x.text
        dict_city[i].append(a)
    print(len(dict_city[i]))

