<div align="center">

# ⚡ Análise Inteligente de Consumo de Energia Elétrica

### Hackathon ONE – Projetos G9 | Alura + Oracle

[![Site do Projeto](https://img.shields.io/badge/Site-Projetos%20Hackathon-blue?style=for-the-badge)](https://alura-es-cursos.github.io/projetos-hackathon-g9-brasil/)
[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=for-the-badge)]()
[![Licença](https://img.shields.io/badge/licença-MVP%20Hackathon-lightgrey?style=for-the-badge)]()

</div>

---

## 📌 Sobre o Projeto

<div align="center">

Uma solução inteligente capaz de **analisar padrões de consumo de energia elétrica** e gerar informações que auxiliem na tomada de decisões relacionadas à **eficiência energética**.

</div>

A aplicação recebe dados de consumo de uma residência ou pequeno estabelecimento — como consumo mensal em kWh, horários de maior utilização, quantidade de equipamentos e perfil de uso dos ambientes — e, utilizando técnicas de **Ciência de Dados**, classifica o perfil energético em categorias definidas pela equipe:

- 🟢 **Eficiente**
- 🟡 **Moderado**
- 🔴 **Ineficiente**

Além da classificação, a solução fornece **recomendações personalizadas** para redução de desperdício e adoção de hábitos mais sustentáveis, e estima o **impacto financeiro** do consumo com base em uma tarifa de referência.

---

## 🎯 Necessidade do Cliente

Muitas pessoas recebem contas de energia elevadas, mas possuem pouca visibilidade sobre os hábitos que mais impactam seus gastos. A solução permite:

- ✅ Entender o perfil de consumo energético
- ✅ Identificar possíveis desperdícios
- ✅ Receber recomendações de melhoria
- ✅ Estimar custos associados ao consumo
- ✅ Acompanhar indicadores de eficiência ao longo do tempo

O objetivo é transformar dados de consumo em **informações claras e úteis** para apoiar decisões mais conscientes.

---

## 📈 Validação de Mercado

A preocupação com eficiência energética e sustentabilidade cresce continuamente em diferentes setores da sociedade. Empresas, governos e consumidores buscam soluções capazes de:

- Reduzir custos operacionais
- Melhorar indicadores de sustentabilidade
- Incentivar o consumo consciente
- Monitorar padrões de utilização de energia
- Apoiar estratégias de eficiência energética

---

## 🏆 Objetivo do Hackathon

Desenvolver um **MVP funcional** capaz de:

1. Analisar padrões de consumo energético
2. Classificar perfis de eficiência energética
3. Gerar recomendações de melhoria
4. Estimar impactos financeiros com base em uma tarifa de referência
5. Disponibilizar os resultados por meio de uma **API REST**
6. Utilizar pelo menos **um serviço OCI** como parte da arquitetura da solução

---

## 🛠️ Resultados Esperados

<div align="center">

### 🧪 Ciência de Dados

</div>

Notebook contendo:

- Exploração e limpeza dos dados (EDA)
- Análise de padrões de consumo
- Tratamento e transformação de variáveis
- Treinamento de modelos supervisionados
- Avaliação utilizando métricas adequadas
- Geração de recomendações baseadas em regras ou modelos
- Serialização do modelo treinado

<div align="center">

### 🔗 Back-End

</div>

API REST contendo:

- Endpoint para análise do consumo
- Endpoint para consulta de resultados
- Validação de entrada
- Tratamento de erros
- Documentação dos endpoints

<div align="center">

### ☁️ OCI (Oracle Cloud Infrastructure)

</div>

Utilização de pelo menos um dos seguintes serviços:

- **Object Storage** – armazenamento de modelos ou dados
- **OCI Compute** – hospedagem da API
- **OCI Functions** – processamento específico
- **Banco de dados** (opcional) – persistência

---

## 🚀 Funcionalidades Obrigatórias (MVP)

### 1. Análise do Perfil Energético

`POST /analise-energetica`

**Entrada:**

```json
{
  "consumo_kwh": 420,
  "uso_horario_pico": true,
  "quantidade_equipamentos": 10,
  "tipo_imovel": "Casa",
  "horas_alto_consumo": 8
}
```

**Saída:**

```json
{
  "categoria": "Ineficiente",
  "probabilidade": 0.81
}
```

### 2. Recomendações de Otimização

**Saída complementar:**

```json
{
  "recomendacoes": [
    "Reduzir o uso de equipamentos durante horários de pico",
    "Avaliar aparelhos com alto consumo energético",
    "Distribuir atividades de maior consumo ao longo do dia"
  ]
}
```

### 3. Estimativa Financeira

Utilizando a tarifa de referência sugerida de **R$ 0,75/kWh**:

```json
{
  "custo_estimado_mensal": 315.00
}
```

---

## ✅ Requisitos Mínimos

- [ ] Modelo treinado e carregado corretamente
- [ ] Classificação funcional
- [ ] Geração de recomendações
- [ ] Estimativa de custo energético
- [ ] API documentada
- [ ] Integração com OCI
- [ ] Mínimo de três exemplos reais ou simulados de utilização

---

## ✨ Recursos Opcionais

<div align="center">

| Recurso | Descrição |
|---|---|
| 📊 Dashboard de acompanhamento | Visualização consolidada dos resultados |
| 🕓 Histórico de análises | Registro das análises realizadas |
| 📁 Processamento em lote via CSV | Análise de múltiplos registros de uma vez |
| 🐳 Containerização com Docker | Empacotamento da aplicação |
| 🧪 Testes automatizados | Garantia de qualidade do código |
| 🚨 Alertas de alto consumo | Notificações de consumo elevado |
| 📈 Visualizações gráficas | Gráficos de consumo e eficiência |
| 🔁 Comparação entre períodos | Análise comparativa de consumo |
| 🏅 Ranking de eficiência energética | Classificação entre perfis analisados |
| 🎛️ Simulação de cenários de economia | Projeções de economia de energia |

</div>

---

## 📚 Diretrizes para Ciência de Dados

Cada equipe deverá construir sua própria base de dados relacionada ao consumo energético, podendo ser:

- Coletados em fontes públicas
- Obtidos em bases abertas
- Gerados manualmente pela equipe
- Simulados para representar diferentes perfis de consumo

**Tecnologias recomendadas:**

<div align="center">

`Python` • `Pandas` • `Scikit-Learn` • `Regressão Logística` • `Random Forest` • `Árvores de Decisão`

</div>

> A utilização de outros modelos é permitida. As equipes deverão definir e justificar os critérios utilizados para caracterizar os diferentes perfis de eficiência energética.

---

## 🔧 Diretrizes para Back-End

A solução deverá disponibilizar uma API REST desenvolvida preferencialmente em **Java com Spring Boot**.

A API deverá:

- Receber os dados de consumo
- Executar a análise
- Retornar classificação, probabilidade e recomendações
- Disponibilizar respostas em formato JSON
- Implementar validações e tratamento de erros

> A arquitetura escolhida deverá ser documentada pela equipe.

---

## ☁️ OCI

A solução deve utilizar pelo menos um serviço OCI como parte obrigatória do projeto:

- **Object Storage** – armazenamento de modelos ou arquivos
- **OCI Compute** – implantação da API
- **OCI Functions** – processamento complementar
- **Banco de dados** (opcional) – persistência

---

## 🎨 Front-End (Opcional)

Opcionalmente, a equipe poderá desenvolver uma interface simples para:

- Inserção de informações de consumo
- Visualização dos resultados da análise
- Exibição de recomendações
- Apresentação de gráficos e indicadores

> O desenvolvimento de front-end não é obrigatório para o MVP.

---

<div align="center">

### 🔗 Links Úteis

[Site do Projeto](https://alura-es-cursos.github.io/projetos-hackathon-g9-brasil/)

**Hackathon ONE – Alura + Oracle**

</div>
