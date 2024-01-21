## Script 1 that only uses selenium for automation and beautiful soup for scrapping.

# Importing Necessary Libraries
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import re
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

firstname = input()
lastname = input()
s=Service("C:/Users/DELL/Downloads/Dataset/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service = s)
link = f"https://www.linkedin.com/search/results/people/?heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAACtRLZMB7ymcym6TQImChrlOhl4BfCxYffw&keywords={firstname}%20{lastname}&origin=SWITCH_SEARCH_VERTICAL&sid=L9b"
driver.get(link)
time.sleep(2)
driver.find_element_by_xpath("""/html/body/div[1]/main/div/p/a""").click()
time.sleep(2)

user_name = driver.find_element_by_xpath("""/html/body/div/main/div[2]/div[1]/form/div[1]/input""")
user_name.send_keys("vishnumurali880@gmail.com")
user_name.send_keys(Keys.ENTER)

password = driver.find_element_by_xpath("""/html/body/div/main/div[2]/div[1]/form/div[2]/input""")
password.send_keys("########")
password.send_keys(Keys.ENTER)


source = BeautifulSoup(driver.page_source,"html.parser")
info = source.find("ul",{'class':'reusable-search__entity-result-list list-style-none'})
profiles = source.find_all("li", {"class": "reusable-search__result-container"})


Name=[]
Location=[]
Followers =[]
About = []
for profile in profiles:
    try:
        name = profile.find("span", {"aria-hidden": "true"}).get_text().strip()
        Name.append(name)
        print("Name :", name)
    except AttributeError:
        Name.append("Not Found")
        
    try:
        location = profile.find('div', {'class': 'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip()
        Location.append(location)
        print("Location:", location)
    except AttributeError:
        Location.append("not found")

    try:
        followers = profile.find('div', {'class': 'reusable-search-simple-insight__text-container'}).get_text().strip()
        Followers.append(followers)
        print('Followers:', followers)
    except AttributeError:
        Followers.append("Not Found")
        
    try:
        profile_name_span = profile.find('div', {'class': 'entity-result__primary-subtitle t-14 t-black t-normal'})
        if profile_name_span:
            about = profile_name_span.get_text().strip() if profile_name_span else "N/A"
            About.append(about)
            print("About:", about)
        else:
            print("Profile Name not found.")
    except AttributeError:
        About.append("Not found")

    print("\n")
    
d={'Name':Name,'Location':Location,'Followers':Followers,"About":About}
data = pd.DataFrame(d)
data