from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cobertura Vacinal no Brasil",
    page_icon="💉",
    layout="wide",
)


# ---------------------------------------------------------
# Utilidades
# ---------------------------------------------------------
def format_int_br(valor: float | int) -> str:
    return f"{valor:,.0f}".replace(",", ".")


def format_pct(valor: float) -> str:
    return f"{valor:.2f}%"


@st.cache_data
def carregar_dados(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho)

    # Conversão e padronização
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    colunas_numericas = [
        "ano",
        "mes",
        "doses_aplicadas",
        "cobertura_percentual",
        "meta_percentual",
        "populacao_alvo",
        "campanhas",
    ]

    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    colunas_texto = [
        "regiao",
        "uf",
        "municipio",
        "vacina",
        "publico_alvo",
        "nivel_alerta",
    ]

    for coluna in colunas_texto:
        df[coluna] = df[coluna].astype("string").str.strip()

    # Limpeza básica
    df = df.drop_duplicates().copy()

    # Remove apenas registros que inviabilizam a análise
    df = df.dropna(
        subset=[
            "data",
            "regiao",
            "uf",
            "municipio",
            "vacina",
            "cobertura_percentual",
            "meta_percentual",
            "doses_aplicadas",
            "populacao_alvo",
            "nivel_alerta",
        ]
    )

    # Validações de domínio
    df = df[
        df["cobertura_percentual"].between(0, 100)
        & df["meta_percentual"].between(0, 100)
        & (df["doses_aplicadas"] >= 0)
        & (df["populacao_alvo"] > 0)
        & (df["campanhas"] >= 0)
    ].copy()

    # Engenharia de atributos
    df["gap_meta"] = (
        df["cobertura_percentual"] - df["meta_percentual"]
    )

    df["atingiu_meta"] = (
        df["cobertura_percentual"] >= df["meta_percentual"]
    )

    df["ano_mes_data"] = df["data"].dt.to_period("M").dt.to_timestamp()

    df["faixa_cobertura"] = pd.cut(
        df["cobertura_percentual"],
        bins=[0, 70, 80, 90, 100],
        labels=[
            "Abaixo de 70%",
            "70% a 79,9%",
            "80% a 89,9%",
            "90% a 100%",
        ],
        include_lowest=True,
    )

    return df


# ---------------------------------------------------------
# Leitura da base
# ---------------------------------------------------------
CAMINHO_DADOS = Path("dados/simulacao_cobertura_vacinal_brasil.csv")

if not CAMINHO_DADOS.exists():
    st.error(
        "Arquivo de dados não encontrado. "
        "Confirme se existe o arquivo "
        "`dados/simulacao_cobertura_vacinal_brasil.csv` no repositório."
    )
    st.stop()

df = carregar_dados(str(CAMINHO_DADOS))


# ---------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------
st.title("💉 Cobertura Vacinal no Brasil")
st.caption(
    "Projeto G1 — Análise e Visualização de Dados com Python"
)

st.info(
    "A base utilizada neste projeto é uma simulação. "
    "Os resultados apresentados descrevem apenas os dados fornecidos "
    "para a atividade e não representam estatísticas oficiais de saúde pública."
)

st.markdown(
    """
### Problema analisado
Este dashboard permite explorar a evolução da cobertura vacinal,
comparar regiões, vacinas e públicos-alvo, acompanhar o cumprimento
das metas e identificar registros classificados como Adequado,
Atenção ou Crítico.
"""
)


# ---------------------------------------------------------
# Filtros
# ---------------------------------------------------------
st.sidebar.header("Filtros")

anos_disponiveis = sorted(df["ano"].dropna().astype(int).unique().tolist())

ano_inicial, ano_final = st.sidebar.select_slider(
    "Período",
    options=anos_disponiveis,
    value=(min(anos_disponiveis), max(anos_disponiveis)),
)

regioes = st.sidebar.multiselect(
    "Região",
    options=sorted(df["regiao"].dropna().unique().tolist()),
)

df_base_uf = df[
    df["ano"].between(ano_inicial, ano_final)
].copy()

