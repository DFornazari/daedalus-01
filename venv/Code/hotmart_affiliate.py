
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

# credentials = {"email":"amaisafilio@gmail.com", "password": "strike00#"}
credentials = {"email":"daedalus.tecnologia@gmail.com", "password": "28089346Df"}
url_login = r"https://app-vlc.hotmart.com/login"

#Selenium setup
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--proxy-bypass-list=*")
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())




#Attempt Login
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

url_switch = False


if url_switch == True:
    #Get market page
    list_market_types = ['?tab=special', '?tab=firstSales', '?tab=hottest', '?tab=dearest', '?tab=newest']
    # list_market_types = ['?tab=hottest', '?tab=dearest', '?tab=newest']
    list_urls_total = []
    for i in list_market_types:
        url_market = r"https://app-vlc.hotmart.com/market" + i
        driver.get(url_market)
        time.sleep(10)

        continue_a = False
        #MAY BREAK
        while continue_a == False:
           try:
                backdrop = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[2]/main/div/div[2]/div[1]')
                backdrop.click()
                continue_a = True
           except:
                print("Could not find backdrop XPATH")
                time.sleep(2)

        # MAY BREAK
        # load_more_button = driver.find_element_by_xpath('//*[@id="__blaze-root"]/div/div[2]/main/div/div[2]/div[5]/div[2]/a')
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



        #Get source code and get product urls
        html_source = driver.page_source

        positions = re.finditer('/products/view', html_source)

        list_positions = []
        for i in positions:
                list_positions.append(i.span())

        list_urls_raw = []
        for i in list_positions:
            list_urls_raw.append(html_source[i[0]: i[1]+37])

        list_urls_products = []
        for i in list_urls_raw:
            list_urls_products.append("https://app-vlc.hotmart.com" + i)

        list_urls_products = list(dict.fromkeys(list_urls_products))
        list_urls_total = list_urls_total + list_urls_products

    list_urls_total = list(dict.fromkeys(list_urls_total))

    df_urls = pd.DataFrame(list_urls_total)
    df_urls.columns = ['URL']
    df_urls.to_excel("G:\My Drive\Affiliate Marketing\df_urls2.xlsx")

else: df_urls = pd.read_excel("G:\My Drive\Affiliate Marketing\df_urls2.xlsx")
# df_urls = df_urls.iloc[50:]


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
        "affiliateUrl"
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

    #IDENTIFICAÇÃO
    id = list_text[list_text.index('ID')+1]

    len_name = len(list_text[list_text.index('Produtor(a)')+1:list_text.index('ID')-1])
    len_name = (len_name+1)/2
    curso = " ".join(list_text[list_text.index('Produtor(a)')+1:list_text.index('Produtor(a)')+1+int(len_name)])

    owner_index = [i for i, x in enumerate(list_text) if x == "•"]
    criado_por = " ".join(list_text[owner_index[0]+3:owner_index[1]])

    email = list_text[list_text.index('suporte:')+1]

    idioma = list_text[list_text.index('Idioma:')+1]

    assunto = " ".join(list_text[list_text.index('Assunto:')+1:list_text.index('Checkout:')-2])

    text_afiliacao = f"""Olá!

Me chamo Daniel e sou da Daedalus Digital Marketing, somos uma empresa 100% focada no mercado de afiliação.

Através das nossas estratégias de tráfego pago, tráfego orgânico, blog posts, entre outras nós já realizamos mais de 10.000 vendas para os nossos parceiros.

A princípio nós gostaríamos de fazer campanhas de tráfego pago para impulsionar as vendas do produto "{curso}".

Utilizaremos estratégias no Google Ads e Facebook Ads.

E-mail que pedimos a afiliação: daedalus.tecnologia@gmail.com

Muito obrigado!

Atenciosamente, 

Daedalus Digital Market
"""


    #METRICAS

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
        moeda = list_text[list_text.index('Afiliar-se')-5]
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


    temperatura = int(list_text[list_text.index('TEMPERATURA')+1][:-1])
    blueprint = int(list_text[list_text.index('BLUEPRINT') + 1][:-1])
    satisfacao = float(list_text[list_text.index('SATISFAÇÃO') + 1][:-1])

    #DESCRIÇAO

    descricao = " ".join(list_text[list_text.index('Divulgação')+1:list_text.index('Idioma:')])

    #LINKS

    time.sleep(2)


    if tipo_afiliacao == 'ABERTA':

        afiliar_se_agora = driver.find_element(By.XPATH, "//*[text()='Afiliar-se Agora']")
        afiliar_se_agora.click()
        time.sleep(2)
        sim_me_afiliar = driver.find_element(By.XPATH, "//*[text()='Sim, me afiliar']")
        sim_me_afiliar.click()
        time.sleep(2)
        veja_link_divulgacao = driver.find_element(By.XPATH, "//*[text()='Ver links de divulgação']")
        veja_link_divulgacao.click()
        time.sleep(5)
        textbox = driver.find_element(By.CLASS_NAME, "hot-form-control")
        affiliate_url = textbox.get_attribute("value")


    elif tipo_afiliacao == 'FECHADA':

        pedir_afiliacao = driver.find_element(By.XPATH, "//*[text()='Solicitar Afiliação']")
        pedir_afiliacao.click()
        time.sleep(2)
        sim_enviar_pedido = driver.find_element(By.XPATH, "//*[text()='Sim, enviar pedido']")
        sim_enviar_pedido.click()
        time.sleep(2)
        textbox_estrategia = driver.find_element_by_xpath('//*[contains(@id, "requested-strategy-message")]')
        textbox_estrategia.send_keys(text_afiliacao)
        time.sleep(2)
        solicitar_click = driver.find_element(By.XPATH, "//*[text()='Solicitar']")
        solicitar_click.click()
        affiliate_url = 'PEDIDO ENVIADO'

    else:
        ver_link = driver.find_element(By.XPATH, "//*[text()='Ver links de divulgação']")
        ver_link.click()
        time.sleep(5)
        textbox = driver.find_element(By.CLASS_NAME, "hot-form-control")
        affiliate_url = textbox.get_attribute("value")




    dict_append ={
        "id":id,
        "name":curso,
        "creator":criado_por,
        "email":email,
        "affiliationType":tipo_afiliacao,
        "language":idioma,
        "category":assunto,
        "maxPay":receba_ate,
        "maxPrice":preco_max,
        "currency":moeda,
        "temperature":temperatura,
        "blueprint":blueprint,
        "rating":satisfacao,
        "description":descricao,
        "productUrl":url,
        "affiliateUrl":affiliate_url


    }
    time.sleep(2)

    return dict_append

counter = 0
for i in range(0, len(df_urls)):
    url = df_urls['URL'].iloc[i]
    try:
        dict_append = get_data(url)
        df_final = df_final.append(dict_append, ignore_index=True)
        print(i)
    except:
        print(str(i) + " erro")
    # counter = counter + 1
    # if counter in list(range(0,1000,50)):
    #     df_final.to_excel(f"G:\My Drive\Affiliate Marketing\df_final{i}.xlsx")

    df_final.to_excel("G:\My Drive\Affiliate Marketing\df_final.xlsx")

