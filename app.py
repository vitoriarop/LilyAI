
import streamlit as st
import pandas as pd
import joblib
import json
from pathlib import Path

# 1. Configuracao da pagina
st.set_page_config(
    page_title="LilyAI | Identificador de Lirios",
    page_icon="🌸",
    layout="wide"
)

BASE = Path(__file__).resolve().parent

# 2. Carregar o modelo treinado
@st.cache_resource
def carregar_modelo():
    return joblib.load(
        BASE / "models" / "model.joblib"
    )

try:
    modelo = carregar_modelo()

    with open(
        BASE / "reports" / "metricas.json",
        encoding="utf-8"
    ) as arquivo:
        metricas = json.load(arquivo)

except Exception as erro:
    st.error(f"Erro ao carregar os arquivos: {erro}")
    st.info("Execute python train.py antes de iniciar.")
    st.stop()

nome_modelo = metricas["modelo_escolhido"]
resultado_modelo = metricas["resultados"][nome_modelo]

# 3. Informacoes das especies
especies = {
    "Lilium henryi": (
        "Espécie caracterizada por flores geralmente "
        "alaranjadas e tépalas fortemente recurvadas."
    ),

    "Lilium regale": (
        "Conhecida como lírio-real, apresenta flores "
        "claras e formato semelhante a uma trombeta."
    ),

    "Lilium leucanthum": (
        "Espécie com flores claras e tubo floral "
        "geralmente alongado."
    )
}

# 4. Barra lateral
with st.sidebar:
    st.title("🌿 LilyAI")

    st.write(
        "Sistema de classificação de lírios "
        "utilizando Machine Learning."
    )

    st.divider()

    st.subheader("Sobre o projeto")

    st.write("**Tipo:** Classificação supervisionada")
    st.write("**Algoritmos:** KNN e Random Forest")
    st.write("**Base:** 87 amostras reais")
    st.write("**Treinamento:** 69 amostras")
    st.write("**Teste:** 18 amostras")

    st.divider()

    st.markdown(
        "[Fonte científica dos dados]"
        "(https://doi.org/10.5061/dryad.5qfttdz6c)"
    )

    st.caption(
        "Projeto acadêmico de Machine Learning."
    )

# 5. Cabecalho principal
st.title("🌸 LilyAI")

st.subheader(
    "Classificação Inteligente de Espécies de Lírios"
)

st.write(
    "Identifique espécies de lírios a partir "
    "de suas características morfológicas."
)

# 6. Indicadores do modelo
col1, col2, col3, col4 = st.columns(4)

col1.metric("Modelo", nome_modelo)

col2.metric(
    "Acurácia",
    f"{resultado_modelo['acuracia']:.2%}"
)

col3.metric(
    "F1-score",
    f"{resultado_modelo['f1_score']:.2%}"
)

col4.metric("Espécies", len(modelo.classes_))

st.divider()

# 7. Criar abas
aba1, aba2, aba3 = st.tabs([
    "🌸 Identificar lírio",
    "📊 Análise dos dados",
    "🤖 Desempenho dos modelos"
])

