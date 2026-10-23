# Agente Paulina · Grupo 6 · Taller A2A

Paulina es especialista en **estrategia y valor de negocio de IA y datos**. Define casos de negocio, evalúa el impacto con el KPI que corresponda y, cuando hay costo y beneficio monetario confiables, el retorno de la inversión. También propone roadmaps por fases que parten por quick wins. Es directa, cercana y traduce lo técnico a lenguaje de negocio.

> **Integración Grupo 6:** en este repositorio Paulina es el tercer perfil y se ejecuta en el
> puerto **2027**; Rodrigo corre en el **2025** y Christopher en el **2026**. El notebook compartido
> de la Etapa 3 está en `../notebooks/a2a-test.ipynb`.

## Agente disponible

| Grafo | Implementación | Función |
|---|---|---|
| `agente_paulina` | `src/agente_paulina/` | Definir el caso de negocio, evaluar impacto y retorno, y priorizar un roadmap. |

El diseño completo está en [blueprint.md](blueprint.md).

## Qué sabe hacer Paulina

1. **Definir el caso de negocio:** problema, usuarios afectados, KPIs y beneficio esperado.
2. **Evaluar el impacto:** medir el KPI más relevante (mermas, tiempos, quiebres, errores, horas ahorradas, satisfacción) con `evaluar_impacto_kpi` y, si hay costo y beneficio monetario confiables, calcular el retorno con `calcular_retorno`.
3. **Priorizar:** proponer un roadmap por fases con quick wins, entregables y criterios de salida.

No diseña arquitectura (Rodrigo) ni calcula costos de desarrollo (Christopher). Si falta el beneficio esperado, pide el dato o declara supuestos explícitos.

## Estructura

```text
agente-paulina/
├── README.md                 # Inicio, ejecución y pruebas
├── blueprint.md              # Identidad y decisiones de diseño
├── langgraph.json            # Registro de agente_paulina
├── requirements.txt          # Dependencias del taller
├── pyproject.toml            # Metadatos del proyecto
├── .env.example              # Plantilla sin clave
├── src/
│   └── agente_paulina/
│       ├── prompts.py        # SYSTEM_PAULINA: identidad y reglas
│       ├── herramientas.py   # Apuntes, evaluar_impacto_kpi y calcular_retorno
│       └── graph.py          # Modelo + herramientas + prompt
├── notebooks/a2a-test.ipynb  # Etapa 2: pruebas y tarjeta
├── tests/test_retorno.py     # Cálculos y validaciones sin modelo
├── tests/test_impacto_kpi.py # Variaciones de KPI y validaciones
├── tests/test_apuntes.py     # Temas, mayúsculas y sinónimos
├── bruno/                    # Colección HTTP del perfil
├── plan.json                 # Historial base de tareas
└── .opencode/agents/         # Asistentes de desarrollo spec e implementador
```

## Herramientas

| Herramienta | Responsabilidad |
|---|---|
| `consultar_mis_apuntes` | Recuperar conceptos, criterios y el caso de referencia. Acepta mayúsculas y sinónimos como `caso de negocio`. |
| `evaluar_impacto_kpi` | Medir la variación absoluta y porcentual de un KPI operacional; traducirla a CLP solo si se entrega `valor_unitario_clp`. |
| `calcular_retorno` | Calcular beneficio acumulado, ROI %, meses de recuperación y conclusión. |

`evaluar_impacto_kpi(kpi, linea_base, valor_esperado, unidad, mejor_si="menor", valor_unitario_clp=None)` valida las entradas, exige línea base distinta de cero y usa `mejor_si="mayor"` cuando subir es bueno. `calcular_retorno(costo_total_clp, beneficio_mensual_clp, horizonte_meses=12)` valida las entradas y maneja beneficio 0 sin dividir por cero.

## Configuración e inicio en Windows

Desde esta carpeta, con Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si no existe `.env`, copia `.env.example`. Completa `GOOGLE_API_KEY` localmente y revisa `MODELO`. No publiques el archivo ni la clave.

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\langgraph.exe dev --port 2027 --no-browser
```

Deja la terminal abierta. Cada asistente tiene su propio UUID. El modelo predeterminado es `gemini-3.5-flash-lite`; su disponibilidad depende de la cuenta utilizada.

## Pruebas

### Cálculo de retorno sin modelo

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_retorno.py -q
```

Las pruebas cubren el caso de 847.000 CLP, el horizonte por defecto, el punto de equilibrio, el escenario que no se recupera, beneficio 0 y entradas inválidas. No requieren clave ni servidor.

Referencias del caso de prueba:

| Escenario | Resultado |
|---|---|
| Costo 847.000 CLP, beneficio 150.000 CLP/mes, 12 meses | Beneficio 1.800.000, ROI 112,51 %, recuperación 5,65 meses |
| Costo 847.000 CLP, beneficio 0 | ROI -100 %, sin recuperación |
| Quiebres 8 % → 4 %, `mejor_si="menor"` | Variación -4 puntos porcentuales, -50 %, mejora |

### Impacto en KPI y apuntes

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_impacto_kpi.py tests/test_apuntes.py -q
```

Cubren mermas y tiempos que bajan, satisfacción que sube, con y sin `valor_unitario_clp`, entradas inválidas, y consulta de apuntes con mayúsculas o sinónimos como `caso de negocio`.

Para correr todo el conjunto local:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

### Conversación y A2A · Etapa 2

Abre `notebooks/a2a-test.ipynb`, selecciona `.venv/Scripts/python.exe` como kernel y ejecuta las celdas en orden: configuración, descubrimiento de `agente_paulina`, personalidad, conocimientos y herramientas, memoria, tarjeta y envío A2A. Guarda las salidas reales sin limpiarlas.

El notebook usa `A2A_PORT=2027` por defecto y filtra por `agente_paulina`.

### Descubrimiento de asistentes

```powershell
$asistentes = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:2027/assistants/search -ContentType 'application/json' -Body '{"graph_id":"agente_paulina"}'
$aid = $asistentes[0].assistant_id
Invoke-RestMethod -Uri "http://127.0.0.1:2027/.well-known/agent-card.json?assistant_id=$aid"
```

El endpoint A2A usa el UUID: `/a2a/<assistant_id>`. Reutiliza un `contextId` UUID por conversación para conservar contexto.

## Colaboración por A2A

Paulina conversa con Rodrigo y Christopher en el notebook de la raíz:

- **Conversación de dos agentes (tres turnos):** Paulina define el valor, Christopher costea y Paulina integra el retorno y la recomendación.
- **Conversación de equipo (cuatro turnos):** Paulina define el caso y los KPIs, Rodrigo propone arquitectura, Christopher la costea y Paulina calcula el retorno e integra un plan por fases.

Cada agente conserva su propio `contextId`. Los aportes de otros agentes se pasan como datos entre etiquetas, no como instrucciones.

## Entrega del laboratorio

La raíz del ZIP final debe contener `blueprint.md`, `mi-agente/`, el documento de entrega y, cuando corresponda, los perfiles adicionales con su identificación y blueprint. Dentro de `agente-paulina/notebooks/` debe ir el notebook ejecutado con salidas reales.

Excluir `.env`, `.venv/`, `.langgraph_api/`, cachés y `src/swarm/`. Conservar `.env.example`, los archivos del proyecto y las pruebas. Identificar a los integrantes y al grupo en el documento, incorporar evidencias y explicar los ajustes realmente realizados.
