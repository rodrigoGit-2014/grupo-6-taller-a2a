# Documento de entrega · Grupo 6 · Taller A2A

**Taller 1 (Módulo 2): mi agente especialista habla por A2A**  
**Grupo 6** · Integrantes: Rodrigo, Constante, Christopher y Paulina  
**Repositorio:** `grupo-6-taller-a2a`  
**Ejecución de referencia:** 23 de octubre de 2026

### Ficha de identificación

| Identificación | Detalle |
|---|---|
| Grupo | **Grupo 6** |
| Integrantes | Rodrigo, Constante, Christopher y Paulina |
| Repositorio | `grupo-6-taller-a2a` |
| Ejecución de referencia | 23 de octubre de 2026 |
| Entrega | `dist/grupo-6-taller-a2a-entrega.zip` |

**Autoría de agentes**

| Agente | Responsable |
|---|---|
| `agente_rodrigo` | Rodrigo |
| `agente_christopher` | Christopher |
| `agente_paulina` | Paulina |

---

## 1. Resumen ejecutivo

El repositorio integra tres especialistas construidos como grafos LangGraph y expuestos por A2A:

| Perfil | Especialidad | Servidor | Grafo |
|---|---|---|---|
| Rodrigo | Arquitectura backend y agentes de IA | `http://127.0.0.1:2025` | `agente_rodrigo` |
| Christopher | Costos de programación y software | `http://127.0.0.1:2026` | `agente_christopher` |
| Paulina | Estrategia y valor de negocio de IA y datos | `http://127.0.0.1:2027` | `agente_paulina` |

El notebook raíz `notebooks/a2a-test.ipynb` descubre los tres servidores, actualiza sus tarjetas,
prueba un router supervisor y ejecuta dos conversaciones:

1. **Paulina → Christopher → Paulina:** caso de negocio, costo y retorno.
2. **Paulina → Rodrigo → Christopher → Paulina:** caso de negocio, arquitectura, costo y decisión.

La integración no importa código de un agente dentro de otro. Cada agente conserva su propio
`contextId` UUID y los aportes ajenos se pasan entre etiquetas como **datos**, no como instrucciones.

---

## 2. Objetivo y alcance

**Objetivo:** demostrar que tres especialistas pueden colaborar por A2A para resolver un caso de
negocio completo, sin acoplar sus implementaciones y sin que un agente invada el rol de otro.

**Caso ficticio del taller:** un e-commerce evalúa un recomendador de productos complementarios en
el carrito. Los datos son explícitos y ficticios; no corresponden a un cliente real:

| Dato de partida | Valor |
|---|---:|
| Sesiones de carrito al mes | 50.000 |
| Conversión base | 2,5 % |
| Ticket promedio | 35.000 CLP |
| Margen | 25 % |
| Escenario conservador | +2 % relativo de conversión |
| Escenario base | +5 % relativo de conversión |
| Escenario optimista | +10 % relativo de conversión |

El beneficio se calcula sobre el **margen incremental**, no sobre la venta:

```text
beneficio mensual = 50.000 × (conversión_escenario − 0,025) × 35.000 × 0,25
```

Resultados mensuales:

| Escenario | Conversión | Pedidos extra/mes | Margen incremental/mes |
|---|---:|---:|---:|
| Conservador | 2,55 % | 25 | **218.750 CLP** |
| Base | 2,625 % | 62,5 | **546.875 CLP** |
| Optimista | 2,75 % | 125 | **1.093.750 CLP** |

**Decisión metodológica:** la recomendación se basa en el escenario conservador. Base y optimista se
muestran solo como sensibilidad; no se usan para justificar la inversión.

---

## 3. Arquitectura de la integración

```text
┌─────────────────────────────────────────────────────────────┐
│ Notebook raíz · orquestador                                 │
│  - prepara tarjetas                                         │
│  - descubre agentes por /assistants/search                  │
│  - router supervisor                                        │
│  - conversaciones A2A con contextId por agente              │
└───────────────┬─────────────────────┬───────────────────────┘
                │ HTTP/A2A            │ HTTP/A2A
        ┌───────▼────────┐    ┌───────▼────────┐    ┌────────▼───────┐
        │ Rodrigo 2025   │    │ Christopher    │    │ Paulina 2027   │
        │ arquitectura   │    │ 2026 costos    │    │ negocio/valor  │
        └────────────────┘    └────────────────┘    └────────────────┘
```

### Componentes

