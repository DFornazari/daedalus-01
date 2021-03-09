import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
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

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
#
# creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\danie\OneDrive\Desktop\testSheet-3df5aea2954b.json", scope)
#
# client = gspread.authorize(creds)

print("Acquiring GSheets Credentials from JSON")
creds = ServiceAccountCredentials.from_json_keyfile_name(r"G:\My Drive\Affiliate Marketing\Credentials\Google APIs\Sheets API\apt-tracker-297423-6f5664b3e0e0.json", scope)

client = gspread.authorize(creds)

print("Opening sheet")
sheet = client.open("Campaign Builder").sheet1  # Open the spreadhseet

data = dt.datetime.now().date()
data_string = data.strftime("%Y-%m-%d")


df = pd.DataFrame(sheet.col_values(2))
df = df[df[0] != ""]
headers = df.iloc[0]
df_courses  = pd.DataFrame(df.values[1:], columns=headers)


# df1 = pd.DataFrame(sheet2.col_values(1)).iloc[1:]
# df2 = pd.DataFrame(sheet2.col_values(2)).iloc[1:]
# joindf1df2 = [df1, df2]
# headers = ['course_id', 'status']
# df3 = pd.concat(joindf1df2, axis=1, keys=headers)
# df3.columns = headers
#
# df_tracked = df3[df3['status']=='tracked']['course_id']
#
df_final = df_courses.copy()



#-------------------HOTMART----------------------
#DATAS
data = dt.datetime.now().date()
data_string = data.strftime("%Y-%m-%d")
dict_months = {1:'1-January',
               2:'2-February',
               3:'3-March',
               4:'4-March',
               5:'5-May',
               6:'6-June',
               7:'7-July',
               8:'8-August',
               9:'9-September',
               10:'10-October',
               11:'11-November',
               12:'12-December'}

credentials = {"email":"daedalus.tecnologia@gmail.com",
               "password": "28089346Df"}


#Selenium setup
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-bypass-list=*")
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

print("Attempting Hotmart Login")
#LOGIN
def hotmart_login(credentials):
    url_login = r"https://app-vlc.hotmart.com/login"
    driver.get(url_login)
    time.sleep(1)
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
    button_login = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[1]/div/div[3]/form[2]/div[4]/button')
    button_login.click()
    time.sleep(1)
hotmart_login(credentials)

def add_pixel(course_id):
    adwords_id = 'AW-457740156'
    adwords_label = 'aSLCCNWP1e0BEPyeotoB'

    time.sleep(1)
    url_pixel = f"https://app-vlc.hotmart.com/products/manage/{course_id}/tools/tracking-pixel"
    driver.get(url_pixel)
    time.sleep(3)

    pixel_button = driver.find_element_by_xpath('//*[@id="tracking-grid"]/div[1]/div[5]/div[2]') #MAY BREAK
    pixel_button.click()
    time.sleep(3)

    adword_id_box = driver.find_element_by_xpath('//*[@id="ADWORDS_ID"]')
    adword_id_box.send_keys(adwords_id)
    time.sleep(2)

    adword_id_box = driver.find_element_by_xpath('//*[@id="ADWORDS_LABEL"]')
    adword_id_box.send_keys(adwords_label)
    time.sleep(1)
    avancar = driver.find_element(By.XPATH, "//*[text()='Avançar']")
    avancar.click()
    time.sleep(1)
    concluir = driver.find_element(By.XPATH, "//*[text()='Concluir']")
    concluir.click()

df_finished = pd.DataFrame(columns=['course_id','status'])
print("Starting pixel tracking...")
for i in range(0, len(df_final)):
    course_id = df_final['ID do Produto'].iloc[i]
    try:
        add_pixel(course_id)
        dict_append = {'course_id':course_id, 'status':'tracked'}
        print(str(i) + ' ok')
    except:
        dict_append = {'course_id':course_id, 'status':'not tracked'}
        print(str(i) + ' erro')

    df_finished = df_finished.append(dict_append, ignore_index=True)

df_finished.to_excel(f"G:\\My Drive\\Affiliate Marketing\\pixel_tracking\\status_pixel_br{data_string}.xlsx")