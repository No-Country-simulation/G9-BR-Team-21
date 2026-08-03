package com.wattsee.backend.exception;

public class ServicoIndisponivelException  extends RuntimeException{
    public ServicoIndisponivelException(String mensagem){
        super(mensagem);
    }
}