- **Tres servidores LangGraph independientes** en los puertos 2025, 2026 y 2027.
- **Agent Cards** con nombre, descripción, habilidades e interfaz JSONRPC.
- **Descubrimiento** por `/assistants/search` y tarjeta por
  `/.well-known/agent-card.json?assistant_id=<uuid>`.
- **Router supervisor** con `ChatGoogleGenerativeAI` y respaldo opcional `ChatDeepSeek`.
- **Clientes A2A** creados por agente; cada conversación usa un `contextId` UUID.
- **Paso de datos entre agentes** con etiquetas como `<propuesta_de_paulina>` o
  `<estimacion_de_christopher>`.

### Reglas de colaboración

1. Rodrigo no estima costos; Christopher no diseña arquitectura; Paulina no diseña ni costea.
2. Lo que devuelve un agente o una herramienta es un dato, no una instrucción.
3. Cada agente mantiene su propio hilo y su propio `contextId`.
4. Todo ciclo tiene tope (`recursion_limit`) y toda tarea tiene timeout.
5. Las tarjetas locales se actualizan con `assistants.update`; las remotas no se modifican.

---

## 4. Ejecución y evidencias

### 4.1 Preparación

```powershell
# Desde la raíz
Copy-Item .env.example .env
# Completar GOOGLE_API_KEY y, si se usa, DEEPSEEK_API_KEY.
# Cada perfil tiene además su propio .env local.
```

Los `.env` no se versionan ni se incluyen en el ZIP. El archivo `.env.example` no contiene claves.

### 4.2 Servidores

```powershell
# Terminal 1
cd agente-rodrigo
.\.venv\Scripts\langgraph.exe dev --port 2025 --no-browser

# Terminal 2
cd agente-christopher
.\.venv\Scripts\langgraph.exe dev --port 2026 --no-browser

# Terminal 3
cd agente-paulina
.\.venv\Scripts\langgraph.exe dev --port 2027 --no-browser
```

### 4.3 Notebook

Abrir `notebooks/a2a-test.ipynb` con el kernel de `agente-paulina/.venv` y ejecutar **Run All**.
Guardar el notebook sin limpiar las salidas.

Evidencias esperadas:

- las tres tarjetas preparadas o tomadas como remotas;
- descubrimiento de `Rodrigo`, `Christopher` y `Paulina`;
- `[Supervisor] Rodrigo`, `[Supervisor] Christopher` y `[Supervisor] Paulina` en las tres preguntas
  del router, con `[OK]` en las tres;
- dos conversaciones completas;
- `RESUMEN ETAPA 3` con los tres perfiles y los turnos esperados;
- `Clientes A2A cerrados.` al final.

### 4.4 Pruebas

| Prueba | Comando | Resultado de referencia |
|---|---|---|
| Paulina · retorno, KPI y apuntes | `cd agente-paulina; .\.venv\Scripts\python.exe -m pytest tests -q` | `45 passed, 2 skipped` |
| Christopher · costos | `cd agente-christopher; .\.venv\Scripts\python.exe -m pytest tests/test_costos.py -q` | `22 passed` |

Las pruebas de cálculo no requieren modelo ni servidor.

### 4.5 Blueprints de los perfiles

| Perfil | Blueprint | Qué respalda |
|---|---|---|
| Rodrigo | [`agente-rodrigo/blueprint.md`](../../agente-rodrigo/blueprint.md) | Rol de arquitectura backend y agentes de IA, límites, herramientas y colaboración A2A. |
| Christopher | [`agente-christopher/blueprint.md`](../../agente-christopher/blueprint.md) | Rol de costos, tarifario simulado, partidas, supuestos y límites. |
| Paulina | [`agente-paulina/blueprint.md`](../../agente-paulina/blueprint.md) | Rol de estrategia y valor, KPIs, retorno, roadmap y límites. |

Los tres blueprints se incluyen en el ZIP de entrega y quedan enlazados desde este documento.

### 4.6 Evidencias por etapa

| Etapa | Evidencia | Dónde verla |
|---|---|---|
| 1. Agente especialista | Paquete propio por perfil, `langgraph.json` y pruebas. | `agente-*/src/agente_<perfil>/`, `agente-*/langgraph.json` |
| 2. Agente especialista | Notebook de Etapa 2 por perfil, tarjeta A2A y pruebas de herramientas. | `agente-*/notebooks/a2a-test.ipynb`, `agente-*/tests/` |
| 3. Integración A2A | Notebook raíz con **Run All**: descubrimiento, router 3/3, dos conversaciones y cierre. | `notebooks/a2a-test.ipynb` |

