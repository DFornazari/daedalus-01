import streamlit as st
import datetime as dt
import pandas as pd
import hotmart_get_urls
import hotmart_get_info
import hotmart_unnafiliate
import hotmart_affiliate


st.title('Dashboard Daedalus')

data = st.date_input(label='Data:')

pages = {
    "Get URLs": hotmart_get_urls,
    "Get Course Info": hotmart_get_info,
    "Affiliate": hotmart_affiliate,
    "Unaffiliate": hotmart_unnafiliate
}



st.sidebar.title('Menu')
selection = st.sidebar.selectbox("Ir para:", list(pages.keys()))

page = pages[selection]
page.init()