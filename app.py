import pandas as pd
from pandas.tseries.offsets import MonthEnd, YearEnd, BusinessDay
import requests

from flask import Flask
app = Flask(__name__)


res = requests.get('https://fintual.cl/api/real_assets/186/days') 

data = res.json()['data']

df = pd.DataFrame(columns=['price'])

for attribute in data:
    df.loc[attribute['attributes']['date'] ] = attribute['attributes']['price']

df.index = pd.to_datetime(df.index, format="%Y/%m/%d")

# precios
p     = df['price'][0]
p_eod = df['price'].loc[df.index[0] + BusinessDay(-1)]
p_eom = df['price'].loc[df.index[0] + MonthEnd(-1)]
p_eoy = df['price'].loc[df.index[0] + YearEnd(-1)]


@app.route('/')
def hello():
    return "Risky Norris P&L {}  <br/> \
            <br/>\
            {:10.2f}% DTD  <br/>  \
            {:10.2f}% MTD  <br/> \
            {:10.2f}% YTD  <br/>".format(df.index[0].date(), p/p_eod-1, p/p_eom, p/p_eoy)

if __name__ == '__main__':
    app.run()
