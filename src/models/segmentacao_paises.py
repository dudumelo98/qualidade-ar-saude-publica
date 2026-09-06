"""Segmentacao de paises por perfil de qualidade do ar e mortalidade."""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

COLUNAS_CLUSTER = ['pm25', 'taxa_mortalidade_poluicao', 'tendencia_pm25_ano']


def preparar_dados_cluster(df: pd.DataFrame) -> tuple:
    X = df[COLUNAS_CLUSTER]
    scaler = StandardScaler()
    return scaler.fit_transform(X), scaler


def escolher_k(X_escalado, k_min: int = 2, k_max: int = 6, seed: int = 42) -> pd.DataFrame:
    resultados = []
    for k in range(k_min, k_max + 1):
        modelo = KMeans(n_clusters=k, random_state=seed, n_init=10)
        labels = modelo.fit_predict(X_escalado)
        resultados.append({'k': k, 'silhouette': silhouette_score(X_escalado, labels)})
    return pd.DataFrame(resultados)


def treinar_kmeans(X_escalado, k: int, seed: int = 42) -> KMeans:
    modelo = KMeans(n_clusters=k, random_state=seed, n_init=10)
    modelo.fit(X_escalado)
    return modelo
