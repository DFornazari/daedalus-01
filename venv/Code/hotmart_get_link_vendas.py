
import time

import urllib
import pyodbc
import pandas as pd

import bizdays
import numpy as np
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import re
import pyperclip

from selenium.webdriver.common.by import By


df_cursos = pd.read_excel("G:\My Drive\Affiliate Marketing\cursos-nacionais-01-12-2020.xlsx")



#Selenium setup
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-bypass-list=*")
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

df_cursos['fullLink'] = ""
df_cursos['salesLink'] = ""
df_cursos['affiliateCode'] = ""


for i in range(0,len(df_cursos['affiliateUrl'])):
    try:
        url = df_cursos['affiliateUrl'].iloc[i]
        driver.get(url)
        time.sleep(2)
        full_link = driver.current_url
        sales_link = driver.current_url.split('?ref=')[0]
        affiliate_code = driver.current_url.split('?ref=')[1]
        df_cursos.at[i, 'fullLink'] = full_link
        df_cursos.at[i, 'salesLink'] = sales_link
        df_cursos.at[i, 'affiliateCode'] =  affiliate_code
        print("OK " + str(i))
    except:
        print("ERRO em " + str(i))


