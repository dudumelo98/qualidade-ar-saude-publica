"""Calculo da tendencia de PM2.5 por pais ao longo da serie 2010-2023."""

import numpy as np
import pandas as pd


def calcular_tendencia_pm25(df_pm25: pd.DataFrame, ano_minimo_pontos: int = 8) -> pd.DataFrame:
    """
    Ajusta uma regressao linear simples (pm25 ~ ano) por pais, e guarda a
    inclinacao. Pais com inclinacao negativa esta melhorando a qualidade do
    ar ao longo do tempo, positiva esta piorando. Exijo pelo menos 8 anos
    de dado pra nao confiar na tendencia de paises com serie curta.
    """
    linhas = []
    for pais, grupo in df_pm25.groupby('pais_iso3'):
        if len(grupo) < ano_minimo_pontos:
            continue
        coef = np.polyfit(grupo['ano'], grupo['pm25'], 1)
        linhas.append({
            'pais_iso3': pais,
            'tendencia_pm25_ano': coef[0],
            'pm25_medio': grupo['pm25'].mean(),
            'n_anos': len(grupo),
        })
    return pd.DataFrame(linhas)
