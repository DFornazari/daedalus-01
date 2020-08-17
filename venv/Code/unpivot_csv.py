import pandas as pd
import datetime as dt

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



dir = "G:\\My Drive\\Finance\\Quant\\Database\\IBrX-100\\GenCorreto\\"

dir_close = dir + "CLOSE.csv"
dir_high = dir + "HIGH.csv"
dir_low = dir + "LOW.csv"
dir_volume = dir + "VOLUME.csv"
dir_open = dir + "OPEN.csv"

df_close = pd.read_csv(dir_close, sep = ";")
df_high = pd.read_csv(dir_high, sep = ";")
df_low = pd.read_csv(dir_low, sep = ";")
df_volume = pd.read_csv(dir_volume, sep = ";")
df_open = pd.read_csv(dir_open, sep = ";")

list_dfs = [df_close, df_high, df_low, df_volume, df_open]

df_close = df_close.set_index(["DATA"])
df_close = df_close.unstack().reset_index()
df_close.columns = ["TICKER", "DATA", "CLOSE"]

df_high = df_high.set_index(["DATA"])
df_high = df_high.unstack().reset_index()
df_high.columns = ["TICKER", "DATA", "HIGH"]

df_low = df_low.set_index(["DATA"])
df_low = df_low.unstack().reset_index()
df_low.columns = ["TICKER", "DATA", "LOW"]

df_volume = df_volume.set_index(["DATA"])
df_volume = df_volume.unstack().reset_index()
df_volume.columns = ["TICKER", "DATA", "VOLUME"]

df_open = df_open.set_index(["DATA"])
df_open = df_open.unstack().reset_index()
df_open.columns = ["TICKER", "DATA", "OPEN"]

df_consolidado = df_close.merge(df_high, how='inner', on=['TICKER', 'DATA']).merge(df_low, how='inner', on=['TICKER', 'DATA']).merge(df_open, how='inner', on=['TICKER', 'DATA']).merge(df_volume, how='inner', on=['TICKER', 'DATA'])

df_consolidado = df_consolidado[df_consolidado['CLOSE']!=0]
df_consolidado["DATA"] = pd.to_datetime(df_consolidado["DATA"], format="%d/%m/%Y")

df_export = pd.DataFrame(columns = ["DATA", "TICKER", "CLOSE", "OPEN", "HIGH", "LOW", "VOLUME"])


for ticker in df_export.columns:
    df_export[ticker] = df_consolidado[ticker]
    
# df_export['DATA'] = df_export['DATA'].dt.strftime('%Y-%m-%d')
#
# df_export["DATA"] = "'" + df_export["DATA"] + "'"
# df_export["TICKER"] = "'" + df_export["TICKER"] + "'"


df_export.to_csv(dir + "CONSOLIDADO_noheader.csv", sep=",", index=False, header=False)


# for i in range(0, len(df_consolidado)):
#     data = df_consolidado['DATA'].iloc[i]
#     ticker = df_consolidado['TICKER'].iloc[i]
#     close = df_consolidado['CLOSE'].iloc[i]
#     open = df_consolidado['OPEN'].iloc[i]
#     high = df_consolidado['HIGH'].iloc[i]
#     low = df_consolidado['LOW'].iloc[i]
#     volume = df_consolidado['VOLUME'].iloc[i]
#     query = (f"INSERT INTO TB_PRECOS_ACOES (DATA, TICKER, CLOSE, OPEN, HIGH, LOW, VOLUME) " \
#             f"VALUES ('{data}', '{ticker}', {close}, {open}, {high}, {low}, {volume})")
#
#     cursor.execute(query)
#
# conn.commit()