**Evidencia visual de la Etapa 1.** El arranque de cada servidor se regenera con `langgraph dev --port <puerto>`; los logs actuales muestran únicamente el grafo del perfil.

### 4.7 Ajustes realizados

- Se incorporó a Paulina como tercer perfil de la integración: puerto 2027, grafo `agente_paulina`, tarjeta, router y turno de cierre.
- Se reemplazó el reto anterior por un caso único de carrito: 50.000 sesiones/mes, conversión base de 2,5 %, ticket de 35.000 CLP y margen de 25 %.
- Paulina usa `evaluar_impacto_kpi` para conversión y ticket, y `calcular_retorno` en tres escenarios relativos (+2 %, +5 % y +10 %); la decisión se toma con el escenario conservador.
- Se agregó `CONTROLES_CARRITO` para evitar el error de factor 10 detectado en la primera ejecución del turno de equipo; después se repitió el **Run All** completo.
- La pregunta del router de Paulina se actualizó al caso del carrito y se quitaron de la celda 11 las cifras de retos anteriores.
- Se actualizaron el README raíz, los `.env.example` y la documentación para los tres perfiles. No se modificaron prompts.
- Se corrigió la presentación de `evaluar_impacto_kpi` para KPI fraccionarios: conserva hasta 6 decimales cuando el valor es menor que 1, en vez de mostrar 0,025 y 0,0255 como 0,03.
- Los costos finales de Christopher son **2.512.000 CLP** para la conversación de tres turnos y **6.132.000 CLP** para la de equipo; este documento usa esos valores.
- Se creó este documento y el script `scripts/empaquetar_entrega.bat`; el ZIP excluye `.env` y `.venv`.

---

## 5. Resultados de las dos conversaciones

### 5.1 Conversación de tres turnos · Paulina → Christopher → Paulina

**Flujo:**

1. Paulina define el caso, usa `evaluar_impacto_kpi` para conversión y ticket promedio, calcula los
   tres beneficios sobre margen y pide el costo a Christopher.
2. Christopher estima el costo total a 12 meses con su tarifario simulado.
3. Paulina usa `calcular_retorno` en los tres escenarios, compara ROI y payback y recomienda según el
   escenario conservador.

**Costo de Christopher:** **2.512.000 CLP a 12 meses** (2.200.000 iniciales + 312.000 recurrentes)  
**Decisión de Paulina:** avanzar solo con alcance reducido y validación temprana; no escalar sin una
señal de mejora de conversión de al menos +2 % relativo.

| Escenario | Beneficio/mes | Beneficio 12 meses | ROI 12 meses | Payback |
|---|---:|---:|---:|---:|
| **Conservador (+2 %)** | 218.750 | 2.625.000 | **+4,5 %** | **11,48 meses** |
| Base (+5 %) — sensibilidad | 546.875 | 6.562.500 | +161,25 % | 4,59 meses |
| Optimista (+10 %) — sensibilidad | 1.093.750 | 13.125.000 | +422,49 % | 2,30 meses |

**Lectura:** el conservador deja solo ~113.000 CLP de holgura sobre el costo a 12 meses; un uplift
levemente inferior a +2 % ya deja el caso en pérdida. Base y optimista muestran que la decisión es muy
sensible a la mejora real de conversión. Por eso la recomendación es una fase 1 acotada (MVP del
widget midiendo conversión), un A/B contra la línea base de 2,5 % y pedir a Christopher la alternativa
liviana que él mismo ofreció.

### 5.2 Conversación de equipo · cuatro turnos · Paulina → Rodrigo → Christopher → Paulina

**Flujo:**

1. Paulina define el caso y los KPIs, calcula los tres beneficios y pide la arquitectura.
2. Rodrigo propone arquitectura, datos, serving, observabilidad y medición del uplift con A/B.
3. Christopher estima el costo total a 12 meses del alcance completo.
4. Paulina usa `calcular_retorno` en los tres escenarios y decide según el conservador.

**Costo de Christopher:** **6.132.000 CLP a 12 meses** (5.820.000 iniciales + 312.000 recurrentes)  
**Decisión de Paulina:** no avanzar con el alcance completo; reducirlo a una fase 1 de reglas curadas
más plumbing de eventos y A/B, y decidir la fase 2 con dato propio.

| Escenario | Beneficio/mes | Beneficio 12 meses | ROI 12 meses | Payback | ¿Recupera en 12 meses? |
|---|---:|---:|---:|---:|---|
| **Conservador (+2 %)** | 218.750 | 2.625.000 | **−57,19 %** | **28,03 meses** | **No** |
| Base (+5 %) — sensibilidad | 546.875 | 6.562.500 | +7,02 % | 11,21 meses | Sí |
| Optimista (+10 %) — sensibilidad | 1.093.750 | 13.125.000 | +114,04 % | 5,61 meses | Sí |

