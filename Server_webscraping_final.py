#!/usr/bin/env python
# coding: utf-8

# In[ ]:



# In[1]:


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import mysql.connector as msql
from sqlalchemy import create_engine
from mysql.connector import Error
import zipfile
import time
from datetime import date
import os
from selenium import webdriver
import pandas as pd 
# import dask.dataframe as dd
# from tqdm import tqdm
# import schedule
import shutil


# In[5]:


# def job():
#     print("I'm working...")

# schedule.every(10).seconds.do(job)
# # schedule.every(10).minutes.do(job)
# # schedule.every().day.at("10:30").do(job)
# # schedule.every().wednesday.at("13:15").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)


# In[6]:


# We are trying to check if their is a folder called MHSA database on our desktop folder

directory = "MHSA Database"
path_dir = "/home/sirigiri" 

dirpath = os.path.join(path_dir, directory)
if os.path.exists(dirpath) and os.path.isdir(dirpath): #Checking for the folder if exists remove it and create a new folder woth same name
    shutil.rmtree(dirpath)

# Added the chrome extension so that each time we run it navigates to the chrome page

#PATH = r'./chromedriver'

PATH = r'/<root>/bin/google-chrome'
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
chromeOptions.add_argument("--no-sandbox") 
chromeOptions.add_argument("--disable-setuid-sandbox") 

chromeOptions.add_argument("--remote-debugging-port=9222")  # this
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--disable-dev-shm-using") 
chromeOptions.add_argument("--disable-extensions") 
chromeOptions.add_argument("--disable-gpu") 
chromeOptions.add_argument("start-maximized") 
chromeOptions.add_argument("disable-infobars")
chromeOptions.add_argument(r"user-data-dir=.\cookies\\test") 

#chromeOptions.binary_location = "/usr/bin/chromium-browser"
b = webdriver.Chrome(chrome_options=chromeOptions) 
b.get("https://google.com/") 
b.quit()
# This sets the default download folder to be MHSA Database
prefs = {"download.default_directory" : "/home/sirigiri/MHSA Database"} #Setting the default download folder to be MHSA Database
chromeOptions.add_experimental_option("prefs",prefs)

#driver = webdriver.Chrome(executable_path=PATH,chrome_options=chromeOptions)

driver = webdriver.Chrome(ChromeDriverManager().install())

# Retrieving the information from the MHSA wesbite
driver.get("https://arlweb.msha.gov/OpenGovernmentData/OGIMSHA.asp") #The link for the website where the information is present

aTagsInLi = driver.find_elements_by_css_selector('li a') #Finding all the elements by the css selector

req_tags = [a.get_attribute("href") for a in aTagsInLi if a.get_attribute("href").endswith(".zip") ] #Looking for hypertext reference and later for the files which ends with .zip in the website

# This would download all the datasets that are present in that page
for i in req_tags:
    driver.get(i)


# In[ ]:


time.sleep(90)


# In[ ]:


# This converts the downloaded zip files to a .txt file.
dir_name = '/home/sirigiri/MHSA Database'
extension = ".zip"

os.chdir(dir_name)

for item in os.listdir(dir_name): # loop through items in dir
    if item.endswith(extension): # check for ".zip" extension
        file_name = os.path.abspath(item) # get full path of files
        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
        zip_ref.extractall(dir_name) # extract file to dir
        zip_ref.close() # close file
        os.remove(file_name) # delete zipped file


#In[ ]:


time.sleep(60)
import os
import mysql.connector as database

#In[ ]:

#In[ ]:


engine = create_engine("mysql://root:MyNewPass@127.0.0.1/MHSA_Database_main2") 


#In[ ]:


directory = r"C:\Users\dharm\OneDrive\Desktop\MHSA Database"
for filename in os.listdir(r"C:\Users\dharm\OneDrive\Desktop\MHSA Database"):
	if filename.endswith(".txt"):
	    df = pd.read_csv(os.path.join(directory, filename),delimiter = '|', error_bad_lines=False,encoding = 'unicode_escape')
	    df.to_sql(filename[:-4],engine,if_exists= "replace")
	    continue
	else:
	    break


# In[ ]:




