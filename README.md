# Grupo 6 · Taller A2A · Integración de dos especialistas

Taller 1 (Módulo 2): **mi agente especialista habla por A2A**. Este repositorio reúne dos perfiles
locales que se descubren y conversan por el protocolo A2A:

| Perfil | Especialidad | Carpeta | Servidor | Grafo |
|---|---|---|---|---|
| Rodrigo | Arquitectura backend y agentes de IA | `agente-rodrigo/` | `http://127.0.0.1:2025` | `agente_rodrigo` |
| Christopher | Costos de programación y software | `agente-christopher/` | `http://127.0.0.1:2026` | `agente_christopher` |

La Etapa 3 no importa código de un agente dentro del otro: el notebook orquestador los descubre por
HTTP/A2A, actualiza sus tarjetas y les pasa mensajes conservando un `contextId` UUID por agente.

## Mapa del repositorio

```text
grupo-6-taller-a2a/
├── README.md                          # Esta guía: estructura, arranque y evidencias.
├── .env.example                       # Plantilla de claves y URLs (el .env real no se versiona).
├── .gitignore                         # Ignora .env, .venv, cachés y docs locales.
│
├── agente-rodrigo/                    # Perfil 1 · mi-agente · servidor 2025.
│   ├── README.md                      # Identidad y arranque del perfil de Rodrigo.
│   ├── AGENTS.md                      # Reglas del taller para este perfil.
│   ├── blueprint.md                   # Diseño del agente (identidad, skills, límites).
│   ├── langgraph.json                 # Registra agente_rodrigo y la base agente_viajes.
│   ├── pyproject.toml                 # Dependencias y metadatos del proyecto.
│   ├── requirements.txt               # Dependencias para instalar el entorno.
│   ├── .env.example                   # Variables del perfil (sin claves).
│   ├── src/
│   │   ├── agente_rodrigo/            # Agente especialista de Rodrigo.
│   │   │   ├── prompts.py             # SYSTEM_RODRIGO: personalidad y reglas.
│   │   │   ├── herramientas.py        # @tool consultar_mis_apuntes y sus apuntes.
│   │   │   └── graph.py               # create_agent(...) + name="agente_rodrigo".
│   │   └── agente_viajes/             # Base del taller (vuelos y hoteles). SE CONSERVA.
│   ├── notebooks/
│   │   └── a2a-test.ipynb             # Etapa 2: preguntas, memoria y A2A + tarjeta.
│   ├── tests/                         # Pruebas del A2A nativo y de la base.
│   └── bruno/                         # Colección HTTP para tarjeta y message/send.
│
├── agente-christopher/                # Perfil 2 · segundo-agente · servidor 2026.
│   ├── README.md                      # Identidad, cálculos y arranque de Christopher.
│   ├── GUIA_CHRISTOPHER.md            # Guía de instalación y verificación.
│   ├── VERIFICACION.md                # Evidencias y límites de las pruebas.
│   ├── blueprint.md                   # Diseño del agente de costos.
│   ├── langgraph.json                 # Registra agente_christopher y la base agente_viajes.
│   ├── src/
│   │   ├── agente_christopher/        # Agente especialista de costos.
│   │   │   ├── prompts.py             # SYSTEM_CHRISTOPHER: identidad y reglas.
│   │   │   ├── herramientas.py        # Apuntes, tarifario simulado y cálculos.
│   │   │   └── graph.py               # create_agent(...) + name="agente_christopher".
│   │   ├── agente_viajes/             # Base del taller. SE CONSERVA.
│   │   └── consumidor/                # Material base conservado; fuera de la Etapa 3.
│   ├── notebooks/
│   │   └── a2a-test.ipynb             # Etapa 2 de Christopher + tarjeta.
│   ├── tests/
│   │   ├── test_costos.py             # 22 pruebas de cálculo, sin modelo ni servidor.
│   │   └── test_a2a_viajes.py         # Pruebas de la base de viajes.
│   └── bruno/                         # Colección HTTP original.
│
├── notebooks/
│   └── a2a-test.ipynb                 # ETAPA 3: descubrir, router y conversación de 3 turnos.
│
└── docs/
    └── taller-a2a-specificacion.png   # Especificación local (ignorada por git).
```

### Por qué cada notebook está donde está

- `agente-*/notebooks/a2a-test.ipynb` prueba **un solo perfil**: personalidad, conocimientos,
  memoria y envío A2A. Ahí vive la celda “Preparar mi tarjeta”.
