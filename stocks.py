import pandas as pd
import requests


#  Data is from https://companiesmarketcap.com/
query_string = "https://companiesmarketcap.com/?download=csv"

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'referer': 'https://www.google.com/'
}


def get_data():
    rank = []
    name = []
    symbol = []
    price = []

    response = requests.get(query_string, headers=header)
    response.encoding = "utf-8"
    csv_file = response.text
    with open("data\stockMarketCapRanking.csv", "w", encoding="utf-8") as data:
        data.write(str(csv_file))
        data.close()

    csv_file = pd.read_csv("data\stockMarketCapRanking.csv")

    for e in range(10):
        rank.append(csv_file["Rank"][e])
        name.append(csv_file["Name"][e])
        symbol.append(csv_file["Symbol"][e])
        price.append(csv_file["price (USD)"][e])

    return rank, name, price, symbol
