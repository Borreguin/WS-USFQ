import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import seaborn as sns

# Configuración de constantes
lb_timestamp = "timestamp"
lb_V005_vent01_CO2 = "V005_vent01_CO2"
lb_V022_vent02_CO2 = "V022_vent02_CO2"
lb_V006_vent01_temp_out = "V006_vent01_temp_out"
lb_V023_vent02_temp_out = "V023_vent02_temp_out"

columns = [lb_timestamp, lb_V005_vent01_CO2, lb_V022_vent02_CO2,
           lb_V006_vent01_temp_out, lb_V023_vent02_temp_out]


def read_and_prepare_data():
    """Lee y prepara los datos para el análisis"""
    script_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_path, "data", "data.csv")

    df = pd.read_csv(file_path, sep=';', decimal='.')
    df[lb_timestamp] = pd.to_datetime(
        df[lb_timestamp], format='%d.%m.%Y %H:%M')
    df.set_index(lb_timestamp, inplace=True)

    # Verificación de valores nulos
    print("\nValores nulos por columna:")
    print(df.isnull().sum())

    # Imputación simple (podría mejorarse)
    df.fillna(df.mean(), inplace=True)

    return df


def multivariate_anomaly_detection(df):
    """Detección de anomalías multivariable"""
    # Selección de características
    features = df.columns

    # Normalización de datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])

    # Reducción de dimensionalidad para visualización
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Modelo de detección de anomalías
    model = IsolationForest(contamination=0.05, random_state=42)
    anomalies = model.fit_predict(X_scaled)

    # Crear DataFrame con resultados
    results = df.copy()
    results['anomaly'] = anomalies
    results['anomaly'] = results['anomaly'].map({1: 0, -1: 1})  # 1=anomalía

    # Visualización PCA
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1],
                    hue=results['anomaly'], palette={0: 'blue', 1: 'red'})
    plt.title('Detección de Anomalías - Visualización PCA')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.legend(title='Anomalía', labels=['Normal', 'Anomalía'])
    plt.show()

    return results


def plot_anomalies_timeseries(results):
    """Visualización temporal de las anomalías"""
    plt.figure(figsize=(15, 10))

    # Gráfico de CO2
    plt.subplot(2, 1, 1)
    plt.plot(results.index, results[lb_V005_vent01_CO2],
             label='Ventilación NE', alpha=0.6)
    plt.plot(results.index, results[lb_V022_vent02_CO2],
             label='Ventilación SW', alpha=0.6)
    anomalies_co2 = results[results['anomaly'] == 1]
    plt.scatter(anomalies_co2.index, anomalies_co2[lb_V005_vent01_CO2],
                color='red', label='Anomalías NE')
    plt.scatter(anomalies_co2.index, anomalies_co2[lb_V022_vent02_CO2],
                color='black', label='Anomalías SW')
    plt.title('Anomalías en Mediciones de CO2')
    plt.ylabel('CO2 (ppm)')
    plt.legend()

    # Gráfico de Temperatura
    plt.subplot(2, 1, 2)
    plt.plot(results.index,
             results[lb_V006_vent01_temp_out], label='Temp. NE', alpha=0.6)
    plt.plot(results.index,
             results[lb_V023_vent02_temp_out], label='Temp. SW', alpha=0.6)
    anomalies_temp = results[results['anomaly'] == 1]
    plt.scatter(anomalies_temp.index, anomalies_temp[lb_V006_vent01_temp_out],
                color='red', label='Anomalías NE')
    plt.scatter(anomalies_temp.index, anomalies_temp[lb_V023_vent02_temp_out],
                color='black', label='Anomalías SW')
    plt.title('Anomalías en Mediciones de Temperatura')
    plt.ylabel('Temperatura (°C)')
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Paso 1: Carga y preparación de datos
    df = read_and_prepare_data()

    # Paso 2: Análisis multivariable de anomalías
    results = multivariate_anomaly_detection(df)

    # Paso 3: Visualización de resultados
    plot_anomalies_timeseries(results)

    # Resumen de anomalías encontradas
    print("\nResumen de anomalías detectadas:")
    print(f"Total de puntos analizados: {len(results)}")
    print(
        f"Anomalías detectadas: {results['anomaly'].sum()} ({results['anomaly'].mean()*100:.2f}%)")

    # Exportar resultados
    results.to_csv('resultados_anomalias.csv', sep=';')
