# app2.py
import streamlit as st
import os
import pandas as pd
import datetime as dt

def init():
    path = r"G:\My Drive\Affiliate Marketing\already_affiliated"

    def file_selector(folder_path=path):
        anos = os.listdir(folder_path)
        selected_year = st.selectbox('Selecionar Ano', anos)
        meses = os.listdir(folder_path + '\\' + selected_year)
        selected_month = st.selectbox('Selecionar Mês', meses)
        path_final = (folder_path + '\\' + selected_year + '\\' + selected_month)

        return list(os.listdir(path_final)), selected_year, selected_month



    filename, selected_year, selected_month = file_selector()
    selected_file = st.selectbox('Selecionar arquivo', filename)
    #country = selected_file.split('_')[2]
    country = 'total'
    total_path = path + '\\' + selected_year + '\\' +  selected_month + '\\' + selected_file




    def get_courses_infos(df_urls):
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
        # Selenium setup
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--proxy-bypass-list=*")
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        driver = webdriver.Chrome(ChromeDriverManager().install())

        def hotmart_login():
            credentials = {"email": "daedalus.tecnologia@gmail.com",
                           "password": "28089346Df"}

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

        hotmart_login()


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





#Selenium setup
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-bypass-list=*")
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())


df_cursos = pd.read_excel(r"G:\My Drive\Affiliate Marketing\urls_new_courses\2021\3-March\selected_courses_affiliated_20210306.xlsx", "OK")

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
        df_cursos.to_excel(r"G:\My Drive\Affiliate Marketing\urls_new_courses\2021\3-March\selected_courses_final_20210306.xlsx")
        print("OK " + str(i))
    except:
        print("ERRO em " + str(i))


