"""Configuracao padrao de estilo dos graficos, e mapa interativo do projeto."""

import matplotlib.pyplot as plt
import seaborn as sns
import folium


def configurar_estilo():
    sns.set_theme(style='whitegrid', palette='muted')
    plt.rcParams['figure.figsize'] = (10, 5)


def salvar_figura(fig, nome: str, pasta='reports/figures'):
    fig.tight_layout()
    fig.savefig(f'{pasta}/{nome}', dpi=150)


def gerar_mapa_pm25(geometrias, snapshot, caminho_saida: str):
    """Mapa coropletico de PM2.5 por pais em 2021, usando as fronteiras de `countries.geo.json`."""
    mapa = folium.Map(location=[10, 0], zoom_start=2, tiles='OpenStreetMap')
    folium.Choropleth(
        geo_data=geometrias.__geo_interface__,
        data=snapshot,
        columns=['pais_iso3', 'pm25'],
        key_on='feature.id',
        fill_color='YlOrRd',
        fill_opacity=0.8,
        line_opacity=0.3,
        legend_name='PM2.5 medio anual (ug/m3), 2021',
        nan_fill_color='lightgray',
    ).add_to(mapa)
    mapa.save(caminho_saida)
