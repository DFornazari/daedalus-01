
import pandas as pd
import numpy as np
import datetime as dt

refdate_start = dt.date(2020,8,13)


df_close = pd.read_csv("G:\\My Drive\\Finance\\Quant\\Database\\xlsx\\df_close.csv", sep = ";")
df_close.columns = list(df_close.columns)

df_close.replace(0, np.nan, inplace=True)



df_close["DATA"] = pd.to_datetime(df_close["DATA"])
df_close["DATA"] = df_close["DATA"].dt.date

df_close.set_index(["DATA"], inplace=True)

df_valid = pd.DataFrame(columns=["TICKER", "FIRST_DATE", "TOTAL_DAYS", "TOTAL_VALID"])
df_close_columns = list(df_close.columns)

for ticker in df_close_columns:
    df_valid = df_valid.append([{"TICKER":ticker, "FIRST_DATE":np.nan, "TOTAL_DAYS":np.nan, "TOTAL_VALID":np.nan}], ignore_index=True)

for i in range(0,len(df_valid)):
    df_valid["FIRST_DATE"].iloc[i] = df_close[df_valid["TICKER"].iloc[i]].first_valid_index()

df_valid["TOTAL_DAYS"] = np.where(df_valid["FIRST_DATE"]!=None, refdate_start-df_valid["FIRST_DATE"], np.nan)

df_valid["TOTAL_DAYS"] = abs(df_valid["TOTAL_DAYS"].dt.days)

for i in range(0,len(df_valid)):
    df_valid["TOTAL_VALID"].iloc[i] = df_close[df_valid["TICKER"].iloc[i]].isna().sum()