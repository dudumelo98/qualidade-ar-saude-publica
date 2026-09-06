"""
Carga dos dados reais de qualidade do ar e saude publica.

Ao contrario dos outros projetos do portfolio, este usa dado real, nao
simulado. A API do WHO Global Health Observatory (ghoapi.azureedge.net) e
publica e nao exige chave. Baixei dois indicadores:

- SDGPM25: concentracao media de PM2.5 por pais, 2010 a 2023.
- AIR_42: taxa de mortalidade atribuida a poluicao do ar ambiente (por
  100 mil habitantes, padronizada por idade), ano 2021.

O NASA Earthdata (MERRA-2) citado no escopo original exige login
institucional e nao da pra baixar sem credencial, por isso o indicador de
saude publica usa dado da WHO em vez do dado de satelite da NASA.
"""

import json
import logging
import pandas as pd
import geopandas as gpd
from pathlib import Path

RAW_PATH = Path(__file__).parents[2] / 'data' / 'raw'
EXTERNAL_PATH = Path(__file__).parents[2] / 'data' / 'external'
PROCESSED_PATH = Path(__file__).parents[2] / 'data' / 'processed'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def carregar_pm25() -> pd.DataFrame:
    with open(RAW_PATH / 'who_sdgpm25.json', encoding='utf-8') as f:
        data = json.load(f)['value']
    df = pd.DataFrame(data)
    df = df[(df['SpatialDimType'] == 'COUNTRY') & (df['Dim1'] == 'RESIDENCEAREATYPE_TOTL')]
    df = df[['SpatialDim', 'TimeDim', 'NumericValue']].rename(
        columns={'SpatialDim': 'pais_iso3', 'TimeDim': 'ano', 'NumericValue': 'pm25'}
    )
    return df.reset_index(drop=True)


def carregar_mortalidade_poluicao() -> pd.DataFrame:
    with open(RAW_PATH / 'who_air_42_death_rate.json', encoding='utf-8') as f:
        data = json.load(f)['value']
    df = pd.DataFrame(data)
    df = df[(df['Dim1'] == 'SEX_BTSX') & (df['Dim2'] == 'GHECAUSE_GHE000000')]
    df = df[['SpatialDim', 'TimeDim', 'NumericValue']].rename(
        columns={'SpatialDim': 'pais_iso3', 'TimeDim': 'ano', 'NumericValue': 'taxa_mortalidade_poluicao'}
    )
    return df.reset_index(drop=True)


def limpar_pm25(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)
    df = df.dropna(subset=['pais_iso3', 'pm25'])
    df = df[df['pm25'] > 0]
    df = df.drop_duplicates(subset=['pais_iso3', 'ano'])
    removidas = antes - len(df)
    logger.info(f'PM2.5: {removidas} linhas removidas na limpeza')
    return df.reset_index(drop=True)


def montar_snapshot_2021() -> pd.DataFrame:
    """Junta PM2.5 e mortalidade no ano de 2021, o unico ano com os dois indicadores disponiveis por pais."""
    pm25 = limpar_pm25(carregar_pm25())
    mortalidade = carregar_mortalidade_poluicao()

    pm25_2021 = pm25[pm25['ano'] == 2021]
    snapshot = pm25_2021.merge(mortalidade[['pais_iso3', 'taxa_mortalidade_poluicao']], on='pais_iso3', how='inner')
    return snapshot.reset_index(drop=True)


def carregar_geometrias_paises() -> gpd.GeoDataFrame:
    return gpd.read_file(EXTERNAL_PATH / 'countries.geo.json')


def pipeline_completo() -> tuple:
    pm25 = limpar_pm25(carregar_pm25())
    snapshot_2021 = montar_snapshot_2021()
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
    pm25.to_parquet(PROCESSED_PATH / 'pm25_serie.parquet', index=False)
    snapshot_2021.to_parquet(PROCESSED_PATH / 'snapshot_2021.parquet', index=False)
    return pm25, snapshot_2021
