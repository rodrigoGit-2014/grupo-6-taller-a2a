"""Pruebas de calcular_retorno, sin modelo ni servidor."""
import json

import pytest

from src.agente_paulina.herramientas import calcular_retorno


def calcular(**datos):
    return json.loads(calcular_retorno.invoke(datos))


def test_caso_costo_847000():
    resultado = calcular(costo_total_clp=847000, beneficio_mensual_clp=150000, horizonte_meses=12)
    assert resultado["costo_total_clp"] == 847000
    assert resultado["beneficio_acumulado_clp"] == 1800000
    assert resultado["roi_pct"] == 112.51
    assert resultado["meses_recuperacion"] == 5.65
    assert resultado["recupera_en_horizonte"] is True
    assert resultado["moneda"] == "CLP"


def test_horizonte_por_defecto_es_doce_meses():
    resultado = calcular(costo_total_clp=847000, beneficio_mensual_clp=100000)
    assert resultado["horizonte_meses"] == 12
    assert resultado["beneficio_acumulado_clp"] == 1200000
    assert resultado["roi_pct"] == 41.68
    assert resultado["meses_recuperacion"] == 8.47


def test_punto_de_equilibrio_en_el_horizonte():
    resultado = calcular(costo_total_clp=1200000, beneficio_mensual_clp=100000, horizonte_meses=12)
    assert resultado["roi_pct"] == 0.0
    assert resultado["meses_recuperacion"] == 12.0
    assert resultado["recupera_en_horizonte"] is True


def test_no_se_recupera_en_el_horizonte():
    resultado = calcular(costo_total_clp=1000000, beneficio_mensual_clp=50000, horizonte_meses=12)
    assert resultado["roi_pct"] == -40.0
    assert resultado["meses_recuperacion"] == 20.0
    assert resultado["recupera_en_horizonte"] is False
    assert "no se recupera" in resultado["conclusion"].lower()


def test_beneficio_cero_no_divide_por_cero():
    resultado = calcular(costo_total_clp=847000, beneficio_mensual_clp=0)
    assert resultado["beneficio_acumulado_clp"] == 0
    assert resultado["roi_pct"] == -100.0
    assert resultado["meses_recuperacion"] is None
    assert resultado["recupera_en_horizonte"] is False
    assert "no se recupera" in resultado["conclusion"].lower()


@pytest.mark.parametrize("costo", [0, -1])
def test_costo_invalido(costo):
    assert "error" in calcular(costo_total_clp=costo, beneficio_mensual_clp=100000)


@pytest.mark.parametrize("beneficio", [-1])
def test_beneficio_invalido(beneficio):
    assert "error" in calcular(costo_total_clp=847000, beneficio_mensual_clp=beneficio)


@pytest.mark.parametrize("horizonte", [0, -3])
def test_horizonte_invalido(horizonte):
    assert "error" in calcular(
        costo_total_clp=847000,
        beneficio_mensual_clp=100000,
        horizonte_meses=horizonte,
    )


@pytest.mark.parametrize(
    "datos",
    [
        {"costo_total_clp": 1.5, "beneficio_mensual_clp": 100000},
        {"costo_total_clp": "847000", "beneficio_mensual_clp": 100000},
        {"costo_total_clp": True, "beneficio_mensual_clp": 100000},
        {"costo_total_clp": None, "beneficio_mensual_clp": 100000},
        {"costo_total_clp": 847000, "beneficio_mensual_clp": 1.5},
        {"costo_total_clp": 847000, "beneficio_mensual_clp": "100000"},
        {"costo_total_clp": 847000, "beneficio_mensual_clp": False},
        {"costo_total_clp": 847000, "beneficio_mensual_clp": None},
        {"costo_total_clp": 847000, "beneficio_mensual_clp": 100000, "horizonte_meses": 1.5},
        {"costo_total_clp": 847000, "beneficio_mensual_clp": 100000, "horizonte_meses": "12"},
        {"costo_total_clp": 847000, "beneficio_mensual_clp": 100000, "horizonte_meses": True},
    ],
)
def test_tipos_invalidos_en_la_funcion(datos):
    """La función también valida cuando se llama sin el esquema del modelo."""
    assert "error" in json.loads(calcular_retorno.func(**datos))
