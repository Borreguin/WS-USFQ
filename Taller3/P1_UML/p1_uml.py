import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin_min

# === Configurar sys.path para importar utilidades ===
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_path, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from Taller3.P1_UML.p1_uml_util import *


# === Preparación de datos ===
def prepare_data():
    script_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_path, "data")
    file_path = os.path.join(data_path, "data.csv")
    _df = read_csv_file(file_path)
    _df[lb_timestamp] = pd.to_datetime(_df[lb_timestamp], dayfirst=True, errors='coerce')
    _df.set_index(lb_timestamp, inplace=True)
    _df.index = pd.to_datetime(_df.index, errors='coerce')
    print(_df.dtypes)
    return _df


# === Visualización ===
def plot_data(_df: pd.DataFrame, lb1, lb2, legend):
    df_to_plot = _df.tail(1000)
    if df_to_plot.empty:
        print(f"Warning: No data to plot for {legend}")
        return
    plt.plot(df_to_plot.index, df_to_plot[lb1], label=alias.get(lb1, lb1))
    plt.plot(df_to_plot.index, df_to_plot[lb2], label=alias.get(lb2, lb2))
    plt.xlabel(lb_timestamp)
    plt.ylabel(legend)
    plt.legend()
    plt.show()
    plt.close()


def plot_variable_por_dia(df: pd.DataFrame, variable: str, expected_length: int = 24):
    df = df.copy()
    df['date'] = df.index.date
    grouped = df.groupby('date')[variable]
    plt.figure(figsize=(10, 5))
    for date, group in grouped:
        if len(group) == expected_length:
            hours = group.index.hour if isinstance(group.index, pd.DatetimeIndex) else range(len(group))
            plt.plot(hours, group.values, alpha=0.5, label=str(date))
    plt.title(f"Patrones diarios superpuestos - {alias.get(variable, variable)}")
    plt.xlabel("Hora del día")
    plt.ylabel(alias.get(variable, variable))
    plt.grid(True)
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), fontsize='small')
    plt.show()
    plt.close()


def plot_boxplot_por_hora(df: pd.DataFrame, variable: str):
    df = df.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, errors='coerce')
    df['hour'] = df.index.hour
    plt.figure(figsize=(10, 5))
    df.boxplot(column=variable, by='hour')
    plt.title(f"Distribución diaria por hora - {alias.get(variable, variable)}")
    plt.suptitle("")
    plt.xlabel("Hora del día")
    plt.ylabel(alias.get(variable, variable))
    plt.grid(True)
    plt.show()
    plt.close()


# === Clustering ===
def reshape_data_by_day(df: pd.DataFrame, variable: str, expected_length: int = 24):
    df = df.copy()
    df['date'] = df.index.date
    df['hour'] = df.index.hour
    pivot = df.pivot_table(index='date', columns='hour', values=variable)
    pivot = pivot.dropna(thresh=expected_length)
    return pivot


def cluster_kmeans(X, n_clusters=3):
    model = KMeans(n_clusters=n_clusters, random_state=0)
    labels = model.fit_predict(X)
    return labels, model


def cluster_agglomerative(X, n_clusters=3):
    model = AgglomerativeClustering(n_clusters=n_clusters)
    labels = model.fit_predict(X)
    return labels, model


def plot_cluster_patterns(X, labels, method_name):
    X['cluster'] = labels
    cluster_means = X.groupby('cluster').mean()
    plt.figure(figsize=(10, 5))
    for cluster_id, row in cluster_means.iterrows():
        plt.plot(row.index, row.values, label=f'Cluster {cluster_id}')
    plt.title(f'Cluster Patterns - {method_name}')
    plt.xlabel("Hora")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.close()


def run_clustering_all_variables(df, variables, n_clusters=3, expected_length=24):
    for var in variables:
        print(f"\n Analizando variable: {alias.get(var, var)}")
        X = reshape_data_by_day(df, var, expected_length)
        if X.empty:
            print(f"️  No hay datos suficientes para: {alias.get(var, var)}")
            continue
        labels_kmeans, _ = cluster_kmeans(X, n_clusters)
        plot_cluster_patterns(X.copy(), labels_kmeans, f"K-Means - {alias.get(var, var)}")
        labels_agglom, _ = cluster_agglomerative(X, n_clusters)
        plot_cluster_patterns(X.copy(), labels_agglom, f"Agglomerative - {alias.get(var, var)}")


