"""
Treina o modelo de Regressão Logística do EnergiAI e salva os artefatos
necessários para o microsserviço: modelo, scaler, ordem das colunas de
features e contexto de recomendação (coeficientes + benchmarks).

Este script é um espelho, em formato executável, da mesma lógica do
notebook de treinamento (`energiai_modelagem_regressao.ipynb`).

Rodar sempre que o dataset for atualizado:
    python train_model.py
"""

import json
from pathlib import Path

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# ---- paths ----
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "energiai_dataset_v1.csv"

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)

MODEL_PATH = ARTIFACTS_DIR / "logistic_regression_model.joblib"
SCALER_PATH = ARTIFACTS_DIR / "scaler.joblib"
FEATURE_COLUMNS_PATH = ARTIFACTS_DIR / "feature_columns.json"
CONTEXT_PATH = ARTIFACTS_DIR / "recommendation_context.json"

RANDOM_STATE = 42

# nomes exatos gerados pelo pd.get_dummies() a partir dos valores originais
# de tipo_imovel na base ("Casa", "Apartamento", "Comercio")
TIPO_IMOVEL_DUMMIES = [
    "tipo_imovel_Apartamento",
    "tipo_imovel_Casa",
    "tipo_imovel_Comercio",
]


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def build_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    df = df.copy()

    # mesma relação usada na construção do score/rótulo original
    df["consumo_por_equipamento"] = df["consumo_kwh"] / df["quantidade_equipamentos"]

    # codificação one-hot: sem relação de ordem entre as categorias
    df_codificado = pd.get_dummies(df, columns=["tipo_imovel"], prefix="tipo_imovel")

    # garante que as 3 colunas de tipo_imovel sempre existam, mesmo que
    # alguma categoria não apareça na base de treino
    for coluna in TIPO_IMOVEL_DUMMIES:
        if coluna not in df_codificado.columns:
            df_codificado[coluna] = False

    colunas_excluir = ["meter_id", "categoria", "custo_estimado_mensal"]
    X = df_codificado.drop(columns=[c for c in colunas_excluir if c in df_codificado.columns])
    y = df_codificado["categoria"]

    return X, y


def compute_benchmarks(df: pd.DataFrame) -> dict:
    """
    Calcula estatísticas de referência usadas na geração de recomendações.
    As chaves de tipo_imovel são normalizadas para maiúsculo, para ficarem
    consistentes com o enum utilizado no contrato da API (CASA, APARTAMENTO,
    COMERCIO).
    """
    df = df.copy()
    df["consumo_por_equipamento"] = df["consumo_kwh"] / df["quantidade_equipamentos"]
    df["tipo_imovel_upper"] = df["tipo_imovel"].str.upper()

    def to_float_dict(series: pd.Series) -> dict:
        return {str(k): float(v) for k, v in series.round(2).items()}

    return {
        "consumo_kwh": {
            "geral": {
                "p25": float(df["consumo_kwh"].quantile(0.25)),
                "p50": float(df["consumo_kwh"].quantile(0.50)),
                "p75": float(df["consumo_kwh"].quantile(0.75)),
            },
            "por_tipo_imovel": to_float_dict(df.groupby("tipo_imovel_upper")["consumo_kwh"].mean()),
        },
        "consumo_por_equipamento": {
            "geral": {
                "p25": float(df["consumo_por_equipamento"].quantile(0.25)),
                "p50": float(df["consumo_por_equipamento"].quantile(0.50)),
                "p75": float(df["consumo_por_equipamento"].quantile(0.75)),
            },
            "por_tipo_imovel": to_float_dict(df.groupby("tipo_imovel_upper")["consumo_por_equipamento"].mean()),
        },
        "horas_alto_consumo": {
            "p50": float(df["horas_alto_consumo"].quantile(0.50)),
            "p75": float(df["horas_alto_consumo"].quantile(0.75)),
        },
        "quantidade_equipamentos": {
            "p50": float(df["quantidade_equipamentos"].quantile(0.50)),
            "p75": float(df["quantidade_equipamentos"].quantile(0.75)),
        },
    }


def main():
    df = load_data()
    X, y = build_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y
    )

    # padronização: ajustada somente no treino, aplicada depois no teste
    # (evita vazamento de dados / data leakage)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    modelo = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    modelo.fit(X_train_scaled, y_train)

    y_pred = modelo.predict(X_test_scaled)
    print("Relatório de avaliação:")
    print(classification_report(y_test, y_pred))
    print(f"Número de iterações até convergir: {modelo.n_iter_}")

    # ---- contexto de recomendação: coeficientes + benchmarks ----
    coeficientes = pd.DataFrame(modelo.coef_, columns=X.columns, index=modelo.classes_)
    coef_ineficiente = coeficientes.loc["Ineficiente"].to_dict()

    # agrega os coeficientes das colunas dummy de tipo_imovel em uma única
    # métrica de importância (mesmo formato usado nas regras de recomendação)
    importance_by_variable: dict[str, float] = {}
    for nome, valor in coef_ineficiente.items():
        variavel = "tipo_imovel" if nome.startswith("tipo_imovel_") else nome
        importance_by_variable[variavel] = importance_by_variable.get(variavel, 0.0) + abs(float(valor))

    print("\nImportância das variáveis (coeficientes da classe 'Ineficiente'):")
    for variavel, importancia in sorted(importance_by_variable.items(), key=lambda x: -x[1]):
        print(f"  {variavel}: {importancia:.3f}")

    benchmarks = compute_benchmarks(df)

    # ---- serialização ----
    joblib.dump(modelo, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    with open(FEATURE_COLUMNS_PATH, "w", encoding="utf-8") as f:
        json.dump(list(X.columns), f, ensure_ascii=False, indent=2)

    context = {
        "feature_importances": importance_by_variable,
        "benchmarks": benchmarks,
    }
    with open(CONTEXT_PATH, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

    print(f"\nModelo salvo em: {MODEL_PATH}")
    print(f"Scaler salvo em: {SCALER_PATH}")
    print(f"Colunas de features salvas em: {FEATURE_COLUMNS_PATH}")
    print(f"Contexto de recomendação salvo em: {CONTEXT_PATH}")


if __name__ == "__main__":
    main()