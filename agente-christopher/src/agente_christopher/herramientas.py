"""Tarifas ficticias y cálculos reproducibles en CLP sin IVA."""
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from langchain_core.tools import tool

VERSION_TARIFARIO = "simulado-v1"
TARIFAS = {
    "analisis": {"nombre": "Análisis de requerimientos", "categoria": "mano de obra", "unidad": "hora", "tarifa_clp": 18000},
    "interfaz": {"nombre": "Desarrollo de interfaz", "categoria": "mano de obra", "unidad": "hora", "tarifa_clp": 20000},
    "logica_datos": {"nombre": "Desarrollo de lógica y datos", "categoria": "mano de obra", "unidad": "hora", "tarifa_clp": 22000},
    "pruebas": {"nombre": "Pruebas funcionales", "categoria": "mano de obra", "unidad": "hora", "tarifa_clp": 16000},
    "despliegue": {"nombre": "Configuración del despliegue", "categoria": "mano de obra", "unidad": "hora", "tarifa_clp": 20000},
    "alojamiento": {"nombre": "Alojamiento de aplicación", "categoria": "servicio recurrente", "unidad": "mes", "tarifa_clp": 15000},
    "dominio": {"nombre": "Dominio", "categoria": "servicio recurrente", "unidad": "año", "tarifa_clp": 12000},
    "router": {"nombre": "Router", "categoria": "equipamiento", "unidad": "unidad", "tarifa_clp": 45000},
    "cable_red": {"nombre": "Cable de red", "categoria": "equipamiento", "unidad": "metro", "tarifa_clp": 1000},
    "licencia": {"nombre": "Licencia de herramienta", "categoria": "servicio recurrente", "unidad": "mes", "tarifa_clp": 10000},
    "equipamiento_no_requerido": {"nombre": "Equipamiento y cableado adicional no requerido", "categoria": "equipamiento", "unidad": "no requerido", "tarifa_clp": 0},
}
APUNTES = {
    "conceptos": "1. Mano de obra = horas por tarifa del rol. 2. Equipamiento = cantidad por precio unitario. 3. Servicios recurrentes = tarifa por período contratado; distinguirlos del trabajo inicial.",
    "criterios": "Tarifario simulado-v1 fijo; variar cantidades según alcance. Mostrar 7 u 8 partidas pertinentes y únicas, total en CLP sin IVA, supuestos y períodos. No inventar compras para completar partidas: se permite equipamiento no requerido a cero. No mezclar períodos sin explicarlos. La estimación es preliminar, no una oferta comercial.",
    "caso": "CASO FICTICIO: aplicación web de solicitudes internas para oficina con computadores y conectividad existentes. Análisis 4h, interfaz 12h, lógica/datos 16h, pruebas 6h, despliegue 3h, alojamiento 1 mes, dominio 1 año, equipamiento no requerido. Total 847000 CLP sin IVA. Trabajo inicial 820000; servicios 27000 por los períodos indicados. Aprendizaje: comparar alternativas con el mismo alcance y horizonte de servicios. No representa experiencia real de Christopher.",
}

def _json(datos) -> str:
    return json.dumps(datos, ensure_ascii=False)

def _error(mensaje: str) -> str:
    return _json({"error": mensaje})

@tool
def consultar_mis_apuntes(tema: str = "") -> str:
    """Consulta conceptos, criterios o caso ficticio de costos de software. Vacío devuelve todos."""
    clave = tema.lower().strip()
    if clave and clave not in APUNTES:
        return _error("Tema desconocido. Usa conceptos, criterios o caso.")
    return _json({clave: APUNTES[clave]} if clave else APUNTES)

@tool
def consultar_tarifas(recurso: str = "") -> str:
    """Consulta el tarifario ficticio fijo en CLP sin IVA. Usa clave de recurso; vacío lista todo."""
    clave = recurso.lower().strip()
    if clave and clave not in TARIFAS:
        return _error("Recurso desconocido. Consulta el catálogo; no inventes una tarifa.")
    return _json({"version": VERSION_TARIFARIO, "simulado": True, "moneda": "CLP", "incluye_iva": False, "tarifas": {clave: TARIFAS[clave]} if clave else TARIFAS})

