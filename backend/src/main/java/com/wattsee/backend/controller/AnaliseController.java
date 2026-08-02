package com.wattsee.backend.controller;

import com.wattsee.backend.client.ModelServiceClient;
import com.wattsee.backend.dto.integracao.RespostaModelo;
import com.wattsee.backend.dto.request.AnaliseRequest;
import com.wattsee.backend.dto.response.AnaliseResponse;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/analise-energetica")
public class AnaliseController {

    // TESTE DO CONTROLER ACESSANDO UMA FALSA REQUISIÇÃO, POIS AINDA NÃO HÁ O MICROSSERVIÇO COMPLETO
    private static final double TARIFA_KWH = 0.75;
    private final ModelServiceClient modelServiceClient;

    public AnaliseController(ModelServiceClient modelServiceClient){
        this.modelServiceClient = modelServiceClient;
    }

    @PostMapping
    public ResponseEntity<AnaliseResponse> analisar(@Valid @RequestBody AnaliseRequest request){

        RespostaModelo respostaModelo = modelServiceClient.analisar(request);
        double custoEstimado = request.consumoKwh() * TARIFA_KWH;

        AnaliseResponse resposta = new AnaliseResponse(
                respostaModelo.categoria(),
                respostaModelo.probabilidade(),
                respostaModelo.recomendacoes(),
                custoEstimado
        );
        return ResponseEntity.ok(resposta);
    }

}
