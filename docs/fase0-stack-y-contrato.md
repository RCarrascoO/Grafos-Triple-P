# Fase 0 — Stack tecnológico, arquitectura y contrato de datos

> Estado: **propuesta para aprobación del equipo** (redacta: Daniel Prado). Una vez aprobada, este documento es vinculante para `core/`, `app.py` y `data/`.
> Fuente de verdad: `Proyecto 2 Simulador de una red de distribución de paquetes.pdf`.

---

## 1. Decisión de stack

**Python 3.11+ (probado en 3.13). Motor con la biblioteca estándar. Interfaz con Streamlit.**

Decisión del equipo (15 de noviembre de 2026): se eligió **Streamlit** sobre Tkinter y CustomTkinter.

| Criterio | Streamlit (elegido) | Tkinter / CustomTkinter |
| --- | --- | --- |
| Cantidad de código de interfaz | La menor: cada control es una línea (`st.selectbox`, `st.number_input`, `st.table`). | Más código de ventanas, marcos y eventos. |
| Defensa línea por línea | Fácil: el archivo se lee de arriba hacia abajo. | Más difícil: callbacks y geometría de widgets. |
| Dibujo de la red | `st.graphviz_chart` con un texto DOT: flechas, colores y etiquetas sin calcular geometría. | `Canvas`: hay que calcular coordenadas y bordes. |
| Instalación | `pip install streamlit` | Ninguna (Tkinter) |

**Qué exige el enunciado.** Prohíbe las bibliotecas "que realicen los cálculos algorítmicos solicitados" y permite las "bibliotecas para gráficos e interfaz". Streamlit es una biblioteca de interfaz. Graphviz, que usa `st.graphviz_chart`, solo decide dónde dibujar los nodos: no calcula flujos, caminos ni cortes.

**Reglas duras:**
- `core/` y `tests/` importan **solo la biblioteca estándar** (`collections`, `json`, `copy`, `itertools`, `random`, `unittest`).
- `app.py` importa `streamlit` y los módulos de `core/`. Nada más.
- Ningún archivo del repositorio importa `networkx`, `scipy`, `numpy`, `pandas` ni `igraph`. Streamlit instala `numpy` y `pandas` como dependencias propias, pero el código del proyecto no los usa. A `st.table` se le pasan listas de diccionarios.
- `requirements.txt` contiene una sola línea: `streamlit`.

---

## 2. Arquitectura

```
Grafos-Triple-P/
├── app.py                   # Interfaz Streamlit: streamlit run app.py
├── requirements.txt         # streamlit
├── core/                    # MOTOR PURO. Solo biblioteca estándar. No conoce a app.py.
│   ├── network.py           # Carga del JSON. La red en memoria ES el diccionario del JSON (sin clases)
│   ├── validation.py        # Invariantes topológicos y perfiles (initial / modified / manual)
│   ├── edits.py             # Ediciones validadas: agregar, cambiar capacidad, desactivar, eliminar
│   ├── max_flow.py          # Edmonds-Karp (BFS) + log de iteraciones
│   ├── min_cut.py           # Partición (S, T) por alcanzabilidad en la red residual
│   ├── verify.py            # Comprobaciones del apartado 5: capacidad, conservación, |x| = c(S,T)
│   └── solver.py            # solve(): une motor, corte y verificación en el resultado del §4
├── data/                    # Redes en formato JSON (contrato §3)
│   ├── figura1.json         # Red de la Figura 1 del PDF (|x| = 14)
│   ├── manual_case.json     # Caso de verificación manual, 6 vértices (|x| = 8)
│   ├── initial_network.json # Red principal, 11 vértices, 19 arcos (|x| = 20)
│   ├── mod1.json            # Modificación 1 (Sebastián + equipo)
│   └── mod2.json            # Modificación 2
├── tests/                   # unittest: python -m unittest
└── docs/                    # Documentos de diseño de cada fase y tareas
```

**Dependencia unidireccional:** `app.py → core`. El motor se puede probar y demostrar por consola sin abrir la interfaz.

### Responsables por módulo

| Módulo | Responsable | Revisa |
| --- | --- | --- |
| `core/network.py`, `data/initial_network.json`, este contrato | Daniel | Rodrigo |
| `core/max_flow.py`, `core/min_cut.py`, `core/solver.py` | Rodrigo | Sebastián |
| `core/validation.py`, `core/edits.py`, `app.py`, `requirements.txt`, README | Renato | Daniel |
| `core/verify.py`, `tests/`, `data/manual_case.json`, `mod1.json`, `mod2.json` | Sebastián | Rodrigo |

