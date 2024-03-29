"""Script 2 that only uses selenium for automation and beautiful soup for scrapping
along with web api (Streamlit)"""

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
import streamlit as st
import pandas as pd
from logger import logging
logging.info("All Libraries installed")

st.sidebar.image("https://gologin.com/wp-content/uploads/Frame-49-1.png")
st.title("Web Scrapping Assignment")

logging.info("Entering into the function")
Name=[]
Location=[]
Followers =[]
About = []
def profile_info_linkdein(FirstName,LastName,EmailID,Password):
    #s=Service("C:/Users/DELL/Downloads/Dataset/chromedriver-win64/chromedriver.exe")
    s=Service("chromedriver.exe") ## Chrome driver extensions
    logging.info("Chrome driver path is executed")
    driver = webdriver.Chrome(service = s)
    logging.info("Hitting the linkdein url using selenium")
    
    # linkdein url
    link = f"https://www.linkedin.com/search/results/people/?heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAACtRLZMB7ymcym6TQImChrlOhl4BfCxYffw&keywords={FirstName}%20{LastName}&origin=SWITCH_SEARCH_VERTICAL&sid=L9b"
    driver.get(link)
    logging.info("The link is getting executed using selenium")
    time.sleep(2)
    
    logging.info("Entering linkdein login page")
    
    ## main linkdein path for login 
    driver.find_element_by_xpath("""/html/body/div[1]/main/div/p/a""").click()
    time.sleep(2)
    
    user_name = driver.find_element_by_xpath("""/html/body/div/main/div[2]/div[1]/form/div[1]/input""")
    ## linkdein url login details
    user_name.send_keys(EmailID) ## provide email id
    user_name.send_keys(Keys.ENTER)
    logging.info("Email id is sucessfully inserted")


    password = driver.find_element_by_xpath("""/html/body/div/main/div[2]/div[1]/form/div[2]/input""")
    password.send_keys(Password) ## provide password
    password.send_keys(Keys.ENTER)
    logging.info('password is sucessfuly inserted')


    source = BeautifulSoup(driver.page_source,"html.parser")
    ## scraping the profile using beautiful soup
    info = source.find("ul",{'class':'reusable-search__entity-result-list list-style-none'})
    profiles = source.find_all("li", {"class": "reusable-search__result-container"})
    ## Loging to lindein page people section
    logging.info("Each box on linkdein profile is being shown")
    
    logging.info("Enetering into each profile")
    for profile in profiles:
        try:
            logging.info("Entering to name profile")
            name = profile.find("span", {"aria-hidden": "true"}).get_text().strip()
            ## retrving name from linkdein profile
            Name.append(name)
            logging.info("Name is executed sucessfully")
            print("Name :", name)
        except AttributeError:
            Name.append("Not Found")
            logging.info("Some error name tag")
            
        try:
            logging.info("Entering to location profile")
            # retriving location from linkdein profile
            location = profile.find('div', {'class': 'entity-result__secondary-subtitle t-14 t-normal'}).get_text().strip()
            Location.append(location)
            logging.info("Location is executed sucessfully")
            print("Location:", location)
        except AttributeError:
            Location.append("not found")
            logging.info("Some error Location tag")

        try:
            logging.info("Entering to followers of each profile")
            #retriving followers from linkdein profile
            followers = profile.find('div', {'class': 'reusable-search-simple-insight__text-container'}).get_text().strip()
            Followers.append(followers)
            logging.info("followers is executed sucessfully")
            print('Followers:', followers)
        except AttributeError:
            Followers.append("Not Found")
            logging.info("Some error followers tag")
            
        try:
            profile_name_span = profile.find('div', {'class': 'entity-result__primary-subtitle t-14 t-black t-normal'})
            if profile_name_span:
                logging.info("Entering to about section")
                about = profile_name_span.get_text().strip() if profile_name_span else "N/A"
                # Retriving about from linkdein profile
                About.append(about)
                logging.info("About is executed sucessfully")
                print("About:", about)
            else:
                print("Profile Name not found.")
                logging.info("Some error About tag")
        except AttributeError:
            About.append("Not found")

        print("\n")
        
    d={'Name':Name,'Location':Location,'Followers':Followers,"About":About}
    ## Creating data frame
    data = pd.DataFrame(d)
    data.to_csv('linkdein_profile_info.csv')
    data


def main():
    st.title("LinkedIn Profile Scraper")

    # Input fields
    FirstName = st.text_input("Enter First Name:") ## Firstname
    LastName = st.text_input("Enter Last Name:") ## lastname
    EmailID = st.text_input("Enter Email ID:")  ## emailid/linkdein id
    Password = st.text_input("Enter Password:") ## linkdein password
    
    if st.button("Scrape LinkedIn"):
        result_df = profile_info_linkdein(FirstName, LastName, EmailID,Password)
        #final result
        st.dataframe(result_df)


## executing the function
if __name__ == "__main__":
    main()