# Dados

Este projeto usa dado real, não simulado.

## Fontes

- **WHO Global Health Observatory** (`ghoapi.azureedge.net`, API pública, sem chave):
  - `SDGPM25`: concentração média anual de PM2.5 por país, 2010 a 2023 (227 países).
  - `AIR_42`: taxa de mortalidade atribuída à poluição do ar ambiente, por 100 mil habitantes, padronizada por idade, ano 2021 (192 países).
- **countries.geo.json**: fronteiras de países em GeoJSON (domínio público, [johan/world.geo.json](https://github.com/johan/world.geo.json)), usado para o mapa coroplético.

## Por que não o NASA Earthdata (MERRA-2)

O escopo original citava dado de satélite da NASA (MERRA-2) para qualidade do ar, mas o Earthdata exige login institucional para download, que não é possível neste ambiente. Usei o indicador de PM2.5 da própria WHO GHO, que é público e não exige credencial.

## Arquivos

- `data/raw/who_sdgpm25.json`: resposta bruta da API para PM2.5.
- `data/raw/who_air_42_death_rate.json`: resposta bruta da API para mortalidade por poluição.
- `data/external/countries.geo.json`: geometrias dos países.

## Geração

Os dados já estão salvos em `data/raw/`. Para baixar novamente:

```bash
curl "https://ghoapi.azureedge.net/api/SDGPM25" -o data/raw/who_sdgpm25.json
curl "https://ghoapi.azureedge.net/api/AIR_42" -o data/raw/who_air_42_death_rate.json
```
