"""Regressao entre PM2.5 e mortalidade atribuida a poluicao do ar."""

import pandas as pd
from scipy import stats


def correlacionar_pm25_mortalidade(snapshot: pd.DataFrame) -> dict:
    resultado = stats.linregress(snapshot['pm25'], snapshot['taxa_mortalidade_poluicao'])
    return {
        'coeficiente_angular': resultado.slope,
        'intercepto': resultado.intercept,
        'r_quadrado': resultado.rvalue ** 2,
        'p_valor': resultado.pvalue,
    }
