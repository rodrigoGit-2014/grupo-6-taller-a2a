# Grupo 6 · Taller A2A · Tres especialistas

Taller 1 (Módulo 2): **mi agente especialista habla por A2A**. Este repositorio reúne tres perfiles
locales que se descubren y conversan por el protocolo A2A:

| Perfil | Especialidad | Carpeta | Servidor | Grafo |
|---|---|---|---|---|
| Rodrigo | Arquitectura backend y agentes de IA | `agente-rodrigo/` | `http://127.0.0.1:2025` | `agente_rodrigo` |
| Christopher | Costos de programación y software | `agente-christopher/` | `http://127.0.0.1:2026` | `agente_christopher` |
| Paulina | Estrategia y valor de negocio de IA y datos | `agente-paulina/` | `http://127.0.0.1:2027` | `agente_paulina` |

La Etapa 3 **no importa código de un agente dentro de otro**: el notebook orquestador los descubre por
HTTP/A2A, actualiza sus tarjetas y les pasa mensajes conservando un `contextId` UUID por agente. Cada
respuesta ajena se entrega entre etiquetas y se trata como **dato**, nunca como instrucción.

## Mapa del repositorio

```text
grupo-6-taller-a2a/
├── README.md                          # Esta guía: estructura, arranque y entrega.
├── .env.example                       # Plantilla de claves y URLs (sin claves reales).
├── .gitignore                         # Ignora .env, .venv, cachés y docs no entregables.
│
├── agente-rodrigo/                    # Perfil 1 · Rodrigo · servidor 2025.
│   ├── README.md / AGENTS.md / blueprint.md
│   ├── langgraph.json                 # Registra agente_rodrigo y la base agente_viajes.
│   ├── src/agente_rodrigo/            # prompts.py, herramientas.py y graph.py.
│   ├── notebooks/a2a-test.ipynb       # Etapa 2: pruebas y tarjeta de Rodrigo.
│   ├── tests/                         # Pruebas del A2A nativo y de la base.
│   └── bruno/                         # Colección HTTP para tarjeta y message/send.
│
├── agente-christopher/                # Perfil 2 · Christopher · servidor 2026.
│   ├── README.md / AGENTS.md / blueprint.md / VERIFICACION.md
│   ├── langgraph.json                 # Registra agente_christopher y la base agente_viajes.
│   ├── src/agente_christopher/        # prompts.py, herramientas.py y graph.py.
│   ├── notebooks/a2a-test.ipynb       # Etapa 2: pruebas y tarjeta de Christopher.
│   ├── tests/test_costos.py           # 22 pruebas de cálculo, sin modelo ni servidor.
│   └── bruno/                         # Colección HTTP original.
│
├── agente-paulina/                    # Perfil 3 · Paulina · servidor 2027.
│   ├── README.md / AGENTS.md / blueprint.md
│   ├── langgraph.json                 # Registra agente_paulina y la base agente_viajes.
│   ├── src/agente_paulina/            # prompts.py, herramientas.py y graph.py.
│   ├── notebooks/a2a-test.ipynb       # Etapa 2: pruebas y tarjeta de Paulina.
│   ├── tests/                         # Retorno, impacto en KPI, apuntes y A2A.
│   └── bruno/                         # Colección HTTP original.
│
├── notebooks/
│   └── a2a-test.ipynb                 # ETAPA 3: descubrimiento, router y dos conversaciones.
│
├── docs/entrega/
│   └── documento-entrega.md           # Documento de entrega y comparación para clase.
│
└── scripts/
    ├── verificar_remoto.sh            # Verificación de una tarjeta remota.
    └── empaquetar_entrega.bat         # Genera el ZIP reproducible de entrega.
```

### Por qué cada notebook está donde está

- `agente-*/notebooks/a2a-test.ipynb` prueba **un solo perfil**: personalidad, conocimientos,
  memoria y envío A2A. Ahí vive la celda “Preparar mi tarjeta”.
- `notebooks/a2a-test.ipynb` es el **orquestador compartido** de la Etapa 3. Descubre los tres
  servidores, prueba el router con una pregunta de cada especialidad y ejecuta dos conversaciones:
  **Paulina → Christopher → Paulina** y **Paulina → Rodrigo → Christopher → Paulina**.
- El orquestador no importa `src/` de ningún perfil; solo usa HTTP/A2A. Por eso vive en la raíz sin
  acoplarse a un proyecto.

## Requisitos

- Python 3.12.
- Una `GOOGLE_API_KEY` válida para Gemini.
- Tres terminales (una por servidor) para la ejecución completa.
- Opcional: `DEEPSEEK_API_KEY` para el respaldo si Gemini falla por cuota o saldo.

## Configuración

