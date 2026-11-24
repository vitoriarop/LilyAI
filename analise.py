
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 1. Criar caminhos do projeto
BASE = Path(__file__).resolve().parent
PASTA_DATA = BASE / "data"
PASTA_GRAFICOS = BASE / "reports" / "graficos"

PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# 2. Ler a planilha original
planilha = pd.read_excel(
    PASTA_DATA / "Floral_traits.xlsx",
    sheet_name="Morphology",
    header=None
)

# 3. Selecionar as especies e suas colunas
especies = {
    "Lilium henryi": (0, 1),
    "Lilium regale": (4, 5),
    "Lilium leucanthum": (6, 7)
}

dados = []

# 4. Organizar os dados em formato de tabela
for especie, colunas in especies.items():

    grupo = planilha.iloc[3:, list(colunas)].copy()

    grupo.columns = [
        "comprimento_tubo",
        "curvatura_tepala"
    ]

    grupo = grupo.apply(pd.to_numeric, errors="coerce")

    grupo = grupo.dropna(how="all")

    grupo["especie"] = especie

    dados.append(grupo)

df = pd.concat(dados, ignore_index=True)

# 5. Exibir informacoes da base
print("\n===== PROJETO LILYAI =====")

print("\nPrimeiros registros:")
print(df.head())

print("\nDimensoes da base:")
print(df.shape)

print("\nQuantidade por especie:")
print(df["especie"].value_counts())

print("\nValores ausentes:")
print(df.isnull().sum())

print("\nRegistros duplicados:")
print(df.duplicated().sum())

print("\nEstatisticas descritivas:")
print(df.describe())

print("\nMedia das caracteristicas por especie:")
print(df.groupby("especie").mean(numeric_only=True))

# 6. Salvar a base organizada
df.to_csv(
    PASTA_DATA / "lilios.csv",
    index=False
)

# 7. Configurar os graficos
sns.set_theme(style="whitegrid")

cores = {
    "Lilium henryi": "#E89B50",
    "Lilium regale": "#629B78",
    "Lilium leucanthum": "#9A82C4"
}

# 8. Grafico de quantidade por especie
plt.figure(figsize=(9, 5))

sns.countplot(
    data=df,
    x="especie",
    hue="especie",
    palette=cores,
    legend=False
)

plt.title("Quantidade de amostras por espécie")
plt.xlabel("Espécie")
plt.ylabel("Quantidade")
plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "quantidade_especies.png",
    dpi=200
)

plt.close()

# 9. Grafico de dispersao
plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=df,
    x="comprimento_tubo",
    y="curvatura_tepala",
    hue="especie",
    palette=cores,
    s=80
)

plt.title("Características morfológicas dos lírios")
plt.xlabel("Comprimento do tubo floral (mm)")
plt.ylabel("Curvatura da tépala")
plt.legend(title="Espécie")
plt.tight_layout()

plt.savefig(
    PASTA_GRAFICOS / "dispersao_especies.png",
    dpi=200
)

plt.close()

print("\n===== ANALISE CONCLUIDA =====")
print("Base organizada: data/lilios.csv")
print("Graficos salvos em: reports/graficos/")