# === Análisis de anomalías ===
def detect_anomalies(df, variable, n_clusters=3, threshold=2.0):
    print(f"\n Detectando anomalías en: {alias.get(variable, variable)}")
    X = reshape_data_by_day(df, variable)
    if X.empty:
        print("No hay datos suficientes.")
        return
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    labels = kmeans.fit_predict(X)
    _, distances = pairwise_distances_argmin_min(X, kmeans.cluster_centers_)
    anomaly_indices = np.where(distances > threshold)[0]
    anomalous_days = X.index[anomaly_indices]
    print(f"🔍 Se encontraron {len(anomalous_days)} días atípicos (distancia > {threshold})")

    # Visualización
    plt.figure(figsize=(10, 5))
    for idx in anomaly_indices:
        row = X.iloc[idx]
        plt.plot(row.index, row.values, alpha=0.6, label=str(row.name))
    plt.title(f"Perfiles atípicos - {alias.get(variable, variable)}")
    plt.xlabel("Hora")
    plt.ylabel("Valor")
    plt.legend(fontsize='small', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()

def reshape_multivariable_by_day(df: pd.DataFrame, variables: list, expected_length: int = 24):
    df = df.copy()
    df['date'] = df.index.date
    df['hour'] = df.index.hour
    daily_data = []

    for var in variables:
        pivot = df.pivot_table(index='date', columns='hour', values=var)
        daily_data.append(pivot)

    # Concatenar horizontalmente (cada fila = un día con varias variables/hora)
    combined = pd.concat(daily_data, axis=1)
    combined = combined.dropna(thresh=len(variables) * expected_length)
    return combined


def run_multivariable_clustering(df, variable_pairs, n_clusters=3):
    for var1, var2 in variable_pairs:
        print(f"\n📊 Análisis multivariable: {alias.get(var1, var1)} + {alias.get(var2, var2)}")
        X = reshape_multivariable_by_day(df, [var1, var2])
        if X.empty:
            print("⚠️  No hay datos suficientes.")
            continue

        # KMeans
        labels_kmeans, _ = cluster_kmeans(X, n_clusters)
        plot_cluster_patterns(X.copy(), labels_kmeans, f"K-Means - {alias.get(var1)} + {alias.get(var2)}")

        # Agglomerative
        labels_agglom, _ = cluster_agglomerative(X, n_clusters)
        plot_cluster_patterns(X.copy(), labels_agglom, f"Agglomerative - {alias.get(var1)} + {alias.get(var2)}")


def detect_multivariable_anomalies(df, variable_pairs, n_clusters=3, threshold=2.5):
    for var1, var2 in variable_pairs:
        print(f"\n🚨 Detectando anomalías multivariables en: {alias.get(var1)} + {alias.get(var2)}")
        X = reshape_multivariable_by_day(df, [var1, var2])
        if X.empty:
            print("⚠️  No hay datos suficientes.")
            continue

        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        labels = kmeans.fit_predict(X)
        _, distances = pairwise_distances_argmin_min(X, kmeans.cluster_centers_)
        anomaly_indices = np.where(distances > threshold)[0]
        anomalous_days = X.index[anomaly_indices]
        print(f"🔍 Se encontraron {len(anomalous_days)} días atípicos")

        # Visualización
        plt.figure(figsize=(10, 5))
        for idx in anomaly_indices:
            row = X.iloc[idx]
            values = row.values.reshape(len([var1, var2]), -1)  # [var][hour]
            for v_i, serie in enumerate(values):
                plt.plot(range(24), serie, alpha=0.5, label=f"{alias.get([var1, var2][v_i])} - {row.name}")
        plt.title(f"Perfiles atípicos - {alias.get(var1)} + {alias.get(var2)}")
        plt.xlabel("Hora")
        plt.ylabel("Valor")
        plt.legend(fontsize='x-small', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.grid(True)
        plt.show()
        plt.close()

from sklearn.decomposition import PCA
import seaborn as sns

def plot_pca_multivariable(df, var1, var2, n_components=2):
    print(f"\n🧬 PCA multivariable: {alias.get(var1)} + {alias.get(var2)}")

    X = reshape_multivariable_by_day(df, [var1, var2])
    if X.empty:
        print("⚠️  No hay datos suficientes para PCA.")
        return

    pca = PCA(n_components=n_components)
    components = pca.fit_transform(X)

    explained = pca.explained_variance_ratio_
    print(f"Varianza explicada: {explained}")

    # Crear un DataFrame con componentes principales
    pca_df = pd.DataFrame(components, columns=[f"PC{i+1}" for i in range(n_components)], index=X.index)

    # Visualización
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=pca_df, x="PC1", y="PC2")
    plt.title(f"PCA - {alias.get(var1)} + {alias.get(var2)}")
    plt.xlabel(f"PC1 ({explained[0]*100:.1f}% varianza)")
    plt.ylabel(f"PC2 ({explained[1]*100:.1f}% varianza)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()


#=======Aplicación Principal======
if __name__ == "__main__":
    df = prepare_data()

    variables = [
        lb_V005_vent01_CO2,
        lb_V022_vent02_CO2,
        lb_V006_vent01_temp_out,
        lb_V023_vent02_temp_out,
    ]

    # === Análisis univariable ===
    run_clustering_all_variables(df, variables)

    for var in variables:
        detect_anomalies(df, variable=var, n_clusters=3, threshold=2.0)

    # === Análisis multivariable ===
    var_pairs = [
        (lb_V005_vent01_CO2, lb_V006_vent01_temp_out),   # Norte Este
        (lb_V022_vent02_CO2, lb_V023_vent02_temp_out),   # Sur Oeste
    ]

    run_multivariable_clustering(df, var_pairs)
    detect_multivariable_anomalies(df, var_pairs, threshold=2.5)

    # === Análisis multivariable con PCA ===
    for var1, var2 in var_pairs:
        plot_pca_multivariable(df, var1, var2)