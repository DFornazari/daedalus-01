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

month = 1
year = 2021
month_str = dict_months[month]

#Selenium setup
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-bypass-list=*")
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())


#LOGIN
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
    button_login = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[1]/div/div[3]/form[2]/div[4]/button')
    button_login.click()
    time.sleep(2)
hotmart_login(credentials)


#URL_MASTER
path_master = f"G:\\My Drive\\Affiliate Marketing\\Status Checking\\{year}\\{month_str}\\df_url_master.xlsx"
df_master = pd.read_excel(path_master)

def get_affiliation_status(url):
    driver.get(url)
    time.sleep(2)
    try:
        info = driver.find_element(By.XPATH, "//*[text()='Ver links de divulgação']")
        status = 'AFFILIATED'
    except:
        try:
            info = driver.find_element(By.XPATH, "//*[text()='Afiliar-se Agora']")
            status = 'NOT_AFFILIATED'
        except:
            try:
                info = driver.find_element(By.XPATH, "//*[text()='Pedido de afiliação enviado!']")
                status = 'AFFILIATION_REQUESTED'
            except:
                try:
                    info = driver.find_element(By.XPATH, "//*[text()='Solicitar Afiliação']")
                    status = 'NOT_REQUESTED'
                except:
                    status = 'ERROR'
    return status

def get_pixel_status(course_id, dict_pixel):
    url_pixel = f"https://app-vlc.hotmart.com/products/manage/{course_id}/tools/tracking-pixel"
    driver.get(url_pixel)
    time.sleep(3)



    found_list = []
    try:
        #TRACKED
        pixel_button = driver.find_element_by_xpath('//*[@id="tracking-grid"]/div[1]/div[5]/div[3]') #MAY BREAK
        pixel_button.click()  # MAY BREAK
        time.sleep(2)

        for i in dict_pixel:
            str_find = f"//*[text()='{i}']"
            try:
                find = driver.find_element(By.XPATH, str_find)
                find_status = i
                found_list.append(i)
            except:
                pass

        status = "TRACKED"
    except:
        try:
            #UNTRACKED
            pixel_button = driver.find_element_by_xpath('//*[@id="tracking-grid"]/div[1]/div[5]/div[2]')
            pixel_button.click()

            status = "UNTRACKED"
        except:
            status = "ERROR"

    return status, found_list




dict_pixel = {
    'AW-457740156': 'aSLCCNWP1e0BEPyeotoB',
    'AW-452203334': 'c9nlCKW7je8BEMam0NcB',
    'AW-452202335': 'qO5vCPG8je8BEN-e0NcB',
    'AW-452139003': 't48OCInonO8BEPuvzNcB',
    'AW-411643357': 'J7FvCM-qhPgBEN3bpMQB',
    'AW-411654155': 'A1ViCPbd5fcBEIuwpcQB',
    'AW-411643060': 'TMw8CPnd5fcBELTZpMQB',
    'AW-411590004': 'l89cCPzd5fcBEPS6ocQB',
    'AW-411653414': '7a3qCOy0-_cBEKaqpcQB'
}




def add_pixel(found_list, dict_pixels, pixelStatus):
    import numpy as np
    list_add = list(np.setdiff1d(list(dict_pixel.keys()),found_list))
    if pixelStatus == 'UNTRACKED':
        #UNTRACKED
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="ADWORDS_ID"]').send_keys(list_add[0])
        driver.find_element_by_xpath('//*[@id="ADWORDS_LABEL"]').send_keys(dict_pixel[list_add[0]])
        driver.find_element(By.XPATH, "//*[text()='Avançar']").click()
        driver.find_element(By.XPATH, "//*[text()='Concluir']").click()
        time.sleep(1)
        for i in list_add[1:]:
            time.sleep(1)
            driver.find_element(By.XPATH, "//*[text()='Adicionar novo Pixel de Rastreamento']").click()
            driver.find_element_by_xpath('//*[@id="ADWORDS_ID"]').send_keys(i)
            driver.find_element_by_xpath('//*[@id="ADWORDS_LABEL"]').send_keys(dict_pixel[i])
            driver.find_element(By.XPATH, "//*[text()='Avançar']").click()
            driver.find_element(By.XPATH, "//*[text()='Concluir']").click()
            time.sleep(3)
        return list_add
    elif pixelStatus == 'TRACKED':
        #TRACKED
        for i in list_add:
            time.sleep(1)
            driver.find_element(By.XPATH, "//*[text()='Adicionar novo Pixel de Rastreamento']").click()
            driver.find_element_by_xpath('//*[@id="ADWORDS_ID"]').send_keys(i)
            driver.find_element_by_xpath('//*[@id="ADWORDS_LABEL"]').send_keys(dict_pixel[i])
            driver.find_element(By.XPATH, "//*[text()='Avançar']").click()
            driver.find_element(By.XPATH, "//*[text()='Concluir']").click()
            time.sleep(3)
        return list_add

df_status = pd.DataFrame(columns=['id', 'affiliationStatus', 'pixelStatus', 'pixelAddedStatus', 'foundPixels', 'addedPixels'])
for i in range(348, len(df_master)):
    course_id = df_master.iloc[i]['id']
    url = df_master.iloc[i]['productUrl']
    affiliationStatus = get_affiliation_status(url)
    # affiliationStatus = "a"
    time.sleep(2)
    pixelStatus, found_list = get_pixel_status(course_id, dict_pixel)
    try:
        list_added = add_pixel(found_list, dict_pixel, pixelStatus)
        status_add = "ADD_SUCCESS"
    except:
        found_list = []
        list_added = []
        status_add = "ERROR_ADD_PIXEL"

    dict_append = {'id':course_id,
                   'affiliationStatus':affiliationStatus,
                   'pixelStatus':pixelStatus,
                   'pixelAddedStatus':status_add,
                   'foundPixels':found_list,
                   'addedPixels':list_added
                   }
    df_status = df_status.append(dict_append, ignore_index=True)
    if i in [50, 100, 150, 200, 250, 300, 350, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900]:
        df_status.to_excel(f"G:\\My Drive\\Affiliate Marketing\\Status Checking\\{year}\\{month_str}\\df_status_checked_int{i}.xlsx")
    print(str(i)+ f": {course_id} - AFF: {affiliationStatus} - PIX: {pixelStatus}")

df_master = df_master.merge(df_status, how='left', on='id')

df_master.to_excel(f"G:\\My Drive\\Affiliate Marketing\\Status Checking\\{year}\\{month_str}\\df_status_checked.xlsx")

