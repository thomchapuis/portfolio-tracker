import yfinance as yf
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

# Fonction pour récupérer les données de l'ETF CAC40
def get_etf_data():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticker = yf.Ticker("CACC.PA")
    infos = ticker.info

    # Récupération des données clés
    market_price = infos.get('regularMarketPrice')
    buy_price_list = [39.93,38.715]
    quantity_list = [5,2]
    
    # Calcul du prix moyen pondéré par les quantités
    weighted_sum = sum(price * qty for price, qty in zip(buy_price_list, quantity_list))
    total_quantity = sum(quantity_list)
    buy_price = weighted_sum / total_quantity
    
    # Quantité totale
    quantity = total_quantity

    # Calculs
    evolution = round(market_price - buy_price, 2)
    gain_eur = evolution * quantity
    gain_pct = round((evolution / buy_price) * 100, 2)
    total_PTF = quantity * market_price

    # Retourne un dictionnaire avec les données
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

# Fonction pour sauvegarder les données dans un DataFrame et un fichier CSV
def save_data_to_csv(data, filename="etf_history.csv"):
    df = pd.DataFrame([data])
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename)
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        df_combined.to_csv(filename, index=False)
    else:
        df.to_csv(filename, index=False)

# Fonction pour afficher l'historique et générer un graphique
def plot_history(filename="etf_history.csv"):
    if not os.path.exists(filename):
        print("Aucune donnée disponible pour l'historique.")
        return

    df = pd.read_csv(filename)
    df = pd.read_csv(filename)
    
    # Conversion robuste
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    # Supprimer les lignes invalides
    df = df.dropna(subset=["timestamp"])
    
    # Trier
    df = df.sort_values("timestamp")
    
    # Extraire la date
    df["date"] = df["timestamp"].dt.date
    
    # Garder la dernière valeur par jour
    df = df.groupby("date").last().reset_index()
    print("\nHistorique des données :")
    print(df)

    # Génération du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(df["timestamp"], df["market_price"], marker='o', label="Prix du marché")
    plt.title("Évolution du prix de l'ETF CAC40")
    plt.xlabel("Date et heure")
    plt.ylabel("Prix (€)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("etf_history.png", format='png', dpi=200)
    plt.close()
    print("\nGraphique sauvegardé sous 'etf_history.png'.")

# Exécution principale
if __name__ == "__main__":
    data = get_etf_data()
    print("------")
    print(f"Run time: {data['timestamp']}")
    print(f"Gain Amundi ETF CAC40: {data['gain_eur']}€, soit {data['gain_pct']}%")
    print(f"Portefeuille PEA: {data['total_PTF']}€")
    print("------")

    # Sauvegarde des données
    save_data_to_csv(data)

    # Affichage de l'historique et génération du graphique
    plot_history()