- `notebooks/a2a-test.ipynb` es el **orquestador compartido** de la Etapa 3. Descubre los dos
  servidores, prueba el router con una pregunta de cada especialidad y ejecuta la conversación
  Rodrigo → Christopher → Rodrigo.
- El orquestador no importa `src/` de ninguno de los dos proyectos; solo usa HTTP/A2A. Por eso puede
  vivir en la raíz sin acoplarse a un perfil.

## Requisitos

- Python 3.11 o superior.
- Una `GOOGLE_API_KEY` válida para el modelo configurado.
- Dos terminales (una por servidor).
- El `.venv` de `agente-rodrigo` sirve para ejecutar el notebook orquestador. Cada perfil puede
  tener su propio `.venv` si se instala por separado.

## Configuración

1. Crea el entorno de Rodrigo si aún no existe:

   ```bash
   cd agente-rodrigo
   python3 -m venv .venv
   source .venv/bin/activate            # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copia las plantillas y completa la clave **solo en local**:

   ```bash
   cp .env.example .env                                   # notebook de Etapa 3
   cp agente-rodrigo/.env.example agente-rodrigo/.env     # servidor 2025
   cp agente-christopher/.env.example agente-christopher/.env  # servidor 2026
   # edita los tres .env y pega GOOGLE_API_KEY
   ```

   El `.env` de la raíz lo usa el notebook de Etapa 3. Cada servidor lee además su propio
   `agente-rodrigo/.env` o `agente-christopher/.env`.

3. Variables de la Etapa 3:

   | Variable | Valor por defecto | Uso |
   |---|---|---|
   | `A2A_URL_1` | `http://127.0.0.1:2025` | Servidor de Rodrigo. |
   | `A2A_GRAPH_1` | `agente_rodrigo` | Grafo que se busca en el servidor 1. |
   | `A2A_NOMBRE_1` | `Rodrigo` | Nombre que se publica en la tarjeta. |
   | `A2A_URL_2` | `http://127.0.0.1:2026` | Servidor de Christopher. |
   | `A2A_GRAPH_2` | `agente_christopher` | Grafo que se busca en el servidor 2. |
   | `A2A_NOMBRE_2` | `Christopher` | Nombre que se publica en la tarjeta. |

## Levantar los dos servidores

Terminal 1 · Rodrigo (2025):

```bash
cd agente-rodrigo
.venv/bin/langgraph dev --port 2025 --no-browser
```

Terminal 2 · Christopher (2026). Puedes usar el `.venv` de Rodrigo o crear el propio:

```bash
cd agente-christopher

# Opción rápida: reutilizar el entorno de Rodrigo.
../agente-rodrigo/.venv/bin/langgraph dev --port 2026 --no-browser

# Opción recomendada si vas a ejecutar su notebook de Etapa 2:
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/langgraph dev --port 2026 --no-browser
```

El notebook de Christopher verifica que el kernel sea su propio `.venv`; para la Etapa 3 puedes
usar el kernel de `agente-rodrigo/.venv` desde el notebook raíz.

Cada servidor publica su propia Agent Card y asigna un `assistant_id` UUID a cada grafo. El
`assistant_id` se descubre en tiempo de ejecución; no se escribe a mano en el notebook.

## Conectar con el agente de un compañero por Cloudflare

Si Christopher corre en otra máquina, **no levantes el servidor 2026**. Deja activo solo el
servidor de Rodrigo en 2025 y configura el perfil 2 en el `.env` de la raíz:

```dotenv
A2A_URL_2=https://assume-setup-see-total.trycloudflare.com
A2A_GRAPH_2=agente_christopher
A2A_NOMBRE_2=Christopher
A2A_ASSISTANT_ID_2=b71a76f3-1a4f-5263-a63d-b005bf9e46e1
A2A_GESTIONAR_TARJETA_2=0
```

- `A2A_ASSISTANT_ID_2` evita depender de `/assistants/search` en el servidor remoto.
- `A2A_GESTIONAR_TARJETA_2=0` indica que **no se modifica** la tarjeta de tu compañero.
- La descripción que usa el router sigue siendo la de Christopher; si quieres otra, define
  `A2A_DESCRIPCION_2`.
- El notebook descarga la tarjeta por HTTPS y, si la tarjeta anuncia `localhost`, reemplaza la
  dirección de la interfaz por la URL pública del túnel.

Comprueba la conexión antes de ejecutar el notebook:

```bash
./scripts/verificar_remoto.sh
```

