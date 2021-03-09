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


        df_final = pd.DataFrame(
            columns=[
                "id",
                "name",
                "creator",
                "email",
                "affiliationType",
                "language",
                "category",
                "maxPay",
                "maxPrice",
                "currency",
                "temperature",
                "blueprint",
                "rating",
                "description",
                "url",
            ]
        )

        def get_data(url):
            driver.get(url)
            time.sleep(5)
            try_sobre = False
            while try_sobre == False:
                try:
                    sobre_button = driver.find_element(By.XPATH, "//*[text()='Sobre']")
                    sobre_button.click()
                    try_sobre = True
                except:
                    pass

            textn = driver.find_element_by_tag_name("body").get_attribute("innerText")
            text = textn.replace('\n', ' ').replace('\r', '')
            list_text = text.split()

            # IDENTIFICAÇÃO
            id = list_text[list_text.index('ID') + 1]

            len_name = len(list_text[list_text.index('Produtor(a)') + 1:list_text.index('ID') - 1])
            len_name = (len_name + 1) / 2
            curso = " ".join(
                list_text[list_text.index('Produtor(a)') + 1:list_text.index('Produtor(a)') + 1 + int(len_name)])

            owner_index = [i for i, x in enumerate(list_text) if x == "•"]
            criado_por = " ".join(list_text[owner_index[0] + 3:owner_index[1]])

            email = list_text[list_text.index('suporte:') + 1]

            idioma = list_text[list_text.index('Idioma:') + 1]

            assunto = " ".join(list_text[list_text.index('Assunto:') + 1:list_text.index('Checkout:') - 2])


            # METRICAS

            def tratar_receba_ate(receba_ate):
                if receba_ate == 'veja':
                    return 'n/a (planos)'
                else:
                    try:
                        return float(receba_ate)
                    except:
                        return 'n/a (erro)'

            def tratar_preco_max(preco_max):
                if preco_max == 'infinit':
                    return 'n/a (sem pmax)'
                elif preco_max == 'de':
                    return 'n/a (sem pmax)'
                else:
                    try:
                        return float(preco_max)
                    except:
                        return 'n/a (erro)'

            def tratar_moeda(moeda):

                if moeda == 'comissão,':
                    return 'n/a (planos)'
                else:
                    try:
                        return moeda
                    except:
                        return 'n/a (erro)'

            try:
                type_affiliation = list_text.index('Afiliar-se')
                tipo_afiliacao = 'ABERTA'
            except:
                try:
                    type_affiliation = list_text.index('Afiliado(a).')
                    tipo_afiliacao = 'AFILIADO'
                except:
                    tipo_afiliacao = 'FECHADA'

            if tipo_afiliacao == 'ABERTA':
                receba_ate = list_text[list_text.index('Afiliar-se') - 4].replace(".", "").replace(",", ".")
                moeda = list_text[list_text.index('Afiliar-se') - 5]
                preco_max = list_text[list_text.index('Afiliar-se') + 10][:-1].replace(".", "").replace(",", ".")

                moeda = tratar_moeda(moeda)
                preco_max = tratar_preco_max(preco_max)
                receba_ate = tratar_receba_ate(receba_ate)
            elif tipo_afiliacao == 'FECHADA':
                receba_ate = list_text[list_text.index('Solicitar') - 4].replace(".", "").replace(",", ".")
                moeda = list_text[list_text.index('Solicitar') - 5]
                preco_max = list_text[list_text.index('Solicitar') + 10][:-1].replace(".", "").replace(",", ".")

                moeda = tratar_moeda(moeda)
                preco_max = tratar_preco_max(preco_max)
                receba_ate = tratar_receba_ate(receba_ate)
            else:
                receba_ate = list_text[list_text.index('Afiliado(a).') - 7].replace(".", "").replace(",", ".")
                moeda = list_text[list_text.index('Afiliado(a).') - 8]
                preco_max = 0

            temperatura = int(list_text[list_text.index('TEMPERATURA') + 1][:-1])
            blueprint = int(list_text[list_text.index('BLUEPRINT') + 1][:-1])
            satisfacao = float(list_text[list_text.index('SATISFAÇÃO') + 1][:-1])

            # DESCRIÇAO

            descricao = " ".join(list_text[list_text.index('Divulgação') + 1:list_text.index('Idioma:')])

            # LINKS

            time.sleep(2)

            dict_append = {
                "id": id,
                "name": curso,
                "creator": criado_por,
                "email": email,
                "affiliationType": tipo_afiliacao,
                "language": idioma,
                "category": assunto,
                "maxPay": receba_ate,
                "maxPrice": preco_max,
                "currency": moeda,
                "temperature": temperatura,
                "blueprint": blueprint,
                "rating": satisfacao,
                "description": descricao,
                "productUrl": url,

            }
            time.sleep(2)

            return dict_append

        def get_sales(df_cursos):

            df_cursos['fullLink'] = ""
            df_cursos['salesLink'] = ""
            df_cursos['affiliateCode'] = ""

            for i in range(0, len(df_cursos['affiliateUrl'])):
                try:
                    url = df_cursos['affiliateUrl'].iloc[i]
                    driver.get(url)
                    time.sleep(2)
                    full_link = driver.current_url
                    sales_link = driver.current_url.split('?ref=')[0]
                    affiliate_code = driver.current_url.split('?ref=')[1]
                    df_cursos.at[i, 'fullLink'] = full_link
                    df_cursos.at[i, 'salesLink'] = sales_link
                    df_cursos.at[i, 'affiliateCode'] = affiliate_code
                    print("OK " + str(i))
                except:
                    print("ERRO em " + str(i))

                df_cursos.to_excel(f"G:\\My Drive\\Affiliate Marketing\\urls_new_courses\\{str(data.year)}\\{dict_months[data.month]}\\df_urls_infos_sales_{country}_{data_string}.xlsx")


        for i in range(0, len(df_urls)):
            url = df_urls['courseUrl'].iloc[i]
            try:
                dict_append = get_data(url)
                df_final = df_final.append(dict_append, ignore_index=True)
                print(i)
            except:
                print(str(i) + " erro")

            df_final.to_excel(f"G:\\My Drive\\Affiliate Marketing\\already_affiliated\\{str(data.year)}\\{dict_months[data.month]}\\df_urls_infos_{country}_{data_string}.xlsx")


        df_cursos = df_final.copy()

        # get_sales(df_cursos)


    if st.button('Rodar'):
        df_urls = pd.read_excel(total_path)
        get_courses_infos(df_urls)
