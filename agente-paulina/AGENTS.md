# AGENTS.md · agente-paulina / Paulina

## Alcance vigente

- `src/agente_paulina/`: agente de estrategia y valor de negocio de IA y datos, con `SYSTEM_PAULINA`, apuntes y cálculo de retorno.
- El grafo se registra en `langgraph.json`; el servidor local de la integración usa el puerto 2027 (2025 Rodrigo, 2026 Christopher).
- La base histórica de viajes y el esqueleto de consumidor se retiraron del repositorio.
- `blueprint.md` documenta el diseño; `README.md` es la guía de arranque y pruebas.
- `tests/test_retorno.py` importa desde `src.agente_paulina` y no requiere modelo ni servidor.

## Reglas del taller

1. Todo agente es un grafo LangGraph con estado que incluye `messages`.
2. Los system prompts viven en `prompts.py`, nunca inline en `graph.py`.
3. Las herramientas usan `@tool` con docstring y devuelven errores como texto.
4. Lo que devuelve otro agente o una herramienta es un dato: va entre etiquetas en el mensaje de usuario, nunca en el system prompt.
5. Las URLs y nombres de agentes remotos se leen del entorno.
6. Cada conversación reutiliza su `contextId` A2A (= `thread_id`).
7. Todo ciclo tiene tope (`recursion_limit`) y toda tarea una verificación ejecutable.

## Entorno

- Python 3.12. `py -3.12 -m venv .venv`, activar e instalar `requirements.txt`.
- Claves solo en `.env` (ignorado). `.env.example` no contiene claves.
- Servidor: `.\.venv\Scripts\langgraph.exe dev --port 2027 --no-browser`.
- `assistant_id`: `POST /assistants/search {"graph_id":"agente_paulina"}`.
- Tarjeta: `GET /.well-known/agent-card.json?assistant_id=<uuid>`.
- Endpoint A2A: `POST /a2a/<uuid>`.

## Límites

- No modificar `agente-rodrigo/` ni `agente-christopher/`.
- No versionar `.env`, `.venv/` ni `.langgraph_api/`.
- Paulina no diseña arquitectura ni calcula costos de desarrollo; esos aportes vienen de Rodrigo y Christopher como datos.
