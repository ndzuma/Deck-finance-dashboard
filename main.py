import streamlit as st
import yfinance as yf
import numpy as np
import plotly.express as px
import pandas as pd
from crypto import get_rank as cr
from crypto import get_info as ci
from stocks import  get_data as si

# ----- Page configurations -----
st.set_page_config(
    page_title="Deck Finance",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# ----- Container initialisation -----
header = st.container()
dataset = st.container()
features = st.container()
footer = st.container()


# ----- Function initialisation -----
def comma(value):
    value1 = str(value)
    values = []
    new_values = []
    final = ""

    # Checks if the value given is more than 999 then checks if value
    # is a decimal (e.g. 0.2128) and if not it returns the same value
    # but if it is more than 999 then it adds a comma to the value
    # and returns that value
    if len(value1) <= 3:
        return value
    elif value1[1] == ".":
        return value
    else:
        # Count is used to place the comma in an interval of 3
        count = 0

        # The characters of a string are added to an array --> value1
        for each in value1:
            values.append(each)

        # value1 is reversed in order to avoid putting commas in decimals
        # And commas are placed on an interval of 3
        array1 = np.flip(np.array(values))
        for i in array1:
            if count == 3:
                new_values.append(",")
                new_values.append(i)
                count = 1
            else:
                new_values.append(i)
                count += 1

        # The array is flipped back to the correct orientation
        # And the array is turned into the final string
        values = np.flip(np.array(new_values))
        for l in values:
            final += l

        # Converts final into a list with the command list()
        # Then checks if "." and "," are next to each other
        # If so it removes the "," next to the "."
        final = list(final)
        if final[-3] == "." and final[-4] == ",":
            final[-4] = ""
            final = "".join(final)
        else:
            final = "".join(final)

        return final


@st.cache
def information_gathering_equity(symbol):
    symbol_info = symbol.info
    hist_data = symbol.history(period="5y")
    name = symbol_info["shortName"]
    industry = symbol_info["industry"]
    website = symbol_info["website"]
    recommendation = symbol_info["recommendationKey"]
    summary = symbol_info["longBusinessSummary"]
    price = symbol_info["currentPrice"]
    market_cap = symbol_info["marketCap"]
    week_change = symbol_info["52WeekChange"]
    news = symbol.news

    return hist_data, name, industry, website, recommendation, summary, price, market_cap, week_change, news


# ----- Header section -----
with header:
    st.title("Deck Investments")

# ----- Equity data section -----
with dataset:
    st.subheader("Equities")

    # Columns are being created
    cont_a1, cont_a2, cont_a3, cont_a4 = st.columns(4)
    cont_b1, cont_b2, cont_b3, cont_b4 = st.columns(4)
    cont_c1, cont_c2 = st.columns(2)

    symbol_input = cont_a1.text_input("Symbol")

    # Getting the symbol from the user
    symbol = yf.Ticker(symbol_input)

    if str(symbol) == "yfinance.Ticker object <>":
        pass
    else:
        info = information_gathering_equity(symbol)

        cont_a2.metric("Share Price", f"${info[6]}", "-$150")
        cont_a3.metric("52 Week Change", f"%{info[8] * 100}", "2%")
        cont_a4.metric("Market Cap", f"${comma(info[7])}", "$2")

        cont_b1.caption("Name")
        cont_b1.text(info[1])
        cont_b2.caption("Industry")
        cont_b2.text(info[2])
        cont_b3.caption("website")
        cont_b3.write(f"[{info[3].replace('https://www.', '')}]({info[3]})")
        cont_b4.caption("Institutional recommendation")
        cont_b4.text(str(info[4]).upper())

        cont_c1.text_area("Summary",
                          info[5],
                          400)
        cont_c1.text("Share price (5y)")
        fig = px.line(info[0].Close)
        fig.update_xaxes(rangeslider_visible=True)
        cont_c1.plotly_chart(fig, use_container_width=True)

        cont_c2.text("News")
        # loop outputs the 4 most recent news articles
        for i in range(5):
            cont_c2.write(f"****{info[9][i]['title']}****")
            cont_c2.write(f"by {info[9][i]['publisher']}")
        
        cont_c2.text("AI predictions here.")
        code = """print("Coming soon...")"""
        cont_c2.code(code, language="python")

# ----- Features section -----
with features:
    st.subheader("Features")

    div_1, div_2 = st.columns(2)
    col_1, col_2, col_3, col_4 = st.columns(4)

    selection = div_1.selectbox("", (
        "Trending",
        "Currency converter",
        "Compound interest calculator",
        "Asset tracker",
        "Risk calculator",
        "Asset research helper",
        "Jim Cramer index"
    )
                                )
    
    # The if statement takes care of the selection
    if selection == "Trending":
        col_1.markdown("****Cryptocurrency****")
        col_2.markdown("****Equities****")
        col_3.markdown("****ETFs****")
        col_4.markdown("****Asset Managers****")

        # spaces is supposed to add spaces to the prices of everything
        # below using markdown
        spaces = "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"

        # CRYPTOCURRENCY
        crypto_rank = cr()  # Returns an array of the top 10-12 crypto assets ranked
        for s in range(10):
            s = crypto_rank[s]
            assetData = ci(s)
            # Variable "name" is getting the name of the crypto asset
            # How? This happens because cr() returns 8 different data points
            # These are --> name, price, hist_data,description, algorithm,
            # proofType, ranking, rating, adoptionRating and performanceRating
            # Therefore we have to use an index to get the desired output
            name = assetData[0]
            price = assetData[1]
            price = comma(price)
            ranking = assetData[6]

            col_1.text(f"{ranking}. {name}")
            col_1.markdown(f"{spaces}*${price}*")

        # EQUITIES
        equity_info = si()  # Returns a tuple made up of 4 arrays
        for e in range(10):
            # the variables below are getting their values from equity_info
            rank = equity_info[0][e]
            name = equity_info[1][e]
            price = equity_info[2][e]
            price = comma(price)

            col_2.text(f"{rank}. {name}")
            col_2.markdown(f"{spaces}*${price}*")

        # ETFs
        rank = []
        name = ["SPDR S&P 500 ETF Trust", "iShares Core S&P 500",
                "Vanguard Total Stock Market ETF", "Vanguard S&P 500 ETF",
                "Invesco QQQ ETF", "Vanguard FTSE Developed Markets ETF",
                "Vanguard Value ETF", "iShares Core MSCI EAFE ETF",
                "iShares Core U.S. Aggregate Bond ETF",
                "Vanguard Total Bond Market ETF"]
        price = ["387.13", "389.74", "193.95", "356.95", "283.01",
                "44.45", "137.91", "64.47", "103.6", "76.68"]
        
        # The for loop is adding the rank to the array and outputting it to the page
        for n in range(10):
            rank.append(str(n+1))

            col_3.text(f"{rank[n]}. {name[n]}")
            col_3.markdown(f"{spaces}*${price[n]}*")


        # ASSET MANAGERS
        rank = []
        name = ["BlackRock", "The Vanguard Group", "UBS Group", "Fidelity",
                "State Street Global Advisors", "Morgan Stanley", "JPMorgan Chase",
                "Allianz", "Capital Group", "Goldman Sachs"]
        aum = ["9.464 trillion", "8.4 trillion", "4.432 trillion", "4.23 trillion",
               "3.86 trillion", "3.274 trillion", "2.996 trillion", "2.953 trillion",
               "2.6 trillion", "2.372 trillion"]
        
        # The for loop is adding the rank to the array and outputting it to the page
        for n in range(10):
            rank.append(str(n+1))

            col_4.text(f"{rank[n]}. {name[n]}")
            col_4.markdown(f"{spaces}*${aum[n]}*")

    elif selection == "Currency converter":
        pass

# ----- Footer section -----
with footer:
    pass