1. Crea el entorno de cada perfil si aún no existe:

   ```powershell
   cd agente-rodrigo
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt

   cd ..\agente-christopher
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt

   cd ..\agente-paulina
   py -3.12 -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

   El kernel recomendado para el notebook raíz es el `.venv` de `agente-paulina`, que trae las
   dependencias del orquestador.

2. Copia las plantillas y completa la clave **solo en local**:

   ```powershell
   Copy-Item .env.example .env
   Copy-Item agente-rodrigo\.env.example agente-rodrigo\.env
   Copy-Item agente-christopher\.env.example agente-christopher\.env
   Copy-Item agente-paulina\.env.example agente-paulina\.env
   # edita los cuatro .env y pega GOOGLE_API_KEY
   ```

   El `.env` de la raíz lo usa el notebook de Etapa 3. Cada servidor lee además su propio `.env`.
   Ningún `.env` se versiona ni se incluye en el ZIP.

3. Variables principales del notebook:

   | Variable | Valor por defecto | Uso |
   |---|---|---|
   | `A2A_URL_1` | `http://127.0.0.1:2025` | Servidor de Rodrigo. |
   | `A2A_GRAPH_1` | `agente_rodrigo` | Grafo que se busca en el servidor 1. |
   | `A2A_NOMBRE_1` | `Rodrigo` | Nombre que usa el router. |
   | `A2A_URL_2` | `http://127.0.0.1:2026` | Servidor de Christopher. |
   | `A2A_GRAPH_2` | `agente_christopher` | Grafo que se busca en el servidor 2. |
   | `A2A_NOMBRE_2` | `Christopher` | Nombre que usa el router. |
   | `A2A_URL_3` | `http://127.0.0.1:2027` | Servidor de Paulina. |
   | `A2A_GRAPH_3` | `agente_paulina` | Grafo que se busca en el servidor 3. |
   | `A2A_NOMBRE_3` | `Paulina` | Nombre que usa el router. |
   | `A2A_NOMBRE_TARJETA_3` | `Agente Paulina` | Nombre visible de la tarjeta (opcional). |
   | `A2A_ASSISTANT_ID_n` | vacío | UUID fijado; vacío = se descubre con `/assistants/search`. |
   | `A2A_GESTIONAR_TARJETA_n` | `1` | `1` actualiza la tarjeta local; `0` no toca una tarjeta remota. |

## Respaldo opcional a DeepSeek

Los tres perfiles usan **Gemini como modelo principal, sin cambios**. Si existe
`DEEPSEEK_API_KEY`, cada `graph.py` agrega `ChatDeepSeek` como respaldo mediante
`ModelFallbackMiddleware`; el router del notebook hace lo mismo con `with_fallbacks`.

Es **opcional**: sin `DEEPSEEK_API_KEY`, todo funciona solo con Gemini. Variables:

| Variable | Valor por defecto | Uso |
|---|---|---|
| `DEEPSEEK_API_KEY` | vacía | Si está definida, activa el respaldo en los tres agentes y en el router. |
| `MODELO_RESPALDO` | `deepseek-chat` | Modelo de DeepSeek usado como respaldo. |

En la ejecución de referencia, Gemini devolvió `402 Payment Required` y el respaldo DeepSeek
respondió correctamente. El notebook no falla si el respaldo está configurado.

## Levantar los tres servidores

Terminal 1 · Rodrigo (2025):

```powershell
cd agente-rodrigo
.\.venv\Scripts\langgraph.exe dev --port 2025 --no-browser
```

Terminal 2 · Christopher (2026):

```powershell
cd agente-christopher
.\.venv\Scripts\langgraph.exe dev --port 2026 --no-browser
```

Terminal 3 · Paulina (2027):

```powershell
cd agente-paulina
.\.venv\Scripts\langgraph.exe dev --port 2027 --no-browser
```

En Linux/macOS usa `.venv/bin/langgraph`. Si un perfil no tiene `.venv` propio, puedes reutilizar
el de otro entorno que tenga sus dependencias, pero no mezcles `.env` ni claves.

Cada servidor publica su Agent Card y asigna un `assistant_id` UUID a cada grafo. El notebook lo
descubre en tiempo de ejecución; no se escribe a mano salvo en modo remoto.

Comprobación rápida:

```powershell
Invoke-RestMethod http://127.0.0.1:2025/ok
Invoke-RestMethod http://127.0.0.1:2026/ok
Invoke-RestMethod http://127.0.0.1:2027/ok
```

## Ejecutar el notebook orquestador

1. Deja los tres servidores arriba.
2. Abre `notebooks/a2a-test.ipynb` con el kernel de `agente-paulina/.venv`.
3. Ejecuta **Run All** (todas las celdas en orden).
4. Guarda el notebook **sin limpiar las salidas**.

El Run All debe mostrar:

- las tres tarjetas preparadas o tomadas como remotas;
- el descubrimiento de `Rodrigo`, `Christopher` y `Paulina`;
- `[Supervisor] Rodrigo`, `[Supervisor] Christopher` y `[Supervisor] Paulina` en las tres preguntas
  del router;
- la conversación de tres turnos y la conversación de equipo de cuatro turnos;
- `Clientes A2A cerrados.` al final.

La ejecución tolera caídas: si una URL no responde, marca el perfil como no disponible y continúa
con los demás. Para la entrega se ejecutan los tres servidores y se muestran las tres especialidades.

## Reto de la ejecución de referencia

