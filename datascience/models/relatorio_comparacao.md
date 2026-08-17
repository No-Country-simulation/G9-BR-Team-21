# Relatório de Avaliação e Seleção do Modelo

## 1. Critérios de Avaliação
Para atender aos requisitos do MVP (uma API REST que retorna a classificação, recomendações e a **probabilidade** da previsão), a escolha do modelo priorizou:
*   **F1-Score e Acurácia:** Para garantir assertividade geral e equilíbrio no acerto de todas as categorias, lidando com possíveis desbalanceamentos.
*   **Análise de Erros (Matriz de Confusão):** Para evitar erros críticos (como classificar um perfil "Ineficiente" como "Eficiente"), o que comprometeria severamente o motor de recomendações.
*   **Calibração de Probabilidades:** A necessidade fundamental de um modelo que forneça valores contínuos e bem calibrados de probabilidade para integrar o payload JSON do endpoint.

## 2. Desempenho dos Modelos
Após o processamento dos dados e treinamento, os modelos apresentaram os seguintes resultados na base de teste:

*   **Regressão Logística (Modelo Selecionado):** Destacou-se como o melhor modelo, alcançando uma Acurácia e F1-Score geral de **0.96 (96%)**. O modelo errou apenas 4 classificações no total e não cometeu nenhum erro grave (não houve confusão direta entre "Eficiente" e "Ineficiente"). Sendo um modelo linear, suas probabilidades nativas são perfeitamente adequadas para a resposta da API.
    *   *Observação Técnica:* Apesar do desempenho elevado, esse resultado é esperado e não representa necessariamente uma evidência de forte generalização para padrões desconhecidos do mundo real. A categoria alvo foi construída a partir de uma combinação quase linear das mesmas variáveis utilizadas no treinamento. Dessa forma, o resultado positivo reflete principalmente a qualidade da engenharia de features (feature engineering) e da modelagem do problema, mais do que uma comprovação de que o modelo generalizaria com a mesma precisão para distribuições de dados completamente inéditas.

*   **Random Forest:** Apresentou uma Acurácia e F1-Score na faixa de **0.90**. Na sua matriz de confusão, cometeu um total de 10 erros, mostrando um pouco mais de dificuldade nas fronteiras entre as classes em comparação ao modelo linear. Por outro lado, o modelo foi útil para confirmar a importância das variáveis, indicando que o consumo em kWh (34.1%) e o uso em horário de pico (24.2%) são os preditores mais fortes.

*   **Decision Tree:** Obteve métricas levemente inferiores ou empatadas com o Random Forest, com Acurácia e F1-Score variando entre **0.89 e 0.91** nas validações. Por sua natureza matemática, tende a gerar probabilidades extremas nas folhas (0 ou 1), o que oferece uma péssima calibração. 

## 3. Conclusão e Próximos Passos
O modelo selecionado para serialização e implantação na arquitetura OCI é a **Regressão Logística**. Além de possuir as melhores métricas preditivas (96% de acerto), é um algoritmo computacionalmente leve, garantindo respostas rápidas e eficientes no endpoint `/analise-energetica`.

Os coeficientes aprendidos pelo modelo validam a regra de negócio (altas horas de alto consumo e uso em horário de pico aumentam severamente o peso para a categoria "Ineficiente"), o que nos fornece uma base analítica sólida para o desenvolvimento da lógica do motor de recomendações na próxima etapa.