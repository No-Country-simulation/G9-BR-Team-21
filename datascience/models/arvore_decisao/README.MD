# EnergiAI — Modelagem e Microsserviço de Classificação Energética

Este diretório contém o **microsserviço em Python** e a documentação do
modelo de **Ciência de Dados** do projeto EnergiAI, responsável por
classificar o perfil de eficiência energética (Eficiente, Moderado ou
Ineficiente) a partir de dados de consumo, e por gerar recomendações
personalizadas.

## Estrutura da pasta

```
models/
├── energiai_modelagem.ipynb           # notebook de treinamento e análise
└── arvore_decisao/
    ├── README.md                      # este arquivo
    ├── artifacts/                     # modelo já treinado (incluso no repositório)
    │   ├── decision_tree_model.joblib
    │   ├── recommendation_context.json
    │   └── arvore_decisao_resumida.png
    ├── train_model.py                 # espelho da lógica de treino em formato de script
    ├── schemas.py                     # contrato de entrada/saída da API
    ├── recommendations.py             # lógica de geração de recomendações
    ├── main.py                        # microsserviço FastAPI
    └── requirements.txt               # dependências da API
```

> ✅ O modelo já vem **treinado e incluído** neste repositório
> (`artifacts/`). Não é necessário rodar o notebook para subir a API —
> basta instalar as dependências e rodar o `uvicorn` (veja o passo a passo
> abaixo). O notebook é útil apenas caso você queira **retreinar o
> modelo** com uma nova base de dados.

---

## Sobre o notebook (`energiai_modelagem.ipynb`)

O notebook documenta toda a etapa de **modelagem** do projeto, a partir da
base de dados já tratada em `data/processed/energiai_dataset_v1.csv`, e é
dividido nas seguintes partes:

| Parte | Conteúdo |
|---|---|
| 1 | Preparação dos dados para modelagem (features, target, split treino/teste) |
| 2 | Treinamento da Árvore de Decisão |
| 3 | Avaliação do modelo (métricas e matriz de confusão) |
| 4 | Importância das variáveis + visualização gráfica da árvore |
| 5 | Lógica de geração de recomendações (regras + benchmarks estatísticos) |
| 6 | Serialização do modelo treinado e do contexto de recomendação |
| 7 | Exemplos de utilização do modelo |

**O que o notebook gera ao ser executado por completo:**

- `artifacts/decision_tree_model.joblib` — pipeline completo
  (pré-processamento + modelo calibrado), consumido diretamente pela API;
- `artifacts/recommendation_context.json` — importância de variáveis e
  benchmarks estatísticos, usados para gerar recomendações;
- `artifacts/arvore_decisao_resumida.png` — visualização gráfica da árvore
  de decisão treinada.

Esses três arquivos **já estão incluídos neste repositório**, gerados a
partir da base de dados atual (`energiai_dataset_v1.csv`). Você só precisa
executar o notebook novamente se quiser treinar o modelo com uma base
diferente ou testar alterações na lógica de modelagem.

---

## Sobre o `train_model.py`

Este arquivo é um **espelho, em formato de script, da mesma lógica de
treinamento presente no notebook** (Partes 1, 2 e 6 — preparação dos
dados, treinamento do modelo e serialização). Ele foi mantido no
repositório para documentar de forma objetiva e executável como o modelo
foi treinado, sem a necessidade de abrir um ambiente Jupyter.

**O notebook (`energiai_modelagem.ipynb`) é a fonte oficial de
documentação do projeto** — nele estão as análises, gráficos, avaliação
detalhada e justificativas de cada decisão de modelagem. O
`train_model.py` não substitui o notebook, apenas oferece uma forma
alternativa e mais rápida de retreinar o modelo via linha de comando:

```bash
cd models/arvore_decisao
python train_model.py
```

> ⚠️ Caso a lógica de treinamento seja alterada no notebook (por exemplo,
> mudança de hiperparâmetros ou de variáveis utilizadas), o
> `train_model.py` deve ser atualizado manualmente para refletir a mesma
> lógica, evitando divergência entre os dois artefatos.

---

## Passo a passo — rodando a API (modelo já treinado)

### Pré-requisitos

- Python 3.11 ou 3.12 instalado (evite versões muito recentes, como 3.13+,
  que ainda podem ter incompatibilidade com `scikit-learn`)
- Git

Para conferir sua versão do Python:

```bash
python --version
```

### Passo 1 — Entrar na pasta do microsserviço e criar o ambiente virtual

