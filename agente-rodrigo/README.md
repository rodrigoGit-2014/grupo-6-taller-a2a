# grupo-6-taller-a2a

Taller 1 (Módulo 2): **mi agente especialista habla por A2A**.
Cada integrante transforma la base `agente-viajes-a2a` en su propio agente especialista y lo expone
por A2A de forma nativa; después dos agentes conversan entre sí para resolver un reto.

> **Integración Grupo 6:** este perfil es `mi-agente` y corre en el puerto **2025**. Christopher está
> integrado como segundo perfil en `../agente-christopher/` (puerto **2026**). El notebook compartido
> de la Etapa 3 está en `../notebooks/a2a-test.ipynb`; el de este perfil conserva la Etapa 2.

## Integrantes

| Integrante | Agente | Estado |
|------------|--------|--------|
| Rodrigo | `src/agente_rodrigo/` · arquitectura backend (Java/Spring Boot, microservicios, APIs REST) + agentes de IA | hecho |
| Constante | `src/agente_constante/` | pendiente |
| Paulina | `src/agente_paulina/` | pendiente |
| Christopher | `../agente-christopher/` · evaluación de costos de software | integrado |

Grupo: **Grupo 6**.

> Constante y Paulina no forman parte de esta rama de integración. La base `src/agente_viajes/` se
> conserva porque la Etapa 1 la exige; no participa en el catálogo de la Etapa 3.

## Qué trae el proyecto

- `src/agente_viajes/` · base del taller (vuelos y hoteles). **Ya funciona**; es el punto de partida.
- `src/agente_<nombre>/` · agente de cada integrante (se crea con `@spec` e `@implementador`).
- `bruno/` · colección para probar la Agent Card y `message/send`.
- `tests/test_a2a_viajes.py` · pruebas del A2A nativo (requieren `langgraph dev` arriba).
- `notebooks/a2a-test.ipynb` · Etapa 2 de este perfil + preparación de su tarjeta.
- `../notebooks/a2a-test.ipynb` · Etapa 3 compartida: descubrimiento, router y conversación.

Fuera de alcance: `src/swarm/` y `src/consumidor/` (no son parte de este taller).

## 1. Levantar la base (A2A nativo, sin código de servidor)
```bash
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate   (Python 3.11+)
pip install -r requirements.txt
cp .env.example .env                                   # pega tu GOOGLE_API_KEY
langgraph dev --port 2025                              # http://127.0.0.1:2025
```
El servidor asigna a cada grafo un `assistant_id` (UUID). Con él se obtiene la tarjeta y el endpoint:
```bash
AID=$(curl -s -X POST http://127.0.0.1:2025/assistants/search -H "Content-Type: application/json" -d '{"graph_id":"agente_viajes"}' | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['assistant_id'])")
curl -s "http://127.0.0.1:2025/.well-known/agent-card.json?assistant_id=$AID" | python3 -m json.tool
CTX=$(python3 -c "import uuid; print(uuid.uuid4())")     # contextId = UUID = thread del agente remoto
curl -s -X POST "http://127.0.0.1:2025/a2a/$AID" -H "Content-Type: application/json" -d "{\"jsonrpc\":\"2.0\",\"id\":\"1\",\"method\":\"message/send\",\"params\":{\"message\":{\"role\":\"user\",\"messageId\":\"m1\",\"contextId\":\"$CTX\",\"parts\":[{\"kind\":\"text\",\"text\":\"Quiero un vuelo de Santiago a Lima el 2026-11-10 y un hotel por 2 noches\"}]}}}"
```
- Bruno: abre `bruno/`, elige el entorno `local`, corre `0-assistant-id`, `1-configurar-tarjeta` y luego `agent-card` y `message-send`.
- Pruebas: `pytest tests/test_a2a_viajes.py` (con `langgraph dev` arriba).

## 2. Crear el agente de cada integrante
Con `langgraph dev` corriendo, abre OpenCode y pide las tareas a `@spec` (grupo `agente_<nombre>`), revísalas
y ejecútalas con `@implementador` una por una. Los pasos y las reglas están en `AGENTS.md`
(sección "Crear el agente de un integrante").

## 3. Hacer conversar a los especialistas (Etapa 3)

Levanta Rodrigo en 2025 y Christopher en 2026:

```bash
# Terminal 1 · Rodrigo
cd agente-rodrigo && .venv/bin/langgraph dev --port 2025 --no-browser

# Terminal 2 · Christopher (desde la raíz)
cd agente-christopher && ../agente-rodrigo/.venv/bin/langgraph dev --port 2026 --no-browser
```

Después abre el notebook compartido `../notebooks/a2a-test.ipynb` con el kernel de
`agente-rodrigo/.venv`. Ese notebook actualiza las dos tarjetas, descubre ambos agentes, prueba el
router y ejecuta la conversación de tres turnos. La Etapa 2 de este perfil se conserva en
`notebooks/a2a-test.ipynb`.
