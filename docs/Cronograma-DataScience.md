# 🗂️ Board de Planejamento

> Este arquivo funciona como um Kanban simples dentro do repositório. </br>
> ## 🧭 Como usar:
> Para mover um item de coluna (Planejamento > Em progresso > Revisão...), **só copiar o bloco e colar na seção de destino**, depois atualize os contadores da tabela abaixo.
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

  - Prazo: `<data>`
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

---

## 🔴 Para Revisar (0/5)

<!-- Itens aguardando revisão de outra pessoa antes de ir para "Finalizado" -->

- [ ] **`<tarefa aguardando revisão>`**
  - Autor: `<nome>`
  - Revisor: `<nome>`


----------------------------------------------



## Semana 2 — ...


**Meta da sprint:** 
Se preferir manter só como arquivo interno (sem virar site), basta deixá-lo na raiz do repo ou em `/docs`, `/planejamento` etc. — ele já renderiza bonito ao abrir direto no GitHub.
