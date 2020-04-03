import pandas as pd
from pandas.tseries.offsets import MonthEnd, YearEnd, BusinessDay
import requests


res = requests.get('https://fintual.cl/api/real_assets/186/days') 

data = res.json()['data']

df = pd.DataFrame(columns=['price'])

for attribute in data:
    df.loc[ attribute['attributes']['date'] ] = attribute['attributes']['price']

df.index = pd.to_datetime(df.index, format="%Y/%m/%d")

# precios
p     = df['price'][0]
p_eod = df['price'].loc[df.index[0] + BusinessDay(-1)]
p_eom = df['price'].loc[df.index[0] + MonthEnd(-1)]
p_eoy = df['price'].loc[df.index[0] + YearEnd(-1)]

# Final Printout
print('Risky Norris P%L {} DTD, {} MTD, {} YTD'.format(
    round(100*(p/p_eod-1),2),
    round(100*(p/p_eom-1),2),
    round(100*(p/p_eoy-1),2),
    ))

