# Projeto G1 — Cobertura Vacinal no Brasil

Projeto acadêmico da disciplina **Linguagem de Programação — Análise e Visualização de Dados com Python**.

O projeto utiliza uma base simulada de cobertura vacinal para demonstrar um fluxo completo de análise de dados, incluindo:

- preparação e tratamento da base;
- análise exploratória;
- criação de KPIs;
- visualizações;
- análise temporal;
- correlação estatística;
- dashboard interativo com Streamlit.

> A base utilizada é uma simulação. Os resultados do projeto não representam estatísticas oficiais de saúde pública.

---

## Estrutura do projeto

```text
projeto-g1/
│
├── app.py
├── requirements.txt
├── README.md
├── index.html
│
├── dados/
│   └── simulacao_cobertura_vacinal_brasil.csv
│
├── database/
├── notebooks/
│   └── analise_cobertura_vacinal_colab.ipynb
│
└── imagens/
```

---

## Tecnologias

- Python
- Pandas
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- GitHub
- GitHub Pages

---

## Dashboard

O dashboard possui:

- filtros múltiplos;
- filtro por intervalo de anos;
- filtros por região, UF e município;
- filtros por vacina e público-alvo;
- filtro por nível de alerta;
- filtro por situação da meta;
- KPIs dinâmicos;
- gráficos interativos;
- análise temporal;
- média móvel de 6 meses;
- comparação entre cobertura e meta;
- matriz de correlação;
- tabela com os dados filtrados;
- download do recorte filtrado;
- interpretação textual;
- conclusão executiva.

---

## Executando localmente

### 1. Criar ambiente virtual

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Streamlit

```bash
streamlit run app.py
```

O Streamlit informará o endereço local, normalmente:

```text
http://localhost:8501
```

---

## Publicação no Streamlit Community Cloud

Antes de publicar, confirme que o repositório GitHub contém pelo menos:

```text
app.py
requirements.txt
dados/simulacao_cobertura_vacinal_brasil.csv
```

Depois:

1. Faça push do projeto para um repositório público no GitHub.
2. Acesse o **Streamlit Community Cloud**.
3. Entre com sua conta do GitHub.
4. Escolha **Create app** / **New app**.
5. Selecione o repositório do projeto.
6. Selecione a branch principal, normalmente `main`.
7. Em **Main file path**, informe:

```text
app.py
```

8. Confirme a publicação.
9. Após o deploy, copie a URL gerada pelo Streamlit.
10. Coloque essa URL no `README.md`, no `index.html` e na entrega da disciplina.

---

## Arquivo de dados

O `app.py` espera encontrar a base neste caminho:

```text
dados/simulacao_cobertura_vacinal_brasil.csv
```

Por isso, não altere o nome do arquivo ou da pasta sem também alterar `CAMINHO_DADOS` dentro de `app.py`.

---

## Notebook

O notebook de análise deve ser colocado em:

```text
notebooks/analise_cobertura_vacinal_colab.ipynb
```

No Google Colab, o notebook espera que o CSV esteja temporariamente na raiz:

```text
/content/simulacao_cobertura_vacinal_brasil.csv
```

Essa configuração do notebook é independente do caminho utilizado pelo Streamlit.

---

## Publicação completa da atividade

A entrega final deverá disponibilizar:

- link do repositório GitHub;
- link do GitHub Pages;
- link do dashboard Streamlit;
- notebook `.ipynb`;
- código-fonte do dashboard.

---

## Observação

Os resultados deste projeto são derivados de uma base simulada fornecida para fins acadêmicos.
