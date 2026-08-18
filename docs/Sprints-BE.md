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

---

## 4) Entregáveis da Semana 3
**Responsável:** João Medeiros

Nesta semana foram realizadas atualizações importantes na integração com o microsserviço de modelo, no tratamento de erros e na configuração do ambiente de desenvolvimento.

### a) `ModelServiceClient.java`
O cliente responsável por consumir o microsserviço de análise foi ajustado para realizar a chamada ao endpoint `/predict` usando `RestClient`.

- Envio do objeto `AnaliseRequest` para o serviço de modelo;
- Desserialização da resposta em `RespostaModelo`;
- Tratamento de falha de conexão com captura de `ResourceAccessException`;
- Lançamento da exceção customizada `ServicoIndisponivelException` quando o serviço estiver indisponível.

**Objetivo entregue:** centralizar a integração com o serviço de modelo e melhorar a tratativa de indisponibilidade.

### b) `ModelServiceConfig.java`
Foi configurado o `RestClient` dedicado ao microsserviço de modelo.

- Leitura da base URL via propriedade `model-service.url`;
- Configuração de `SimpleClientHttpRequestFactory`;
- Definição de timeout de conexão de 3 segundos;
- Definição de timeout de leitura de 5 segundos.

**Objetivo entregue:** tornar a comunicação com o microsserviço mais controlada e configurável.

### c) `AnaliseController.java`
O controller da análise energética foi atualizado para consumir a resposta do microsserviço de modelo e montar a resposta final da API.

- Endpoint `POST /api/v1/analise-energetica`;
- Recebimento de `AnaliseRequest` validado com `@Valid`;
- Chamada ao `ModelServiceClient` para obter a classificação do modelo;
- Cálculo do custo estimado com base na tarifa fixa `TARIFA_KWH = 0.75`;
- Retorno de `AnaliseResponse` com:
    - categoria;
    - probabilidade;
    - recomendações;
    - custo estimado.

**Objetivo entregue:** integrar a API principal ao resultado do modelo de análise energética.

### d) `RespostaModelo.java`
Foi definido o DTO de integração que representa a resposta recebida do microsserviço de modelo.

- Campos:
    - `categoria`
    - `probabilidade`
    - `recomendacoes`
- Uso de `@JsonProperty` para garantir compatibilidade na desserialização JSON.

**Objetivo entregue:** padronizar o contrato de resposta entre os serviços.

### e) `GlobalExceptionHandler.java`
O tratamento global de exceções foi ampliado para cobrir falhas de comunicação com o microsserviço.

- Mantido o tratamento de:
    - `MethodArgumentNotValidException`;
    - `HttpMessageNotReadableException`;
    - `ValorInvalidoException`;
    - `Exception` genérica.
- Adicionado tratamento para `ServicoIndisponivelException`;
- Resposta com status `503 Service Unavailable` quando o serviço de análise não estiver acessível.

**Objetivo entregue:** melhorar a robustez da API e informar corretamente indisponibilidade externa.

### f) `ServicoIndisponivelException.java`
Foi criada a exceção customizada para representar indisponibilidade do serviço de modelo.

- Classe estende `RuntimeException`;
- Usada para sinalizar falhas de comunicação com o microsserviço.

**Objetivo entregue:** permitir tratamento semântico e centralizado de falhas externas.

### g) `application-dev.yml`
A configuração de desenvolvimento foi atualizada para suportar a integração com o serviço de modelo.

- Definição de `ml.service.url` com fallback para `http://localhost:8000`;
- Inclusão de `ml.service.timeout`;
- Configuração de `model-service.url` apontando para `http://localhost:9999` em ambiente local de testes;
- Comentário com URL alternativa de mock.

**Objetivo entregue:** facilitar testes locais e a troca da base URL do microsserviço em desenvolvimento.

## Resultado da Semana 3
Os entregáveis da semana 3 consolidaram a integração da API backend com o microsserviço de modelo, incluindo:

- cliente HTTP dedicado ao serviço de análise;
- configuração de conexão com timeout;
- atualização do controller para consumir a resposta do modelo;
- DTO de integração para resposta do microsserviço;
- tratamento específico para indisponibilidade do serviço;
- ajustes no ambiente de desenvolvimento.