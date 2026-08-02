package com.wattsee.backend.exception;

import com.wattsee.backend.dto.response.ErrorResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {

        FieldError fieldError = ex.getBindingResult().getFieldError();

        if (fieldError == null) {
            return ResponseEntity.badRequest().body(
                    new ErrorResponse("JSON inválido", 400, null)
            );
        }

        String campo = fieldError.getField();
        String mensagem = fieldError.getDefaultMessage();
        String codigo = fieldError.getCode();

        boolean unprocessable =
                        "Positive".equals(codigo) ||
                        "PositiveOrZero".equals(codigo) ||
                        "DecimalMin".equals(codigo) ||
                        "DecimalMax".equals(codigo) ||
                        "Min".equals(codigo) ||
                        "Max".equals(codigo);

        int status = unprocessable ? 422 : 400;

        ErrorResponse erro = new ErrorResponse(mensagem, status, campo);
        return ResponseEntity.status(status).body(erro);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleJsonInvalido(HttpMessageNotReadableException ex) {

        String mensagem = ex.getMostSpecificCause().getMessage();

        if (mensagem != null && mensagem.contains("tipo_imovel")) {
            return ResponseEntity.unprocessableEntity().body(
                    new ErrorResponse(
                            "tipo_imovel deve ser um dos seguintes valores: Casa, Apartamento, Comércio",
                            422,
                            "tipo_imovel"
                    )
            );
        }

        return ResponseEntity.badRequest().body(
                new ErrorResponse(
                        "JSON inválido",
                        400,
                        null
                )
        );
    }

    @ExceptionHandler(ValorInvalidoException.class)
    public ResponseEntity<ErrorResponse> handleValorInvalido(ValorInvalidoException ex) {

        ErrorResponse erro = new ErrorResponse(
                ex.getMessage(),
                422,
                ex.getCampo()
        );

        return ResponseEntity.unprocessableEntity().body(erro);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGenerico(Exception ex) {

        ErrorResponse erro = new ErrorResponse(
                "Erro interno do servidor",
                500,
                null
        );

        return ResponseEntity.internalServerError().body(erro);
    }

    @ExceptionHandler(ServicoIndisponivelException.class)
    public ResponseEntity<ErrorResponse> handleServicoIndisponivel(ServicoIndisponivelException ex){
        ErrorResponse erro = new ErrorResponse(ex.getMessage(), 503, null);
        return ResponseEntity.status(503).body(erro);
    }
}