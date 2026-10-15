# grupo-6-taller-a2a

Taller 1 (Módulo 2): **mi agente especialista habla por A2A**.
Cada integrante transforma la base `agente-viajes-a2a` en su propio agente especialista y lo expone
por A2A de forma nativa; después dos agentes conversan entre sí para resolver un reto.

## Integrantes

| Integrante | Agente | Estado |
|------------|--------|--------|
| Rodrigo | `src/agente_rodrigo/` | pendiente |
| Constante | `src/agente_constante/` | pendiente |
| Paulina | `src/agente_paulina/` | pendiente |
| Christopher | `src/agente_christopher/` | pendiente |

Grupo: **Grupo 6**.

## Qué trae el proyecto

- `src/agente_viajes/` · base del taller (vuelos y hoteles). **Ya funciona**; es el punto de partida.
- `src/agente_<nombre>/` · agente de cada integrante (se crea con `@spec` e `@implementador`).
- `bruno/` · colección para probar la Agent Card y `message/send`.
- `tests/test_a2a_viajes.py` · pruebas del A2A nativo (requieren `langgraph dev` arriba).
- `notebooks/a2a-test.ipynb` · notebook del taller (etapas 2 y 3).

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
Levanta el segundo agente en otro puerto y usa `notebooks/a2a-test.ipynb`:
```bash
langgraph dev --port 2025      # agente 1
langgraph dev --port 2026      # agente 2 (en otra terminal / otro equipo)
```
