package com.wattsee.backend.config;

import com.wattsee.backend.deserializer.NormalizedEnumDeserializer;
import com.wattsee.backend.enums.TipoImovel;
import org.springframework.boot.jackson.autoconfigure.JsonMapperBuilderCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import tools.jackson.databind.module.SimpleModule;

@Configuration
public class EnumConfig {

    @Bean
    public JsonMapperBuilderCustomizer enumNormalizado() {
        SimpleModule modulo = new SimpleModule();
        modulo.addDeserializer(TipoImovel.class, new NormalizedEnumDeserializer<>(TipoImovel.class));

        return builder -> builder.addModule(modulo);
    }
}