# Verificación de la reorganización · 17 de octubre de 2026

- Christopher ahora está en `src/agente_christopher/`, con `SYSTEM_CHRISTOPHER` y reglas separadas por propósito.
- Viajes conserva exactamente los cuatro archivos Python de la base original en `src/agente_viajes/`.
- `langgraph.json` publica ambos grafos. Los dos compilaron y exponen `messages`, sin consultas al proveedor; se usó un marcador temporal de clave solo para esa comprobación estructural.
- `python -m pytest tests/test_costos.py -q`: **22 passed** después de cambiar los imports al paquete nuevo.
- Herramientas de viajes verificadas localmente: dos vuelos SCL-LIM y cálculo de hotel por dos noches.
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
- Configuración: agente_christopher; src/swarm omitido; archivos originales conservados en la carpeta base; notebook sin editar.

## Pendiente para demostrar la ejecución completa

El .env de mi-agente tiene GOOGLE_API_KEY vacía. Al intentar `langgraph dev --port 2025 --no-browser`, la carga del grafo se detuvo con:

```text
Configura GOOGLE_API_KEY en el archivo .env local de mi-agente antes de iniciar Christopher.
```

No se ha verificado una conversación real con Gemini ni la disponibilidad del modelo configurado para la cuenta del usuario. Los tests de cálculo no necesitan esa conexión.

Para completar la evidencia del taller: configurar la clave local, iniciar el servidor, obtener la captura de la terminal y completar la identificación individual o grupal en el documento de entrega. La captura de un intento fallido no acredita un arranque exitoso.
