# Tratamento de Erros da API
## Objetivo
Este documento define o padrão de respostas de erro da API do EnergiAI. Todos os endpoints devem seguir a mesma estrutura para facilitar a integração entre front-end, back-end e consumidores da API.
---
## Estrutura padrão da resposta de erro
```json
{
  "erro": "Campo consumo_kwh é obrigatório",
  "codigo": 400,
  "campo": "consumo_kwh"
}
```
### Campos
| Campo    | Tipo          | Descrição                                                                                |
| -------- | ------------- | ---------------------------------------------------------------------------------------- |
| `erro`   | String        | Mensagem descritiva do erro.                                                             |
| `codigo` | Integer       | Código HTTP correspondente ao erro.                                                      |
| `campo`  | String \| null | Campo relacionado ao erro, quando aplicável. Em erros gerais pode ser `null` ou omitido. |
---
# Cenários de erro do MVP
## 1. Campo obrigatório ausente
**Código HTTP:** `400 Bad Request`
**Quando ocorre:**
* Um campo obrigatório não é enviado na requisição.
### Exemplo
```json
{
  "erro": "Campo consumo_kwh é obrigatório",
  "codigo": 400,
  "campo": "consumo_kwh"
}
```
---
## 2. Tipo de dado inválido
**Código HTTP:** `400 Bad Request`
**Quando ocorre:**
* O tipo do valor enviado é diferente do esperado.
* Exemplo: enviar `"abc"` onde é esperado um número.
### Exemplo
```json
{
  "erro": "O campo consumo_kwh deve ser um número",
  "codigo": 400,
  "campo": "consumo_kwh"
}
```
---
## 3. Valor fora da faixa permitida
**Código HTTP:** `422 Unprocessable Entity`
**Quando ocorre:**
* O dado possui o tipo correto, mas viola uma regra de negócio.
* Exemplo: consumo negativo.
### Exemplo
```json
{
  "erro": "O consumo_kwh deve ser maior que zero",
  "codigo": 422,
  "campo": "consumo_kwh"
}
```
---
## 4. Valor de enum inválido (`tipo_imovel`)
**Código HTTP:** `422 Unprocessable Entity`
**Quando ocorre:**
* O campo `tipo_imovel` tem o tipo correto (string), mas o valor enviado não está entre os valores aceitos.
* Exemplo: enviar `"Escritório"` quando os valores válidos são apenas `Casa`, `Apartamento` e `Comércio`.
* Os valores exatos aceitos (grafia, acentuação) devem ser confirmados junto ao time de Data Science antes da implementação.
### Exemplo
```json
{
  "erro": "tipo_imovel deve ser um dos seguintes valores: Casa, Apartamento, Comércio",
  "codigo": 422,
  "campo": "tipo_imovel"
}
```
---
## 5. Serviço de análise indisponível
**Código HTTP:** `503 Service Unavailable`
**Quando ocorre:**
* O model service (Python) não responde à chamada da API — timeout ou conexão recusada.
* Diferente de um erro interno genérico: este cenário indica especificamente que a dependência externa está fora do ar, facilitando o diagnóstico em produção sem precisar consultar logs.
### Exemplo
```json
{
  "erro": "Serviço de análise indisponível no momento",
  "codigo": 503,
  "campo": null
}
```
---
## 6. Erro interno inesperado
**Código HTTP:** `500 Internal Server Error`
**Quando ocorre:**
* Falha inesperada na aplicação.
* Banco de dados indisponível.
* Erros não tratados.
* (Indisponibilidade do serviço de IA passa a ser tratada especificamente pelo cenário 5, com código `503`.)
### Exemplo
```json
{
  "erro": "Erro interno do servidor",
  "codigo": 500,
  "campo": null
}
```
---
# Resumo
| Cenário                          | Código HTTP | Exemplo                                              |
| --------------------------------- | ----------- | ----------------------------------------------------- |
| Campo obrigatório ausente         | **400**     | Campo `consumo_kwh` não enviado                       |
| Tipo de dado inválido             | **400**     | Texto enviado onde é esperado um número                |
| Valor fora da faixa permitida     | **422**     | `consumo_kwh` menor ou igual a zero                    |
| Valor de enum inválido            | **422**     | `tipo_imovel` com valor fora da lista aceita            |
| Serviço de análise indisponível   | **503**     | Model service (Python) fora do ar ou sem resposta       |
| Erro interno inesperado           | **500**     | Falha no banco ou erro não tratado                      |
---
## Observações para implementação
* Todas as respostas de erro devem seguir exatamente a estrutura definida neste documento.
* O campo `campo` deve ser preenchido sempre que o erro estiver relacionado a um atributo específico da requisição.
* Para erros gerais (`500`, `503`), o campo `campo` deve ser `null` (ou pode ser omitido, caso a implementação adote essa convenção).
* A implementação será centralizada por meio de um `@RestControllerAdvice` com `@ExceptionHandler` global no Spring Boot, garantindo consistência em todos os endpoints da API.
* O cenário de `503` deve ser tratado separadamente do `500` genérico na chamada HTTP ao model service (ex: capturando timeout/connection refused de forma específica), para permitir diagnóstico mais rápido em produção.