**Lectura:** solo el escenario optimista es cómodo; incluso el base deja apenas +7,02 % de ROI a 12
meses, por lo que cualquier desviación (menos tráfico, canibalización, devoluciones o efecto novedad)
lo vuelve negativo. El costo recurrente es bajo; el problema es el costo inicial del alcance completo.
La recomendación es no comprometer los 6.132.000 CLP, reducir a fase 1 y pedir a Christopher la
variante "solo fase 1" que él mismo ofreció. Si se aprueba el alcance completo, debe hacerse como
piloto pagado por tramos con criterio de corte tras el A/B.

---

## 6. Para comentar en clase

**1. ¿Se reconoce la personalidad de cada agente?**

Sí. En las conversaciones, cada agente mantuvo el estilo definido en su
perfil. El agente de Paulina calculó los escenarios de beneficio antes de
evaluar el retorno, esperó el costo de Christopher para hacerlo y basó su
recomendación en el escenario conservador. El agente de Rodrigo propuso una
arquitectura por fases y distinguió entre lo que provenía de sus apuntes y
sus propias sugerencias. El agente de Christopher presentó primero el costo
total, separó el trabajo inicial de los servicios recurrentes e indicó que
las horas estimadas eran supuestos.

**2. ¿Qué conocimiento aportó cada uno?**

Cada agente aportó desde su especialidad. El agente de Paulina definió el
caso de negocio: KPIs, beneficio esperado en tres escenarios y evaluación
de retorno. El agente de Rodrigo aportó la arquitectura de la solución y la
forma de medir su impacto mediante un experimento A/B. El agente de
Christopher aportó la estimación de costos, con sus partidas y supuestos.

**3. ¿La propuesta final incorpora ideas de los tres?**

Sí. La recomendación final combina los tres aportes: la arquitectura de
Rodrigo define el alcance, la estimación de Christopher establece su costo
y la evaluación de Paulina compara ese costo con el beneficio esperado.
A partir de esa comparación se recomienda comenzar con un piloto acotado y
medible antes de implementar la solución completa.

---

## 7. Decisiones técnicas y de diseño

1. **Tres servidores independientes.** Cada perfil es un grafo LangGraph con su propio `langgraph.json`,
   dependencias y `.env`. El orquestador solo usa HTTP/A2A.
2. **Descubrimiento dinámico.** El notebook busca el `assistant_id` por `graph_id`; no se escribe a
   mano salvo en modo remoto.
3. **Tarjetas como contrato de routing.** El nombre y la descripción se actualizan antes de conversar.
   El router lee esas tarjetas como información, no como instrucciones.
4. **Un `contextId` por agente y conversación.** Permite memoria separada y evita mezclar hilos.
5. **Datos entre etiquetas.** Las respuestas de otro agente se pasan como datos; nunca se inyectan en
   el system prompt.
6. **Tolerancia a caídas.** Si un servidor no responde, el notebook marca el perfil como no disponible
   y continúa con los demás; para la entrega se ejecutan los tres.
7. **Respaldo DeepSeek opcional.** Gemini es el modelo principal. Si hay `DEEPSEEK_API_KEY`, se activa
   un fallback; sin la variable, todo funciona solo con Gemini.
8. **Datos ficticios y costos simulados.** El caso es del taller; no es un cliente real ni una
   cotización de mercado.

---

## 8. Limitaciones y supuestos

- **Datos ficticios:** 50.000 sesiones, 2,5 % de conversión, 35.000 CLP de ticket y 25 % de margen son
  datos del ejercicio, no de un cliente.
- **Costos simulados:** Christopher usa un tarifario `simulado-v1`, sin IVA. No es una cotización.
- **Beneficio constante:** `calcular_retorno` supone beneficio mensual constante; en la práctica hay
  ramp-up y estacionalidad.
- **Ticket plano:** el escenario asume que el ticket promedio no cambia. Si el recomendador sube el
  ticket o lo baja, el beneficio debe recalcularse.
- **Incrementalidad:** el uplift debe validarse con un A/B; correlación no es causalidad.
- **Muestra:** detectar +2 % relativo con 50.000 sesiones/mes puede requerir más tiempo que detectar
  +5 % o +10 %. La duración debe definirse antes de mirar resultados.