Los dos retos usan datos **ficticios del taller**, no de un cliente real:

- 50.000 sesiones de carrito al mes.
- Conversión base: 2,5 %.
- Ticket promedio: 35.000 CLP.
- Margen: 25 %.
- Escenarios relativos de conversión: conservador +2 %, base +5 %, optimista +10 %.
- Beneficio mensual sobre el **margen incremental**, no sobre la venta.

Beneficios mensuales: **218.750 / 546.875 / 1.093.750 CLP**.

| Conversación | Costo de Christopher | Decisión con el escenario conservador |
|---|---:|---|
| Paulina → Christopher → Paulina | **2.512.000 CLP** | Avanzar solo con alcance reducido/MVP y A/B; ROI 4,5 %, payback 11,48 meses. No escalar sin señal ≥2 % relativo. |
| Paulina → Rodrigo → Christopher → Paulina | **6.132.000 CLP** | No avanzar con el alcance completo; ROI −57,19 %, payback 28,03 meses. Reducirlo a fase 1 con reglas + A/B y decidir fase 2 con dato propio. |

La diferencia no es una contradicción: el segundo alcance incluye arquitectura, event bus,
experimentación A/B, logging y model serving; el primero es una intervención más acotada. El
documento de entrega explica la comparación en “Para comentar en clase”.

Los costos son **simulados** y pueden cambiar si se repite la conversación con otro alcance. La
documentación usa los de la última ejecución completa.

## Pruebas automáticas

Paulina:

```powershell
cd agente-paulina
.\.venv\Scripts\python.exe -m pytest tests -q
```

Resultado de referencia: `45 passed, 2 skipped`.

Christopher:

```powershell
cd agente-christopher
.\.venv\Scripts\python.exe -m pytest tests/test_costos.py -q
```

Resultado de referencia: `22 passed`. No requiere clave ni servidor.

Las pruebas de A2A de la base de viajes requieren un servidor levantado; no forman parte de la
conversación de Etapa 3.

## Empaquetar la entrega

Desde la raíz:

```powershell
.\scripts\empaquetar_entrega.bat
```

El script crea `dist/grupo-6-taller-a2a-entrega.zip` y excluye `.env`, `.venv/`,
`.langgraph_api/`, `.git/`, `dist/`, `__pycache__/`, `.pytest_cache/` y `.ipynb_checkpoints/`.
También verifica que el ZIP no contenga `.env` ni `.venv`; si los encuentra, falla.

El documento de entrega está en `docs/entrega/documento-entrega.md` e incluye la comparación de las
dos conversaciones para comentar en clase.

## Decisiones de la integración

1. **`src/agente_viajes/` se conserva** en los perfiles. La especificación de la Etapa 1 pide
   entregar la base tal cual. No participa en el catálogo de Etapa 3: el descubrimiento busca los
   grafos `agente_rodrigo`, `agente_christopher` y `agente_paulina`.
2. **Cada perfil conserva su notebook de Etapa 2.** El router dinámico vive en el notebook
   compartido de la raíz para no mezclar pruebas individuales con orquestación.
3. **Las tarjetas se actualizan con `assistants.update`.** El nombre y la descripción son los que
   el supervisor lee para elegir especialista. La operación es idempotente.
4. **Cada conversación usa un `contextId` UUID por agente.** Así cada uno recuerda su propio hilo y
   las respuestas del otro se pasan como datos entre etiquetas.
5. **Todo ciclo tiene tope.** Los agentes usan `recursion_limit`; el notebook espera tareas A2A con
   timeout y falla con un mensaje claro si un servidor no responde.
6. **Paulina no diseña arquitectura ni calcula costos.** Rodrigo aporta arquitectura; Christopher
   aporta costos; Paulina integra el caso de negocio, el impacto y la recomendación.
7. **El escenario conservador decide.** Base y optimista se muestran como sensibilidad, no como
   justificación para invertir.

## Evidencias de la entrega

- `notebooks/a2a-test.ipynb` ejecutado con **Run All**, sin errores, con:
  - las tres tarjetas actualizadas;
  - el descubrimiento mostrando `Rodrigo`, `Christopher` y `Paulina`;
  - las tres decisiones `[Supervisor]` correctas;
  - las dos conversaciones y sus cierres;
  - el resumen final y `Clientes A2A cerrados.`.
- `agente-rodrigo/notebooks/a2a-test.ipynb`, `agente-christopher/notebooks/a2a-test.ipynb` y
  `agente-paulina/notebooks/a2a-test.ipynb` ejecutados para la Etapa 2.
- `agente-paulina/tests` en verde y `agente-christopher/tests/test_costos.py` en verde.
- `docs/entrega/documento-entrega.md` con la comparación de las dos conversaciones.
- Capturas de respaldo de los cierres y de las tarjetas, si el grupo las incorpora al documento.

> No se versionan `.env`, `.venv/`, `.langgraph_api/`, cachés ni claves. La clave se queda en local.

## Rama de trabajo

Rama actual: `agente-paulina`. Los cambios de esta fase no se publican con `git push`; la entrega se
genera con el script de empaquetado.
