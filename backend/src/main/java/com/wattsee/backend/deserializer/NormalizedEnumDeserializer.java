package com.wattsee.backend.deserializer;

import tools.jackson.core.JsonParser;
import tools.jackson.databind.DeserializationContext;
import tools.jackson.databind.ValueDeserializer;
import com.wattsee.backend.util.NormalizadorTexto;

public class NormalizedEnumDeserializer<T extends Enum<T>> extends ValueDeserializer<T> {

    private final Class<T> tipoDoEnum;

    public NormalizedEnumDeserializer(Class<T> tipoDoEnum) {
        this.tipoDoEnum = tipoDoEnum;
    }

    @Override
    public T deserialize(JsonParser parser, DeserializationContext contexto) {
        String valor = parser.getText();
        String normalizado = NormalizadorTexto.removerAcentosEMaiusculizar(valor);
        return Enum.valueOf(tipoDoEnum, normalizado);
    }
}