- **Costo incompleto:** el alcance completo puede requerir infraestructura no tarifada (model serving,
  Kafka gestionado, warehouse). Eso eleva el costo y empeora el payback.
- **Modelo:** Gemini puede fallar por cuota o saldo; en la ejecución de referencia devolvió
  `402 Payment Required` y DeepSeek respondió como respaldo.

---

## 9. Entrega y reproducibilidad

### Contenido del ZIP

El script `scripts/empaquetar_entrega.bat` genera `dist/grupo-6-taller-a2a-entrega.zip` con:

- `README.md`, `.env.example` y `.gitignore`;
- los tres perfiles (`agente-rodrigo/`, `agente-christopher/`, `agente-paulina/`);
- el notebook raíz ejecutado y los notebooks de Etapa 2;
- `docs/entrega/documento-entrega.md` y `documento-entrega.pdf`;
- `scripts/` y las pruebas;
- blueprints, README y AGENTS de cada perfil; el `blueprint.md` de Paulina también queda en la raíz del ZIP.

**Excluye:** `.env`, `.venv/`, `.langgraph_api/`, `.git/`, `dist/`, `__pycache__/`,
`.pytest_cache/` y `.ipynb_checkpoints/`. El script verifica que el ZIP no contenga `.env` ni
`.venv`; si los encuentra, falla.

### Reproducir la ejecución

1. Crear los entornos e instalar dependencias.
2. Copiar los `.env.example` a `.env` y completar las claves en local.
3. Levantar los tres servidores en 2025, 2026 y 2027.
4. Abrir `notebooks/a2a-test.ipynb` con el kernel de Paulina.
5. Ejecutar **Run All** y guardar las salidas.
6. Ejecutar las pruebas de Paulina y Christopher.
7. Generar el ZIP con `scripts/empaquetar_entrega.bat`.

### Checklist de entrega

- [x] Tres perfiles con tarjeta A2A y `assistant_id` descubierto.
- [x] Router 3/3 con `[Supervisor]` correcto.
- [x] Conversación de tres turnos ejecutada.
- [x] Conversación de equipo de cuatro turnos ejecutada.
- [x] Beneficio calculado sobre margen y con escenario conservador como decisión.
- [x] Costos de Christopher integrados en ambos cierres.
- [x] Notebook raíz con **Run All** y salidas coherentes.
- [x] Documento de entrega con comparación de las dos conversaciones.
- [x] Blueprints de los tres perfiles referenciados.
- [x] Evidencias por etapa y ajustes realizados documentados.
- [x] Script de empaquetado con exclusión de `.env` y `.venv`.
- [x] Evidencia de arranque descrita en la sección 4.6.
- [ ] Capturas de respaldo adicionales, si se requieren en el anexo.

---

## 10. Comentarios finales

Las dos conversaciones parten del mismo beneficio conservador (218.750 CLP/mes), pero el alcance y el costo cambian la recomendación: el alcance acotado se justifica con un ROI de +4,5 % y un payback de 11,48 meses, mientras que el alcance completo no se justifica con un ROI de −57,19 % y un payback de 28,03 meses. Por eso la propuesta final es avanzar solo con una fase 1 acotada, comprar aprendizaje con un A/B y no comprometer la plataforma completa sin evidencia propia.

| Conversación | Beneficio conservador | Costo | ROI conservador | Payback | Recomendación |
|---|---:|---:|---:|---:|---|
| Paulina → Christopher → Paulina | 218.750/mes | **2.512.000** | **+4,5 %** | **11,48 meses** | Avanzar solo con alcance reducido/MVP y A/B; no escalar sin señal ≥2 % relativo |
| Paulina → Rodrigo → Christopher → Paulina | 218.750/mes | **6.132.000** | **−57,19 %** | **28,03 meses** | No avanzar con el alcance completo; fase 1 con reglas + A/B y decidir fase 2 con dato propio |

---

## 11. Etapa 2 · Agente Paulina

Esta sección documenta la prueba individual del agente Paulina con `agente-paulina/notebooks/a2a-test.ipynb`. El notebook usa primero la API de LangGraph y luego repite una consulta por A2A; las respuestas se conservan tal como se obtuvieron en la ejecución de referencia.

### 11.1 Blueprint

