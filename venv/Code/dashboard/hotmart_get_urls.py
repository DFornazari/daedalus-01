# app1.py
import streamlit as st


def init():
    dict_countries = {'brasil': {'countryId': '1', 'locale': 'PT_BR'},
                      'colombia': {'countryId': '50', 'locale': 'ES'},
                      'argentina': {'countryId': '14', 'locale': 'ES'}}
    country = st.selectbox('Escolher país',list(dict_countries.keys()))

    def run(dict_countries, country):
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


        # brasil, colombia, argentina
        def get_urls(country):


            # Get market page
            list_market_types = ['?tab=firstSales', '?tab=hottest', '?tab=dearest', '?tab=newest']

            list_urls_total = []
            for market in list_market_types:
                url_market = r"https://app-vlc.hotmart.com/market" + market + '&countryId=' + dict_countries[country][
                    'countryId'] + '&locale=' + dict_countries[country]['locale']
                driver.get(url_market)
                time.sleep(10)

                continue_a = False
                # MAY BREAK
                # while continue_a == False:
                #     try:
                #         backdrop = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[2]/main/div/div[2]/div[1]')
                #         backdrop.click()
                #         continue_a = True
                #     except:
                #         print("Could not find backdrop XPATH")
                #         time.sleep(2)

                # MAY BREAK
                try:
                    load_more_button = driver.find_element(By.XPATH, "//*[text()='Carregar Mais']")
                    count_error = 0
                    while count_error < 5:
                        try:
                            time.sleep(2)
                            load_more_button.click()
                            count_error = 0
                        except:
                            count_error = count_error + 1
                            print("Erro " + str(count_error))
                except:
                    print('ok')

                # Get source code and get product urls
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

                list_urls_products = list(dict.fromkeys(list_urls_products))
                list_urls_total = list_urls_total + list_urls_products

            list_urls_total = list(dict.fromkeys(list_urls_total))

            df_urls = pd.DataFrame(list_urls_total)
            df_urls.columns = ['URL']
            df_urls.to_excel(
                f"G:\\My Drive\\Affiliate Marketing\\urls_new_courses\\{str(data.year)}\\{dict_months[data.month]}\\df_urls_{country}_{data_string}.xlsx")
            return df_urls

        get_urls(country)

    if st.button('Rodar'):
        run(dict_countries, country)