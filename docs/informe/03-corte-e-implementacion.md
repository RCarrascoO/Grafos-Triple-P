# 3. Corte mínimo e implementación del algoritmo

> Apartado 3 del informe (tarea R10, redacta: Rodrigo Pedraza). Base: `docs/fase2-algoritmo.md` §6–§7 y código en `core/`.
> Notación: `docs/informe/00-notacion.md`.

## 3.1 Teorema de flujo máximo–corte mínimo

**Definición de corte.** Un **corte** $(S, T)$ en la red $G = (V, E)$ es una partición del conjunto de vértices tal que $V = S \cup T$, $S \cap T = \emptyset$, $s \in S$ y $t \in T$. Su capacidad es la suma de las capacidades de los arcos que cruzan desde $S$ hacia $T$:

$$c(S, T) = \sum_{\substack{(u,v)\in E \\ u\in S,\ v\in T}} c(u,v).$$

Los arcos orientados desde $T$ hacia $S$ no contribuyen a $c(S, T)$.

**Lema 1 (flujo a través de un corte).** Para todo flujo factible $x$ y todo corte $(S, T)$, el valor del flujo coincide con el flujo neto que cruza de $S$ hacia $T$ (Cormen et al., 2009, §26.2; Kleinberg y Tardos, 2006, §7.2):

$$\lvert x\rvert = \sum_{\substack{(u,v)\in E \\ u\in S,\ v\in T}} x(u,v) \;-\; \sum_{\substack{(v,u)\in E \\ v\in T,\ u\in S}} x(v,u).$$

Esta identidad se obtiene sumando las ecuaciones de conservación de flujo sobre todos los vértices de $S$: los arcos con ambos extremos en $S$ se cancelan entre sí y solo sobreviven los que cruzan la frontera entre $S$ y $T$.

**Lema 2 (dualidad débil).** Para todo flujo factible $x$ y todo corte $(S, T)$ se cumple $\lvert x\rvert \le c(S, T)$. En efecto, en el Lema 1 el primer término es a lo más $c(S, T)$ (por la restricción de capacidad $x(u,v) \le c(u,v)$) y el segundo término es no negativo ($x(v,u) \ge 0$).

**Teorema de flujo máximo–corte mínimo** (Ford y Fulkerson, 1956). Para un flujo factible $x$ en $G$, las tres afirmaciones siguientes son equivalentes:

1. $x$ es un flujo máximo ($\lvert x\rvert = \lvert x^*\rvert$).
2. La red residual $G_x$ no contiene ningún camino aumentante de $s$ a $t$.
3. Existe un corte $(S, T)$ tal que $\lvert x\rvert = c(S, T)$.

En particular, **el valor del flujo máximo es igual a la capacidad del corte mínimo**.

**Idea de la demostración:**

- *(1 $\Rightarrow$ 2)* Si existiera un camino aumentante en $G_x$ con cuello de botella $\delta > 0$, podría aumentarse el flujo hasta $\lvert x\rvert + \delta$, contradiciendo que $x$ es máximo.
- *(2 $\Rightarrow$ 3)* Sea $S$ el conjunto de vértices alcanzables desde $s$ en $G_x$ mediante arcos con $c_x > 0$, y sea $T = V \setminus S$. Como no hay camino aumentante, $t \notin S$ y por tanto $t \in T$. Además:
  - Todo arco $(u,v) \in E$ con $u \in S$ y $v \in T$ está **saturado** ($x(u,v) = c(u,v)$); si no lo estuviera, $c_x(u,v) > 0$ y $v$ sería alcanzable desde $s$.
  - Todo arco $(v,u) \in E$ con $v \in T$ y $u \in S$ lleva **flujo nulo** ($x(v,u) = 0$); si llevara flujo positivo, su arco inverso tendría $c_x(u,v) = x(v,u) > 0$ y $v$ sería alcanzable desde $s$.
  Por el Lema 1 resulta $\lvert x\rvert = c(S, T) - 0 = c(S, T)$.
- *(3 $\Rightarrow$ 1)* Por el Lema 2 ningún flujo factible puede superar $c(S, T)$ y ningún corte puede tener capacidad menor que $\lvert x\rvert$; en consecuencia, $x$ es un flujo máximo y $(S, T)$ es un corte mínimo.

**Teorema de integralidad** (Ford y Fulkerson, 1956; Ahuja, Magnanti y Orlin, 1993, cap. 6). Si todas las capacidades $c(u,v)$ son enteras, existe un flujo máximo $x^*$ con valores enteros en todos los arcos, y Edmonds–Karp lo encuentra porque parte de $x = 0$ y cada cuello de botella $\delta$ es entero. Esto garantiza coherencia con el modelo: los paquetes por hora no se fraccionan.