| Aspecto | Definición |
|---|---|
| Rol y alcance | Hace: define el caso de negocio (problema, KPIs y beneficio esperado), evalúa el impacto con el KPI más relevante y, cuando hay costo y beneficio monetario confiables, el retorno; propone un roadmap por fases con quick wins. No hace: diseño de arquitectura (Rodrigo) ni cálculo de costos de desarrollo (Christopher). |
| Herramientas | `consultar_mis_apuntes`, `evaluar_impacto_kpi`, `calcular_retorno`. |
| Autonomía | Analiza, evalúa impactos y retornos, y recomienda prioridades. Puede proponer supuestos explícitos cuando falta un dato, sin presentarlos como cifras reales. No compra, contrata, paga ni ejecuta inversiones. |
| Cuándo pide ayuda | Pide beneficio, costo, horizonte o KPIs cuando faltan; deriva a Rodrigo si se requiere arquitectura y a Christopher si se requieren costos de desarrollo. |
| Dónde se ejecuta | `http://127.0.0.1:2027` · grafo `agente_paulina`. |

### 11.2 Respuestas de la prueba

#### Personalidad

**Pregunta:** Preséntate y cuéntame cómo me puedes ayudar.

**Respuesta:**

> Soy Paulina, especialista en estrategia y valor de negocio de IA y datos. Ayudo a convertir ideas técnicas en decisiones: qué problema resuelven, cómo se mide el éxito (mermas, tiempos, quiebres, errores, horas, satisfacción) y qué valor o retorno se espera.
>
> También armo roadmaps por fases partiendo por quick wins, con entregable y KPI de salida en cada una.
>
> No diseño arquitectura ni calculo costos de desarrollo; para eso derivo a Rodrigo y Christopher, aunque uso sus costos como dato para evaluar retorno.
>
> ¿Tienes una iniciativa en mente? Cuéntame el problema y los usuarios afectados y vemos el caso de negocio.

#### Conocimientos y skills

**Pregunta:** Usa el caso ficticio de tus apuntes para evaluar primero el impacto operacional y luego el retorno. Con `evaluar_impacto_kpi` mide los quiebres de stock: línea base 8 %, valor esperado 4 %, unidad %, `mejor_si` menor y sin `valor_unitario_clp`; la monetización se hace después con `calcular_retorno`. Después usa `calcular_retorno` con el costo del piloto (9.000.000 CLP) y el beneficio mensual del caso (1.200.000 CLP) a 12 meses. Consulta tus apuntes. Muestra la variación absoluta y porcentual del KPI, el beneficio acumulado, el ROI, los meses de recuperación y una conclusión breve. Declara los supuestos y recuerda que el caso es ficticio.

**Respuesta:**

> **Conclusión:** el piloto mejora el KPI a la mitad y se paga dentro del horizonte: recuperación en 7,5 meses y ROI de 60 % a 12 meses. Caso ficticio de taller, no experiencia real.
>
> **1) Impacto operacional (`evaluar_impacto_kpi`)**
> - KPI: quiebres de stock en productos de alta rotación
> - Línea base 8 % → esperado 4 %: variación absoluta **-4 puntos porcentuales**, variación relativa **-50 %** (mejora, porque bajar es bueno).
>
> **2) Retorno (`calcular_retorno`)**
> - Costo del piloto: 9.000.000 CLP
> - Beneficio mensual: 1.200.000 CLP → acumulado 12 meses: **14.400.000 CLP**
> - ROI del horizonte: **60 %** · Meses de recuperación: **7,5**
> - Contexto del caso: ventas perdidas estimadas 6.000.000 CLP/mes; se recupera 1.200.000 CLP/mes en las 10 tiendas del piloto.
>
> **Supuestos a validar (no confirmados)**
> - Beneficio mensual constante en los 12 meses, sin IVA ni financiamiento (supuesto de la herramienta).
> - Reducción de quiebres a la mitad como supuesto conservador del caso; el beneficio de 1.200.000 CLP/mes depende de que esa reducción se traduzca efectivamente en ventas recuperadas.
> - Calidad de datos de inventario: el aprendizaje del caso es que es el principal riesgo; conviene evaluar madurez de datos y medir línea base desde el día uno antes de comprometer plazos.
> - El costo de 9.000.000 CLP es el del caso ficticio; si Christopher entrega un costo real de desarrollo, se recalcula el retorno con ese dato.
> - Cifras del caso son ficticias y de referencia para el taller; no hay evidencia de cliente real.

**Herramientas observadas:** `consultar_mis_apuntes`, `evaluar_impacto_kpi`, `calcular_retorno`.

#### Memoria

**Mensaje inicial:** Mi objetivo para este proyecto es: Evaluar un piloto de pronóstico de demanda para reducir quiebres de stock en 10 tiendas de retail. Guárdalo como contexto para esta conversación.

