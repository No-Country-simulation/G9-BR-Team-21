package com.wattsee.backend.dto.response;

import com.fasterxml.jackson.annotation.JsonProperty;

public record ErrorResponse (

        @JsonProperty("erro")
        String erro,

        @JsonProperty("codigo")
        Integer codigo,

        @JsonProperty("campo")
        String campo

) {}