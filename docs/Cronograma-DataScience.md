# 🗂️ Board de Planejamento

> Este arquivo funciona como um Kanban simples dentro do repositório. </br>
> ## 🧭 Como usar:
> 1. **Criar tarefa nova** → adiciona um bloco `- [ ]` na coluna "Planejamento".
> 2. **Mover + Atualizar Progresso (Planejando > Fazendo > Revisão...)**
>      * Só dar check [x] na coluna atual e copiar e colar a 'tarefa' para a nova seção de destino,
>      * depois atualize na tabela "Visão geral" (ex. 3/3 itens planejados ja foram iniciados; 1/3 itens em progresso ja foram concluidos...) facilitando a todos acompanhar.
> 3. **Definir sua "tarefa" da semana** → No início de cada a fazer tem **"DSx"**; substituir pelo seu nome, a fim de não repetirem tarefas ou não realizarem.
> 4. **Sujestões e alterações são bem vindas ♥**
---

## 📊 Visão geral

| Status | Feitos-Itens | Equipe |
|---|---|---|
| 🟡 Planejamento | 3/3 | Suellen |
| 🔵 Em Progresso | 1/3 | nome |
| 🟢 Finalizado | 1/5 | nome |
| 🔴 Para Revisar | 0/5 | |

</br>

---

## 🟡 Planejamento </br> Semana 1 — Fundação, dados e contrato de API  

> **Meta Geral:** dataset inicial bruto documentado (com dicionário de variáveis) + contrato de API _ esqueleto do projeto rodando local + escolher a OCI que vamos usar.

</br>

- [x] **DSx**
  - Definir fontes de dados:
  - * públicas (ex: bases abertas de consumo residencial), simuladas manualmente, ou geradas por script (simular se não achar base pública boa o suficiente — o edital permite)

- [x] **DSx**
  - Gerar dataset inicial com as 5 variáveis do contrato: consumo_kwh, uso_horario_pico, quantidade_equipamentos, tipo_imovel, horas_alto_consumo
     
- [ ] **DSx**
  - EDA inicial: distribuições, outliers, correlações entre variáveis
  
- [ ] **DSx**
  - Sugestão de critério inicial: relação consumo_kwh/quantidade_equipamentos + peso para uso em horário de pico, ajustável com o time

- [ ] **DSx**
  - Definir e documentar por escrito os critérios que separam Eficiente / Moderado / Ineficiente (isso é cobrado explicitamente no edital — precisa de justificativa, não pode ser arbitrário)

<!--
Adicione novos itens de planejamento assim:
- [ ] **Título da tarefa**
  - Responsável:
  - Prazo:
  - Observações:
-->

</br>

---

## 🔵 Em Progresso (1/3)

- [ ] **Colar o que está sendo feito (Planejamento)**
  - Responsável: `<DSX>`
  - Progresso: `▓▓▓▓▓▓░░░░` 60%
  - Notas: `<atualizações recentes aqui>`

<!--
Modelo para novos itens em progresso:
- [ ] **Título da tarefa**
  - Responsável:
  - Progresso: `▓░░░░░░░░░` 10%
  - Notas:
-->

</br>

---

## 🟢 Finalizado (1/5)

- [x] **---**
  - Concluído em: `<data>`
  - Responsável: `<nome>`

<!--
Modelo:
- [x] **Título da tarefa**
  - Concluído em:
  - Responsável:
-->

</br>

---

## 🔴 Para Revisar (0/5)

<!-- Itens aguardando revisão de outra pessoa antes de ir para "Finalizado" -->

- [ ] **`<tarefa aguardando revisão>`**
  - Autor: `<nome>`
  - Revisor: `<nome>`

</br>

----------------------------------------------


# Semana 2  
## 🟡 Planejamento </br> — Modelagem baseline + endpoints mockados

> **Meta Geral:** modelo baseline com métricas registradas + endpoint mockado testável + decisão de arquitetura  DS↔Back-End + documentar no README.

</br>

- [ ] **DSx**
  - Limpeza e tratamento de dados (nulos, normalização, encoding de tipo_imovel)
    
- [ ] **DSx**
  - Feature engineering (ex: consumo por equipamento, índice de uso em pico)
    
- [ ] **DSx**
  - Treinar modelo baseline: Regressão Logística
    
