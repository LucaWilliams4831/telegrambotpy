from coinmarketcapapi import CoinMarketCapAPI

cmc = CoinMarketCapAPI('0caa3779-3cb2-4665-a7d3-652823b53908')

r = cmc.cryptocurrency_quotes_latest(symbol='APT')
print(r.data['APT']['quote']['USD']['price'])


  