Debe imprimir el `name`, la `description` y la interfaz JSONRPC. Si aparece
`Cloudflare error 1033`, el túnel no está activo o la URL cambió: pide la URL actual y actualiza
`A2A_URL_2`. Los quick tunnels de Cloudflare son efímeros y cambian al reiniciar `cloudflared`.

Después ejecuta `notebooks/a2a-test.ipynb` como siempre. El router llamará a Rodrigo en 2025 y a
Christopher por el túnel. También puedes levantar 2025 y 2026 en local y usar el bloque local de
`.env.example`; el notebook funciona en ambos modos.

Comprobación rápida de los servidores locales:

```bash
curl -s http://127.0.0.1:2025/ok
curl -s http://127.0.0.1:2026/ok

curl -s -X POST http://127.0.0.1:2025/assistants/search \
  -H 'Content-Type: application/json' -d '{"graph_id":"agente_rodrigo"}'
curl -s -X POST http://127.0.0.1:2026/assistants/search \
  -H 'Content-Type: application/json' -d '{"graph_id":"agente_christopher"}'
```

## Ejecutar los notebooks

### Etapa 2 · cada perfil por separado

- Abre `agente-rodrigo/notebooks/a2a-test.ipynb` contra el servidor 2025.
- Abre `agente-christopher/notebooks/a2a-test.ipynb` contra el servidor 2026. Si el kernel no tiene
  `A2A_PORT`, define `A2A_PORT=2026` antes de ejecutar.
- Ejecuta las celdas en orden y guarda las salidas. La última celda de cada notebook prepara la
  tarjeta que leerá el supervisor.

### Etapa 3 · conversación conjunta

1. Deja los dos servidores arriba.
2. Abre `notebooks/a2a-test.ipynb` con el kernel de `agente-rodrigo/.venv`.
3. Ejecuta todas las celdas en orden. El notebook:
   - actualiza las tarjetas de Rodrigo y Christopher;
   - descubre ambos agentes y crea un cliente A2A por especialista;
   - prueba el router con una pregunta de backend y una de costos;
   - ejecuta los tres turnos del reto del carrito de compras;
   - cierra las conexiones.
4. Guarda el notebook **sin limpiar las salidas**.

## Pruebas automáticas

```bash
cd agente-christopher

# Con el .venv propio de Christopher (recomendado):
.venv/bin/python -m pytest tests/test_costos.py -q

# Alternativa: reutilizar el entorno de Rodrigo.
../agente-rodrigo/.venv/bin/python -m pytest tests/test_costos.py -q
```

Resultado esperado: `22 passed`. No requiere clave ni servidor.

Las pruebas de A2A de la base de viajes requieren un servidor levantado y están pensadas para el
perfil que las ejecute; no forman parte de la conversación de Etapa 3.

## Decisiones de la integración

1. **`src/agente_viajes/` se conserva** en ambos perfiles. La especificación de la Etapa 1 pide
   entregar la base tal cual, salvo `src/swarm/`. No participa en el catálogo de Etapa 3: el
   descubrimiento solo busca los grafos `agente_rodrigo` y `agente_christopher`.
2. **Cada perfil conserva su notebook de Etapa 2.** El router dinámico se movió al notebook
   compartido de la raíz para no mezclar pruebas individuales con orquestación.
3. **Las tarjetas se actualizan con `assistants.update`.** El nombre y la descripción son los que
   el supervisor lee para elegir especialista. La operación es idempotente.
4. **La conversación usa un `contextId` UUID por agente.** Así cada uno recuerda su propio hilo y
   las respuestas del otro se pasan como datos entre etiquetas.
5. **Todo ciclo tiene tope.** Los agentes usan `recursion_limit`; el notebook espera tareas A2A con
   timeout y falla con un mensaje claro si un servidor no responde.

## Evidencias de la entrega

- `notebooks/a2a-test.ipynb` ejecutado, con:
  - las dos tarjetas actualizadas;
  - el descubrimiento mostrando `Rodrigo` y `Christopher`;
  - las líneas `[Supervisor]` de una pregunta por especialidad;
  - los tres turnos y la propuesta final.
- `agente-rodrigo/notebooks/a2a-test.ipynb` y `agente-christopher/notebooks/a2a-test.ipynb`
  ejecutados para la Etapa 2.
- `agente-christopher/tests/test_costos.py` en verde.
- Capturas o copias de las respuestas para el documento de entrega.

> No se versionan `.env`, `.venv/`, `.langgraph_api/` ni cachés. La clave se queda en local.

## Rama de trabajo

Los cambios de la integración se desarrollan en `integracion-agentes-v1`.