`validation.py` queda en `core/` aunque lo escriba Renato. Así el validador es testeable y los perfiles se aplican igual desde la UI y desde los tests.

---

## 3. Contrato de datos: archivo de red (`data/*.json`)

```json
{
  "schema_version": 1,
  "name": "Figura 1 del enunciado",
  "profile": "manual",
  "units": "paquetes/hora",
  "source": "O",
  "sink": "T",
  "nodes": [
    { "id": "O", "label": "Origen", "x": 80, "y": 300 }
  ],
  "arcs": [
    { "id": "O-A", "from": "O", "to": "A", "capacity": 8, "active": true }
  ]
}
```

| Campo | Tipo | Regla |
| --- | --- | --- |
| `schema_version` | int | Siempre `1` por ahora. |
| `profile` | `"initial"` \| `"modified"` \| `"manual"` | Indica qué reglas de tamaño se aplican (§5). |
| `source`, `sink` | id de nodo | Son los valores sugeridos. La UI permite cambiarlos. Deben cumplir `source ≠ sink`. |
| `nodes[].id` | string | Único, corto y sin espacios (`"O"`, `"C1"`). Es la clave en todo el sistema. |
| `nodes[].label` | string | Nombre logístico para el informe ("Centro Temuco"). |
| `nodes[].x`, `y` | int | Coordenadas sugeridas en un lienzo lógico de **1000 × 600**. La interfaz Streamlit **no las usa** (Graphviz ubica los nodos solo); quedan como referencia para las figuras del informe. |
| `arcs[].id` | string | Por convención `"<from>-<to>"`. Es único. |
| `arcs[].capacity` | int | $c(u,v) \in \{1,\dots,12\}$. Nunca 0: "cortar" una ruta se modela con `active: false`. |
| `arcs[].active` | bool | Un arco con `false` **no participa** en el flujo ni en el corte, pero sí **existe** para las reglas de repetidos y recíprocos (§5, decisión D1). |

$E$ (del informe) = conjunto de arcos con `active: true`.

---

## 4. Contrato de datos: resultado del motor

`core` expone una sola función de alto nivel. La UI y los tests consumen exactamente este diccionario:

```python
solve(network, source, sink) -> dict
```

```json
{
  "source": "O", "sink": "T",
  "max_flow_value": 14,
  "flows": { "O-A": 8, "O-B": 6, "A-C": 5, "A-D": 3, "B-D": 6, "C-T": 5, "D-T": 9 },
  "iterations": [
    { "k": 1, "path": ["O", "A", "C", "T"], "bottleneck": 5, "value_after": 5 }
  ],
  "cut": {
    "S": ["O"],
    "T": ["A", "B", "C", "D", "T"],
    "arcs": ["O-A", "O-B"],
    "capacity": 14
  },
  "checks": {
    "capacity_ok": true,
    "conservation_ok": true,
    "conservation_table": [ { "node": "A", "in": 8, "out": 8 } ],
    "duality_ok": true
  }
}
```

- `flows` contiene **todos los arcos activos originales**, incluidos los de flujo 0. Es la etiqueta $x(u,v)/c(u,v)$ que dibuja la UI.
- `iterations` es el insumo del Derivado 2.3, que sirve para contrastar con el cálculo manual de Sebastián.
- `checks` lo calcula `verify.py` con fórmulas independientes del algoritmo, es decir, no confía en el motor. Las tablas del apartado 5 del informe salen directamente de aquí.
- Los conjuntos y listas van **ordenados** para que la salida sea determinista y reproducible en las capturas.

> El ejemplo de `flows` e `iterations` es ilustrativo. El orden y los caminos exactos dependen del orden de vecinos en el BFS. El valor **14** y el corte $S=\{O\}$ sí son únicos para la Figura 1.

---

## 5. Reglas de validación (`core/validation.py`)

Cada regla devuelve un código estable. La UI muestra el mensaje y los tests verifican el código.

### Invariantes globales: se aplican a todo perfil y a toda edición

| Código | Regla | Formalización |
| --- | --- | --- |
| `E_LOOP` | Sin lazos | $(u,u) \notin E$ |
| `E_DUPLICATE` | Sin arcos repetidos | a lo sumo un arco $u \to v$ |
| `E_RECIPROCAL` | Sin arcos recíprocos | $(u,v) \in E \Rightarrow (v,u) \notin E$ |
| `E_CAPACITY` | Capacidad entera en rango | $c(u,v) \in \{1,\dots,12\}$, de tipo `int` (no `bool` ni `float`) |
| `E_UNKNOWN_NODE` | Los extremos existen | $u, v \in V$ |
| `E_ST_EQUAL` | Terminales distintos | $s \neq t$, ambos en $V$ |

