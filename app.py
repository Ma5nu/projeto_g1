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
