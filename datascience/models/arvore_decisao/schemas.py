from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class TipoImovel(str, Enum):
    CASA = "CASA"
    APARTAMENTO = "APARTAMENTO"
    COMERCIO = "COMERCIO"


class ConsumoInput(BaseModel):
    consumo_kwh: float = Field(..., gt=0, example=420)
    horas_alto_consumo: float = Field(..., ge=0, le=24, example=8)
    uso_horario_pico: bool = Field(..., example=True)
    tipo_imovel: TipoImovel = Field(..., example="CASA")
    quantidade_equipamentos: int = Field(..., ge=0, example=10)


class PredictResponse(BaseModel):
    categoria: str
    probabilidade: float
    recomendacoes: List[str]