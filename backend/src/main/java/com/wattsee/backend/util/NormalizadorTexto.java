package com.wattsee.backend.util;

import java.text.Normalizer;

public final class NormalizadorTexto {

    private NormalizadorTexto() {}

    public static String removerAcentosEMaiusculizar(String texto) {
        if (texto == null) {
            return null;
        }
        String semAcento = Normalizer.normalize(texto.trim(), Normalizer.Form.NFD)
                .replaceAll("\\p{M}", "");
        return semAcento.toUpperCase();
    }
}