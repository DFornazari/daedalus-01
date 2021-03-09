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
    country = selected_file.split('_')[2]
    total_path = path + '\\' + selected_year + '\\' +  selected_month + '\\' + selected_file




    def unnafiliate(df_urls):
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
            field_pass.clear()
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

        #df_unnafiliate = pd.read_excel(total_path, "DISCARD")
        counter = 0
        driver.get("https://app-vlc.hotmart.com/products/affiliate")
        time.sleep(10)
        for course in df_unnafiliate['name']:
            try:
                driver.get("https://app-vlc.hotmart.com/products/affiliate")
                time.sleep(1)
                search_box = sobre_button = driver.find_element(By.XPATH, '//*[@id="search-container"]')
                search_box.send_keys(course)
                time.sleep(3)

                error_counter_1 = 0
                succeed_1 = False
                while error_counter_1 < 3 and succeed_1 == False:
                    try:
                        threedots = driver.find_element(By.XPATH, '//*[@id="__blaze-root"]/div/div[2]/main/div/div[2]/div[6]/div/div/div/div/div/div[3]/button')
                        threedots.click()
                        succeed_1 = True
                        time.sleep(1)
                    except:
                        time.sleep(1)
                        error_counter_1 =error_counter + 1
                        print(error_counter_1)

                cancel_button = driver.find_element(By.XPATH, "//*[text()='Cancelar Afiliação']")
                cancel_button.click()
                time.sleep(1)
                yes_button = driver.find_element(By.XPATH, "//*[text()='Sim']")
                yes_button.click()
                counter = counter + 1
                print(str(counter) + "ok")
            except:
                print("erro " +  str(counter) +  " " + course)