- [ ] **DSx**
  - Calcular métricas: acurácia, F1-score, matriz de confusão
    
- [ ] **DSx**
  - Registrar tudo no notebook (isso é entregável obrigatório: EDA → treino → avaliação)  

</br>

---

## 🔵 Em Progresso (/)

- [ ] **Colar o que está sendo feito (Planejamento)**
  - Responsável: `<DSX>`
  - Progresso: `▓▓▓▓▓▓░░░░` 60%
  - Notas: `<atualizações recentes aqui>`

<!--
Modelo para novos itens em progresso:
- [ ] **Título da tarefa**
  - Responsável:
  - Progresso: `▓░░░░░░░░░` 10%
  - Notas:
-->

</br>

---

## 🟢 Finalizado (1/5)

- [x] **---**
  - Concluído em: `<data>`
  - Responsável: `<nome>`

<!--
Modelo:
- [x] **Título da tarefa**
  - Concluído em:
  - Responsável:
-->

</br>

---

## 🔴 Para Revisar (0/5)

<!-- Itens aguardando revisão de outra pessoa antes de ir para "Finalizado" -->

- [ ] **`<tarefa aguardando revisão>`**
  - Autor: `<nome>`
  - Revisor: `<nome>`

</br>

----------------------------------------------


# Semana 3   
## 🟡 Planejamento </br> — Modelo final + integração real

> **Meta Geral:** modelo final escolhido e serializado + API consumindo o modelo de verdade (não mais mock).
> Entregável da semana: modelo serializado e versionado no repositório + API consumindo o modelo real, sem mock.  


⚠️ Ponto de atenção: esta é a semana indica ser mais arriscada — se o contrato de dados da S1 der problema, a integração trava aqui. Façam um check-in entre DS ↔ BE no meio da semana (ex: terça) para validar que o formato de entrada/saída bate exatamente com o que o modelo espera e retorna.

</br>

- [ ] **DSx**
  - Comparar modelos: Random Forest e Árvore de Decisão contra o baseline (Regressão Logística)
    
- [ ] **DSx**
  - Ajuste de hiperparâmetros e seleção do modelo final (critério: melhor F1-score, com atenção a overfitting dado que o dataset é pequeno/simulado)
    
- [ ] **DSx**
  - Serializar o modelo treinado (joblib/pickle, ou converter conforme a decisão de arquitetura da S2)
    
- [ ] **DSx**
  - Começar a lógica de recomendações baseada em regras por categoria (não precisa ser ML — pode ser regra condicional simples, o edital aceita)
    
    </br>

---

## 🔵 Em Progresso (/)

- [ ] **Colar o que está sendo feito (Planejamento)**
  - Responsável: `<DSX>`
  - Progresso: `▓▓▓▓▓▓░░░░` 60%
  - Notas: `<atualizações recentes aqui>`

<!--
Modelo para novos itens em progresso:
- [ ] **Título da tarefa**
  - Responsável:
  - Progresso: `▓░░░░░░░░░` 10%
  - Notas:
-->

</br>

---

## 🟢 Finalizado (1/5)

- [x] **---**
  - Concluído em: `<data>`
  - Responsável: `<nome>`

<!--
Modelo:
- [x] **Título da tarefa**
  - Concluído em:
  - Responsável:
-->

</br>

---

## 🔴 Para Revisar (0/5)

<!-- Itens aguardando revisão de outra pessoa antes de ir para "Finalizado" -->

- [ ] **`<tarefa aguardando revisão>`**
  - Autor: `<nome>`
  - Revisor: `<nome>`

</br>

----------------------------------------------



# Semana 4 
## 🟡 Planejamento </br> — Recomendações, custo financeiro e OCI (fechamento do MVP)

> **Meta Geral:**  MVP completo obrigatório já rodando e implantado na OCI.
> Entregável da semana: 🎯 MVP completo — classificação + recomendações + custo estimado + integração OCI funcionando de ponta a ponta, acessível publicamente (ou pelo menos demonstrável).

</br>

- [ ] **DSx**
  - Finalizar lógica de recomendações — mensagens específicas por categoria, seguindo o padrão do edital (ex: "Reduzir uso em horário de pico", "Avaliar aparelhos de alto consumo")
    