```bash
cd models/arvore_decisao
python -m venv venv
```

Ative o ambiente:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Passo 2 — Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 3 — Subir a API

```bash
uvicorn main:app --reload --port 8000
```

Se tudo estiver certo, o terminal deve mostrar:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Passo 5 — Testar o endpoint

Acesse a documentação interativa gerada automaticamente pelo FastAPI:

```
http://127.0.0.1:8000/docs
```

Ou teste via terminal:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "consumo_kwh": 420,
    "horas_alto_consumo": 8,
    "uso_horario_pico": true,
    "tipo_imovel": "CASA",
    "quantidade_equipamentos": 10
  }'
```

Resposta esperada:

```json
{
  "categoria": "Ineficiente",
  "probabilidade": 0.8,
  "recomendacoes": [
    "Perfil ineficiente: revise os hábitos gerais de consumo o quanto antes.",
    "Seu consumo está concentrado no horário de pico por 8h/dia..."
  ]
}
```

---

## Referência da API

### `POST /predict`

**Entrada:**

| Campo | Tipo | Valores aceitos |
|---|---|---|
| `consumo_kwh` | float | maior que 0 |
| `horas_alto_consumo` | float | entre 0 e 24 |
| `uso_horario_pico` | boolean | `true` / `false` |
| `tipo_imovel` | string (enum) | `"CASA"`, `"APARTAMENTO"`, `"COMERCIO"` |
| `quantidade_equipamentos` | integer | 0 ou mais |

> ⚠️ O campo `tipo_imovel` deve ser enviado **em letras maiúsculas**,
> exatamente como no enum. Valores fora desse padrão são rejeitados
> automaticamente pela API com erro HTTP `422`.

**Saída:**

```json
{
  "categoria": "Eficiente | Moderado | Ineficiente",
  "probabilidade": 0.0,
  "recomendacoes": ["string", "..."]
}
```

**O que a API não retorna** (por design, ver observações abaixo):

- Custo estimado mensal — calculado no back-end (Java);
- Formato de erro customizado — erros são retornados no padrão HTTP/JSON
  padrão do FastAPI, e traduzidos pelo back-end para o formato final do
  cliente.

---

## Retreinar o modelo (opcional)

Caso queira treinar o modelo novamente — por exemplo, após atualizar a base
de dados em `data/processed/energiai_dataset_v1.csv` — existem duas formas
de fazer isso: pelo notebook (recomendado, mais completo) ou pelo script
`train_model.py` (mais rápido, sem Jupyter).

### Opção A — via notebook (recomendada)

#### 1. Criar um ambiente para o notebook

A partir da raiz do projeto:

```bash
cd models
python -m venv venv-notebook

# Windows
venv-notebook\Scripts\activate
# Linux/Mac
source venv-notebook/bin/activate

pip install --upgrade pip
pip install pandas scikit-learn matplotlib seaborn joblib jupyter
```

#### 2. Rodar o notebook

```bash
jupyter notebook
```

Abra `energiai_modelagem.ipynb` (localizado em `models/`) e execute todas
as células, em ordem, do início ao fim (`Kernel → Restart & Run All`).
Isso irá **sobrescrever** os artefatos existentes em
`arvore_decisao/artifacts/` com a versão mais recente do modelo.

### Opção B — via script (mais rápida)

Se preferir não abrir o Jupyter, é possível rodar a mesma lógica de
treinamento diretamente pelo terminal, dentro do ambiente virtual da API
(`venv`, criado no Passo 2 da seção "Passo a passo — rodando a API"):

```bash
cd models/arvore_decisao
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

python train_model.py
```

Isso sobrescreve os mesmos artefatos em `artifacts/`, sem necessidade de
Jupyter ou das bibliotecas de visualização (`matplotlib`, `seaborn`).

### Reiniciar a API após retreinar

Independente da opção escolhida, o modelo é carregado apenas na
inicialização do servidor — após retreinar, é necessário reiniciar:

```bash
# no terminal onde a API está rodando
CTRL + C
uvicorn main:app --reload --port 8000
```

---

## Stack utilizada

- **Python 3.11+**
- **scikit-learn** — treinamento e calibração do modelo (Árvore de Decisão)
- **pandas** — manipulação de dados
- **FastAPI** — exposição do endpoint REST
- **uvicorn** — servidor ASGI
- **joblib** — serialização do modelo
- **matplotlib / seaborn** — visualizações (usadas apenas no notebook)