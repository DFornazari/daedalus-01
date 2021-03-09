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

# DATAS
data = dt.datetime.now().date()
data_string = data.strftime("%Y-%m-%d")
dict_months = {1: '1-January',
               2: '2-February',
               3: '3-March',
               4: '4-March',
               5: '5-May',
               6: '6-June',
               7: '7-July',
               8: '8-August',
               9: '9-September',
               10: '10-October',
               11: '11-November',
               12: '12-December'}

credentials = {"email": "daedalus.tecnologia@gmail.com",
               "password": "28089346Df"}

# Selenium setup
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-bypass-list=*")
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


# LOGIN
def hotmart_login(credentials):
    url_login = r"https://app-vlc.hotmart.com/login"
    driver.get(url_login)
    time.sleep(2)
    login_list = driver.find_elements_by_xpath('//*[contains(@id, "input-")]')
    field_email = login_list[0]
    field_pass = login_list[1]
    field_email.clear()
    time.sleep(1)
    field_pass.clear()
    time.sleep(1)
    field_email.click()
    field_email.send_keys(credentials['email'])
    time.sleep(1)
    field_pass.click()
    field_pass.send_keys(credentials['password'])
    time.sleep(1)
    button_login = driver.find_element_by_xpath(
        '//*[@id="__blaze-root"]/div/div[1]/div/div[3]/form[2]/div[4]/button')
    button_login.click()
    time.sleep(2)


hotmart_login(credentials)



df_urls = pd.read_excel(r"G:\My Drive\Affiliate Marketing\CURSOS AFFI.xlsx", "NOT FOUND")

df_final = pd.DataFrame(columns=['id', 'url'])

for id in df_urls['courseId']:
    try:

        time.sleep(1)
        url = "https://app-vlc.hotmart.com/market"
        driver.get(url)



        try:
            backdrop = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[2]/main/div/div[2]/div[1]')
            backdrop.click()
        except:
            pass
        searchbox = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[2]/main/div/form/div/input')
        searchbox.clear()
        searchbox.send_keys(str(id))
        searchbutton = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[2]/main/div/form/div/span/button')
        searchbutton.click()
        time.sleep(3)


        html_source = driver.page_source
        positions = re.finditer('/products/view', html_source)
        list_positions = []
        for i in positions:
            list_positions.append(i.span())

        list_urls_raw = []
        for i in list_positions:
            list_urls_raw.append(html_source[i[0]: i[1] + 37])

        list_urls_products = []
        for i in list_urls_raw:
            list_urls_products.append("https://app-vlc.hotmart.com" + i)

        course_url = pd.DataFrame(list_urls_products).drop_duplicates().at[0,0]

        dict_append = {'id':str(id), 'url':course_url}
        df_final = df_final.append(dict_append, ignore_index=True)
        print(str(id) + "OK")
    except:
        dict_append = {'id': str(id), 'url': "erro"}
        df_final = df_final.append(dict_append, ignore_index=True)
        print(str(id) + "ERRO")
    df_final.to_excel("G:\My Drive\Affiliate Marketing\CURSOS AFFI NOT FOUND.xlsx")