**Respuesta inicial:**

> Anotado: piloto de pronóstico de demanda en 10 tiendas de retail, foco en reducir quiebres de stock.
>
> Para armarte un caso de negocio y un roadmap necesito tres datos: línea base de quiebres (por ejemplo, % de SKU-día sin stock hoy), meta esperada tras el piloto, y horizonte/usuarios afectados. ¿Los tienes?

**Pregunta de memoria:** ¿Qué objetivo te acabo de contar?

**Respuesta:**

> Me contaste: evaluar un piloto de pronóstico de demanda para reducir quiebres de stock en 10 tiendas de retail. Es el contexto con el que voy a trabajar en esta conversación.

### 11.3 Ajustes tras la prueba

Después de probar el agente se hicieron cinco ajustes. Primero, se retiró la mención de docencia del perfil para que la identidad se centre en consultoría, estrategia y datos. Segundo, se acortaron las respuestas iniciales a 5-6 líneas, dejando el detalle para las evaluaciones o para cuando se pida. Tercero, se reforzó que primero se evalúe el KPI operacional (mermas, tiempos, quiebres, errores, horas, satisfacción) y que ROI y payback se usen solo cuando existan costo y beneficio monetario confiables. Cuarto, `consultar_mis_apuntes` acepta temas válidos y sinónimos (`concepto`, `criterio`, `casos`, `caso de negocio`, `caso de uso`, `negocio`, `ejemplo`, `referencia`) además de los temas canónicos. Quinto, se corrigió la precisión de `evaluar_impacto_kpi` para KPI fraccionarios: conserva hasta 6 decimales cuando el valor absoluto es menor que 1, en vez de mostrar 0,025 y 0,0255 como 0,03. La prueba de regresión está en `agente-paulina/tests/test_impacto_kpi.py`. La nota del anexo sobre 2,625 % → 2,63 % corresponde a un redondeo de presentación a dos decimales en un valor mayor o igual a 1; el cálculo se hizo con 0,02625. La corrección de precisión aplica a los KPI fraccionarios menores que 1, que era el caso de 0,025 y 0,0255. Estos ajustes no cambian el alcance: Paulina sigue sin diseñar arquitectura ni calcular costos de desarrollo.

---

## Anexo A. Conversación de tres turnos · Paulina → Christopher → Paulina

Copia textual de la salida de la nueva ejecución del notebook raíz (23 de octubre de 2026). Se conservan las tablas y las cifras; solo se normalizó el espaciado de los encabezados. Contextos A2A: Paulina `5ddfbdd0-940a-4570-9103-a5ccd6630e58`; Christopher `064a7390-7e0b-4f3a-b56d-5094eccee6a6`.

### Turno 1 · Paulina define el caso

**Conclusión:** los tres escenarios mejoran la conversión y el beneficio mensual incremental de margen va de **218.750 a 1.093.750 CLP/mes**. Falta el costo de Christopher para poder hablar de ROI y payback.

**KPIs (`evaluar_impacto_kpi`):**
- Conversión conservador: 2,5 % → 2,55 % (+2,0 %, mejora).
- Conversión base: 2,5 % → 2,625 % (+5,0 %, mejora).
- Conversión optimista: 2,5 % → 2,75 % (+10,0 %, mejora).
- Ticket promedio: 35.000 → 35.000 CLP (0 %, sin cambio — se mantiene por supuesto).

**Beneficio mensual incremental (margen incremental, no venta ni margen total):**

| Escenario | Conversión | Pedidos extra/mes | Venta extra CLP/mes | Margen extra CLP/mes |
|---|---|---|---|---|
| Conservador | 0,0255 | 25 | 875.000 | 218.750 |
| Base | 0,02625 | 62,5 | 2.187.500 | 546.875 |
| Optimista | 0,0275 | 125 | 4.375.000 | 1.093.750 |

Cálculo: 50.000 × (conv. − 0,025) × 35.000 × 0,25. **Contrastado con tus controles: coincide en los tres escenarios** (usé 2,5 % = 0,025). Nota menor: la herramienta redondeó el 2,625 % a 2,63 % en el texto, pero el cálculo se hizo con 0,02625.

**Pendiente:** Christopher, necesitamos el **costo total a 12 meses** del recomendador para calcular beneficio acumulado, ROI y meses de recuperación con los tres beneficios mensuales ya fijados.

**Supuestos a validar:** conversión incremental atribuible al recomendador (sin canibalización ni efecto temporada); ticket promedio constante; margen 25 % constante; las mejoras son relativas sobre la base, no puntos porcentuales.

