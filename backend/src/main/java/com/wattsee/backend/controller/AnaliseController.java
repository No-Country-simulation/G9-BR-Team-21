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

@RestController
@RequestMapping("/api/v1/analise-energetica")
public class AnaliseController {

    @PostMapping
    public ResponseEntity<AnaliseResponse> analisar(@Valid @RequestBody AnaliseRequest request){
        if (request.consumoKwh() != null && request.consumoKwh() > 100000) {
            throw new ValorInvalidoException("consumo_kwh excede o limite permitido", "consumo_kwh");
        }
        AnaliseResponse mock = new AnaliseResponse(
                "Eficiente",
                0.96,
                List.of(
                        "Continue mantendo hábitos de consumo consciente.",
                        "Realize manutenção periódica dos equipamentos.",
                        "Considere instalar painéis solares para aumentar a economia."
                ),
                90.00
        );

        return ResponseEntity.ok(mock);
    }

}
