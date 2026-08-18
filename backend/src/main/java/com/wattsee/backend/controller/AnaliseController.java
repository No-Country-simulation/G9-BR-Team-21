package com.wattsee.backend.controller;

import com.wattsee.backend.client.ModelServiceClient;
import com.wattsee.backend.dto.integracao.RespostaModelo;
import com.wattsee.backend.dto.request.AnaliseRequest;
import com.wattsee.backend.dto.response.AnaliseResponse;
import com.wattsee.backend.exception.AnaliseNaoEncontradaException;
import com.wattsee.backend.repository.ResultadoRepository;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;


@RestController
@RequestMapping("/api/v1/analise-energetica")
public class AnaliseController {

    // TESTE DO CONTROLER ACESSANDO UMA FALSA REQUISIÇÃO, POIS AINDA NÃO HÁ O MICROSSERVIÇO COMPLETO
    private static final double TARIFA_KWH = 0.75;
    private final ModelServiceClient modelServiceClient;
    private final ResultadoRepository resultadoRepository;

    public AnaliseController(ModelServiceClient modelServiceClient, ResultadoRepository resultadoRepository) {
        this.modelServiceClient = modelServiceClient;
        this.resultadoRepository = resultadoRepository;
    }

    @PostMapping
    public ResponseEntity<AnaliseResponse> analisar(@Valid @RequestBody AnaliseRequest request) {

        RespostaModelo respostaModelo = modelServiceClient.analisar(request);
        double custoEstimado = request.consumoKwh() * TARIFA_KWH;
        String id = UUID.randomUUID().toString();

        AnaliseResponse resposta = new AnaliseResponse(
                id,
                respostaModelo.categoria(),
                respostaModelo.probabilidade(),
                respostaModelo.recomendacoes(),
                custoEstimado
        );

        resultadoRepository.salvar(id, resposta);
        return ResponseEntity.ok(resposta);
    }

    @GetMapping("/{id}")
    public ResponseEntity<AnaliseResponse> buscarPorId(@PathVariable String id) {
        AnaliseResponse resposta = resultadoRepository.buscarPorId(id)
                .orElseThrow(() -> new AnaliseNaoEncontradaException(id));
        return ResponseEntity.ok(resposta);
    }
}
