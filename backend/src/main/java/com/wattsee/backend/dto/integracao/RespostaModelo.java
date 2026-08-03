package com.wattsee.backend.dto.integracao;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

public record RespostaModelo(
        @JsonProperty("categoria")
        String categoria,
        @JsonProperty("probabilidade")
        Double probabilidade,
        @JsonProperty("recomendacoes")
        List<String> recomendacoes
) {
}
