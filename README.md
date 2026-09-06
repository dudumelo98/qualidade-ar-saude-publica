# Monitor de Qualidade do Ar e Saúde Pública

Correlação entre poluição do ar (PM2.5) e mortalidade, tendência histórica por país e mapa interativo, com dados reais da OMS (WHO Global Health Observatory).

## Objetivo

Entender a relação entre poluição do ar e mortalidade por país, identificar quem está melhorando ou piorando ao longo do tempo, e visualizar isso num mapa.

## Dado real, não simulado

Diferente da maioria dos outros projetos deste portfólio, este usa dado público real da OMS, sem simulação. Detalhes em [data/README.md](data/README.md).

## Resultados

- **Correlação PM2.5 x mortalidade**: R2 de 0,55, estatisticamente significativo (p < 0,001).
- **Tendência 2010-2023**: China tem a maior melhora de PM2.5 do período (-2,8 μg/m³/ano). Nigéria e outros países da África Ocidental estão entre os que mais pioraram.
- **Segmentação (K-Means)**: 3 perfis de país por nível de PM2.5 e tendência.
- **Mapa interativo**: coroplético de PM2.5 por país em 2021.

## Estrutura

```
data/            dados reais da OMS (raw, processed, external)
notebooks/       EDA, correlacao, tendencia e segmentacao, mapa
src/             carga de dados, features, modelos
reports/         relatorio final e graficos
tests/           testes automatizados
```

## Como rodar

```bash
pip install -r requirements.txt
jupyter notebook notebooks/
pytest tests/
```

## Metodologia

Regressão linear simples pra correlacionar PM2.5 e mortalidade. Regressão linear por país pra medir tendência de PM2.5 ao longo de 2010-2023. K-Means pra segmentar países por perfil. Folium pra gerar o mapa coroplético.

Detalhes completos em [reports/relatorio_final.md](reports/relatorio_final.md).
