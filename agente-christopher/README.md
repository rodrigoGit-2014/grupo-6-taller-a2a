# Agente Christopher · Grupo 6 · Taller A2A

Christopher estima costos de programación y desarrollo de software en pesos chilenos. Utiliza un tarifario **simulado y fijo**, explica el desglose y compara alternativas con supuestos explícitos. Responde de forma amable, breve y técnica.

El proyecto conserva además el agente original de viajes como ejemplo independiente. Ambos se publican desde el mismo servidor LangGraph y tienen identidades distintas.

## Agentes disponibles

| Grafo | Implementación | Función |
|---|---|---|
| `agente_christopher` | `src/agente_christopher/` | Estimar, comparar y explicar costos de software. |
| `agente_viajes` | `src/agente_viajes/` | Buscar vuelos y hoteles con los datos simulados originales. |

El diseño completo de Christopher está en [blueprint.md](blueprint.md). La separación en un paquete propio fue solicitada por Christopher; la carpeta y las constantes originales de viajes se conservan para ese agente.

## Qué sabe hacer Christopher

1. **Estimar:** calcular una tarea usando cantidades y tarifas de mano de obra, equipamiento y servicios.
2. **Comparar:** recalcular alternativas con las mismas tarifas y explicar qué recursos o cantidades cambian.
3. **Desglosar:** mostrar 7 u 8 partidas pertinentes, sus subtotales y el total en CLP sin IVA.

Puede proponer una estimación preliminar con supuestos. Si no puede determinar recursos u horas razonables, pregunta o solicita revisión especializada. No realiza compras, contrataciones, pagos ni despliegues efectivos.

## Estructura y responsabilidades

```text
mi-agente/
├── README.md                 # Inicio, ejecución y pruebas
├── blueprint.md              # Identidad y decisiones de diseño
├── langgraph.json            # Registro de los dos grafos
├── requirements.txt          # Dependencias originales
├── constraints-etapa1.txt    # Restricciones verificadas para su instalación
├── requirements-lock.txt     # Versiones del entorno verificado
├── .env.example              # Plantilla sin clave
├── src/
│   ├── agente_christopher/
│   │   ├── prompts.py        # Identidad y reglas por propósito
│   │   ├── herramientas.py   # Apuntes, tarifario, validaciones y cálculos
│   │   └── graph.py          # Modelo + herramientas + prompt
│   ├── agente_viajes/        # Ejemplo original, independiente
│   └── consumidor/           # Material base conservado; fuera de esta etapa
├── notebooks/a2a-test.ipynb   # Pruebas de Christopher y consulta por A2A
├── tests/test_costos.py      # Cálculos y validaciones sin usar Gemini
├── tests/test_a2a_viajes.py  # Pruebas originales de integración de viajes
├── bruno/                    # Solicitudes originales de viajes
├── plan.json                 # Historial de tareas y verificaciones
└── .opencode/agents/         # Asistentes de desarrollo spec e implementador
```

### Cómo se construye el agente

En `prompts.py`, `SYSTEM_CHRISTOPHER` ensambla la identidad y reglas separadas de alcance, estimación, comparación, formato, ayuda, autonomía y colaboración.

En `herramientas.py` están las cuatro funciones que puede ejecutar:

| Herramienta | Responsabilidad |
|---|---|
| `consultar_mis_apuntes` | Recuperar conceptos, criterios y el caso ficticio. |
| `consultar_tarifas` | Consultar precios y unidades del tarifario `simulado-v1`. |
| `calcular_estimacion` | Validar 7 u 8 partidas y calcular cantidades × tarifas. |
| `comparar_estimaciones` | Recalcular escenarios y explicar diferencias por partida. |

En `graph.py`, `create_agent` une Gemini, las herramientas y el prompt. El estado contiene `messages`; el ciclo de Christopher tiene un límite de 30 pasos. El servidor administra la memoria por conversación cuando se reutiliza el mismo hilo.

## Configuración e inicio en Windows

Desde esta carpeta, con Python 3.11 o superior:

```powershell
# Solo si necesitas crear/reconstruir el entorno:
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -c constraints-etapa1.txt
```

