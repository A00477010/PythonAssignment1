import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt


def get_coin_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    return response.json()['prices'] if response.status_code == 200 else []


def get_coin_id(name):
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    if response.status_code == 200:
        for coin in response.json():
            if coin['name'].lower() == name.lower():
                return coin['id']
    return None

# UI
st.title("Cryptocurrency Comparison")

coin1_name = st.text_input("Enter the name of the first cryptocurrency and press 'ENTER' after entering value ")
coin2_name = st.text_input("Enter the name of the second cryptocurrency and press 'ENTER' after entering value ")
timeframe = st.selectbox("Select the timeframe for comparison:", ['1 week', '1 month', '1 year', '5 years'])

timeframe_dict = {'1 week': 7, '1 month': 30, '1 year': 365, '5 years': 1825}
days = timeframe_dict[timeframe]

if st.button("Compare"):
    coin1_id = get_coin_id(coin1_name)
    coin2_id = get_coin_id(coin2_name)

    if coin1_id and coin2_id:
        data1 = get_coin_data(coin1_id, days)
        data2 = get_coin_data(coin2_id, days)

        if data1 and data2:
            df1 = pd.DataFrame(data1, columns=['timestamp', 'price'])
            df1['date'] = pd.to_datetime(df1['timestamp'], unit='ms')

            df2 = pd.DataFrame(data2, columns=['timestamp', 'price'])
            df2['date'] = pd.to_datetime(df2['timestamp'], unit='ms')

            # Plotting
            plt.figure(figsize=(10, 6))
            plt.plot(df1['date'], df1['price'], label=coin1_name)
            plt.plot(df2['date'], df2['price'], label=coin2_name)
            plt.xlabel("Date")
            plt.ylabel("Price in USD")
            plt.title(f"{coin1_name} vs {coin2_name} Price Comparison")
            plt.legend()
            st.pyplot(plt)
        else:
            st.error("Failed to fetch data for one or both coins.")
    else:
        st.error("Please make sure both cryptocurrency names are valid.")
if st.button("Reset"):
    # Clear the session state (thus resetting the form)
    st.session_state['coin1_name'] = ""
    st.session_state['coin2_name'] = ""
    # Rerun the app to reflect the reset state
    st.experimental_rerun()
