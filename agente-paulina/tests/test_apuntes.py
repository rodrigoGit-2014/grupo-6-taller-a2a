"""Pruebas de consultar_mis_apuntes: temas, mayúsculas y sinónimos simples."""
import json

import pytest

from src.agente_paulina.herramientas import consultar_mis_apuntes


@pytest.mark.parametrize(
    "tema",
    ["CASO", "Caso de negocio", "  caso   de   negocio  ", "caso de uso", "Casos"],
)
def test_consulta_el_caso_con_mayusculas_y_sinonimos(tema):
    resultado = json.loads(consultar_mis_apuntes.invoke({"tema": tema}))
    assert "caso" in resultado
    assert "CASO FICTICIO" in resultado["caso"]


@pytest.mark.parametrize(
    ("tema", "clave"),
    [("CONCEPTOS", "conceptos"), ("Concepto", "conceptos"), ("Criterio", "criterios")],
)
def test_consulta_temas_validos_con_mayusculas(tema, clave):
    resultado = json.loads(consultar_mis_apuntes.invoke({"tema": tema}))
    assert clave in resultado


def test_tema_desconocido_devuelve_error():
    resultado = json.loads(consultar_mis_apuntes.invoke({"tema": "otro"}))
    assert "error" in resultado