if regioes:
    df_base_uf = df_base_uf[df_base_uf["regiao"].isin(regioes)]

ufs = st.sidebar.multiselect(
    "UF",
    options=sorted(df_base_uf["uf"].dropna().unique().tolist()),
)

df_base_municipio = df_base_uf.copy()

if ufs:
    df_base_municipio = df_base_municipio[
        df_base_municipio["uf"].isin(ufs)
    ]

municipios = st.sidebar.multiselect(
    "Município",
    options=sorted(
        df_base_municipio["municipio"].dropna().unique().tolist()
    ),
)

vacinas = st.sidebar.multiselect(
    "Vacina",
    options=sorted(df["vacina"].dropna().unique().tolist()),
)

publicos = st.sidebar.multiselect(
    "Público-alvo",
    options=sorted(df["publico_alvo"].dropna().unique().tolist()),
)

alertas = st.sidebar.multiselect(
    "Nível de alerta",
    options=sorted(df["nivel_alerta"].dropna().unique().tolist()),
)

atingiu_meta_filtro = st.sidebar.selectbox(
    "Situação da meta",
    options=["Todos", "Atingiu a meta", "Não atingiu a meta"],
)


# ---------------------------------------------------------
# Aplicação dos filtros
# ---------------------------------------------------------
filtrado = df[
    df["ano"].between(ano_inicial, ano_final)
].copy()

if regioes:
    filtrado = filtrado[filtrado["regiao"].isin(regioes)]

if ufs:
    filtrado = filtrado[filtrado["uf"].isin(ufs)]

if municipios:
    filtrado = filtrado[filtrado["municipio"].isin(municipios)]

if vacinas:
    filtrado = filtrado[filtrado["vacina"].isin(vacinas)]

if publicos:
    filtrado = filtrado[filtrado["publico_alvo"].isin(publicos)]

if alertas:
    filtrado = filtrado[filtrado["nivel_alerta"].isin(alertas)]

if atingiu_meta_filtro == "Atingiu a meta":
    filtrado = filtrado[filtrado["atingiu_meta"]]

elif atingiu_meta_filtro == "Não atingiu a meta":
    filtrado = filtrado[~filtrado["atingiu_meta"]]

if filtrado.empty:
    st.warning("Nenhum registro corresponde aos filtros selecionados.")
    st.stop()


# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------
st.subheader("Indicadores principais")

cobertura_media = filtrado["cobertura_percentual"].mean()
meta_media = filtrado["meta_percentual"].mean()
atingiu_meta_pct = filtrado["atingiu_meta"].mean() * 100
gap_medio = filtrado["gap_meta"].mean()
doses_total = filtrado["doses_aplicadas"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Cobertura média",
    format_pct(cobertura_media),
)

col2.metric(
    "Meta média",
    format_pct(meta_media),
)

col3.metric(
    "Atingiram a meta",
    format_pct(atingiu_meta_pct),
)

col4.metric(
    "Gap médio",
    f"{gap_medio:+.2f} p.p.",
)

col5.metric(
    "Doses aplicadas",
    format_int_br(doses_total),
)

st.caption(
    f"{format_int_br(len(filtrado))} registros selecionados após os filtros."
)


# ---------------------------------------------------------
# Abas
# ---------------------------------------------------------
tab_visao, tab_tempo, tab_comparacoes, tab_dados = st.tabs(
    [
        "Visão geral",
        "Série temporal",
        "Comparações",
        "Dados",
    ]
)


