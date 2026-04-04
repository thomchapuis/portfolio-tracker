import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Portfolio Tracker", layout="wide")

# =========================
# DATA FETCH
# =========================
@st.cache_data(ttl=3600)
def get_etf_data():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticker = yf.Ticker("CACC.PA")
    infos = ticker.info

    market_price = infos.get('regularMarketPrice')

    buy_price_list = [39.93, 38.715]
    quantity_list = [5, 2]

    weighted_sum = sum(price * qty for price, qty in zip(buy_price_list, quantity_list))
    total_quantity = sum(quantity_list)
    buy_price = weighted_sum / total_quantity

    quantity = total_quantity

    evolution = round(market_price - buy_price, 2)
    gain_eur = evolution * quantity
    gain_pct = round((evolution / buy_price) * 100, 2)
    total_PTF = quantity * market_price

    return {
        "timestamp": now,
        "market_price": market_price,
        "buy_price": buy_price,
        "quantity": quantity,
        "evolution": evolution,
        "gain_eur": gain_eur,
        "gain_pct": gain_pct,
        "total_PTF": total_PTF
    }

# =========================
# SAVE CSV
# =========================
def save_data_to_csv(data, filename="etf_history.csv"):
    df = pd.DataFrame([data])
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        df_combined.to_csv(filename, index=False)
    else:
        df.to_csv(filename, index=False)

# =========================
# LOAD HISTORY
# =========================
def load_history(filename="etf_history.csv"):
    if not os.path.exists(filename):
        return pd.DataFrame()
    df = pd.read_csv(filename)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# =========================
# UI
# =========================
st.title("📊 Portfolio Tracker")

tab1, tab2 = st.tabs(["📋 Portefeuille", "📈 Graphique"])

# =========================
# TAB 1 : PORTEFEUILLE
# =========================
with tab1:
    st.subheader("Situation actuelle")

    if st.button("🔄 Rafraîchir les données"):
        data = get_etf_data()
        save_data_to_csv(data)

    df = load_history()

    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        latest_row = df.sort_values("timestamp").iloc[-1]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("💰 Valeur portefeuille", f"{latest_row['total_PTF']:.2f} €")
        col2.metric("🛒 Prix moyen achat", f"{latest_row['buy_price']:.2f} €")
        col3.metric("📈 Gain (€)", f"{latest_row['gain_eur']:.2f} €")
        col4.metric("📊 Gain (%)", f"{latest_row['gain_pct']:.2f} %")

        st.divider()
        st.subheader("Ligne du jour")
        st.dataframe(latest_row.to_frame().T)

# =========================
# TAB 2 : GRAPHIQUE
# =========================
with tab2:
    st.subheader("Évolution du portefeuille")

    df = load_history()

    if df.empty:
        st.warning("Pas encore de données historiques.")
    else:
        df = df.sort_values("timestamp")

        fig, ax = plt.subplots()
        ax.plot(df["timestamp"], df["total_PTF"], marker='o')
        ax.set_title("Valeur du portefeuille dans le temps")
        ax.set_xlabel("Date")
        ax.set_ylabel("€")
        plt.xticks(rotation=45)

        st.pyplot(fig)
