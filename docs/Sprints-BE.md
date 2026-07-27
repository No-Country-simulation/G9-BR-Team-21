# Sprintes BE - Segunda Semana

## Responsável
- **João Medeiros**

## Escopo da Sprint (Backend)
Documentação das implementações realizadas nos arquivos:
- `backend/src/main/java/com/wattsee/backend/controller/AnaliseController.java`
- `backend/src/main/java/com/wattsee/backend/exception/GlobalExceptionHandler.java`
- `backend/src/main/java/com/wattsee/backend/exception/ValorInvalidoException.java`

---

## 1) `AnaliseController.java`
Foi implementado o endpoint de análise energética:

- `@RestController` com rota base `"/api/v1/analise-energetica"`.
- Método `POST` `analisar(@Valid @RequestBody AnaliseRequest request)`.
- Validação de regra de negócio para `consumoKwh`:
    - Se `consumoKwh` for maior que `100000`, lança `ValorInvalidoException` com:
        - mensagem: `"consumo_kwh excede o limite permitido"`
        - campo: `"consumo_kwh"`
- Retorno de `AnaliseResponse` mockado contendo:
    - classificação: `"Eficiente"`
    - score: `0.96`
    - recomendações (lista de 3 itens)
    - economia estimada: `90.00`

**Objetivo entregue:** disponibilizar a estrutura inicial do endpoint com validação de limite de consumo e resposta padronizada.

---

## 2) `GlobalExceptionHandler.java`
Foi centralizado o tratamento global de exceções da API com `@RestControllerAdvice`:

### a) Tratamento de validação (`MethodArgumentNotValidException`)
- Recupera o primeiro `FieldError`.
- Se não houver erro de campo, retorna:
    - mensagem: `"JSON inválido"`
    - status: `400`
- Para erros de campo, classifica status:
    - `422` para violações semânticas/regras de valor (`Positive`, `Min`, `Max`, `DecimalMin`, etc.)
    - `400` para demais erros de requisição
- Retorna `ErrorResponse` com `mensagem`, `status` e `campo`.

### b) JSON malformado (`HttpMessageNotReadableException`)
- Quando a causa menciona `tipo_imovel`, retorna:
    - mensagem orientativa com valores aceitos (`Casa, Apartamento, Comércio`)
    - status: `422`
    - campo: `"tipo_imovel"`
- Caso contrário:
    - mensagem: `"JSON inválido"`
    - status: `400`

### c) Exceção de valor de negócio (`ValorInvalidoException`)
- Retorna `422 Unprocessable Entity` com:
    - mensagem da exceção
    - campo inválido (`ex.getCampo()`)

### d) Tratamento genérico (`Exception`)
- Fallback para erro interno:
    - mensagem: `"Erro interno do servidor"`
    - status: `500`

**Objetivo entregue:** padronização de respostas de erro e melhoria da clareza para clientes da API.

---

## 3) `ValorInvalidoException.java`
Foi criada exceção customizada de domínio:

- Classe estende `RuntimeException`.
- Atributo `campo` para identificar qual entrada é inválida.
- Construtor recebe:
    - `mensagem`
    - `campo`
- Getter `getCampo()` para uso no `GlobalExceptionHandler`.

**Objetivo entregue:** representar violações de regra de negócio com contexto de campo, facilitando retorno HTTP 422 estruturado.

---

## Resultado da Sprint (Semana 2)
A sprint de backend da segunda semana, **realizada por João Medeiros**, entregou:

- Endpoint inicial de análise energética (`POST /api/v1/analise-energetica`);
- Validação de regra de negócio para limite de consumo;
- Exceção customizada para valores inválidos;
- Tratamento global e padronizado de erros (`400`, `422`, `500`) com `ErrorResponse`.