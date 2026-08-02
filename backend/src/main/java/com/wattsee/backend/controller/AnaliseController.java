package com.wattsee.backend.controller;

import com.wattsee.backend.dto.request.AnaliseRequest;
import com.wattsee.backend.dto.response.AnaliseResponse;
import com.wattsee.backend.exception.ValorInvalidoException;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.UUID;


@RestController
@RequestMapping("/api/v1/analise-energetica")
public class AnaliseController {

    private static final double TARIFA_KWH = 0.75;

    @PostMapping
    public ResponseEntity<AnaliseResponse> analisar(@Valid @RequestBody AnaliseRequest request){
        double custoEstimado = request.consumoKwh() * TARIFA_KWH;

        String id = UUID.randomUUID().toString();

        AnaliseResponse mock = new AnaliseResponse(
                id,
                "Eficiente",
                0.96,
                List.of(
                        "Continue mantendo hábitos de consumo consciente.",
                        "Realize manutenção periódica dos equipamentos.",
                        "Considere instalar painéis solares para aumentar a economia."
                ),
                custoEstimado
        );
        return ResponseEntity.ok(mock);
    }

}
