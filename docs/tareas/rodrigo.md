# Tareas de Rodrigo — motor de flujo máximo y corte mínimo

**Leer antes:** `docs/fase2-algoritmo.md` (teoría, pseudocódigo en §7.1, casos borde en §7.5) y las convenciones de `docs/tareas/README.md`.

**Archivos propios:** `core/flujo_maximo.py`, `core/corte_minimo.py`, `core/resolvedor.py`.
**Imports permitidos:** `from collections import deque` y `from core.red import arcos_activos`. Nada más.

La red residual es un diccionario de diccionarios: `residual[u][v]` es la capacidad residual de $u$ a $v$.

---

## Código

### R1 — `construir_residual(red) -> dict`
Archivo: `core/flujo_maximo.py`.
- Crea `residual = {id: {} for cada nodo}` (todos los nodos, aunque no tengan arcos).
- Por cada arco activo $(u,v)$ con capacidad $c$: `residual[u][v] = c` y `residual[v][u] = 0`.

**Listo cuando:** con `figura1.json`, `residual["O"]["A"] == 8`, `residual["A"]["O"] == 0` y `residual` tiene 6 claves.

### R2 — `buscar_camino(residual, s, t) -> list | None`
Archivo: `core/flujo_maximo.py`.
- BFS con `deque` desde `s`. Usa un diccionario `parent`.
- Solo avanza por `residual[u][v] > 0`. Recorre `sorted(residual[u])`.
- Si llega a `t`, reconstruye y devuelve el camino `[s, ..., t]`. Si no, devuelve `None`.

**Listo cuando:** en la residual inicial de `figura1.json` devuelve `["O", "A", "C", "T"]`. Con todas las salidas de `O` en 0 devuelve `None`.

### R3 — `cuello_botella(residual, camino) -> int`
Archivo: `core/flujo_maximo.py`. Devuelve el mínimo de `residual[u][v]` sobre los pares consecutivos del camino.

**Listo cuando:** para el camino de R2 devuelve `5`.

### R4 — `aumentar(residual, camino, delta) -> None`
Archivo: `core/flujo_maximo.py`. Por cada par consecutivo $(u,v)$: `residual[u][v] -= delta` y `residual[v][u] += delta`.

**Listo cuando:** tras aumentar 5 por `O-A-C-T`: `residual["O"]["A"] == 3`, `residual["A"]["O"] == 5`, `residual["C"]["T"] == 0`.

### R5 — `edmonds_karp(red, s, t) -> tuple`
Archivo: `core/flujo_maximo.py`. Bucle principal (pseudocódigo en `fase2-algoritmo.md` §7.1).
- Devuelve `(valor, flujos, iteraciones, residual)`.
- `flows`: `{arc_id: c - residual[u][v]}` para **cada** arco activo, incluidos los de flujo 0.
- `iterations`: lista de `{"k": int, "path": list, "bottleneck": int, "value_after": int}`.

**Listo cuando:**

| Red | `value` | Nº de iteraciones |
| --- | --- | --- |
| `figura1.json` (O → T) | 14 | 3 |
| `manual_case.json` (s → t) | 8 | 3, y la tercera es `s-c-a-b-d-t` con cuello de botella 3 |
| `initial_network.json` (STG → PMO) | 20 | 9 |

### R6 — `alcanzables_desde(residual, s) -> set`
Archivo: `core/corte_minimo.py`. BFS desde `s` por `residual[u][v] > 0`. Devuelve el conjunto de nodos alcanzados (incluye `s`).

**Listo cuando:** con la residual final de `manual_case.json` devuelve `{"s", "a", "c"}`.

### R7 — `corte_minimo(red, residual, s) -> dict`
Archivo: `core/corte_minimo.py`.
- `S = alcanzables_desde(residual, s)`; `T` = el resto de los nodos.
- `arcs` = ids de arcos activos con `from` en `S` y `to` en `T`.
- Devuelve `{"S": sorted, "T": sorted, "arcs": sorted, "capacity": suma de capacidades}`.

**Listo cuando:** en `initial_network.json` da `arcs == ["CHI-TEM", "CON-TEM", "LAN-TEM", "LAN-VAL"]` y `capacity == 20`. En `figura1.json` da `S == ["O"]` y `capacity == 14`.

### R8 — `resolver(red, origen, destino) -> dict`
Archivo: `core/resolvedor.py`. **Necesita S6** (`verificar_todo` de Sebastián).
- Si `source == sink` devuelve `{"error": "E_ST_EQUAL"}`. Si alguno no es un nodo, `{"error": "E_UNKNOWN_NODE"}`.
- Llama a `edmonds_karp`, `corte_minimo` y `verificar_todo`.
- Devuelve exactamente el diccionario de `docs/fase0-stack-y-contrato.md` §4: `source`, `sink`, `max_flow_value`, `flows`, `iterations`, `cut`, `checks`.

**Listo cuando:** con las tres redes, `max_flow_value == cut["capacity"]` y los tres valores de `checks` (`capacity_ok`, `conservation_ok`, `duality_ok`) son `True`. Con un destino inalcanzable devuelve `max_flow_value == 0`, `iterations == []` y `cut["capacity"] == 0`.

---

## Informe y presentación

### R9 — Redactar la sección 2 del informe (investigación y selección)
Base: `docs/fase2-algoritmo.md` §2–§5. Debe incluir el funcionamiento de las dos alternativas, la tabla comparativa, la justificación y las citas.

**Listo cuando:** no afirma que DFS "no termina" ni que Edmonds–Karp es "más rápido" en esta red (ver "Lo que no se debe afirmar" en §5).

### R10 — Redactar la teoría del corte mínimo y la explicación de la implementación
Base: `docs/fase2-algoritmo.md` §6 y §7. Explicar cada función de R1–R8 en una o dos líneas y mostrar el log de iteraciones de la red inicial.

**Listo cuando:** la sección enlaza cada función con su archivo y explica por qué los arcos inversos no contradicen la prohibición de recíprocos.

### R11 — Confirmar las fuentes
Verificar autor, año, edición y páginas de las seis referencias de `docs/fase2-algoritmo.md` §9 con el ejemplar o la fuente original.

**Listo cuando:** cada cita del informe está confirmada o reemplazada por una que sí se consultó.
