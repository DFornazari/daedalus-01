import psycopg2

server = '34.95.215.207'
port = '4532'
db = 'daedalus-01'
user = 'dforn'
password = '28089346'

string = f"host='{server}' dbname='{db}' user= '{user}' password='{password}'"

conn = psycopg2.connect(string)

cursor = conn.cursor()

query = 'SELECT * FROM TESTE_01'

import pandas as pd

df = pd.read_sql(query, conn)
print(df)
