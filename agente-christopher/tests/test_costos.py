"""Pruebas de cálculos y validaciones, sin servidor ni clave de Gemini."""
import copy
import json
import pytest
from src.agente_christopher.herramientas import calcular_estimacion, comparar_estimaciones, consultar_tarifas

@pytest.fixture
def escenario():
    recursos = [("analisis", 4), ("interfaz", 12), ("logica_datos", 16), ("pruebas", 6), ("despliegue", 3), ("alojamiento", 1), ("dominio", 1), ("equipamiento_no_requerido", 0)]
    return {"nombre": "Aplicación base", "partidas": [{"recurso": r, "cantidad": c} for r, c in recursos], "supuestos": ["Oficina con infraestructura existente; alojamiento 1 mes y dominio 1 año."]}

def test_caso_acordado(escenario):
    resultado = json.loads(calcular_estimacion.invoke(escenario))
    assert resultado["total_clp"] == 847000
    assert resultado["costo_inicial_clp"] == 820000
    assert resultado["servicios_por_periodos_clp"] == 27000
    assert resultado["simulado"] is True
    assert resultado["incluye_iva"] is False
    assert len(resultado["partidas"]) == 8

def test_comparar_conserva_tarifas_y_explica_diferencias(escenario):
    alternativa = copy.deepcopy(escenario)
    alternativa["nombre"] = "Interfaz ampliada"
    alternativa["partidas"][1]["cantidad"] = 20
    r = json.loads(comparar_estimaciones.invoke({"evaluaciones": [escenario, alternativa]}))
    assert r["evaluaciones"][1]["total_clp"] == 1007000
    assert r["comparaciones"][0]["diferencia_total_clp"] == 160000
    assert r["comparaciones"][0]["detalle"][0]["recurso"] == "interfaz"
    assert r["evaluaciones"][0]["partidas"][1]["tarifa_clp"] == r["evaluaciones"][1]["partidas"][1]["tarifa_clp"] == 20000

@pytest.mark.parametrize("cantidad", [-1, "NaN", "Infinity", True, "texto", None])
def test_cantidades_invalidas(escenario, cantidad):
    escenario["partidas"][0]["cantidad"] = cantidad
    assert "error" in json.loads(calcular_estimacion.invoke(escenario))

@pytest.mark.parametrize("cantidad", [0, 6, 9])
def test_numero_partidas(escenario, cantidad):
    escenario["partidas"] = (escenario["partidas"] + [escenario["partidas"][0]])[:cantidad]
    assert "error" in json.loads(calcular_estimacion.invoke(escenario))

def test_siete_partidas_validas(escenario):
    escenario["partidas"].pop()
    assert json.loads(calcular_estimacion.invoke(escenario))["total_clp"] == 847000

def test_no_sobrescribir_tarifa(escenario):
    escenario["partidas"][0]["tarifa_clp"] = 1
    assert json.loads(calcular_estimacion.invoke(escenario))["partidas"][0]["subtotal_clp"] == 72000

def test_recurso_desconocido(escenario):
    escenario["partidas"][0]["recurso"] = "inventado"
    assert "error" in json.loads(calcular_estimacion.invoke(escenario))

def test_duplicados(escenario):
    escenario["partidas"][1] = escenario["partidas"][0]
    assert "error" in json.loads(calcular_estimacion.invoke(escenario))

def test_no_comprar_y_declarar_no_requerido(escenario):
    escenario["partidas"][0] = {"recurso": "router", "cantidad": 1}
    assert "error" in json.loads(calcular_estimacion.invoke(escenario))

def test_sin_supuestos(escenario):
    escenario["supuestos"] = []
    assert "error" in json.loads(calcular_estimacion.invoke(escenario))

def test_comparacion_requiere_dos(escenario):
    assert "error" in json.loads(comparar_estimaciones.invoke({"evaluaciones": [escenario]}))

def test_catalogo():
    catalogo = json.loads(consultar_tarifas.invoke({}))
    assert catalogo["version"] == "simulado-v1"
    assert catalogo["tarifas"]["router"]["tarifa_clp"] == 45000

def test_router_y_cableado(escenario):
    escenario["partidas"].pop()
    escenario["partidas"][0] = {"recurso": "router", "cantidad": 1}
    escenario["partidas"].append({"recurso": "cable_red", "cantidad": 10})
    resultado = json.loads(calcular_estimacion.invoke(escenario))
    assert resultado["total_clp"] == 830000
    assert resultado["costo_inicial_clp"] == 803000

def test_periodo_alojamiento(escenario):
    escenario["partidas"][5]["cantidad"] = 12
    resultado = json.loads(calcular_estimacion.invoke(escenario))
    assert resultado["servicios_por_periodos_clp"] == 192000
    assert resultado["total_clp"] == 1012000

def test_router_fraccionario(escenario):
    escenario["partidas"].pop()
    escenario["partidas"][0] = {"recurso": "router", "cantidad": 0.5}
    assert "error" in json.loads(calcular_estimacion.invoke(escenario))
