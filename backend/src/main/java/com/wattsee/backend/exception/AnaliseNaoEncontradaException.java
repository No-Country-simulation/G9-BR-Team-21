package com.wattsee.backend.exception;

public class AnaliseNaoEncontradaException extends RuntimeException {
    public AnaliseNaoEncontradaException(String id) {
        super("Análise não encontrada para o id: " + id);
    }
}