### Solo perfil `initial`

| Código | Regla |
| --- | --- |
| `E_V_RANGE` | $10 \le \lvert V\rvert \le 12$ |
| `E_E_RANGE` | $15 \le \lvert E\rvert \le 20$, contando arcos activos |
| `E_ISOLATED` | $\deg^+(v) + \deg^-(v) \ge 1$ para todo $v$ |
| `E_PATHS` | Existen al menos 2 caminos dirigidos simples distintos de $s$ a $t$ |

### Solo perfil `manual`

`E_V_RANGE_MANUAL`: $4 \le \lvert V\rvert \le 6$.

### Perfil `modified`

Solo invariantes globales. El enunciado dice que "Las modificaciones podrán alterar el número inicial de arcos".

### Decisiones de diseño (requieren visto bueno del equipo)

- **D1 — Arcos desactivados.** Un arco desactivado sigue "ocupando" el par $\{u,v\}$:
  - No se puede crear $(u,v)$ (sería repetido) ni $(v,u)$ (sería recíproco).
  - Para invertir el sentido de una ruta hay que **eliminarla**, así que la UI ofrece *desactivar/reactivar* y también *eliminar*.
  - Con esto, reactivar un arco nunca puede romper un invariante.
- **D2 — "Caminos distintos".** La validación exige 2 caminos simples que difieran en al menos un arco (lectura literal del enunciado). Como buena práctica, la red inicial que diseñe Daniel tendrá además **2 caminos arco-disjuntos**. Esto equivale a $|x| \ge 2$ con capacidades unitarias y queda bien defendido en el informe.
- **D3 — Capacidad 0.** No se permite. Bajar una ruta a "0" es desactivarla, lo que respeta $c: E \to \{1,\dots,12\}$.

---

## 6. Representación interna del motor (guía para Rodrigo)

- **Red residual:** `residual: dict[str, dict[str, int]]`, con `residual[u][v]` = $c_f(u,v)$. Se construye desde los arcos activos:
  - Arco directo: $c_f(u,v) = c(u,v) - x(u,v)$.
  - Arco inverso: $c_f(v,u) = x(u,v)$.
- **Por qué el enunciado prohíbe arcos recíprocos:** como no existen $(u,v)$ y $(v,u)$ a la vez en $G$, el arco inverso residual de $(u,v)$ **nunca colisiona** con un arco original. Por eso basta un único valor por par ordenado, y el flujo de cada arco original se recupera como `x(u,v) = c(u,v) - residual[u][v]`. Conviene mencionarlo en el informe y en la defensa.
- **BFS:** `collections.deque` y un diccionario `parent`. Los vecinos se recorren en **orden lexicográfico** para que el resultado sea determinista.
- **Corte mínimo:** $S$ = vértices alcanzables desde $s$ en la red residual final con $c_f > 0$, $T = V \setminus S$. Los arcos del corte son los arcos activos $(u,v)$ con $u \in S$, $v \in T$.
- **Complejidad que se cita:** Edmonds-Karp $O(|V|\,|E|^2)$, Ford-Fulkerson-DFS $O(|E|\,|x^*|)$. Ojo: con capacidades enteras **ambos terminan**. El argumento a favor de EK es que su cota no depende de las capacidades y que usa el camino más corto en número de arcos. No es un argumento de terminación.

---

## 7. Casos de aceptación de la Fase 0

1. `data/figura1.json` cargado → `solve(·, "O", "T")` da `max_flow_value = 14`, `cut.S = ["O"]` y `cut.capacity = 14`.
2. Intentar agregar `A-O` sobre la Figura 1 → `E_RECIPROCAL`.
3. Intentar agregar `A-A` → `E_LOOP`. Capacidad `0`, `13` o `2.5` → `E_CAPACITY`.
4. `figura1.json` validado con perfil `initial` → falla con `E_V_RANGE` y `E_E_RANGE` (6 vértices y 7 arcos). Con perfil `manual` pasa.

## 8. Próximo paso

Aprobado este documento:
- **Fase 1:** Daniel diseña `data/initial_network.json` y Sebastián diseña `data/manual_case.json`.
- **En paralelo:** Renato crea el esqueleto de directorios y Rodrigo empieza `max_flow.py` contra `figura1.json`.
