''' template of original scrapper to output values to csv file '''

import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get("http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s=0")
c = r.content

soup = BeautifulSoup(c, "html.parser")
all = soup.find_all ("div",{"class":"propertyRow"})
all[0].find("h4",{"class":"propPrice"}).text.strip()

page_nr=soup.find_all("a",{"class":"Page"})[-1].text
#print(type(page_nr))

property_info = []
base_url="http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="
for page in range(0,int(page_nr)*10,10):
    #print(base_url + str(page) + ".html")
    c=requests.get(base_url + str(page) + ".html")
    c=r.content
    soup = BeautifulSoup(c,"html.parser")
    #print (soup.prettify())
    all=soup.find_all("div",{"class":"propertyRow"})
    for item in all:
        d={}
        d["House Price"]=item.find("h4",{"class":"propPrice"}).text.strip()
        d["address"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text
        try:
            d["Town,State,Zip"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text
        except:
            d["Town,State,Zip"]=None
        try:
            d["beds"]=item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["beds"]=None
        try:
            d["Area (SqFt)"]=item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area (SqFt)"]=None
        try:
            d["Full Baths"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None
        try:
            d["Half Baths"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None
        for column_group in item.find_all("div",{"class":"columnGroup"}):
            #print(column_group)
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text
                #print (feature_group.text,feature_name.text)
        property_info.append(d)

df = pandas.DataFrame(property_info)
df.to_csv("data.csv")
