package com.wattsee.backend.client;

import com.wattsee.backend.dto.integracao.RespostaModelo;
import com.wattsee.backend.dto.request.AnaliseRequest;
import com.wattsee.backend.exception.ServicoIndisponivelException;
import org.springframework.stereotype.Component;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

@Component
public class ModelServiceClient {

    private final RestClient restClient;

    public ModelServiceClient(RestClient modelServiceRestClient) {
        this.restClient = modelServiceRestClient;
    }

    public RespostaModelo analisar(AnaliseRequest request) {
        try {
            return restClient.post()
                    .uri("/predict")
                    .body(request)
                    .retrieve()
                    .body(RespostaModelo.class);
        } catch (ResourceAccessException exception){
            throw new ServicoIndisponivelException("Serviço de analise indisponivel no momento");
        }
    }

}