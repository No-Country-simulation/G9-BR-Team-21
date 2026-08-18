# EnergiAI — Microsserviço de Classificação (Regressão Logística)

Microsserviço em Python responsável por classificar o perfil de eficiência
energética (Eficiente, Moderado ou Ineficiente) utilizando um modelo de
Regressão Logística, e por gerar recomendações personalizadas.

## Estrutura da pasta

```
models/
├── energiai_modelagem_regressao.ipynb   # notebook de treinamento e análise
└── regressao_logistica/
    ├── README.md                        # este arquivo
    ├── artifacts/                       # modelo já treinado (incluso no repositório)
    │   ├── logistic_regression_model.joblib
    │   ├── scaler.joblib
    │   ├── feature_columns.json
    │   └── recommendation_context.json
    ├── train_model.py                   # espelho da lógica de treino em formato de script
    ├── schemas.py                       # contrato de entrada/saída da API
    ├── recommendations.py               # lógica de geração de recomendações
    ├── main.py                          # microsserviço FastAPI
    ├── requirements.txt                 # dependências da API
    └── Dockerfile                       # imagem para deploy (ex: OCI)
```

> ✅ O modelo já vem **treinado e incluído** neste repositório
> (`artifacts/`). Não é necessário rodar o notebook ou o script de
> treino para subir a API.

---

## Sobre o notebook (`energiai_modelagem_regressao.ipynb`)

Documenta o treinamento do modelo, a partir da base tratada em
`data/processed/energiai_dataset_v1.csv`:

| Etapa | Conteúdo |
|---|---|
| 1 | Carregamento e exploração dos dados |
| 2 | Preparação das features (engenharia de `consumo_por_equipamento`, one-hot encoding de `tipo_imovel`) |
| 3 | Divisão treino/teste (estratificada) |
| 4 | Padronização (`StandardScaler`, ajustado só no treino) |
| 5 | Treinamento da Regressão Logística |
| 6 | Avaliação (acurácia, classification report, matriz de confusão) |
| 7 | Interpretação dos coeficientes |
| 8 | Relatório geral de treinamento |

O modelo atingiu **95,8% de acurácia** no conjunto de teste.

## Sobre o `train_model.py`

Espelha a mesma lógica de treinamento do notebook (Etapas 1 a 5), em
formato de script executável, e adiciona a extração dos coeficientes e
dos benchmarks estatísticos utilizados pela geração de recomendações.

O notebook continua sendo a fonte oficial de documentação e análise —
o script serve apenas para retreinar rapidamente via terminal:

```bash
cd models/regressao_logistica
python train_model.py
```

---

## Como rodar a API do zero

### Pré-requisitos

- Python 3.11 ou 3.12
- Git

### Passo 1 — Clonar o repositório

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### Passo 2 — Criar o ambiente virtual

```bash
cd models/regressao_logistica
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Passo 3 — Instalar as dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Passo 4 — Subir a API

```bash
uvicorn main:app --reload --port 8001
```

> Usamos a porta **8001** aqui para não conflitar com o microsserviço da
> Árvore de Decisão (porta 8000), caso ambos rodem ao mesmo tempo.

### Passo 5 — Testar

```
http://127.0.0.1:8001/docs
```

Ou via terminal:

```bash
curl -X POST http://127.0.0.1:8001/predict \
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
  "probabilidade": 0.87,
  "recomendacoes": [
    "Perfil ineficiente: revise os hábitos gerais de consumo o quanto antes.",
    "Seu consumo está concentrado no horário de pico..."
  ]
}
```

---

## Retreinar o modelo (opcional)

```bash
cd models/regressao_logistica
venv\Scripts\activate        # Windows
python train_model.py
```

Depois, reinicie a API (`CTRL+C` e suba de novo com `uvicorn`), pois o
modelo é carregado apenas na inicialização.

---

## Deploy na OCI (resumo simples)

1. Construir a imagem Docker:
   ```bash
   docker build -t energiai-regressao-logistica .
   ```
2. Enviar a imagem para o **OCI Container Registry (OCIR)**.
3. Rodar a imagem em uma **OCI Compute Instance** ou em **OCI Container
   Instances**, expondo a porta `8000`.
4. Configurar as regras de segurança (Security List / NSG) liberando a
   porta utilizada pela API.

---

## Stack utilizada

- **Python 3.11+**
- **scikit-learn** — Regressão Logística + padronização (`StandardScaler`)
- **pandas** — manipulação de dados
- **FastAPI** — exposição do endpoint REST
- **uvicorn** — servidor ASGI
- **joblib** — serialização do modelo e do scaler