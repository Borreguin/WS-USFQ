import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from p1_uml_util import (
    read_csv_file, alias,
    lb_timestamp,
    lb_V005_vent01_CO2,
    lb_V022_vent02_CO2,
    lb_V006_vent01_temp_out,
    lb_V023_vent02_temp_out
)

def prepare_data():
    script_path = os.path.dirname(__file__)
    data_path = os.path.join(script_path, "data")
    file_path = os.path.join(data_path, "data.csv")
    df = read_csv_file(file_path)
    df[lb_timestamp] = pd.to_datetime(df[lb_timestamp], format="%d.%m.%Y %H:%M")
    df["date"] = df[lb_timestamp].dt.date
    df["hour"] = df[lb_timestamp].dt.hour
    df["hour_decimal"] = df[lb_timestamp].dt.hour + df[lb_timestamp].dt.minute / 60
    df["day"] = df[lb_timestamp].dt.date
    return df

def plot_daily_graphs(df: pd.DataFrame):
    variables = [
        lb_V005_vent01_CO2,
        lb_V022_vent02_CO2,
        lb_V006_vent01_temp_out,
        lb_V023_vent02_temp_out
    ]
    for var in variables:
        plt.figure(figsize=(12, 5))
        for date, group in df.groupby("date"):
            plt.plot(group["hour_decimal"], group[var], alpha=0.4)
        plt.title(f"Valores diarios superpuestos: {alias[var]}")
        plt.xlabel("Hora del día (decimal)")
        plt.ylabel(alias[var])
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def analyze_patterns_and_anomalies(df: pd.DataFrame):
    variables = [
        lb_V005_vent01_CO2,
        lb_V022_vent02_CO2,
        lb_V006_vent01_temp_out,
        lb_V023_vent02_temp_out
    ]

    for var in variables:
        pivot = df.pivot_table(index="day", columns="hour", values=var)
        pivot = pivot.dropna()
        X = StandardScaler().fit_transform(pivot)

        # KMeans clustering
        kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
        kmeans_labels = kmeans.labels_

        # DBSCAN clustering
        dbscan = DBSCAN(eps=1.5, min_samples=2).fit(X)
        dbscan_labels = dbscan.labels_

        # PCA for plotting
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)

        # Plot clustering
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans_labels, cmap="Set1")
        plt.title(f"{alias[var]} - KMeans")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")

        plt.subplot(1, 2, 2)
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=dbscan_labels, cmap="Set2")
        plt.title(f"{alias[var]} - DBSCAN")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.tight_layout()
        plt.show()

        # Detect anomalies (label -1 in DBSCAN)
        anomalies = pivot.index[dbscan_labels == -1]
        print(f"Anomalías en {alias[var]}:")
        for d in anomalies:
            print(f"  - {d}")
        print()

if __name__ == "__main__":
    df = prepare_data()
    plot_daily_graphs(df)                 # Literal A
    analyze_patterns_and_anomalies(df)    # Literales B y C