import json
import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI

from schemas import ConsumoInput, PredictResponse
from recommendations import gerar_recomendacoes

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "logistic_regression_model.joblib"
SCALER_PATH = ARTIFACTS_DIR / "scaler.joblib"
FEATURE_COLUMNS_PATH = ARTIFACTS_DIR / "feature_columns.json"

app = FastAPI(
    title="EnergiAI - Serviço de Classificação (Regressão Logística)",
    description="Microsserviço em Python responsável por classificar o perfil "
                "de consumo energético e sugerir recomendações, utilizando "
                "um modelo de Regressão Logística.",
    version="1.0.0",
)

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

with open(FEATURE_COLUMNS_PATH, "r", encoding="utf-8") as f:
    FEATURE_COLUMNS = json.load(f)

# mapeia o enum da API para o nome exato da coluna dummy gerada no treino
TIPO_IMOVEL_DUMMY_MAP = {
    "CASA": "tipo_imovel_Casa",
    "APARTAMENTO": "tipo_imovel_Apartamento",
    "COMERCIO": "tipo_imovel_Comercio",
}


def montar_vetor_features(dados: ConsumoInput) -> pd.DataFrame:
    """
    Reconstrói manualmente o vetor de features no mesmo formato usado no
    treinamento (mesmas colunas, mesma ordem), evitando o uso de
    pd.get_dummies() em tempo de predição — que não é seguro para uma
    única requisição isolada.
    """
    consumo_por_equipamento = dados.consumo_kwh / max(dados.quantidade_equipamentos, 1)

    linha = {coluna: 0 for coluna in FEATURE_COLUMNS}
    linha["consumo_kwh"] = dados.consumo_kwh
    linha["horas_alto_consumo"] = dados.horas_alto_consumo
    linha["uso_horario_pico"] = int(dados.uso_horario_pico)
    linha["quantidade_equipamentos"] = dados.quantidade_equipamentos
    linha["consumo_por_equipamento"] = consumo_por_equipamento

    coluna_dummy = TIPO_IMOVEL_DUMMY_MAP[dados.tipo_imovel.value]
    linha[coluna_dummy] = 1

    df = pd.DataFrame([linha])
    df = df.reindex(columns=FEATURE_COLUMNS, fill_value=0)
    return df


@app.post("/predict", response_model=PredictResponse)
def predict(dados: ConsumoInput):
    input_df = montar_vetor_features(dados)
    input_scaled = scaler.transform(input_df)

    categoria_predita = model.predict(input_scaled)[0]
    probabilidade = float(max(model.predict_proba(input_scaled)[0]))

    recomendacoes = gerar_recomendacoes(categoria_predita, probabilidade, dados)

    return PredictResponse(
        categoria=categoria_predita,
        probabilidade=round(probabilidade, 2),
        recomendacoes=recomendacoes,
    )