- [ ] **DSx**
  - Validar as recomendações com no mínimo 3 exemplos reais/simulados (exigência explícita do edital — não pode entregar com menos)
    
</br>
</br>


---

## 🔵 Em Progresso (/)

- [ ] **Colar o que está sendo feito (Planejamento)**
  - Responsável: `<DSX>`
  - Progresso: `▓▓▓▓▓▓░░░░` 60%
  - Notas: `<atualizações recentes aqui>`

<!--
Modelo para novos itens em progresso:
- [ ] **Título da tarefa**
  - Responsável:
  - Progresso: `▓░░░░░░░░░` 10%
  - Notas:
-->

</br>

---

## 🟢 Finalizado (1/5)

- [x] **---**
  - Concluído em: `<data>`
  - Responsável: `<nome>`

<!--
Modelo:
- [x] **Título da tarefa**
  - Concluído em:
  - Responsável:
-->

</br>

---

## 🔴 Para Revisar (0/5)

<!-- Itens aguardando revisão de outra pessoa antes de ir para "Finalizado" -->

- [ ] **`<tarefa aguardando revisão>`**
  - Autor: `<nome>`
  - Revisor: `<nome>`

</br>

----------------------------------------------



# Semana 5
## 🟡 Planejamento </br> — estes, documentação, opcional, apresentação

> **Meta Geral:** projeto testado, documentado, com os 4 entregáveis da plataforma preenchidos e pitch pronto.
> Entregável da semana: 🎯 MVP completo — classificação + recomendações + custo estimado + integração OCI funcionando de ponta a ponta, acessível publicamente (ou pelo menos demonstrável).

</br>

**Todos**

- [ ] **DSx**
  - Revisar tratamento de erros e casos-limite (valores negativos, tipo_imovel inválido, campos ausentes)
    
- [ ] **DSx**
  - Testes de ponta a ponta com os 3+ exemplos obrigatórios
     
- [ ] **DSx**
  - Documentar endpoints via Swagger (garantir que está acessível/publicado)
        
- [ ] **DSx**
  - Documentar o notebook de Data Science: EDA → limpeza → treino → avaliação → serialização, com texto explicando decisões
        
- [ ] **DSx**
  - Escolher 1 opcional viável dado o tempo apertado — sugestão mais barata: Docker (BE) ou visualizações gráficas no notebook (DS)
        
- [ ] **DSx**
  - Ajustes finais de bugs
        
- [ ] **DSx**
  - Revisar README do repositório: arquitetura, como rodar localmente, decisões técnicas tomadas (inclusive a de integração DS↔BE da S2/S3)

- [ ] **DSx**
  - Preparar roteiro do pitch/demo + gravar vídeo
  
  - [ ] Ensaiar apresentação

## Preencher os 4 entregáveis oficiais na plataforma (obrigatórios para avaliação) </br>

*: Documentação do projeto em Markdown (visão geral, tecnologias, arquitetura, como rodar) 
* Link do YouTube com o vídeo demo
* Selecionar as ferramentas/tecnologias usadas (Python, Java, Spring Boot, OCI, etc.)
* Links do projeto (repositório Github, API publicada, notebook)

  
     **Etc, ajustaremos ao longo do caminho..
    
    
</br>
</br>


---

## 🔵 Em Progresso (/)

- [ ] **Colar o que está sendo feito (Planejamento)**
  - Responsável: `<DSX>`
  - Progresso: `▓▓▓▓▓▓░░░░` 60%
  - Notas: `<atualizações recentes aqui>`

<!--
Modelo para novos itens em progresso:
- [ ] **Título da tarefa**
  - Responsável:
  - Progresso: `▓░░░░░░░░░` 10%
  - Notas:
-->

</br>

---

## 🟢 Finalizado (1/5)

- [x] **---**
  - Concluído em: `<data>`
  - Responsável: `<nome>`

<!--
Modelo:
- [x] **Título da tarefa**
  - Concluído em:
  - Responsável:
-->

</br>

---

## 🔴 Para Revisar (0/5)

<!-- Itens aguardando revisão de outra pessoa antes de ir para "Finalizado" -->

- [ ] **`<tarefa aguardando revisão>`**
  - Autor: `<nome>`
  - Revisor: `<nome>`

