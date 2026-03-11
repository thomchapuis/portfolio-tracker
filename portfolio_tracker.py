import yfinance as yf
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ETF CAC40
ticker5 = yf.Ticker("CACC.PA")
quantity5 = 5
buy_price = 39.93

infos = ticker5.info

print("------")
#print(f"Previous close: {infos.get('regularMarketPreviousClose')}")
#print(f"Market Price: {infos.get('regularMarketPrice')}")

evolution = round(infos.get('regularMarketPrice')-buy_price,2)
gain_eur = evolution*quantity5
gain_pct = round((evolution/buy_price)*100,2)
total_PTF = quantity5*infos.get('regularMarketPrice')

print(f"Run time: {now}")
print(f"gain Amundi ETF CAC40: {gain_eur}€, soit {gain_pct}%")
print(f"portefeuille PEA: {total_PTF}")
print("------")