Si no existe `.env`, copia `.env.example`. Completa `GOOGLE_API_KEY` localmente y revisa `MODELO`. No publiques el archivo ni la clave. Ambos agentes usan esa configuración del modelo; el saldo o acceso del proveedor debe permitir las solicitudes.

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\langgraph.exe dev --port 2025 --no-browser
```

Deja la terminal abierta. Los dos grafos comparten `http://127.0.0.1:2025`; cada asistente tiene su propio UUID. El modelo predeterminado de la base es `gemini-3.5-flash-lite`; su disponibilidad debe verificarse en la cuenta que se utilice.

## Pruebas de Christopher

### Cálculos sin modelo

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_costos.py -q
```

Las pruebas comprueban totales, diferencias, períodos y entradas inválidas. No requieren clave ni servidor.

Referencias del caso ficticio:

| Escenario | Total CLP |
|---|---:|
| Caso base de solicitudes internas | 847.000 |
| Mismo caso con 20 horas de interfaz en lugar de 12 | 1.007.000 |
| Diferencia | 160.000 |

El caso base incluye 820.000 CLP de trabajo inicial y 27.000 CLP de servicios por los períodos indicados: alojamiento de un mes y dominio de un año. No es un costo mensual uniforme.

### Conversación y A2A · etapa 2

Abre `notebooks/a2a-test.ipynb` y selecciona `.venv/Scripts/python.exe` como kernel. Ejecuta en orden: configuración, descubrimiento de `agente_christopher`, personalidad, conocimientos y herramientas, memoria, tarjeta y envío A2A. Guarda las salidas reales sin limpiarlas.

El notebook filtra por `agente_christopher`: la presencia de viajes no cambia esa selección. Si reinicias el servidor o cambias de copia, vuelve a ejecutar el descubrimiento. Un hilo de conversación y un UUID de asistente tienen funciones diferentes.

### Descubrimiento de asistentes

```powershell
$asistentes = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:2025/assistants/search -ContentType 'application/json' -Body '{"graph_id":"agente_christopher"}'
$aid = $asistentes[0].assistant_id
Invoke-RestMethod -Uri "http://127.0.0.1:2025/.well-known/agent-card.json?assistant_id=$aid"
```

Para viajes, busca `agente_viajes` en su lugar. El endpoint A2A usa el UUID: `/a2a/<assistant_id>`. Reutiliza un `contextId` UUID por conversación para conservar contexto.

Las solicitudes de `bruno/` y `tests/test_a2a_viajes.py` siguen siendo las originales de viajes; usan su configuración original (puerto 2024 por defecto). No son las pruebas de costos. Para ejecutar el test de viajes contra este servidor:

```powershell
$env:A2A_VIAJES_URL = "http://127.0.0.1:2025"
$env:A2A_VIAJES_GRAPH = "agente_viajes"
.\.venv\Scripts\python.exe -m pytest tests/test_a2a_viajes.py -q
```

## Colaboración con otros integrantes · etapa 3

Christopher puede recibir una propuesta técnica de otro especialista y estimar sus costos. El flujo que pasa mensajes entre agentes se prepara en el notebook; registrar dos grafos no crea automáticamente una conversación entre ellos. Rodrigo no está incluido en este proyecto y debe ejecutarse o incorporarse por separado.

## Entrega del laboratorio

La raíz del ZIP final debe contener `blueprint.md`, `mi-agente/`, el documento de entrega y, cuando corresponda, `segundo-agente/` con su identificación y blueprint. Dentro de `mi-agente/notebooks/` debe ir el notebook ejecutado con salidas reales.

Excluir `.env`, `.venv/`, `.langgraph_api/`, cachés y `src/swarm/`. Conservar `.env.example`, los archivos del proyecto y las pruebas. Identificar a los integrantes y al grupo en el documento, incorporar evidencias y explicar los ajustes realmente realizados.

El reporte [VERIFICACION.md](VERIFICACION.md) distingue pruebas locales de evidencia de conversación. El ZIP de código es un avance y no sustituye los entregables pendientes del laboratorio.
