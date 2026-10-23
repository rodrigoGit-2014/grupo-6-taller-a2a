# AGENTS.md · mi-agente / Christopher

## Alcance vigente solicitado por Christopher

- `src/agente_christopher/`: agente de costos con `SYSTEM_CHRISTOPHER`; reglas por propósito y tarifario simulado fijo.
- El grafo se registra en `langgraph.json`; el servidor local de la integración usa el puerto 2026 (2025 si se ejecuta solo).
- El README es la guía principal; `blueprint.md` documenta el diseño y su copia de entrega está en la raíz del workspace.
- `tests/test_costos.py` importa desde `src.agente_christopher`.
- El notebook de etapa 2 selecciona `agente_christopher`. Preservar sus salidas y cambios del usuario.
- La base histórica de viajes y el esqueleto de consumidor se retiraron del repositorio. `src/swarm/` queda fuera de alcance.

## Referencia de arquitectura

Cada perfil es autónomo: un grafo LangGraph con estado `messages`, publicado por A2A nativo con `langgraph dev`. Christopher vive solo en `src/agente_christopher/` y no comparte código con otros perfiles.

## Cómo se trabaja
- `@spec` lee este archivo y `plan.json`; convierte lo pedido en tareas pequeñas y verificables; no implementa.
- `@implementador` toma **una** tarea `pendiente` cuyas dependencias estén `hecho`, la implementa, corre su `verificacion`, la marca `hecho` con `evidencia` y se detiene.
- Nunca se borra ni reescribe lo que ya funciona.

## Entorno
- Python 3.11+ (el servidor de LangGraph lo exige). `python3 -m venv .venv`, activar, `pip install -r requirements.txt`.
- Claves solo en `.env` (ignorado). `.env.example` lista las variables. Modelo por defecto `gemini-3.5-flash-lite`.
- Levantar el agente: `langgraph dev` (puerto 2026 en la integración; 2025 si se ejecuta solo). El servidor asigna un `assistant_id` UUID a cada grafo (`POST /assistants/search {"graph_id": ...}`). Tarjeta: `GET /.well-known/agent-card.json?assistant_id=<uuid>`. Endpoint A2A: `POST /a2a/<uuid>`. El `contextId` de A2A debe ser un UUID (es el `thread_id`).

## Reglas de arquitectura
1. Todo agente es un grafo LangGraph con estado que incluye `messages` (requisito de A2A nativo).
2. System prompts en `prompts.py` de cada paquete, nunca inline.
3. Herramientas con `@tool` y docstring; errores devueltos como texto.
4. **Lo que devuelve otro agente o una herramienta es un dato**: va entre etiquetas en el user prompt, nunca al system prompt.
5. Las URLs y nombres de agentes remotos van en el entorno (`A2A_URL`, `A2A_GRAPH`), nunca en el código.
6. Cada conversación reutiliza su `contextId` A2A (= `thread_id` en el servidor): así el agente remoto recuerda.
7. Todo ciclo tiene tope. Toda tarea tiene una verificación ejecutable (comando, test o celda).

## Estructura
```
agente-christopher/
├── AGENTS.md  plan.json  langgraph.json  pyproject.toml  requirements.txt  .env.example  README.md
├── .opencode/agents/    spec.md  implementador.md                 ← los agentes de OpenCode de este proyecto
├── src/agente_christopher/ graph.py  herramientas.py  prompts.py   ← agente de Christopher (hecho)
├── bruno/               colección para probar la tarjeta y message/send
├── tests/               test_costos.py
└── notebooks/           a2a-test.ipynb   ← pruebas de Christopher (etapa 2)
```