**Unicidad.** El valor $\lvert x^*\rvert$ y la capacidad mínima de corte son únicos, pero ni la asignación de flujo $x$ por arco ni el corte mínimo $(S, T)$ tienen por qué serlo (por ejemplo, la Figura 1 del enunciado admite dos cortes mínimos de capacidad 14). La construcción del paso *(2 $\Rightarrow$ 3)* implementada en el proyecto entrega siempre el corte mínimo con el conjunto $S$ más pequeño, es decir, el cuello de botella más cercano al origen.

## 3.2 Arquitectura del motor y representación de la red residual

El código se organiza en dos capas con dependencia unidireccional (`app.py` $\to$ `core/`):

- **`core/`** contiene la lógica algorítmica y de verificación utilizando **exclusivamente la biblioteca estándar de Python** (`collections.deque` y `json`), sin importar bibliotecas externas de grafos. Ninguna función del motor muta el diccionario `network` recibido.
- **`app.py`** implementa únicamente la interfaz interactiva con Streamlit (`requirements.txt` contiene una sola dependencia: `streamlit`) y dibuja la red mediante `st.graphviz_chart`, sin realizar cálculos de flujo ni de corte.

La red en memoria corresponde directamente al diccionario cargado desde JSON (`nodes`, `arcs`, `source`, `sink`, `profile`). Para el cálculo se consideran solo los arcos con `"active": true`, filtrados con `active_arcs(network)` en `core/network.py`.

**Red residual y prohibición de arcos recíprocos.** La red residual $G_x$ se representa como un diccionario de diccionarios `res`, donde `res[u][v]` almacena la capacidad residual $c_x(u,v)$. Que `res` cree un arco inverso `res[v][u]` para cada arco activo $(u,v) \in E$ **no contradice** la prohibición de arcos recíprocos del enunciado:

- La prohibición aplica al grafo original $G = (V, E)$, es decir, a las rutas físicas de transporte de sentido único.
- El arco inverso $(v,u)$ existe únicamente en la estructura auxiliar $G_x$ y representa la posibilidad algorítmica de reducir o cancelar flujo ya enviado por $(u,v)$.
- Precisamente porque $G$ no contiene arcos recíprocos, el par $(v,u)$ nunca colisiona con otro arco original en `res`. Así, cada par ordenado almacena un único entero, se conserva el invariante $c_x(u,v) + c_x(v,u) = c(u,v)$ en todo momento y al terminar se recupera el flujo original mediante $x(u,v) = c(u,v) - \text{res}[u][v]$.

**Pseudocódigo implementado:**

```text
EDMONDS-KARP(G, c, s, t):
    res ← BUILD-RESIDUAL(G, c)
    valor ← 0 ; iteraciones ← []
    mientras verdadero:
        P ← BFS-CAMINO(res, s, t)
        si P = NULO: terminar el bucle
        δ ← mín { res[u][v] : (u,v) arco consecutivo de P }
        para cada (u,v) consecutivo en P:
            res[u][v] ← res[u][v] − δ
            res[v][u] ← res[v][u] + δ
        valor ← valor + δ
        agregar (k, P, δ, valor) a iteraciones
    para cada arco activo (u,v): x(u,v) ← c(u,v) − res[u][v]
    devolver valor, x, iteraciones, res
```

## 3.3 Funciones implementadas (R1–R8)

Cada función cuenta con su *docstring* documentando propósito, entradas, salidas e invariantes. Las ocho funciones del motor se distribuyen en tres módulos de `core/`:

| Tarea | Archivo | Función | Descripción (propósito, entradas y salida) |
| --- | --- | --- | --- |
| R1 | `core/max_flow.py` | `build_residual(network)` | Recibe el diccionario `network` y construye la red residual inicial `res` para $x = 0$, inicializando una entrada para todos los vértices e insertando `res[u][v] = c(u,v)` y `res[v][u] = 0` por cada arco activo. |
| R2 | `core/max_flow.py` | `bfs_augmenting_path(res, s, t)` | Recibe la red residual `res` y los terminales `s`, `t`; ejecuta una BFS con `collections.deque` recorriendo `sorted(res[u])` solo por arcos con `res[u][v] > 0` y devuelve el camino más corto `[s, ..., t]` o `None`. |
| R3 | `core/max_flow.py` | `bottleneck(res, path)` | Recibe `res` y un camino aumentante `path`; devuelve el entero mínimo $\delta = \min \text{res}[u][v]$ entre los pares consecutivos del camino. |
| R4 | `core/max_flow.py` | `augment(res, path, delta)` | Recibe `res`, `path` y $\delta$; actualiza la residual in-place haciendo `res[u][v] -= delta` y `res[v][u] += delta` en cada par consecutivo del camino (no devuelve valor). |
| R5 | `core/max_flow.py` | `edmonds_karp(network, s, t)` | Recibe `network`, `s` y `t`; coordina el bucle de R1–R4 hasta agotar caminos aumentantes y devuelve `(value, flows, iterations, res)`, con `flows` definido para todos los arcos activos (incluidos los de flujo 0). |
| R6 | `core/min_cut.py` | `reachable_from(res, s)` | Recibe la residual final `res` y el origen `s`; realiza una BFS desde `s` por arcos con `res[u][v] > 0` y devuelve el conjunto `set` de vértices alcanzables $S$ (incluye a `s`). |
| R7 | `core/min_cut.py` | `min_cut(network, res, s)` | Recibe `network`, `res` y `s`; calcula $S = \text{reachable\_from}(\text{res}, s)$ y $T = V \setminus S$, identifica los arcos activos con origen en $S$ y destino en $T$, y devuelve `{"S", "T", "arcs", "capacity"}` con listas ordenadas. |
| R8 | `core/solver.py` | `solve(network, source, sink)` | Punto de entrada único del motor: valida los terminales (`E_UNKNOWN_NODE`, `E_ST_EQUAL`), invoca `edmonds_karp`, `min_cut` y `verify_all` (`core/verify.py`) y devuelve el diccionario de resultado completo del contrato. |