# ---------------------------------------------------------
# Visão geral
# ---------------------------------------------------------
with tab_visao:
    c1, c2 = st.columns(2)

    with c1:
        media_regiao = (
            filtrado.groupby("regiao", as_index=False)
            .agg(
                cobertura_media=("cobertura_percentual", "mean"),
                meta_media=("meta_percentual", "mean"),
            )
            .sort_values("cobertura_media", ascending=False)
        )

        fig_regiao = px.bar(
            media_regiao,
            x="cobertura_media",
            y="regiao",
            orientation="h",
            title="Cobertura média por região",
            labels={
                "cobertura_media": "Cobertura média (%)",
                "regiao": "Região",
            },
            text_auto=".2f",
        )

        fig_regiao.update_layout(
            yaxis={"categoryorder": "total ascending"},
            xaxis_range=[0, 100],
        )

        st.plotly_chart(fig_regiao, use_container_width=True)

    with c2:
        alertas_df = (
            filtrado["nivel_alerta"]
            .value_counts()
            .rename_axis("nivel_alerta")
            .reset_index(name="registros")
        )

        fig_alertas = px.pie(
            alertas_df,
            names="nivel_alerta",
            values="registros",
            hole=0.45,
            title="Distribuição por nível de alerta",
        )

        st.plotly_chart(fig_alertas, use_container_width=True)

    hist = px.histogram(
        filtrado,
        x="cobertura_percentual",
        nbins=25,
        title="Distribuição da cobertura percentual",
        labels={
            "cobertura_percentual": "Cobertura percentual (%)"
        },
    )

    st.plotly_chart(hist, use_container_width=True)


# ---------------------------------------------------------
# Série temporal
# ---------------------------------------------------------
with tab_tempo:
    serie = (
        filtrado.groupby("ano_mes_data", as_index=False)
        .agg(
            cobertura_media=("cobertura_percentual", "mean"),
            meta_media=("meta_percentual", "mean"),
        )
        .sort_values("ano_mes_data")
    )

    serie["media_movel_6m"] = (
        serie["cobertura_media"]
        .rolling(window=6, min_periods=1)
        .mean()
    )

    serie_long = serie.melt(
        id_vars="ano_mes_data",
        value_vars=[
            "cobertura_media",
            "meta_media",
            "media_movel_6m",
        ],
        var_name="indicador",
        value_name="percentual",
    )

    nomes = {
        "cobertura_media": "Cobertura média",
        "meta_media": "Meta média",
        "media_movel_6m": "Média móvel de 6 meses",
    }

    serie_long["indicador"] = serie_long["indicador"].map(nomes)

    fig_serie = px.line(
        serie_long,
        x="ano_mes_data",
        y="percentual",
        color="indicador",
        title="Evolução temporal da cobertura e da meta",
        labels={
            "ano_mes_data": "Data",
            "percentual": "Percentual",
            "indicador": "Indicador",
        },
    )

    fig_serie.update_yaxes(range=[0, 100])

    st.plotly_chart(fig_serie, use_container_width=True)

    media_ano = (
        filtrado.groupby("ano", as_index=False)
        .agg(
            cobertura_media=("cobertura_percentual", "mean"),
            meta_media=("meta_percentual", "mean"),
        )
    )

    fig_ano = px.bar(
        media_ano,
        x="ano",
        y=["cobertura_media", "meta_media"],
        barmode="group",
        title="Cobertura média x meta média por ano",
        labels={
            "value": "Percentual",
            "variable": "Indicador",
            "ano": "Ano",
        },
    )

    fig_ano.update_yaxes(range=[0, 100])

    st.plotly_chart(fig_ano, use_container_width=True)


# ---------------------------------------------------------
# Comparações
# ---------------------------------------------------------
with tab_comparacoes:
    comparacao_vacina = (
        filtrado.groupby("vacina", as_index=False)
        .agg(
            cobertura_media=("cobertura_percentual", "mean"),
            meta_media=("meta_percentual", "mean"),
            taxa_meta=("atingiu_meta", "mean"),
        )
        .sort_values("cobertura_media", ascending=False)
    )

    comparacao_vacina["taxa_meta"] *= 100

    comparacao_long = comparacao_vacina.melt(
        id_vars="vacina",
        value_vars=["cobertura_media", "meta_media"],
        var_name="indicador",
        value_name="percentual",
    )

    nomes_comp = {
        "cobertura_media": "Cobertura média",
        "meta_media": "Meta média",
    }

    comparacao_long["indicador"] = (
        comparacao_long["indicador"].map(nomes_comp)
    )

    fig_vacina = px.bar(
        comparacao_long,
        x="vacina",
        y="percentual",
        color="indicador",
        barmode="group",
        title="Cobertura média x meta média por vacina",
        labels={
            "vacina": "Vacina",
            "percentual": "Percentual",
            "indicador": "Indicador",
        },
    )

    fig_vacina.update_yaxes(range=[0, 100])

    st.plotly_chart(fig_vacina, use_container_width=True)

    correlacao_cols = [
        "cobertura_percentual",
        "meta_percentual",
        "doses_aplicadas",
        "populacao_alvo",
        "campanhas",
        "gap_meta",
    ]

    correlacao = filtrado[correlacao_cols].corr().round(2)

    fig_corr = px.imshow(
        correlacao,
        text_auto=True,
        aspect="auto",
        zmin=-1,
        zmax=1,
        color_continuous_scale="RdBu_r",
        title="Matriz de correlação",
    )

    st.plotly_chart(fig_corr, use_container_width=True)


