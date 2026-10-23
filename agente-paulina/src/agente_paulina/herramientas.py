"""Apuntes de Paulina y cálculo reproducible de retorno en CLP."""
import json
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from langchain_core.tools import tool

# Apuntes entregados por Paulina. Se mantienen separados del prompt para que el
# agente los consulte como datos y distinga apuntes de sugerencias.
APUNTES = {
    "conceptos": (
        "1. Caso de negocio: justifica un proyecto de IA a partir de un problema de negocio y una métrica, no de la tecnología. Responde qué problema resuelve, para quién, cuánto vale resolverlo y cómo se medirá.\n"
        "2. KPI: indicador que mide el resultado de negocio (ventas, tiempo, costo, conversión). Debe ser específico, medible, con dueño y frecuencia de medición.\n"
        "3. Línea base: valor actual del KPI antes del proyecto. Sin línea base no se puede demostrar impacto.\n"
        "4. Beneficio esperado: mejora del KPI en su unidad operacional; si se puede monetizar con un supuesto confiable, se traduce a CLP por período.\n"
        "5. ROI: (beneficio acumulado - costo total) / costo total, en un horizonte definido.\n"
        "6. Payback: meses necesarios para que el beneficio acumulado iguale el costo total.\n"
        "7. Quick win: caso de bajo esfuerzo, con datos ya disponibles y valor visible en semanas; sirve para validar y ganar confianza antes de proyectos mayores.\n"
        "8. Madurez de datos: los datos deben existir, ser accesibles, tener calidad suficiente y un dueño claro; si no, el caso no llega a producción aunque el piloto funcione.\n"
        "KPIs operacionales: no todo beneficio se mide en dinero; mermas, tiempos de proceso, errores, quiebres y horas ahorradas muestran el impacto antes que el ROI y son más fáciles de validar en un piloto."
    ),
    "criterios": (
        "- Un buen caso parte de un problema concreto con un KPI medible y su línea base.\n"
        "- Un KPI válido es específico, medible con datos existentes, atribuible al proyecto y revisado con una frecuencia definida.\n"
        "- Los supuestos se declaran siempre y se estiman de forma conservadora; si un dato no existe, se pide o se presenta como supuesto, nunca como hecho.\n"
        "- Elige primero el KPI operacional más relevante; usa ROI y payback solo si hay costo y beneficio monetario confiables. Si el beneficio no se monetiza con seguridad, informa el KPI y declara la monetización como supuesto aparte.\n"
        "- El costo considera desarrollo y operación (infraestructura, mantención), no solo construir la solución.\n"
        "- Para comparar alternativas: mismo horizonte, mismos supuestos de beneficio, y se priorizan payback menor, menor riesgo de datos y adopción clara por un usuario de negocio.\n"
        "- Se recomienda partir con un piloto acotado y medible antes de escalar.\n"
        "- Un caso que no se recupera dentro de 12 a 18 meses debe replantearse, acotarse o descartarse, salvo que tenga un valor estratégico explícito."
    ),
    "caso": (
        "CASO FICTICIO de referencia para el taller (no es experiencia real ni un cliente real). "
        "Una cadena de retail mediana quería reducir quiebres de stock en tienda. "
        "Línea base: 8% de quiebres en productos de alta rotación, con ventas perdidas estimadas en 6.000.000 CLP mensuales. "
        "Se propuso un modelo de pronóstico de demanda por tienda y producto, partiendo como piloto en 10 tiendas. "
        "Supuesto conservador: reducir los quiebres a la mitad en el piloto, recuperando 1.200.000 CLP mensuales en esas tiendas. "
        "Costo estimado del piloto: 9.000.000 CLP; payback aproximado de 7,5 meses. "
        "Aprendizaje: el mayor riesgo no fue el modelo, sino la calidad de los datos de inventario (registros desactualizados entre sistemas); "
        "por eso se recomienda evaluar la madurez de datos antes de comprometer plazos y medir la línea base desde el día uno."
    ),
}


TEMAS_VALIDOS = ("conceptos", "criterios", "caso")
SINONIMOS_TEMAS = {
    "concepto": "conceptos",
    "criterio": "criterios",
    "casos": "caso",
    "caso de negocio": "caso",
    "caso de uso": "caso",
    "negocio": "caso",
    "ejemplo": "caso",
    "referencia": "caso",
}


