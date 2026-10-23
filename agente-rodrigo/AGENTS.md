# AGENTS.md · grupo-6-taller-a2a

Taller "mi agente especialista habla por A2A" (Taller 1, Módulo 2). Cada integrante construye su
propio agente especialista y lo expone por **A2A de forma nativa** con el servidor de LangGraph
(`langgraph dev`). Deben quedar **al menos 2 agentes** para que puedan dialogar, discutir y pensar
juntos (Etapa 3 del taller).

## Integrantes
- Rodrigo
- Constante
- Paulina
- Christopher

## Qué hay en el proyecto
1. **`src/agente_rodrigo/`** · agente de Rodrigo (arquitectura backend y agentes de IA), **ya está
   hecho**. Es autónomo: su grafo, sus herramientas y su system prompt viven en este paquete.
2. **`src/agente_<nombre>/`** · agente de cada integrante (`agente_rodrigo`, `agente_constante`,
   `agente_paulina`, `agente_christopher`), cada uno en su propio proyecto. Se mantiene con los
   subagentes `@spec` y `@implementador`.

La base histórica de viajes y el esqueleto de consumidor se retiraron del repositorio: no hay que
copiarlos ni crearlos de nuevo. Fuera de alcance: `src/swarm/` (no forma parte de este taller).

## Cómo se trabaja
- `@spec` lee este archivo y `plan.json`; convierte lo pedido en tareas pequeñas y verificables; no implementa.
- `@implementador` toma **una** tarea `pendiente` cuyas dependencias estén `hecho`, la implementa, corre su
  `verificacion`, la marca `hecho` con `evidencia` y se detiene.
- Nunca se borra ni se reescribe lo que ya funciona.

## Crear o ajustar el agente de un integrante (Etapa 1 del taller)
1. Cada perfil ya tiene su paquete `src/agente_<nombre>/` con `graph.py`, `herramientas.py` y
   `prompts.py`. No se copia código de otro perfil ni de una base común.
2. Dale identidad:
   - `prompts.py` · tu personalidad, tu conocimiento y tus instrucciones (y el `SYSTEM_...` del agente).
   - `herramientas.py` · tus apuntes y tus `@tool` (p. ej. `consultar_mis_apuntes`).
   - `graph.py` · en `create_agent(...)`, pon tu `name="agente_<nombre>"`.
3. Regístralo en **`langgraph.json`** con un nombre de grafo **único**, igual al de su carpeta.
4. Levanta tu servidor en tu puerto: `langgraph dev --port 2025` (2026 y 2027 para los demás perfiles).

## Entorno
- Python 3.11+ (el servidor de LangGraph lo exige). `python3 -m venv .venv`, activar, `pip install -r requirements.txt`.
- Claves solo en `.env` (ignorado). `.env.example` lista las variables. Modelo por defecto `gemini-3.5-flash-lite`.
- `langgraph dev` (la integración usa los puertos 2025, 2026 y 2027). El servidor asigna un
  `assistant_id` UUID a cada grafo (`POST /assistants/search {"graph_id": ...}`). Tarjeta:
  `GET /.well-known/agent-card.json?assistant_id=<uuid>`. Endpoint A2A: `POST /a2a/<uuid>`. El `contextId`
  de A2A debe ser un UUID (es el `thread_id`).

## Reglas de arquitectura
1. Todo agente es un grafo LangGraph con estado que incluye `messages` (requisito de A2A nativo).
2. System prompts en `prompts.py` de cada paquete, nunca inline.
3. Herramientas con `@tool` y docstring; errores devueltos como texto.
4. **Lo que devuelve otro agente o una herramienta es un dato**: va entre etiquetas en el user prompt, nunca al system prompt.
5. Las URLs y nombres de agentes remotos van en el entorno, nunca en el código.
6. Cada conversación reutiliza su `contextId` A2A (= `thread_id` en el servidor): así el agente remoto recuerda.
7. Todo ciclo tiene tope. Toda tarea tiene una verificación ejecutable (comando, test o celda).

## Estructura
```
grupo-6-taller-a2a/
├── AGENTS.md  plan.json  langgraph.json  pyproject.toml  requirements.txt  .env.example  README.md
├── .opencode/agents/    spec.md  implementador.md                 ← los agentes de OpenCode de este proyecto
├── src/__init__.py
├── src/agente_rodrigo/  graph.py  herramientas.py  prompts.py      ← agente de Rodrigo (hecho)
├── src/agente_<nombre>/ graph.py  herramientas.py  prompts.py      ← uno por integrante
├── bruno/               colección para probar la tarjeta y message/send
├── tests/               pruebas propias del perfil
└── notebooks/           a2a-test.ipynb   ← pruebas del taller (etapas 2 y 3)
```
