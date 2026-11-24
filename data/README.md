
# Base de dados — LilyAI

## Fonte científica

- Dataset: Data from: Papilio butterfly vs. hawkmoth
  pollination explains floral syndrome dichotomy
  in a clade of Lilium.
- Autor: Chang-Qiu Liu
- Instituição: Guangxi Institute of Botany
- Repositório: Dryad
- Publicação: 02/11/2021
- Acesso: 24/11/2026
- Licença: CC0 1.0, conforme política do Dryad
- DOI: https://doi.org/10.5061/dryad.5qfttdz6c

## Arquivos

| Arquivo | Descrição |
|---|---|
| Floral_traits.xlsx | Planilha científica original |
| readme.xlsx | Documentação científica das variáveis |
| lilios.csv | Base organizada para Machine Learning |

## Obtenção dos dados

Acesse:

https://doi.org/10.5061/dryad.5qfttdz6c

Baixe os arquivos Floral_traits.xlsx e readme.xlsx
e coloque-os nesta pasta, caso não estejam presentes.

Para gerar a base organizada, execute na pasta
principal do projeto:

```bash
python analise.py
```

## Tratamento realizado

Foi selecionada a aba Morphology da planilha original.

Foram extraídas 87 amostras das espécies:

- Lilium henryi: 30 amostras.
- Lilium regale: 27 amostras.
- Lilium leucanthum: 30 amostras.

## Dicionário de dados

| Coluna | Significado | Unidade |
|---|---|---|
| comprimento_tubo | Comprimento do tubo floral | mm |
| curvatura_tepala | Razão de curvatura da tépala | Adimensional |
| especie | Espécie do lírio | Categoria |

## Atribuição

Os dados originais são de autoria dos pesquisadores
responsáveis pelo estudo científico citado.

O projeto LilyAI realizou somente a seleção,
organização e utilização desses dados para fins
educacionais de Machine Learning.
