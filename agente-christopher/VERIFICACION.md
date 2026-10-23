# Verificación de la reorganización · 17 de octubre de 2026

- Christopher ahora está en `src/agente_christopher/`, con `SYSTEM_CHRISTOPHER` y reglas separadas por propósito.
- La base de viajes se retiró del repositorio; el perfil conserva solo su paquete `src/agente_christopher/`.
- `langgraph.json` publica el grafo `agente_christopher`. Compiló y expone `messages`, sin consultas al proveedor; se usó un marcador temporal de clave solo para esa comprobación estructural.
- `python -m pytest tests/test_costos.py -q`: **22 passed** después de cambiar los imports al paquete nuevo.
- Blueprint del proyecto y copia de la raíz idénticos. README consolidado; guía auxiliar reducida a referencias.
- Notebook, configuración local de VS Code y `.env` sin modificar en esta reorganización. Volver a descubrir asistentes tras reiniciar el servidor.

No se realizó una nueva consulta real a Gemini. El último error del proveedor observado en la sesión fue `402 RESOURCE_EXHAUSTED` por créditos agotados; esta reorganización no modifica esa condición ni acredita su resolución. Las evidencias del laboratorio deben provenir de ejecuciones reales guardadas.

## Historial anterior a esta reorganización

El reporte siguiente corresponde a la preparación inicial. Su nota sobre la clave vacía es histórica: Christopher indicó después haber configurado su clave localmente.

---

# Verificación de Christopher · 17 de octubre de 2026

## Completado

- Entorno virtual creado y dependencias instaladas con constraints-etapa1.txt.
- `python -m pytest tests/test_costos.py -q`: **22 passed**.
- Caso de referencia: **847.000 CLP**; trabajo inicial 820.000 y servicios por períodos indicados 27.000.
- Alternativa con interfaz de 20 horas: **1.007.000 CLP**; diferencia de **160.000 CLP** respecto del caso base.
- Validaciones: 7 u 8 partidas, cantidades finitas no negativas, recursos únicos y conocidos, supuestos obligatorios y consistencia del tarifario.
- Equipamiento, períodos de alojamiento y errores de entrada comprobados.
- Grafo compilado como CompiledStateGraph, estado de salida con messages y límite de 30 pasos. Se utilizó un marcador temporal de clave solo en el proceso de verificación; no se llamó a Gemini ni se guardó una clave ficticia en .env.
- `python -m pip check`: **No broken requirements found**.
- Configuración: agente_christopher; src/swarm omitido; notebook sin editar.

## Pendiente para demostrar la ejecución completa

El .env de mi-agente tiene GOOGLE_API_KEY vacía. Al intentar `langgraph dev --port 2025 --no-browser`, la carga del grafo se detuvo con:

```text
Configura GOOGLE_API_KEY en el archivo .env local de mi-agente antes de iniciar Christopher.
```

No se ha verificado una conversación real con Gemini ni la disponibilidad del modelo configurado para la cuenta del usuario. Los tests de cálculo no necesitan esa conexión.

Para completar la evidencia del taller: configurar la clave local, iniciar el servidor, obtener la captura de la terminal y completar la identificación individual o grupal en el documento de entrega. La captura de un intento fallido no acredita un arranque exitoso.

---

# Integración Grupo 6 · Etapa 3 · 18 de octubre de 2026

Esta sección documenta la ejecución real dentro del repositorio integrado, con Rodrigo en el
puerto 2025 y Christopher en el 2026.

## Ejecución de Christopher

- Entorno: `.venv` propio de `agente-christopher/` (Python 3.12), dependencias de
  `requirements.txt` instaladas.
- Servidor: `langgraph dev --port 2026 --no-browser` responde `{"ok":true}`.
- `POST /assistants/search {"graph_id":"agente_christopher"}` devuelve el UUID
  `b71a76f3-1a4f-5263-a63d-b005bf9e46e1`.
- Notebook `notebooks/a2a-test.ipynb` ejecutado con salidas reales:
  - personalidad: se presenta como Christopher, especialista en costos;
  - conocimientos: usa apuntes, tarifario y `calcular_estimacion`; entrega **847.000 CLP** con
    ocho partidas, 820.000 de trabajo inicial y 27.000 de servicios;
  - memoria: recuerda el objetivo usando el mismo `thread_id`;
  - A2A: la Task termina `TASK_STATE_COMPLETED` y devuelve el artifact con el desglose;
  - tarjeta: se actualiza a `name="Christopher"` con la descripción de su especialidad.
- `pytest tests/test_costos.py -q`: **22 passed** con el `.venv` propio.

## Ajuste de compatibilidad A2A

El notebook fija `protocol_version = "0.3.0"` en la interfaz JSONRPC antes de crear el cliente.
Con `langgraph-api` 0.16.1 y `a2a-sdk` 1.2.2, el mensaje incluye el campo `kind` en la Task y el
protobuf del cliente no lo reconoce; la versión 0.3.0 usa el formato compatible. El notebook de
Etapa 3 aplica el mismo ajuste.

## Conversación con Rodrigo

El notebook compartido `../notebooks/a2a-test.ipynb` descubre las tarjetas `Rodrigo` y
`Christopher`, prueba el router con una pregunta de backend y otra de costos, y ejecuta los tres
turnos del reto del carrito de compras. La propuesta final integra las ideas de resiliencia de
Rodrigo con la estimación en CLP de Christopher.
