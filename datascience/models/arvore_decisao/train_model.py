"""
Treina a árvore de decisão do EnergiAI, calibra as probabilidades,
calcula o contexto de recomendação (importância de variáveis + benchmarks)
e salva os artefatos.

Rodar sempre que o dataset for atualizado:
    python train_model.py
"""
"""
 Este script é um espelho da lógica de treinamento do notebook
`models/energiai_modelagem.ipynb` (Partes 1 a 6). Mantido apenas como
atalho para retreino rápido via linha de comando.

O notebook é a fonte oficial de documentação e justificativa do modelo.
Se você alterar a lógica de treinamento, atualize os dois arquivos.
"""

import json
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report
import joblib

# ---- paths ----
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "energiai_dataset_v1.csv"

MODEL_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_DIR.mkdir(exist_ok=True)
MODEL_PATH = MODEL_DIR / "decision_tree_model.joblib"
CONTEXT_PATH = MODEL_DIR / "recommendation_context.json"

FEATURES = [
    "consumo_kwh",
    "horas_alto_consumo",
    "uso_horario_pico",
    "tipo_imovel",
    "quantidade_equipamentos",
]
TARGET = "categoria"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["tipo_imovel"] = df["tipo_imovel"].str.upper()
    df["uso_horario_pico"] = df["uso_horario_pico"].astype(bool).astype(int)
    return df


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("tipo_imovel_ohe", OneHotEncoder(handle_unknown="ignore"), ["tipo_imovel"]),
        ],
        remainder="passthrough",
    )


def build_calibrated_pipeline() -> Pipeline:
    """Pipeline definitivo, usado em produção (probabilidades calibradas)."""
    base_tree = DecisionTreeClassifier(
        max_depth=6,
        random_state=42,
        class_weight="balanced",
    )

    calibrated_tree = CalibratedClassifierCV(
        estimator=base_tree,
        method="sigmoid",
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    )

    return Pipeline(steps=[
        ("preprocessor", build_preprocessor()),
        ("classifier", calibrated_tree),
    ])


def compute_feature_importances(X_train: pd.DataFrame, y_train: pd.Series) -> dict:
    """
    Treina uma árvore simples (não calibrada) apenas para extrair
    feature_importances_, usada para priorizar as recomendações.
    """
    tree = DecisionTreeClassifier(max_depth=6, random_state=42, class_weight="balanced")
    pipe = Pipeline(steps=[
        ("preprocessor", build_preprocessor()),
        ("classifier", tree),
    ])
    pipe.fit(X_train, y_train)

    feature_names = pipe.named_steps["preprocessor"].get_feature_names_out()
    importances = pipe.named_steps["classifier"].feature_importances_

    # mapeia nomes de features (após one-hot) de volta para a variável original
    importance_by_variable: dict[str, float] = {}
    for name, importance in zip(feature_names, importances):
        if name.startswith("tipo_imovel_ohe__"):
            variavel = "tipo_imovel"
        else:
            variavel = name.replace("remainder__", "")
        importance_by_variable[variavel] = importance_by_variable.get(variavel, 0.0) + float(importance)

    return importance_by_variable


def compute_benchmarks(df: pd.DataFrame) -> dict:
    """
    Calcula estatísticas de referência (médias e percentis) usadas
    para comparar cada nova entrada com o comportamento típico do dataset.
    """
    df = df.copy()
    df["consumo_por_equipamento"] = (
        df["consumo_kwh"] / df["quantidade_equipamentos"].replace(0, 1)
    )

    def to_float_dict(series: pd.Series) -> dict:
        return {str(k): float(v) for k, v in series.round(2).items()}

    benchmarks = {
        "consumo_kwh": {
            "geral": {
                "p25": float(df["consumo_kwh"].quantile(0.25)),
                "p50": float(df["consumo_kwh"].quantile(0.50)),
                "p75": float(df["consumo_kwh"].quantile(0.75)),
            },
            "por_tipo_imovel": to_float_dict(df.groupby("tipo_imovel")["consumo_kwh"].mean()),
        },
        "consumo_por_equipamento": {
            "geral": {
                "p25": float(df["consumo_por_equipamento"].quantile(0.25)),
                "p50": float(df["consumo_por_equipamento"].quantile(0.50)),
                "p75": float(df["consumo_por_equipamento"].quantile(0.75)),
            },
            "por_tipo_imovel": to_float_dict(df.groupby("tipo_imovel")["consumo_por_equipamento"].mean()),
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
    return benchmarks


def main():
    df = load_data()
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ---- modelo definitivo (calibrado) ----
    pipeline = build_calibrated_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    print("Relatório de avaliação:")
    print(classification_report(y_test, y_pred))

    joblib.dump(pipeline, MODEL_PATH)
    print(f"Modelo salvo em: {MODEL_PATH}")

    # ---- contexto de recomendação (importâncias + benchmarks) ----
    feature_importances = compute_feature_importances(X_train, y_train)
    benchmarks = compute_benchmarks(df)

    print("\nImportância das variáveis (segundo a árvore de decisão):")
    for variavel, importancia in sorted(feature_importances.items(), key=lambda x: -x[1]):
        print(f"  {variavel}: {importancia:.3f}")

    context = {
        "feature_importances": feature_importances,
        "benchmarks": benchmarks,
    }

    with open(CONTEXT_PATH, "w", encoding="utf-8") as f:
        json.dump(context, f, ensure_ascii=False, indent=2)

    print(f"\nContexto de recomendação salvo em: {CONTEXT_PATH}")


if __name__ == "__main__":
    main()