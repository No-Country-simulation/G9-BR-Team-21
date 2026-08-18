import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI

from schemas import ConsumoInput, PredictResponse
from recommendations import gerar_recomendacoes

MODEL_PATH = Path(__file__).resolve().parent / "artifacts" / "decision_tree_model.joblib"

app = FastAPI(
    title="EnergiAI - Serviço de Classificação de Eficiência Energética",
    description="Microsserviço em Python responsável por classificar o perfil "
                "de consumo energético e sugerir recomendações.",
    version="1.0.0",
)

model = joblib.load(MODEL_PATH)


@app.post("/predict", response_model=PredictResponse)
def predict(dados: ConsumoInput):
    input_df = pd.DataFrame([{
        "consumo_kwh": dados.consumo_kwh,
        "horas_alto_consumo": dados.horas_alto_consumo,
        "uso_horario_pico": int(dados.uso_horario_pico),
        "tipo_imovel": dados.tipo_imovel.value,
        "quantidade_equipamentos": dados.quantidade_equipamentos,
    }])

    categoria_predita = model.predict(input_df)[0]
    probabilidade = float(max(model.predict_proba(input_df)[0]))

    recomendacoes = gerar_recomendacoes(categoria_predita, probabilidade, dados)

    return PredictResponse(
        categoria=categoria_predita,
        probabilidade=round(probabilidade, 2),
        recomendacoes=recomendacoes,
    )