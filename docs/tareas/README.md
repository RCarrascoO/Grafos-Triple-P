# Tareas por integrante

Cada tarea es pequeña: una función, un archivo de datos o una sección del informe. Tiene un **id**, lo que hay que crear, y un **"listo cuando"** verificable.

- [Rodrigo — motor de flujo máximo y corte mínimo](rodrigo.md)
- [Renato — validación, ediciones, interfaz y repositorio](renato.md)
- [Sebastián — verificación, pruebas, escenarios y QA](sebastian.md)
- Daniel — ver la tabla al final de este archivo.

Antes de empezar una tarea, leer el documento de fase que cita. Si se trabaja con un agente de IA, el agente debe seguir las reglas de `AGENTS.md`, en la raíz.

## Convenciones comunes (valen para todas las tareas)

1. **La red en memoria es el diccionario del JSON.** No hay clases. Todas las funciones reciben `network: dict` con las claves `nodes`, `arcs`, `source`, `sink`, `profile` (contrato: `docs/fase0-stack-y-contrato.md` §3).
2. **Arcos activos.** Para calcular se usa siempre `active_arcs(network)` de `core/network.py`. Los arcos con `"active": false` solo importan para las reglas de repetidos y recíprocos.
3. **Errores de validación.** Las funciones no lanzan excepciones: devuelven un **código** (`"E_LOOP"`, `"E_RECIPROCAL"`, …) o `None` si todo está bien. Los códigos están en `docs/fase0-stack-y-contrato.md` §5.
4. **Orden determinista.** Al recorrer vecinos o devolver listas de nodos/arcos, usar `sorted(...)`.
5. **Solo biblioteca estándar.** En `core/` y `tests/` no se importa nada externo. En `app.py` solo `streamlit`.
6. **Docstring obligatorio** en cada función: una línea de propósito, entradas y salida. Lo exige el enunciado.
7. **Nombres y firmas fijos.** Los nombres de función y sus firmas son los de estas tareas, porque otros integrantes dependen de ellos. Si hace falta cambiar una firma, avisar al equipo primero.

## Orden y fechas

| Etapa | Fechas | Qué se hace | Tareas |
| --- | --- | --- | --- |
| 1 | 16–17 nov | Base común | D1, D2, N1, S1 |
| 2 | 18–21 nov | Motor, verificación, validación e interfaz, en paralelo | R1–R7, S2–S6, N2–N9, N10–N12 |
| 3 | 22–23 nov | Integración, pruebas y escenarios | R8, S7–S12, N13–N18 |
| 4 | 24–26 nov | Informe, QA y ensayo | R9–R11, S13–S14, N19, D3–D6 |

Dependencias que bloquean:
- Todo `core/` necesita **D1 y D2** (`load_network`, `active_arcs`).
- **R8** (`solve`) necesita R5, R7 y **S6** (`verify_all`).
- **N13** en adelante (botón Calcular) necesita **R8**. Mientras tanto la interfaz se puede construir y probar dibujando la red sin resultados.
- **S8 y S11** (tests de ediciones y validación) necesitan N2–N8.
- **S12** (`mod1.json`, `mod2.json`) necesita que el equipo elija las dos modificaciones.

## Tareas de Daniel

| Id | Tarea | Listo cuando |
| --- | --- | --- |
| D1 | Crear `load_network(path) -> dict` en `core/network.py`. Abre el archivo con `encoding="utf-8"` y devuelve `json.load`. | Carga los tres JSON de `data/` y devuelve un `dict` con `nodes` y `arcs`. |
| D2 | Crear `active_arcs(network) -> list[dict]` en `core/network.py`. Devuelve los arcos con `active == True`. | En `figura1.json` devuelve 7 arcos; si se pone uno en `false`, devuelve 6. |
| D3 | Redactar el Apartado 1 del informe a partir de `docs/fase1-diseno-redes.md` §1. | Contiene $V$, $E$, tabla de $c$, tabla de grados, auditoría de restricciones e interpretación. |
| D4 | Escribir el glosario de notación común ($G$, $V$, $E$, $c$, $x$, $\lvert x\rvert$, $S$, $T$, $c(S,T)$, red residual) y revisar que las secciones de Rodrigo y Sebastián lo usen. | Las cinco secciones del informe usan los mismos símbolos que el enunciado. |
| D5 | Conseguir la aprobación del equipo de las decisiones D1–D3 de la Fase 0 y del frontend. | Decisión anotada en `docs/fase0-stack-y-contrato.md`. |
| D6 | Ensamblar el informe PDF y preparar su parte de la presentación (problema y modelo). | PDF completo revisado contra la rúbrica. |