def _json(datos) -> str:
    return json.dumps(datos, ensure_ascii=False)


def _error(mensaje: str) -> str:
    return _json({"error": mensaje})


def _entero(valor, nombre: str) -> int:
    """Convierte un monto CLP a entero, rechazando booleanos, texto y decimales."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{nombre} debe ser un número entero en CLP.")
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{nombre} debe ser un número entero en CLP.") from exc
    if not numero.is_finite():
        raise ValueError(f"{nombre} debe ser finito.")
    if numero != numero.to_integral_value():
        raise ValueError(f"{nombre} debe ser un número entero de pesos, sin decimales.")
    return int(numero)


def _numero(valor, nombre: str) -> Decimal:
    """Convierte un número finito a Decimal, rechazando booleanos y texto."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError(f"{nombre} debe ser un número.")
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{nombre} debe ser un número.") from exc
    if not numero.is_finite():
        raise ValueError(f"{nombre} debe ser finito.")
    return numero


def _redondear(valor: Decimal) -> float:
    return float(valor.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _redondear_kpi(valor: Decimal) -> float:
    """Conserva precisión en KPI fraccionarios; usa 2 decimales si |valor| >= 1."""
    if abs(valor) < 1:
        return float(valor.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
    return _redondear(valor)


def _normalizar_tema(tema: str) -> str | None:
    clave = " ".join(str(tema).lower().strip().split())
    if not clave:
        return ""
    if clave in APUNTES:
        return clave
    return SINONIMOS_TEMAS.get(clave)


@tool
def consultar_mis_apuntes(tema: str = "") -> str:
    """Consulta tus apuntes. Temas válidos: conceptos, criterios o caso (acepta mayúsculas y sinónimos como "caso de negocio"). Sin tema devuelve todos."""
    clave = _normalizar_tema(tema)
    if clave is None:
        return _error("Tema desconocido. Usa conceptos, criterios o caso.")
    return _json({clave: APUNTES[clave]} if clave else APUNTES)


@tool
def calcular_retorno(costo_total_clp: int, beneficio_mensual_clp: int, horizonte_meses: int = 12) -> str:
    """Calcula beneficio acumulado, ROI del horizonte y meses de recuperación. Montos en CLP; supone beneficio mensual constante. Devuelve errores como texto."""
    try:
        costo = _entero(costo_total_clp, "costo_total_clp")
        beneficio = _entero(beneficio_mensual_clp, "beneficio_mensual_clp")
        if isinstance(horizonte_meses, bool) or not isinstance(horizonte_meses, int):
            raise ValueError("horizonte_meses debe ser un entero positivo.")
        if costo <= 0:
            raise ValueError("costo_total_clp debe ser mayor que cero.")
        if beneficio < 0:
            raise ValueError("beneficio_mensual_clp no puede ser negativo.")
        if horizonte_meses <= 0:
            raise ValueError("horizonte_meses debe ser mayor que cero.")

        acumulado = beneficio * horizonte_meses
        roi = _redondear((Decimal(acumulado) - Decimal(costo)) / Decimal(costo) * 100)

        if beneficio == 0:
            meses = None
            recupera = False
            conclusion = (
                "Con un beneficio mensual de 0 CLP la inversión no se recupera. "
                "Declara un supuesto de beneficio antes de recomendar el proyecto."
            )
        else:
            meses = _redondear(Decimal(costo) / Decimal(beneficio))
            recupera = meses <= horizonte_meses
            if recupera:
                conclusion = (
                    f"La inversión se recupera en {meses} meses, dentro del horizonte "
                    f"de {horizonte_meses} meses, con un ROI de {roi}%."
                )
            else:
                conclusion = (
                    f"La inversión no se recupera dentro de {horizonte_meses} meses: "
                    f"requiere {meses} meses. El ROI del horizonte es {roi}%."
                )

        return _json(
            {
                "moneda": "CLP",
                "costo_total_clp": costo,
                "beneficio_mensual_clp": beneficio,
                "horizonte_meses": horizonte_meses,
                "beneficio_acumulado_clp": acumulado,
                "roi_pct": roi,
                "meses_recuperacion": meses,
                "recupera_en_horizonte": recupera,
                "supuesto": "Beneficio mensual constante durante todo el horizonte; no incluye IVA ni financiamiento.",
                "conclusion": conclusion,
            }
        )
    except (ValueError, TypeError, InvalidOperation, OverflowError) as exc:
        return _error(str(exc))


@tool
def evaluar_impacto_kpi(
    kpi: str,
    linea_base: float,
    valor_esperado: float,
    unidad: str,
    mejor_si: str = "menor",
    valor_unitario_clp: float | None = None,
) -> str:
    """Evalúa la variación de un KPI operacional y, si se entrega valor_unitario_clp, la traduce a CLP.

    Usa mejor_si="menor" cuando bajar es bueno (mermas, tiempos, errores, quiebres)
    y mejor_si="mayor" cuando subir es bueno (satisfacción, conversión).
    linea_base debe ser distinta de cero para calcular la variación porcentual.
    El impacto en CLP es positivo si es mejora y negativo si es empeoramiento.
    """
    try:
        if not isinstance(kpi, str) or not kpi.strip():
            raise ValueError("kpi debe ser un texto no vacío.")
        if not isinstance(unidad, str) or not unidad.strip():
            raise ValueError("unidad debe ser un texto no vacío.")

        base = _numero(linea_base, "linea_base")
        esperado = _numero(valor_esperado, "valor_esperado")
        if base == 0:
            raise ValueError(
                "linea_base no puede ser cero: la variación porcentual no estaría definida."
            )

        direccion = str(mejor_si).strip().lower()
        if direccion not in {"menor", "mayor"}:
            raise ValueError('mejor_si debe ser "menor" o "mayor".')

        variacion = esperado - base
        variacion_pct = variacion / abs(base) * 100

        if variacion == 0:
            mejora = False
            empeoramiento = False
            etiqueta = "sin cambio"
        elif (direccion == "menor" and variacion < 0) or (
            direccion == "mayor" and variacion > 0
        ):
            mejora = True
            empeoramiento = False
            etiqueta = "mejora"
        else:
            mejora = False
            empeoramiento = True
            etiqueta = "empeoramiento"

        resultado = {
            "kpi": kpi.strip(),
            "unidad": unidad.strip(),
            "linea_base": _redondear_kpi(base),
            "valor_esperado": _redondear_kpi(esperado),
            "variacion_absoluta": _redondear_kpi(variacion),
            "variacion_pct": _redondear_kpi(variacion_pct),
            "mejor_si": direccion,
            "es_mejora": mejora,
            "es_empeoramiento": empeoramiento,
            "sin_cambio": not mejora and not empeoramiento,
            "evaluacion": etiqueta,
        }

        if valor_unitario_clp is not None:
            unitario = _numero(valor_unitario_clp, "valor_unitario_clp")
            if unitario <= 0:
                raise ValueError("valor_unitario_clp debe ser mayor que cero.")
            magnitud = abs(variacion) * unitario
            if mejora:
                impacto = magnitud
            elif empeoramiento:
                impacto = -magnitud
            else:
                impacto = Decimal("0")
            resultado["impacto_clp"] = _redondear(impacto)
            resultado["moneda"] = "CLP"
            resultado["supuesto_monetizacion"] = (
                "El equivalente en CLP usa valor_unitario_clp y asume una relación "
                "lineal entre la variación del KPI y el valor económico."
            )

        if etiqueta == "sin cambio":
            resultado["conclusion"] = (
                f"El KPI '{kpi.strip()}' se mantiene en {_redondear_kpi(base)} "
                f"{unidad.strip()}."
            )
        else:
            verbo = "baja" if variacion < 0 else "sube"
            resultado["conclusion"] = (
                f"El KPI '{kpi.strip()}' {etiqueta}: {verbo} de {_redondear_kpi(base)} a "
                f"{_redondear_kpi(esperado)} {unidad.strip()} (variación "
                f"{_redondear_kpi(variacion)} {unidad.strip()}, "
                f"{_redondear_kpi(variacion_pct)}%)."
            )
            if valor_unitario_clp is not None:
                resultado["conclusion"] += (
                    f" Equivale a {resultado['impacto_clp']} CLP."
                )

        return _json(resultado)
    except (ValueError, TypeError, InvalidOperation, OverflowError) as exc:
        return _error(str(exc))


HERRAMIENTAS = [consultar_mis_apuntes, evaluar_impacto_kpi, calcular_retorno]