def _calcular(nombre, partidas, supuestos):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("Indica un nombre para la evaluación.")
    if not isinstance(partidas, list) or len(partidas) not in (7, 8):
        raise ValueError("La evaluación debe tener 7 u 8 partidas.")
    if not isinstance(supuestos, list) or not supuestos or any(not isinstance(s, str) or not s.strip() for s in supuestos):
        raise ValueError("Indica al menos un supuesto explícito.")
    filas, vistos = [], set()
    for partida in partidas:
        if not isinstance(partida, dict):
            raise ValueError("Cada partida debe indicar recurso y cantidad.")
        recurso = partida.get("recurso")
        if not isinstance(recurso, str) or recurso not in TARIFAS:
            raise ValueError("Recurso desconocido; consulta consultar_tarifas.")
        if recurso in vistos:
            raise ValueError("No repitas recursos: suma sus cantidades en una partida.")
        vistos.add(recurso)
        valor = partida.get("cantidad")
        if isinstance(valor, bool):
            raise ValueError("La cantidad debe ser numérica.")
        cantidad = Decimal(str(valor))
        if not cantidad.is_finite() or cantidad < 0:
            raise ValueError("Las cantidades deben ser finitas y no negativas.")
        if recurso == "equipamiento_no_requerido" and cantidad != 0:
            raise ValueError("Equipamiento no requerido debe tener cantidad cero.")
        if recurso != "equipamiento_no_requerido" and cantidad <= 0:
            raise ValueError("Los recursos requeridos deben tener cantidad positiva.")
        if recurso == "router" and cantidad != cantidad.to_integral_value():
            raise ValueError("La cantidad de routers debe ser entera.")
        tarifa = TARIFAS[recurso]
        subtotal = int((cantidad * tarifa["tarifa_clp"]).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
        filas.append({"recurso": recurso, **tarifa, "cantidad": float(cantidad), "subtotal_clp": subtotal})
    if "equipamiento_no_requerido" in vistos and vistos.intersection({"router", "cable_red"}):
        raise ValueError("No combines equipamiento no requerido con compras de equipamiento.")
    if len({f["categoria"] for f in filas}) < 2:
        raise ValueError("Incluye partidas de al menos dos categorías pertinentes.")
    return {"nombre": nombre.strip(), "version_tarifario": VERSION_TARIFARIO, "simulado": True, "preliminar": True, "moneda": "CLP", "incluye_iva": False, "supuestos": supuestos, "partidas": filas, "total_clp": sum(f["subtotal_clp"] for f in filas), "costo_inicial_clp": sum(f["subtotal_clp"] for f in filas if f["categoria"] != "servicio recurrente"), "servicios_por_periodos_clp": sum(f["subtotal_clp"] for f in filas if f["categoria"] == "servicio recurrente")}

@tool
def calcular_estimacion(nombre: str, partidas: list[dict], supuestos: list[str]) -> str:
    """Calcula 7 u 8 partidas usando tarifas fijas. Cada partida: recurso (clave del catálogo) y cantidad. Supuestos obligatorios. Devuelve desglose, total inicial y servicios por sus períodos; errores como texto."""
    try:
        return _json(_calcular(nombre, partidas, supuestos))
    except (ValueError, TypeError, InvalidOperation, OverflowError) as exc:
        return _error(str(exc))

@tool
def comparar_estimaciones(evaluaciones: list[dict]) -> str:
    """Compara dos o más escenarios recalculando con el mismo tarifario. Cada escenario contiene nombre, partidas (recurso y cantidad) y supuestos. Diferencias relativas al primero."""
    try:
        if len(evaluaciones) < 2 or any(not isinstance(e, dict) for e in evaluaciones):
            raise ValueError("Entrega al menos dos escenarios con nombre, partidas y supuestos.")
        resultados = [_calcular(e.get("nombre"), e.get("partidas"), e.get("supuestos")) for e in evaluaciones]
        if len({r["nombre"] for r in resultados}) != len(resultados):
            raise ValueError("Usa nombres diferentes para distinguir escenarios.")
        base = resultados[0]
        diferencias = []
        for otro in resultados[1:]:
            a = {f["recurso"]: f for f in base["partidas"]}
            b = {f["recurso"]: f for f in otro["partidas"]}
            detalle = []
            for recurso in sorted(a.keys() | b.keys()):
                primero, segundo = a.get(recurso, {}), b.get(recurso, {})
                cambio = segundo.get("subtotal_clp", 0) - primero.get("subtotal_clp", 0)
                if primero.get("cantidad", 0) != segundo.get("cantidad", 0):
                    detalle.append({"recurso": recurso, "unidad": TARIFAS[recurso]["unidad"], "cantidad_base": primero.get("cantidad", 0), "cantidad_alternativa": segundo.get("cantidad", 0), "diferencia_clp": cambio})
            diferencias.append({"base": base["nombre"], "alternativa": otro["nombre"], "diferencia_total_clp": otro["total_clp"] - base["total_clp"], "detalle": detalle})
        return _json({"evaluaciones": resultados, "comparaciones": diferencias, "nota": "Tarifas idénticas y simuladas. Las diferencias corresponden a cantidades o recursos. Revisar alcance, supuestos y períodos antes de concluir cuál conviene."})
    except (ValueError, TypeError, InvalidOperation, OverflowError) as exc:
        return _error(str(exc))

HERRAMIENTAS = [consultar_mis_apuntes, consultar_tarifas, calcular_estimacion, comparar_estimaciones]
