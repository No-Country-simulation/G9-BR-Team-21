"""
Motor de recomendações do EnergiAI.

As regras correlacionam múltiplas variáveis (não avaliam campos isolados)
e são priorizadas de acordo com a importância que a própria árvore de
decisão atribuiu a cada variável durante o treinamento, cruzada com
benchmarks estatísticos calculados a partir do dataset de treino.
"""

import json
from pathlib import Path
from schemas import ConsumoInput

CONTEXT_PATH = Path(__file__).resolve().parent / "artifacts" / "recommendation_context.json"

with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
    _CONTEXT = json.load(f)

FEATURE_IMPORTANCES: dict = _CONTEXT["feature_importances"]
BENCHMARKS: dict = _CONTEXT["benchmarks"]


def _consumo_por_equipamento(dados: ConsumoInput) -> float:
    equipamentos = max(dados.quantidade_equipamentos, 1)
    return dados.consumo_kwh / equipamentos


def _construir_regras(dados: ConsumoInput, categoria: str, probabilidade: float) -> list[dict]:
    consumo_equip = _consumo_por_equipamento(dados)

    bench_consumo_geral = BENCHMARKS["consumo_kwh"]["geral"]
    bench_consumo_tipo = BENCHMARKS["consumo_kwh"]["por_tipo_imovel"].get(dados.tipo_imovel.value)

    bench_equip_geral = BENCHMARKS["consumo_por_equipamento"]["geral"]
    bench_equip_tipo = BENCHMARKS["consumo_por_equipamento"]["por_tipo_imovel"].get(dados.tipo_imovel.value)

    bench_horas_p75 = BENCHMARKS["horas_alto_consumo"]["p75"]
    bench_qtd_equip_p75 = BENCHMARKS["quantidade_equipamentos"]["p75"]

    regras = []

    # Regra 1 — concentração de consumo no horário de pico
    # correlaciona: uso_horario_pico + horas_alto_consumo
    if dados.uso_horario_pico and dados.horas_alto_consumo >= bench_horas_p75:
        regras.append({
            "mensagem": (
                f"Seu consumo está concentrado no horário de pico por "
                f"{dados.horas_alto_consumo:.0f}h/dia, acima da média observada "
                f"({bench_horas_p75:.1f}h). Migrar atividades para fora do pico "
                f"pode reduzir custos, especialmente se a concessionária "
                f"oferecer tarifa branca ou horária."
            ),
            "prioridade": FEATURE_IMPORTANCES.get("horas_alto_consumo", 0)
                          + FEATURE_IMPORTANCES.get("uso_horario_pico", 0),
        })

    # Regra 2 — consumo por equipamento acima do esperado (equipamentos ineficientes)
    # correlaciona: consumo_kwh + quantidade_equipamentos + tipo_imovel
    limite_equip = bench_equip_tipo if bench_equip_tipo else bench_equip_geral["p75"]
    if consumo_equip > limite_equip:
        regras.append({
            "mensagem": (
                f"O consumo médio por equipamento está em "
                f"{consumo_equip:.1f} kWh, acima do esperado para imóveis do tipo "
                f"{dados.tipo_imovel.value.title()} ({limite_equip:.1f} kWh). "
                f"Isso pode indicar aparelhos antigos ou pouco eficientes — "
                f"vale avaliar a troca ou manutenção dos equipamentos de maior uso."
            ),
            "prioridade": FEATURE_IMPORTANCES.get("quantidade_equipamentos", 0)
                          + FEATURE_IMPORTANCES.get("consumo_kwh", 0),
        })

    # Regra 3 — muitos equipamentos, mas consumo controlado (elogio + alerta de standby)
    # correlaciona: quantidade_equipamentos + consumo_kwh
    if (dados.quantidade_equipamentos >= bench_qtd_equip_p75
            and dados.consumo_kwh <= bench_consumo_geral["p50"]):
        regras.append({
            "mensagem": (
                "Mesmo com uma quantidade relativamente alta de equipamentos, "
                "o consumo total está controlado — bom sinal de uso consciente. "
                "Ainda assim, vale revisar aparelhos em modo standby, que "
                "consomem energia mesmo desligados."
            ),
            "prioridade": FEATURE_IMPORTANCES.get("quantidade_equipamentos", 0),
        })

    # Regra 4 — consumo total acima da média para o tipo de imóvel
    # correlaciona: consumo_kwh + tipo_imovel
    if bench_consumo_tipo and dados.consumo_kwh > bench_consumo_tipo * 1.2:
        percentual = ((dados.consumo_kwh / bench_consumo_tipo) - 1) * 100
        regras.append({
            "mensagem": (
                f"O consumo de {dados.consumo_kwh:.0f} kWh está "
                f"{percentual:.0f}% acima da média para imóveis do tipo "
                f"{dados.tipo_imovel.value.title()} ({bench_consumo_tipo:.0f} kWh). "
                f"Comparar hábitos com imóveis semelhantes pode ajudar a "
                f"identificar pontos de desperdício."
            ),
            "prioridade": FEATURE_IMPORTANCES.get("consumo_kwh", 0),
        })

    # Regra 5 — caso "fronteiriço" (baixa confiança do modelo)
    # correlaciona: categoria + probabilidade
    if categoria == "Moderado" and probabilidade < 0.6:
        regras.append({
            "mensagem": (
                "Seu perfil está próximo da fronteira entre Moderado e "
                "Eficiente. Pequenos ajustes pontuais — como reduzir o uso "
                "durante o horário de pico — podem ser suficientes para "
                "mudar de categoria."
            ),
            "prioridade": 0.05,
        })

    return regras


def gerar_recomendacoes(categoria: str, probabilidade: float, dados: ConsumoInput) -> list[str]:
    resumo = {
        "Eficiente": "Perfil eficiente: continue mantendo os hábitos atuais de consumo.",
        "Moderado": "Perfil moderado: pequenos ajustes já trazem ganhos relevantes de eficiência.",
        "Ineficiente": "Perfil ineficiente: revise os hábitos gerais de consumo o quanto antes.",
    }.get(categoria, "Perfil analisado com base nos dados informados.")

    regras = _construir_regras(dados, categoria, probabilidade)
    regras_ordenadas = sorted(regras, key=lambda r: r["prioridade"], reverse=True)

    mensagens = [resumo] + [r["mensagem"] for r in regras_ordenadas]

    # resumo + até 4 recomendações específicas mais relevantes
    return mensagens[:5]