"""Pruebas de evaluar_impacto_kpi, sin modelo ni servidor."""
import json

import pytest

from src.agente_paulina.herramientas import evaluar_impacto_kpi


def evaluar(**datos):
    return json.loads(evaluar_impacto_kpi.invoke(datos))


def test_mermas_que_bajan_son_mejora_y_se_monetizan():
    resultado = evaluar(
        kpi="mermas",
        linea_base=100,
        valor_esperado=80,
        unidad="kg",
        mejor_si="menor",
        valor_unitario_clp=500,
    )
    assert resultado["variacion_absoluta"] == -20.0
    assert resultado["variacion_pct"] == -20.0
    assert resultado["es_mejora"] is True
    assert resultado["es_empeoramiento"] is False
    assert resultado["impacto_clp"] == 10000.0


def test_tiempos_que_bajan_sin_valor_unitario_no_traen_clp():
    resultado = evaluar(
        kpi="tiempo de proceso",
        linea_base=120,
        valor_esperado=90,
        unidad="minutos",
    )
    assert resultado["variacion_absoluta"] == -30.0
    assert resultado["variacion_pct"] == -25.0
    assert resultado["es_mejora"] is True
    assert "impacto_clp" not in resultado
    assert "moneda" not in resultado


def test_satisfaccion_que_sube_es_mejora_con_valor_unitario():
    resultado = evaluar(
        kpi="satisfacción",
        linea_base=70,
        valor_esperado=80,
        unidad="puntos",
        mejor_si="mayor",
        valor_unitario_clp=1000,
    )
    assert resultado["variacion_absoluta"] == 10.0
    assert resultado["variacion_pct"] == 14.29
    assert resultado["es_mejora"] is True
    assert resultado["impacto_clp"] == 10000.0


def test_satisfaccion_que_baja_es_empeoramiento_y_clp_negativo():
    resultado = evaluar(
        kpi="satisfacción",
        linea_base=80,
        valor_esperado=70,
        unidad="puntos",
        mejor_si="mayor",
        valor_unitario_clp=1000,
    )
    assert resultado["es_empeoramiento"] is True
    assert resultado["impacto_clp"] == -10000.0


def test_sin_cambio():
    resultado = evaluar(
        kpi="errores",
        linea_base=5,
        valor_esperado=5,
        unidad="errores",
    )
    assert resultado["variacion_absoluta"] == 0.0
    assert resultado["variacion_pct"] == 0.0
    assert resultado["es_mejora"] is False
    assert resultado["es_empeoramiento"] is False
    assert resultado["sin_cambio"] is True


def test_direccion_acepta_mayusculas():
    resultado = evaluar(
        kpi="conversión",
        linea_base=10,
        valor_esperado=12,
        unidad="%",
        mejor_si="MAYOR",
    )
    assert resultado["mejor_si"] == "mayor"
    assert resultado["es_mejora"] is True


def test_conversion_fraccionaria_conserva_precision():
    resultado = evaluar(
        kpi="conversión",
        linea_base=0.025,
        valor_esperado=0.0255,
        unidad="fracción",
        mejor_si="mayor",
    )
    assert resultado["linea_base"] == 0.025
    assert resultado["valor_esperado"] == 0.0255
    assert resultado["variacion_absoluta"] == 0.0005
    assert resultado["variacion_pct"] == 2.0
    assert "0.0255" in resultado["conclusion"]


@pytest.mark.parametrize(
    "datos",
    [
        {"kpi": "", "linea_base": 10, "valor_esperado": 8, "unidad": "%"},
        {"kpi": "mermas", "linea_base": 0, "valor_esperado": 0, "unidad": "%"},
        {"kpi": "mermas", "linea_base": 10, "valor_esperado": 8, "unidad": ""},
        {"kpi": "mermas", "linea_base": "10", "valor_esperado": 8, "unidad": "%"},
        {"kpi": "mermas", "linea_base": 10, "valor_esperado": None, "unidad": "%"},
        {"kpi": "mermas", "linea_base": 10, "valor_esperado": 8, "unidad": "%", "mejor_si": "igual"},
        {"kpi": "mermas", "linea_base": 10, "valor_esperado": 8, "unidad": "%", "valor_unitario_clp": 0},
        {"kpi": "mermas", "linea_base": 10, "valor_esperado": 8, "unidad": "%", "valor_unitario_clp": -5},
    ],
)
def test_entradas_invalidas_devuelven_error(datos):
    resultado = json.loads(evaluar_impacto_kpi.func(**datos))
    assert "error" in resultado
