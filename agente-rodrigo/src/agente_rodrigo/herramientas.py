"""Herramientas del agente de Rodrigo.

Rodrigo no vende vuelos ni hoteles: su herramienta es `consultar_mis_apuntes`,
que lee del diccionario `APUNTES` (sus apuntes personales de especialista en
arquitectura backend y agentes de IA). Los errores se devuelven como texto
(regla de AGENTS.md: 'Herramientas con @tool y docstring; errores devueltos
como texto').
"""
from langchain_core.tools import tool

APUNTES = {
    "conceptos": (
        "Tres conceptos importantes de mi especialidad:\n"
        "1) Microservicios y APIs REST: contratos explícitos y compatibilidad "
        "hacia atrás (versionado, nunca romper consumidores).\n"
        "2) Arquitectura multi-tenant en cloud: aislamiento de datos por "
        "inquilino, tenencia compartida vs. dedicada, costos y seguridad.\n"
        "3) Agentes de IA: tool calling, orquestación multiagente, RAG "
        "(retrieval-augmented generation) y MCP (Model Context Protocol)."
    ),
    "criterios": (
        "Cómo evalúo una buena solución en mi área:\n"
        "- Contratos claros (API estable, documentada y versionada).\n"
        "- Tolerancia a fallos (retries, circuit breakers, degradación "
        "elegante).\n"
        "- Caché y performance (latencia baja, caché donde aporta).\n"
        "- Observabilidad (logs, métricas, trazas, dashboards).\n"
        "- Testeabilidad (pruebas automatizadas, fácil de verificar).\n"
        "- Honestidad de alcance (qué resuelve y qué no, sin prometer de más)."
    ),
    "caso": (
        "Caso real que me marcó: el carro de compras de Falabella.\n"
        "- Contexto: alto tráfico multi-país (varios países, miles de "
        "usuarios concurrentes).\n"
        "- APIs REST entre servicios internos.\n"
        "- Caché con Redis para aliviar la base de datos y bajar latencia.\n"
        "- Arquitectura multi-tenant en GCP con Docker y Kubernetes.\n"
        "- Dashboards de observabilidad para monitorear en tiempo real.\n"
        "Qué aprendí: separar bien los contratos, dimensionar el caché, "
        "diseñar para fallar de forma controlada y medir todo lo que importa."
    ),
    "acordeon": (
        "Vendo acordeones Hohner por YouTube.\n"
        "Texto de referencia (no navego, solo lo cito): "
        "https://www.youtube.com/watch?v=Zk3QGM_Sik0"
    ),
}


@tool
def consultar_mis_apuntes(tema: str = "") -> str:
    """Consulta los apuntes personales de Rodrigo.

    Args:
        tema: Clave del apunte a consultar. Valores disponibles: "conceptos",
            "criterios", "caso" y "acordeon". Si se pasa vacío (""), devuelve
            todos los apuntes. Si el tema no existe, devuelve un mensaje claro
            de error como texto.

    Returns:
        El texto del apunte solicitado (o de todos los apuntes si tema está
        vacío). Los errores se devuelven como texto, no como excepción.
    """
    tema = (tema or "").strip().lower()

    if tema == "":
        return "\n\n".join(
            f"--- {clave} ---\n{texto}" for clave, texto in APUNTES.items()
        )

    if tema not in APUNTES:
        claves = ", ".join(sorted(APUNTES.keys()))
        return (
            f"No tengo un apunte llamado '{tema}'. Temas disponibles: "
            f"{claves}."
        )

    return APUNTES[tema]


HERRAMIENTAS = [consultar_mis_apuntes]
