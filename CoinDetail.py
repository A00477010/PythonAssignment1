import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import random

def get_coin_list():
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Fetch historical market data for a coin
def get_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=365"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


st.title("Cryptocurrency Details Explorer")

# Display a random selection of cryptocurrency names for suggestion
coins = get_coin_list()
if coins:
    random.shuffle(coins) # Shuffle the list to get random coins
    suggested_names = ', '.join([coin['name'] for coin in coins[:7]])
    st.sidebar.markdown(f"### 💡 Want some name suggestions?")
    st.sidebar.info(f"Here are some random picks: {suggested_names}")

coin_name = st.text_input("Enter the name of a cryptocurrency (e.g., Bitcoin, Ethereum):")

if coin_name:
    coin_id = next((item["id"] for item in coins if item["name"].lower() == coin_name.lower()), None)

    if coin_id:
        data = get_coin_data(coin_id)

        if data:
            prices = data["prices"]
            df = pd.DataFrame(prices, columns=["timestamp", "price"])
            df["date"] = pd.to_datetime(df["timestamp"], unit='ms')

            # Data Visualization
            fig, ax = plt.subplots()
            ax.plot(df["date"], df["price"], label="Price", color='purple')
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Price in USD", fontsize=12)
            ax.set_title(f"{coin_name} Price Over the Last Year", fontsize=14)
            ax.grid(True, which='major', linestyle='--', linewidth='0.5', color='grey')
            ax.legend()
            st.pyplot(fig)

            # Display max and min details
            max_price = df["price"].max()
            min_price = df["price"].min()
            max_date = df[df["price"] == max_price]["date"].dt.date.iloc[0]
            min_date = df[df["price"] == min_price]["date"].dt.date.iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Maximum Price", value=f"${max_price:.2f}", delta=str(max_date))
            with col2:
                st.metric(label="Minimum Price", value=f"${min_price:.2f}", delta=str(min_date))

            # Additional info for highest and lowest trading days
            st.write(f"**Highest Trading Day:** {max_date.strftime('%Y-%m-%d')}")
            st.write(f"**Lowest Trading Day:** {min_date.strftime('%Y-%m-%d')}")

        else:
            st.error("Failed to fetch data for the selected coin.")
    else:
        st.error("Invalid cryptocurrency name. Please enter a valid name.")

