# Tareas de Rodrigo — motor de flujo máximo y corte mínimo

**Leer antes:** `docs/fase2-algoritmo.md` (teoría, pseudocódigo en §7.1, casos borde en §7.5) y las convenciones de `docs/tareas/README.md`.

**Archivos propios:** `core/max_flow.py`, `core/min_cut.py`, `core/solver.py`.
**Imports permitidos:** `from collections import deque` y `from core.network import active_arcs`. Nada más.

La red residual es un diccionario de diccionarios: `res[u][v]` es la capacidad residual de $u$ a $v$.

---

## Código

### R1 — `build_residual(network) -> dict`
Archivo: `core/max_flow.py`.
- Crea `res = {id: {} for cada nodo}` (todos los nodos, aunque no tengan arcos).
- Por cada arco activo $(u,v)$ con capacidad $c$: `res[u][v] = c` y `res[v][u] = 0`.

**Listo cuando:** con `figura1.json`, `res["O"]["A"] == 8`, `res["A"]["O"] == 0` y `res` tiene 6 claves.

### R2 — `bfs_augmenting_path(res, s, t) -> list | None`
Archivo: `core/max_flow.py`.
- BFS con `deque` desde `s`. Usa un diccionario `parent`.
- Solo avanza por `res[u][v] > 0`. Recorre `sorted(res[u])`.
- Si llega a `t`, reconstruye y devuelve el camino `[s, ..., t]`. Si no, devuelve `None`.

**Listo cuando:** en la residual inicial de `figura1.json` devuelve `["O", "A", "C", "T"]`. Con todas las salidas de `O` en 0 devuelve `None`.

### R3 — `bottleneck(res, path) -> int`
Archivo: `core/max_flow.py`. Devuelve el mínimo de `res[u][v]` sobre los pares consecutivos del camino.

**Listo cuando:** para el camino de R2 devuelve `5`.

### R4 — `augment(res, path, delta) -> None`
Archivo: `core/max_flow.py`. Por cada par consecutivo $(u,v)$: `res[u][v] -= delta` y `res[v][u] += delta`.

**Listo cuando:** tras aumentar 5 por `O-A-C-T`: `res["O"]["A"] == 3`, `res["A"]["O"] == 5`, `res["C"]["T"] == 0`.

### R5 — `edmonds_karp(network, s, t) -> tuple`
Archivo: `core/max_flow.py`. Bucle principal (pseudocódigo en `fase2-algoritmo.md` §7.1).
- Devuelve `(value, flows, iterations, res)`.
- `flows`: `{arc_id: c - res[u][v]}` para **cada** arco activo, incluidos los de flujo 0.
- `iterations`: lista de `{"k": int, "path": list, "bottleneck": int, "value_after": int}`.

**Listo cuando:**

| Red | `value` | Nº de iteraciones |
| --- | --- | --- |
| `figura1.json` (O → T) | 14 | 3 |
| `manual_case.json` (s → t) | 8 | 3, y la tercera es `s-c-a-b-d-t` con cuello de botella 3 |
| `initial_network.json` (STG → PMO) | 20 | 9 |

### R6 — `reachable_from(res, s) -> set`
Archivo: `core/min_cut.py`. BFS desde `s` por `res[u][v] > 0`. Devuelve el conjunto de nodos alcanzados (incluye `s`).

**Listo cuando:** con la residual final de `manual_case.json` devuelve `{"s", "a", "c"}`.

### R7 — `min_cut(network, res, s) -> dict`
Archivo: `core/min_cut.py`.
- `S = reachable_from(res, s)`; `T` = el resto de los nodos.
- `arcs` = ids de arcos activos con `from` en `S` y `to` en `T`.
- Devuelve `{"S": sorted, "T": sorted, "arcs": sorted, "capacity": suma de capacidades}`.

**Listo cuando:** en `initial_network.json` da `arcs == ["CHI-TEM", "CON-TEM", "LAN-TEM", "LAN-VAL"]` y `capacity == 20`. En `figura1.json` da `S == ["O"]` y `capacity == 14`.

### R8 — `solve(network, source, sink) -> dict`
Archivo: `core/solver.py`. **Necesita S6** (`verify_all` de Sebastián).
- Si `source == sink` devuelve `{"error": "E_ST_EQUAL"}`. Si alguno no es un nodo, `{"error": "E_UNKNOWN_NODE"}`.
- Llama a `edmonds_karp`, `min_cut` y `verify_all`.
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
