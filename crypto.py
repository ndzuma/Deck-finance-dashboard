import cryptocompare as cc

lists = cc.get_coin_list(format=False)


def get_rank():
    top_10 = []
    count = 1
    while len(top_10) <= 10:
        for symbol in lists:
            info = lists[f"{symbol}"]
            post = info["SortOrder"]
            if int(post) == count:
                top_10.append(symbol)
                count += 1

    return top_10


# CoinName TotalCoinSupply Description AssetTokenStatus Rating
def get_info(symbol):
    info = lists[symbol]
    name = info["CoinName"]
    descriiption = info["Description"]
    algorithm = info["Algorithm"]
    proofTyper = info["ProofType"]
    ranking = info["SortOrder"]
    rating = info["Rating"]["Weiss"]["Rating"]
    adoptionRating = info["Rating"]["Weiss"]["TechnologyAdoptionRating"]
    performanceRating = info["Rating"]["Weiss"]["MarketPerformanceRating"]

    price = cc.get_price(symbol, currency="USD")
    price = price[symbol]["USD"]
    hist_data = cc.get_historical_price_day(symbol, currency="USD")

    return name, price, hist_data, descriiption, algorithm, proofTyper, ranking, rating, adoptionRating, performanceRating
