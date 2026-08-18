package com.wattsee.backend.exception;

public class ValorInvalidoException extends RuntimeException {

    private final String campo;

    public ValorInvalidoException(String mensagem, String campo) {
        super(mensagem);
        this.campo = campo;
    }

    public String getCampo() {
        return campo;
    }
}