# ---------------------------------------------------------
# Tabela
# ---------------------------------------------------------
with tab_dados:
    st.markdown("### Dados filtrados")

    colunas_tabela = [
        "data",
        "regiao",
        "uf",
        "municipio",
        "vacina",
        "publico_alvo",
        "doses_aplicadas",
        "populacao_alvo",
        "cobertura_percentual",
        "meta_percentual",
        "gap_meta",
        "nivel_alerta",
    ]

    tabela = filtrado[colunas_tabela].copy()

    tabela["data"] = tabela["data"].dt.strftime("%d/%m/%Y")
    tabela["cobertura_percentual"] = tabela[
        "cobertura_percentual"
    ].round(2)
    tabela["meta_percentual"] = tabela["meta_percentual"].round(2)
    tabela["gap_meta"] = tabela["gap_meta"].round(2)

    st.dataframe(
        tabela,
        use_container_width=True,
        hide_index=True,
    )

    csv_filtrado = tabela.to_csv(
        index=False,
        encoding="utf-8-sig",
    ).encode("utf-8-sig")

    st.download_button(
        "Baixar dados filtrados em CSV",
        data=csv_filtrado,
        file_name="cobertura_vacinal_filtrada.csv",
        mime="text/csv",
    )


# ---------------------------------------------------------
# Interpretação textual
# ---------------------------------------------------------
st.divider()
st.subheader("Interpretação do recorte selecionado")

melhor_regiao = (
    filtrado.groupby("regiao")["cobertura_percentual"]
    .mean()
    .idxmax()
)

pior_regiao = (
    filtrado.groupby("regiao")["cobertura_percentual"]
    .mean()
    .idxmin()
)

melhor_vacina = (
    filtrado.groupby("vacina")["cobertura_percentual"]
    .mean()
    .idxmax()
)

alerta_mais_frequente = (
    filtrado["nivel_alerta"]
    .value_counts()
    .idxmax()
)

st.markdown(
    f"""
- A cobertura média do recorte selecionado é **{format_pct(cobertura_media)}**.
- A meta média é **{format_pct(meta_media)}**, gerando um gap médio de **{gap_medio:+.2f} ponto(s) percentual(is)**.
- **{format_pct(atingiu_meta_pct)}** dos registros selecionados atingem ou superam a própria meta.
- A região com maior cobertura média no recorte é **{melhor_regiao}**.
- A região com menor cobertura média no recorte é **{pior_regiao}**.
- A vacina com maior cobertura média no recorte é **{melhor_vacina}**.
- O nível de alerta mais frequente é **{alerta_mais_frequente}**.
"""
)


# ---------------------------------------------------------
# Conclusão executiva
# ---------------------------------------------------------
st.subheader("Conclusão executiva")

if cobertura_media >= meta_media:
    conclusao_meta = (
        "A cobertura média do recorte está igual ou acima da meta média."
    )
else:
    conclusao_meta = (
        "A cobertura média do recorte está abaixo da meta média."
    )

st.write(
    f"{conclusao_meta} "
    f"O dashboard permite aprofundar essa leitura por período, região, "
    f"UF, município, vacina, público-alvo e nível de alerta. "
    f"Os resultados devem ser interpretados somente dentro da base simulada."
)