# 8. Interface de previsao
with aba1:

    st.subheader("Características da flor")

    st.write(
        "Informe as duas medidas abaixo para "
        "realizar uma classificação."
    )

    with st.form("formulario_lirio"):

        c1, c2 = st.columns(2)

        with c1:
            comprimento = st.number_input(
                "Comprimento do tubo floral (mm)",
                min_value=0.0,
                value=8.0,
                step=0.1,
                format="%.2f"
            )

        with c2:
            curvatura = st.number_input(
                "Curvatura da tépala",
                min_value=0.0,
                value=4.35,
                step=0.01,
                format="%.4f",
                help="Razão adimensional de curvatura."
            )

        prever = st.form_submit_button(
            "🔍 Identificar espécie",
            type="primary"
        )

    if prever:

        if comprimento <= 0 or curvatura < 1:
            st.error(
                "Informe comprimento maior que zero "
                "e curvatura igual ou superior a 1."
            )

        else:

            if not (
                5.9 <= comprimento <= 139
                and 1.084211 <= curvatura <= 5.22
            ):
                st.warning(
                    "As medidas estão fora dos intervalos "
                    "observados na base científica. "
                    "A previsão pode ser pouco confiável."
                )

            # Organizar os dados de entrada
            entrada = pd.DataFrame([{
                "comprimento_tubo": comprimento,
                "curvatura_tepala": curvatura
            }])

            # Realizar previsao com o modelo treinado
            previsao = modelo.predict(entrada)[0]

            st.success(
                f"Espécie prevista: {previsao}"
            )

            st.write(
                especies.get(previsao, "")
            )

            # Mostrar pontuacao por especie
            probabilidades = modelo.predict_proba(
                entrada
            )[0]

            st.subheader(
                "Pontuação atribuída a cada espécie"
            )

            for especie, prob in zip(
                modelo.classes_,
                probabilidades
            ):
                st.write(f"**{especie}: {prob:.1%}**")
                st.progress(float(prob))

            st.caption(
                "As pontuações do modelo não representam "
                "certeza científica da identificação."
            )

    st.info(
        "O sistema identifica somente as três espécies "
        "presentes na base de treinamento."
    )

# 9. Aba de analise exploratoria
with aba2:

    st.subheader("Conhecendo a base de dados")

    st.write(
        "A base selecionada possui 87 amostras "
        "distribuídas entre três espécies de lírios."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.image(
            str(BASE / "reports" / "graficos"
                / "quantidade_especies.png"),
            caption="Distribuição das amostras"
        )

    with c2:
        st.image(
            str(BASE / "reports" / "graficos"
                / "dispersao_especies.png"),
            caption="Características morfológicas"
        )

    st.subheader("Principais conclusões")

    st.markdown("""
    - As três espécies possuem quantidades semelhantes
      de amostras.
    - Lilium henryi apresenta tubo floral menor e
      maior curvatura da tépala.
    - Lilium regale e Lilium leucanthum apresentam
      características semelhantes, dificultando
      algumas classificações.
    """)

# 10. Aba de desempenho
with aba3:

    st.subheader("Comparação dos algoritmos")

    tabela = []

    for nome, valores in metricas["resultados"].items():

        tabela.append({
            "Algoritmo": nome,
            "Acurácia": f"{valores['acuracia']:.2%}",
            "Precisão": f"{valores['precisao']:.2%}",
            "Recall": f"{valores['recall']:.2%}",
            "F1-score": f"{valores['f1_score']:.2%}",
            "F1 validação cruzada":
                f"{valores['f1_validacao_cruzada']:.2%}"
        })

    st.dataframe(
        pd.DataFrame(tabela),
        hide_index=True
    )

    st.success(f"Modelo selecionado: {nome_modelo}")

    st.write(
        "Critério de seleção: maior F1-score macro "
        "na validação cruzada do conjunto de treinamento."
    )

    st.subheader("Matrizes de confusão")

    c1, c2 = st.columns(2)

    with c1:
        st.image(
            str(BASE / "reports" / "graficos"
                / "matriz_knn.png"),
            caption="KNN"
        )

    with c2:
        st.image(
            str(BASE / "reports" / "graficos"
                / "matriz_random_forest.png"),
            caption="Random Forest"
        )

    st.subheader("Limitações do projeto")

    st.markdown("""
    - Quantidade reduzida de amostras.
    - Apenas três espécies disponíveis.
    - Uso de somente duas características físicas.
    - Ausência de validação com populações externas.
    """)

# 11. Rodape
st.divider()

st.caption(
    "🌿 LilyAI — Protótipo educacional de Machine Learning. "
    "Não substitui a identificação botânica especializada."
)
