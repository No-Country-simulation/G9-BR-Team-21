package com.wattsee.backend.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.wattsee.backend.enums.TipoImovel;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

public record AnaliseRequest(

        @NotNull(message = "Campo consumo_kwh é obrigatório")
        @DecimalMin(value = "0", inclusive = false, message = "O consumo_kwh deve ser maior que zero")
        @JsonProperty("consumo_kwh")
        Double consumoKwh,

        @NotNull(message = "Campo uso_horario_pico é obrigatório")
        @JsonProperty("uso_horario_pico")
        Boolean usoHorarioPico,

        @NotNull(message = "Campo quantidade_equipamentos é obrigatório")
        @Positive(message = "quantidade_equipamentos deve ser maior que zero")
        @JsonProperty("quantidade_equipamentos")
        Integer quantidadeEquipamentos,

        @NotNull(message = "Campo tipo_imovel é obrigatório")
        @JsonProperty("tipo_imovel")
        TipoImovel tipoImovel,

        @NotNull(message = "Campo horas_alto_consumo é obrigatório")
        @Positive(message = "horas_alto_consumo deve ser maior que zero")
        @Max(value = 24, message = "horas_alto_consumo não pode ultrapassar 24")
        @JsonProperty("horas_alto_consumo")
        Integer horasAltoConsumo
) {}
