
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import json

from pathlib import Path
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay
)

# 1. Configurar caminhos
BASE = Path(__file__).resolve().parent

PASTA_MODELOS = BASE / "models"
PASTA_REPORTS = BASE / "reports"
PASTA_GRAFICOS = PASTA_REPORTS / "graficos"

PASTA_MODELOS.mkdir(exist_ok=True)
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# 2. Carregar a base organizada
df = pd.read_csv(BASE / "data" / "lilios.csv")

# 3. Separar atributos e variavel-alvo
X = df[["comprimento_tubo", "curvatura_tepala"]]
y = df["especie"]

# 4. Dividir a base em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\n===== TREINAMENTO LILYAI =====")
print("Amostras de treinamento:", len(X_train))
print("Amostras de teste:", len(X_test))

# 5. Definir os dois algoritmos
modelos = {
    "KNN": Pipeline([
        ("imputacao", SimpleImputer(strategy="median")),
        ("normalizacao", StandardScaler()),
        ("modelo", KNeighborsClassifier(n_neighbors=5))
    ]),

    "Random Forest": Pipeline([
        ("imputacao", SimpleImputer(strategy="median")),
        ("modelo", RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ))
    ])
}

# 6. Configurar validacao cruzada
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

resultados = {}

# 7. Treinar e avaliar os modelos
for nome, modelo in modelos.items():

    print(f"\n===== MODELO: {nome} =====")

    scores = cross_val_score(
        modelo,
        X_train,
        y_train,
        cv=cv,
        scoring="f1_macro"
    )

    modelo.fit(X_train, y_train)

    previsoes = modelo.predict(X_test)

    acuracia = accuracy_score(y_test, previsoes)

    precisao = precision_score(
        y_test, previsoes,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        y_test, previsoes,
        average="macro",
        zero_division=0
    )

    f1 = f1_score(
        y_test, previsoes,
        average="macro",
        zero_division=0
    )

    resultados[nome] = {
        "acuracia": float(acuracia),
        "precisao": float(precisao),
        "recall": float(recall),
        "f1_score": float(f1),
        "f1_validacao_cruzada": float(scores.mean()),
        "metricas_por_classe": classification_report(
            y_test,
            previsoes,
            output_dict=True,
            zero_division=0
        )
    }

    print(f"Acuracia: {acuracia:.4f}")
    print(f"Precisao: {precisao:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    print(f"F1 validacao cruzada: {scores.mean():.4f}")

    print("\nRelatorio de classificacao:")
    print(classification_report(
        y_test,
        previsoes,
        zero_division=0
    ))

    # 8. Gerar matriz de confusao
    fig, ax = plt.subplots(figsize=(9, 6))

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        previsoes,
        cmap="Blues",
        xticks_rotation=30,
        colorbar=False,
        ax=ax
    )

    ax.set_title(f"Matriz de Confusao - {nome}")
    ax.set_xlabel("Especie prevista")
    ax.set_ylabel("Especie real")

    plt.tight_layout()

    nome_arquivo = nome.lower().replace(" ", "_")

    plt.savefig(
        PASTA_GRAFICOS / f"matriz_{nome_arquivo}.png",
        dpi=200
    )

    plt.close()

# 9. Escolher o melhor modelo pela validacao
melhor_nome = max(
    resultados,
    key=lambda nome: resultados[nome]["f1_validacao_cruzada"]
)

melhor_modelo = modelos[melhor_nome]

# 10. Salvar o modelo treinado
joblib.dump(
    melhor_modelo,
    PASTA_MODELOS / "model.joblib"
)

# 11. Salvar as metricas
relatorio = {
    "modelo_escolhido": melhor_nome,
    "criterio_selecao": "Maior F1 macro na validacao cruzada",
    "amostras_treino": len(X_train),
    "amostras_teste": len(X_test),
    "resultados": resultados
}

with open(
    PASTA_REPORTS / "metricas.json",
    "w",
    encoding="utf-8"
) as arquivo:
    json.dump(
        relatorio,
        arquivo,
        indent=4,
        ensure_ascii=False
    )

# 12. Apresentar o resultado final
print("\n===== RESULTADO FINAL =====")
print("Melhor modelo:", melhor_nome)
print(f"Acuracia no teste: {resultados[melhor_nome]['acuracia']:.2%}")

print("\nModelo salvo em: models/model.joblib")
print("Metricas salvas em: reports/metricas.json")
print("Matrizes salvas em: reports/graficos/")

print("\n===== TREINAMENTO CONCLUIDO =====")