### Turno 2 · Christopher estima

**Costo total a 12 meses: 2.512.000 CLP sin IVA** (`costo_total_clp`).

Precios **SIMULADOS** (tarifario simulado-v1), estimación preliminar; no es oferta comercial.

| Concepto | Cantidad y unidad | Tarifa (CLP) | Subtotal (CLP) |
|---|---|---|---|
| Análisis de requerimientos | 12 hora | 18.000 | 216.000 |
| Desarrollo de interfaz | 32 hora | 20.000 | 640.000 |
| Desarrollo de lógica y datos | 44 hora | 22.000 | 968.000 |
| Pruebas funcionales | 16 hora | 16.000 | 256.000 |
| Configuración del despliegue | 6 hora | 20.000 | 120.000 |
| Alojamiento de aplicación | 12 mes | 15.000 | 180.000 |
| Dominio | 1 año | 12.000 | 12.000 |
| Licencia de herramienta | 12 mes | 10.000 | 120.000 |

**Desglose por naturaleza**
- **Costo inicial (trabajo, una vez): 2.200.000 CLP**
- **Servicios recurrentes 12 meses: 312.000 CLP** → alojamiento 15.000/mes, licencia 10.000/mes, dominio 12.000/año.

**Supuestos esenciales**
- Alcance: widget de complementos en el carrito con lógica de afinidad, integración al catálogo y registro de eventos para medir conversión; horas preliminares (12/32/44/16/6 h) a validar.
- Infraestructura, equipos y conectividad existentes: no se requiere router ni cableado adicional.
- Horizonte de servicios igual a 12 meses (dominio cubre 1 año), comparable con tus beneficios mensuales.
- El costo **no incluye** canibalización, temporada ni marketing; el beneficio de 218.750 / 546.875 / 1.093.750 CLP/mes queda como supuesto tuyo.

**Para tu ROI/payback (referencia)**: payback del costo inicial = 2.200.000 ÷ margen mensual → ~10,1 meses (conservador), ~4,0 (base), ~2,0 (optimista). El costo total de 12 meses (2.512.000) conviene usarlo para el ROI anual, no para el payback.

¿Quieres que compare esta versión con una alternativa más liviana (recomendador básico) para ver el efecto en el payback?

### Turno 3 · Paulina integra y decide

**Conclusión:** con el escenario conservador el proyecto **sí se recupera en 12 meses, pero por muy poco margen** (ROI 4,5 %, payback 11,5 meses). Recomiendo avanzar solo con alcance reducido y validando la mejora de conversión temprano; no comprometer el alcance completo confiando en base/optimista.

Costo usado: **2.512.000 CLP a 12 meses** (estimación simulada de Christopher, tarifario simulado-v1, sin IVA).

| Escenario | Beneficio mes | Beneficio 12 meses | ROI 12 m | Payback | Rol |
|---|---|---|---|---|---|
| Conservador | 218.750 | 2.625.000 | **4,5 %** | **11,48 meses** | base de la decisión |
| Base | 546.875 | 6.562.500 | 161,25 % | 4,59 meses | sensibilidad |
| Optimista | 1.093.750 | 13.125.000 | 422,49 % | 2,30 meses | sensibilidad |

**Lectura de negocio:** el conservador deja solo ~113.000 CLP de holgura sobre el costo en 12 meses. Cualquier desviación (menos sesiones, ticket menor, mejora de conversión menor a +2 %, o mayor esfuerzo de desarrollo) lo vuelve negativo. Base y optimista muestran que la decisión es muy sensible a la mejora real de conversión.

**Recomendación:** fase 1 acotada (MVP del widget midiendo conversión real), medir vs. línea base 2,5 % y decidir la ampliación con el KPI observado. Si no hay señal de mejora ≥2 % relativo, no escalar. Pidamos a Christopher la alternativa liviana que ofreció: bajar el costo inicial es la palanca más directa para hacer viable el conservador.

**Supuestos a validar (no confirmados):**
- Atribución: que el alza de conversión venga del recomendador y no de temporada, marketing o canibalización (Christopher tampoco lo incluye en el costo).
- 2,5 % de conversión base y 50.000 sesiones de carrito/mes reales y estables.
- Ticket 35.000 CLP y margen 25 % constantes; el margen no se erosiona por descuentos del complemento.
- Beneficio mensual constante desde el mes 1 (supuesto de la herramienta); en la práctica habrá rampa.
- Costo simulado preliminar, sin IVA: debe validarse antes de una decisión de inversión.
