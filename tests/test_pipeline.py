"""Testes de sanidade do pipeline de qualidade do ar."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))

import pandas as pd

from src.data.load_data import limpar_pm25
from src.features.engenharia_features import calcular_tendencia_pm25


def test_limpar_pm25_remove_invalidas():
    df = pd.DataFrame({
        'pais_iso3': ['BRA', 'BRA', 'ARG'],
        'ano': [2020, 2020, 2021],
        'pm25': [12.0, 12.0, -1.0],
    })
    resultado = limpar_pm25(df)
    assert list(resultado['pais_iso3']) == ['BRA']


def test_tendencia_pm25_ignora_pais_com_poucos_anos():
    df = pd.DataFrame({
        'pais_iso3': ['BRA'] * 10 + ['ARG'] * 3,
        'ano': list(range(2010, 2020)) + list(range(2010, 2013)),
        'pm25': [10 - 0.1 * i for i in range(10)] + [15, 14, 13],
    })
    tendencia = calcular_tendencia_pm25(df, ano_minimo_pontos=8)
    assert list(tendencia['pais_iso3']) == ['BRA']
    assert tendencia.iloc[0]['tendencia_pm25_ano'] < 0
