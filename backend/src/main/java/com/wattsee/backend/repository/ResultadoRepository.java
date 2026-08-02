package com.wattsee.backend.repository;


import com.wattsee.backend.dto.response.AnaliseResponse;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Repository
public class ResultadoRepository {

    private final Map<String, AnaliseResponse> armazenamento = new ConcurrentHashMap<>();

    public void salvar(String id, AnaliseResponse response) {
        armazenamento.put(id, response);
    }
    public Optional<AnaliseResponse> buscarPorId(String id) {
        return Optional.ofNullable(armazenamento.get(id));
    }

}
