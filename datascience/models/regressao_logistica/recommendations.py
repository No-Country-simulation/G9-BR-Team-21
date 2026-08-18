"""
Motor de recomendações do EnergiAI (modelo de Regressão Logística).

Em vez de aplicar regras isoladas e gerar frases fixas por classificação,
este motor monta um diagnóstico narrativo: começa citando a variável que
mais pesou na decisão do modelo (segundo os coeficientes aprendidos),
depois detalha os pontos de atenção com intensidade proporcional ao
quanto o usuário se distancia do comportamento típico (benchmarks), e
finaliza reforçando hábitos positivos já identificados — mesmo em perfis
menos eficientes.

Tudo é determinístico: a mesma entrada sempre produz a mesma saída. A
variação de linguagem vem dos números reais de cada caso, não de
sorteio aleatório.
"""

import json
from pathlib import Path
from schemas import ConsumoInput

CONTEXT_PATH = Path(__file__).resolve().parent / "artifacts" / "recommendation_context.json"

with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
    _CONTEXT = json.load(f)

FEATURE_IMPORTANCES: dict = _CONTEXT["feature_importances"]
BENCHMARKS: dict = _CONTEXT["benchmarks"]

# nomes amigáveis para citar as variáveis em linguagem natural
ROTULOS_VARIAVEIS = {
    "consumo_kwh": "o consumo total de energia",
    "horas_alto_consumo": "o tempo em horário de alto consumo",
    "uso_horario_pico": "o uso em horário de pico",
    "quantidade_equipamentos": "a quantidade de equipamentos",
    "consumo_por_equipamento": "a eficiência dos equipamentos",
    "tipo_imovel": "o perfil do imóvel",
}


def _consumo_por_equipamento(dados: ConsumoInput) -> float:
    equipamentos = max(dados.quantidade_equipamentos, 1)
    return dados.consumo_kwh / equipamentos


def _nivel(ratio: float) -> str:
    """Classifica o quão acima do esperado um valor está, em relação ao benchmark."""
    if ratio >= 1.6:
        return "alto"
    if ratio >= 1.3:
        return "moderado"
    return "leve"


def _top_variavel_relevante(sinais_ativos: list[str]) -> str | None:
    """
    Entre as variáveis que efetivamente pesaram negativamente neste caso
    (sinais_ativos), retorna a que o modelo considera mais importante.
    Isso conecta a explicação diretamente ao que o modelo aprendeu, em vez
    de citar sempre a mesma variável por padrão.
    """
    if not sinais_ativos:
        return None
    return max(sinais_ativos, key=lambda v: FEATURE_IMPORTANCES.get(v, 0))


