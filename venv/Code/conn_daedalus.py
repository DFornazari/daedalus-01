
def conn_daedalus01():
    import psycopg2

    server = '34.95.215.207'
    port = '4532'
    db = 'daedalus-01'
    user = 'dforn'
    password = '28089346'

    string = f"host='{server}' dbname='{db}' user= '{user}' password='{password}'"

    conn = psycopg2.connect(string)

    return conn

conn = conn_daedalus01()
cursor = conn.cursor()

import pandas as pd

df = pd.read_csv("G:\\My Drive\\Finance\\Quant\\Database\\xlsx\\TICKERS.csv", sep=";", dtype ="str")

for i in range(0,len(df)):
    ticker = df['TICKER'].iloc[i]
    nome_empresa = df['NOME_EMPRESA'].iloc[i]
    cnpj = df['CNPJ'].iloc[i]
    seg_bovespa = df['SEGMENTO_BOVESPA'].iloc[i]
    sub_bovespa = df['SUBSETOR_BOVESPA'].iloc[i]
    setor_economatica = df['SETOR_ECONOMATICA'].iloc[i]
    naics = df['NAICS'].iloc[i]

    query_insert = (f"INSERT INTO TB_TICKERS_ACOES_BOVESPA (TICKER, NOME_EMPRESA, CNPJ, SEGMENTO_BOVESPA, SUBSETOR_BOVESPA, SETOR_ECONOMATICA, NAICS) VALUES (" \
                    f"'{ticker}', '{nome_empresa}', '{cnpj}', '{seg_bovespa}', '{sub_bovespa}', '{setor_economatica}', '{naics}')")

    cursor.execute(query_insert)

conn.commit()