**Verificación independiente y casos borde.** `solve` delega las comprobaciones matemáticas a `verify_all` en `core/verify.py`, que recalcula restricciones de capacidad, conservación en cada vértice intermedio y la igualdad $\lvert x\rvert = c(S, T)$ usando únicamente `flows` y `network`, sin tocar `res`. Además, el motor maneja explícitamente los casos borde del contrato: terminales iguales o inexistentes, destino inalcanzable ($\lvert x\rvert = 0$, `iterations = []`, `cut["arcs"] = []`, $c(S, T) = 0$), arcos desactivados (excluidos de `res`, `flows` y del corte) y vértices sin arcos activos (permanecen en $T$, salvo si son $s$). Las pruebas automatizadas se ejecutan con `python -m unittest` y la interfaz con `streamlit run app.py` (ver instrucciones completas en `README.md`).

## 3.4 Registro de iteraciones de la red inicial

Al ejecutar `solve(network, "STG", "PMO")` sobre la red inicial del apartado 1 (`data/initial_network.json`, $\lvert V\rvert = 11$, $\lvert E\rvert = 19$), Edmonds–Karp encuentra el flujo máximo $\lvert x^*\rvert = 20$ paquetes por hora en **9 iteraciones**:

| $k$ | Camino aumentante en $G_x$ | Largo (arcos) | Cuello de botella $\delta$ | $\lvert x\rvert$ acumulado |
| --- | --- | --- | --- | --- |
| 1 | STG → CON → LAN → VAL → PMO | 4 | 5 | 5 |
| 2 | STG → CON → TEM → OSO → PMO | 4 | 1 | 6 |
| 3 | STG → RAN → CHI → LAN → VAL → PMO | 5 | 1 | 7 |
| 4 | STG → RAN → CHI → TEM → OSO → PMO | 5 | 3 | 10 |
| 5 | STG → RAN → CHI → TEM → VAL → PMO | 5 | 1 | 11 |
| 6 | STG → TAL → CON → TEM → VAL → PMO | 5 | 5 | 16 |
| 7 | STG → TAL → CON → TEM → VIL → OSO → PMO | 6 | 1 | 17 |
| 8 | STG → RAN → CHI → LAN → TEM → VIL → OSO → PMO | 7 | 2 | 19 |
| 9 | STG → TAL → CHI → LAN → TEM → VIL → OSO → PMO | 7 | 1 | 20 |

Se verifican directamente en la ejecución las propiedades teóricas del algoritmo: la longitud de los caminos aumentantes es no decreciente ($4, 4, 5, 5, 5, 5, 6, 7, 7$), cada cuello de botella cumple $\delta \ge 1$ y el flujo crece estrictamente hasta $\lvert x^*\rvert = 20$ paquetes por hora. Tras la novena iteración, `min_cut` obtiene sobre la red residual final:

- $S = \{\text{CHI}, \text{CON}, \text{LAN}, \text{RAN}, \text{STG}, \text{TAL}\}$,
- $T = \{\text{OSO}, \text{PMO}, \text{TEM}, \text{VAL}, \text{VIL}\}$,
- Arcos del corte de $S$ hacia $T$: $(\text{CHI}, \text{TEM})$, $(\text{CON}, \text{TEM})$, $(\text{LAN}, \text{TEM})$ y $(\text{LAN}, \text{VAL})$, todos saturados ($4/4$, $7/7$, $3/3$ y $6/6$),
- Capacidad del corte: $c(S, T) = 4 + 7 + 3 + 6 = 20 = \lvert x^*\rvert$, lo que certifica la optimalidad del flujo máximo hallado.