def gerar_recomendacoes(categoria: str, probabilidade: float, dados: ConsumoInput) -> list[str]:
    consumo_equip = _consumo_por_equipamento(dados)

    bench_consumo_geral = BENCHMARKS["consumo_kwh"]["geral"]
    bench_consumo_tipo = BENCHMARKS["consumo_kwh"]["por_tipo_imovel"].get(dados.tipo_imovel.value)

    bench_equip_geral = BENCHMARKS["consumo_por_equipamento"]["geral"]
    bench_equip_tipo = BENCHMARKS["consumo_por_equipamento"]["por_tipo_imovel"].get(dados.tipo_imovel.value)
    limite_equip = bench_equip_tipo if bench_equip_tipo else bench_equip_geral["p75"]

    bench_horas_p75 = BENCHMARKS["horas_alto_consumo"]["p75"]
    bench_qtd_equip_p75 = BENCHMARKS["quantidade_equipamentos"]["p75"]

    ratio_pico = (dados.horas_alto_consumo / bench_horas_p75) if dados.uso_horario_pico else 0
    ratio_equip = consumo_equip / limite_equip if limite_equip else 0
    ratio_consumo = (dados.consumo_kwh / bench_consumo_tipo) if bench_consumo_tipo else 0

    sinais_ativos = []
    if ratio_pico > 1:
        sinais_ativos.append("uso_horario_pico")
    if ratio_equip > 1:
        sinais_ativos.append("consumo_por_equipamento")
    if ratio_consumo > 1.15:
        sinais_ativos.append("consumo_kwh")

    top_variavel = _top_variavel_relevante(sinais_ativos)

    mensagens: list[str] = []

    # ---- abertura: diagnóstico personalizado ----
    if categoria == "Ineficiente":
        if top_variavel:
            mensagens.append(
                f"Seu perfil foi classificado como Ineficiente. O ponto que mais "
                f"pesou nessa avaliação foi {ROTULOS_VARIAVEIS[top_variavel]} — "
                f"essa é justamente a variável de maior peso no modelo para "
                f"identificar desperdício energético."
            )
        else:
            mensagens.append(
                "Seu perfil foi classificado como Ineficiente. Vale revisar os "
                "hábitos gerais de consumo o quanto antes."
            )
    elif categoria == "Moderado":
        if probabilidade < 0.6:
            mensagens.append(
                "Seu perfil está no limite entre Moderado e Eficiente — pequenos "
                "ajustes pontuais já podem ser suficientes para mudar de "
                "categoria."
            )
        else:
            mensagens.append(
                "Seu perfil foi classificado como Moderado. Já existe um uso "
                "consciente de energia, mas ainda há espaço para otimizações."
            )
    else:  # Eficiente
        if bench_consumo_tipo and dados.consumo_kwh < bench_consumo_tipo:
            percentual_abaixo = (1 - dados.consumo_kwh / bench_consumo_tipo) * 100
            mensagens.append(
                f"Seu perfil foi classificado como Eficiente. O consumo de "
                f"{dados.consumo_kwh:.0f} kWh está {percentual_abaixo:.0f}% abaixo "
                f"da média para imóveis do tipo {dados.tipo_imovel.value.title()} "
                f"({bench_consumo_tipo:.0f} kWh) — um resultado consistente."
            )
        else:
            mensagens.append(
                "Seu perfil foi classificado como Eficiente — os hábitos de "
                "consumo atuais estão alinhados com o que se espera de um uso "
                "consciente de energia."
            )

    # ---- pontos de atenção, com intensidade proporcional ao desvio (Moderado/Ineficiente) ----
    if ratio_pico > 1:
        nivel = _nivel(ratio_pico)
        frases = {
            "leve": (
                f"O uso em horário de pico está um pouco acima do esperado "
                f"({dados.horas_alto_consumo:.0f}h/dia, ante uma referência de "
                f"{bench_horas_p75:.1f}h). Reduzir aos poucos as atividades "
                f"nesse período já ajuda."
            ),
            "moderado": (
                f"Há uma concentração relevante de consumo no horário de pico "
                f"({dados.horas_alto_consumo:.0f}h/dia, contra {bench_horas_p75:.1f}h "
                f"de referência). Migrar parte dessas atividades para outros "
                f"horários tende a gerar economia perceptível."
            ),
            "alto": (
                f"O horário de pico concentra boa parte do seu consumo "
                f"({dados.horas_alto_consumo:.0f}h/dia, bem acima da referência de "
                f"{bench_horas_p75:.1f}h). Esse é provavelmente o ajuste com maior "
                f"potencial de impacto no seu perfil."
            ),
        }
        mensagens.append(frases[nivel])

    if ratio_equip > 1:
        nivel = _nivel(ratio_equip)
        frases = {
            "leve": (
                f"O consumo por equipamento ({consumo_equip:.1f} kWh) está "
                f"discretamente acima da média para imóveis do tipo "
                f"{dados.tipo_imovel.value.title()} ({limite_equip:.1f} kWh)."
            ),
            "moderado": (
                f"O consumo por equipamento ({consumo_equip:.1f} kWh) está "
                f"visivelmente acima da média esperada para "
                f"{dados.tipo_imovel.value.title()} ({limite_equip:.1f} kWh) — "
                f"pode valer a pena avaliar o estado dos aparelhos mais usados."
            ),
            "alto": (
                f"O consumo por equipamento ({consumo_equip:.1f} kWh) está muito "
                f"acima do esperado para {dados.tipo_imovel.value.title()} "
                f"({limite_equip:.1f} kWh), o que costuma indicar aparelhos "
                f"antigos ou pouco eficientes — vale uma revisão."
            ),
        }
        mensagens.append(frases[nivel])

    if ratio_consumo > 1.15:
        percentual = (ratio_consumo - 1) * 100
        mensagens.append(
            f"No total, o consumo de {dados.consumo_kwh:.0f} kWh está "
            f"{percentual:.0f}% acima da média para imóveis do tipo "
            f"{dados.tipo_imovel.value.title()} ({bench_consumo_tipo:.0f} kWh) — "
            f"comparar hábitos com imóveis semelhantes pode ajudar a mapear "
            f"onde está o desperdício."
        )

    # ---- reforço positivo para Moderado/Ineficiente: destaca o que já vai bem ----
    if categoria != "Eficiente":
        if not dados.uso_horario_pico:
            mensagens.append(
                "Um ponto a favor: seu consumo não está concentrado no horário "
                "de pico — vale manter esse hábito."
            )
        elif dados.quantidade_equipamentos >= bench_qtd_equip_p75 and ratio_equip <= 1:
            mensagens.append(
                "Apesar do número elevado de equipamentos, o consumo por "
                "aparelho está dentro do esperado — sinal de que os "
                "equipamentos em si não são o principal problema."
            )

    # ---- dicas de manutenção específicas para quem já é Eficiente ----
    if categoria == "Eficiente":
        if dados.quantidade_equipamentos >= bench_qtd_equip_p75:
            mensagens.append(
                f"Mesmo com {dados.quantidade_equipamentos} equipamentos — acima "
                f"da média geral —, o consumo se manteve controlado. É um "
                f"indício de bom uso dos aparelhos; vale manter o hábito de "
                f"desligá-los quando não estiverem em uso."
            )
        else:
            mensagens.append(
                "A quantidade de equipamentos e o tempo de uso estão dentro do "
                "esperado. Manter o consumo fora do horário de pico, quando "
                "possível, ajuda a preservar esse resultado a longo prazo."
            )

        if dados.tipo_imovel.value == "COMERCIO":
            mensagens.append(
                "Para estabelecimentos comerciais, automatizar iluminação e "
                "climatização é um bom próximo passo para manter a eficiência "
                "mesmo com o crescimento da operação."
            )
        else:
            mensagens.append(
                "Vale considerar acompanhar o consumo mensalmente — pequenas "
                "mudanças de hábito costumam aparecer antes de impactar a "
                "conta de energia."
            )

    return mensagens[:5]