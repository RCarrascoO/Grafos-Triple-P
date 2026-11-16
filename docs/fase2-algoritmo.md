# Fase 2 — Fundamento teórico y diseño modular del algoritmo

> Estado: **propuesta para revisión del equipo**. Responsable de la sección en el informe y del código: Rodrigo Pedraza.
> Depende de: `docs/fase0-stack-y-contrato.md` (contrato) y `docs/fase1-diseno-redes.md` (casos de prueba).
> Este documento es diseño. El código de `core/` se escribe después de aprobarlo.

---

## 1. El problema

Dada una red $G=(V,E)$ con capacidades $c: E \to \{1,\dots,12\}$, un origen $s$ y un destino $t$, se busca un flujo $x$ que cumpla:

- **Capacidad:** $0 \le x(u,v) \le c(u,v)$ para todo $(u,v) \in E$.
- **Conservación:** $\sum_{(u,v)\in E} x(u,v) = \sum_{(v,w)\in E} x(v,w)$ para todo $v \in V \setminus \{s,t\}$.

y que maximice $|x| = \sum_{(s,v)\in E} x(s,v) - \sum_{(u,s)\in E} x(u,s)$.

## 2. Conceptos comunes a ambas alternativas

**Red residual $G_x$.** Dado un flujo $x$, para cada arco $(u,v) \in E$ se definen dos capacidades residuales:

- Directa: $c_x(u,v) = c(u,v) - x(u,v)$. Es lo que aún cabe por la ruta.
- Inversa: $c_x(v,u) = x(u,v)$. Es lo que se puede **devolver**, es decir, flujo ya enviado que se puede cancelar.

**Camino aumentante.** Es un camino de $s$ a $t$ en $G_x$ que usa solo arcos con capacidad residual positiva. Su **cuello de botella** $\delta$ es la menor capacidad residual del camino. Enviar $\delta$ por él produce un nuevo flujo factible de valor $|x| + \delta$.

**Por qué hacen falta los arcos inversos.** Sin ellos el método es una heurística voraz que puede quedar atrapada. En el caso manual de la Fase 1, enviar 3 por $s \to b \to a \to t$ y 2 por $s \to b \to d \to t$ deja el flujo en 5 sin más caminos directos. El óptimo es 8 y solo se alcanza cancelando el flujo de $(b,a)$.

**Consecuencia de prohibir arcos recíprocos.** Como en $G$ nunca coexisten $(u,v)$ y $(v,u)$, el arco inverso residual de $(u,v)$ no se mezcla con ningún arco original. Por eso se cumple siempre $c_x(u,v) + c_x(v,u) = c(u,v)$, y el flujo se recupera como $x(u,v) = c(u,v) - c_x(u,v)$.

## 3. Alternativa A: método de Ford–Fulkerson con búsqueda en profundidad (DFS)

**Funcionamiento.** Parte de $x = 0$. Mientras exista un camino aumentante en $G_x$, lo encuentra con una DFS desde $s$ y aumenta el flujo en su cuello de botella. Termina cuando $t$ ya no es alcanzable.

**Características:**
- Ford y Fulkerson (1956) lo plantean como **método**: no fija cómo elegir el camino. La DFS es una elección posible.
- **Terminación:** con capacidades enteras, cada aumento suma al menos 1, así que termina en a lo más $|x^*|$ iteraciones ($x^*$ = flujo máximo). Con capacidades irracionales puede no terminar, pero ese caso no aplica a este proyecto.
- **Complejidad:** $O(|E| \cdot |x^*|)$. Depende del **valor** de las capacidades, no solo del tamaño de la red (es pseudo-polinomial).
- **Caminos:** la DFS puede encontrar caminos largos y con cuellos de botella pequeños. El resultado depende mucho del orden de exploración.

**Ejemplo del peor caso** (adaptado a capacidades de este proyecto). Red con arcos $(s,a)=12$, $(s,b)=12$, $(a,b)=1$, $(a,t)=12$, $(b,t)=12$. El flujo máximo es 24. Si la DFS elige alternadamente $s \to a \to b \to t$ y $s \to b \Rightarrow a \to t$ (devolviendo por el inverso de $(a,b)$), cada iteración aporta 1 y se necesitan **24 iteraciones**. Con BFS bastan **2**.

## 4. Alternativa B: algoritmo de Edmonds–Karp (BFS)

**Funcionamiento.** Es el método de Ford–Fulkerson con una regla fija: el camino aumentante se busca con **búsqueda en anchura (BFS)**, de modo que siempre se elige uno con el **menor número de arcos**.

**Características:**
- **Terminación:** garantizada para cualquier capacidad, incluso no entera.
- **Complejidad:** $O(|V| \cdot |E|^2)$. Depende solo del tamaño de la red.
- **Idea de la demostración** (Edmonds y Karp, 1972; Cormen et al., cap. 26):
  1. La distancia en arcos de $s$ a cada vértice en $G_x$ nunca disminuye de una iteración a otra.
  2. En cada aumento al menos un arco queda saturado ("crítico"). Para que el mismo arco vuelva a ser crítico, la distancia de $s$ a su extremo inicial debe haber crecido en al menos 2.
  3. Por lo tanto cada arco es crítico a lo más $|V|/2$ veces. Hay $O(|E|)$ arcos residuales, así que hay $O(|V||E|)$ aumentos, y cada BFS cuesta $O(|E|)$.
- **Caminos:** cortos y predecibles. Si los vecinos se recorren en orden fijo (lexicográfico), la ejecución es **determinista**.

## 5. Comparación y selección

| Criterio | Ford–Fulkerson + DFS | Edmonds–Karp (BFS) |
| --- | --- | --- |
| Elección del camino | El primero que encuentre la DFS | El más corto en número de arcos |
| Estructura auxiliar | Pila o recursión | Cola FIFO (`collections.deque`) |
| Complejidad | $O(\lvert E\rvert \cdot \lvert x^*\rvert)$ | $O(\lvert V\rvert \cdot \lvert E\rvert^2)$ |
| ¿Depende del valor de las capacidades? | Sí | No |
| Termina con capacidades enteras | Sí | Sí |
| Termina con capacidades reales cualesquiera | No siempre | Sí |
| Reproducibilidad para el cálculo manual | Baja: depende del orden de la DFS | Alta: caminos más cortos y orden fijo |
| Reutilización para el corte mínimo | Requiere otra búsqueda | La misma BFS entrega $S$ |

**Se selecciona Edmonds–Karp.** Justificación, en orden de importancia para este proyecto:

1. **Cota independiente de las capacidades.** La aplicación permite editar capacidades y agregar rutas. La garantía de Edmonds–Karp no cambia con esas ediciones.
2. **Determinismo y trazabilidad.** El apartado 5 exige contrastar el cálculo manual con el código. Con caminos más cortos y vecinos en orden lexicográfico, una persona puede reproducir a mano exactamente las iteraciones del programa.
3. **Una sola búsqueda para dos resultados.** La BFS final, la que ya no encuentra $t$, entrega directamente el conjunto $S$ del corte mínimo.
4. **Respaldo bibliográfico.** Es la variante que los textos estándar presentan con demostración completa de corrección y complejidad.

**Lo que no se debe afirmar.** A la escala de este proyecto ($|V| \le 12$, capacidades $\le 12$) ambos algoritmos son instantáneos. De hecho, en la red inicial la cota de DFS ($|x^*| = 20$ aumentos) es numéricamente menor que la cota teórica de Edmonds–Karp ($|V||E| \approx 209$ aumentos). En la práctica Edmonds–Karp usa 9. La elección se justifica por las garantías y la trazabilidad, **no** por velocidad medida ni porque DFS "no termine".

**Otras alternativas existentes** (se mencionan, no se implementan): el algoritmo de Dinic (1970), que agrupa los caminos más cortos en fases y logra $O(|V|^2|E|)$, y los algoritmos de preflujo push–relabel. Son más eficientes en redes grandes, pero su complejidad de implementación no se justifica para 12 vértices.

## 6. Teorema de flujo máximo – corte mínimo

**Definiciones.** Un corte $(S,T)$ es una partición $V = S \cup T$, $S \cap T = \varnothing$, con $s \in S$ y $t \in T$. Su capacidad es $c(S,T) = \sum_{(u,v)\in E,\ u\in S,\ v\in T} c(u,v)$.

**Lema 1 (flujo a través de un corte).** Para todo flujo $x$ y todo corte $(S,T)$:

$$|x| = \sum_{\substack{(u,v)\in E\\ u\in S,\ v\in T}} x(u,v) \;-\; \sum_{\substack{(v,u)\in E\\ v\in T,\ u\in S}} x(v,u).$$

Se obtiene sumando la conservación de flujo sobre los vértices de $S$.

**Lema 2 (dualidad débil).** $|x| \le c(S,T)$ para todo flujo y todo corte. Sale del Lema 1: el primer término es a lo más $c(S,T)$ y el segundo es no negativo.

**Teorema (Ford y Fulkerson, 1956).** Para un flujo $x$, las siguientes afirmaciones son equivalentes:

1. $x$ es un flujo máximo.
2. La red residual $G_x$ no contiene caminos aumentantes.
3. Existe un corte $(S,T)$ con $|x| = c(S,T)$.

En consecuencia, **el valor del flujo máximo es igual a la capacidad del corte mínimo**.

**Idea de la demostración.**
- (1 ⇒ 2): si hubiera un camino aumentante, se podría aumentar $|x|$, y $x$ no sería máximo.
- (2 ⇒ 3): sea $S$ el conjunto de vértices alcanzables desde $s$ en $G_x$ y $T = V \setminus S$. Como no hay camino aumentante, $t \in T$. Todo arco original de $S$ a $T$ está **saturado** (si no, su extremo final sería alcanzable). Todo arco original de $T$ a $S$ lleva **flujo 0** (si no, su arco inverso haría alcanzable al extremo en $T$). Por el Lema 1, $|x| = c(S,T) - 0$.
- (3 ⇒ 1): por el Lema 2 ningún flujo supera $c(S,T)$, así que $x$ es máximo. El mismo argumento muestra que el corte es mínimo.

**Cómo se usa en el proyecto.** El paso (2 ⇒ 3) **es** el procedimiento de `min_cut.py`: una búsqueda desde $s$ en la red residual final. El caso manual lo ilustra completo: los arcos $S \to T$ quedan en 5/5 y 3/3, y los arcos $T \to S$ quedan en 0/6 y 0/5.

**Teorema de integralidad.** Si todas las capacidades son enteras, existe un flujo máximo con todos los $x(u,v)$ enteros, y Ford–Fulkerson/Edmonds–Karp lo encuentran. Esto importa para el modelo: los paquetes no se fraccionan.

**Unicidad.** El valor del flujo máximo es único. El flujo por arco y el corte mínimo pueden no serlo. La búsqueda desde $s$ entrega siempre el corte mínimo con el $S$ más pequeño (el más cercano al origen).

## 7. Diseño modular

Reglas generales: solo biblioteca estándar; ninguna función modifica el objeto `network`; los vecinos se recorren en orden lexicográfico; todas las funciones llevan docstring con propósito, entradas, salidas e invariantes.

### 7.1 `core/max_flow.py`

| Función | Entrada | Salida | Responsabilidad |
| --- | --- | --- | --- |
| `build_residual(network)` | Red | `dict[str, dict[str, int]]` | Crea $G_x$ para $x=0$: `res[u][v] = c(u,v)` y `res[v][u] = 0` por cada arco **activo**. Incluye como clave a **todos** los nodos, aunque no tengan arcos activos. |
| `bfs_augmenting_path(res, s, t)` | Residual, terminales | `list[str]` o `None` | BFS sobre arcos con residual $> 0$. Devuelve el camino más corto $[s,\dots,t]$ o `None`. |
| `bottleneck(res, path)` | Residual, camino | `int` | $\delta = \min$ de los residuales del camino. |
| `augment(res, path, delta)` | Residual, camino, $\delta$ | `None` | Para cada $(u,v)$ del camino: `res[u][v] -= delta`, `res[v][u] += delta`. |
| `edmonds_karp(network, s, t)` | Red, terminales | `(value, flows, iterations, res)` | Bucle principal. `flows[arc_id] = c - res[u][v]` para cada arco activo. |

Pseudocódigo:

```
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
    para cada arco activo (u,v):  x(u,v) ← c(u,v) − res[u][v]
    devolver valor, x, iteraciones, res

BFS-CAMINO(res, s, t):
    padre ← { s: NULO } ; cola ← [s]
    mientras cola no vacía:
        u ← sacar el primero de cola
        para cada v en vecinos de u, en orden lexicográfico:
            si res[u][v] > 0 y v no está en padre:
                padre[v] ← u
                si v = t: reconstruir el camino con padre y devolverlo
                agregar v al final de cola
    devolver NULO
```

**Invariantes del bucle** (se comprueban en los tests):
- I1. Antes y después de cada iteración, $x$ es un flujo factible (capacidad y conservación).
- I2. Para cada arco activo $(u,v)$: `res[u][v] + res[v][u] == c(u,v)`.
- I3. `valor` es estrictamente creciente y cada $\delta \ge 1$.
- I4. La longitud de los caminos encontrados nunca disminuye (propiedad de Edmonds–Karp).

### 7.2 `core/min_cut.py`

| Función | Entrada | Salida | Responsabilidad |
| --- | --- | --- | --- |
| `reachable_from(res, s)` | Residual final, origen | `set[str]` | BFS sobre residual $> 0$. Devuelve $S$. |
| `min_cut(network, res, s)` | Red, residual final, origen | `dict` con `S`, `T`, `arcs`, `capacity` | $T = V \setminus S$. `arcs` = arcos activos con $u \in S$, $v \in T$. `capacity` = suma de sus capacidades. Listas ordenadas. |

### 7.3 `core/verify.py` (independiente del motor)

Recalcula todo a partir de `flows` y de la red, sin usar la red residual. Así un error del motor no puede ocultarse a sí mismo.

| Función | Comprueba |
| --- | --- |
| `check_capacity(network, flows)` | $0 \le x(u,v) \le c(u,v)$ y $x$ entero en cada arco activo. |
| `check_conservation(network, flows, s, t)` | Entrada = salida en cada $v \ne s,t$. Devuelve además la tabla `node / in / out`. |
| `flow_value(network, flows, s)` | $\lvert x\rvert$ según la fórmula del enunciado (salida neta de $s$). |
| `cut_capacity(network, S)` | $c(S,T)$ según la definición. |
| `verify_all(network, flows, S, s, t)` | Arma el bloque `checks` del resultado: las tres comprobaciones anteriores más `duality_ok` (`flow_value == cut_capacity`, $s \in S$, $t \notin S$). |

### 7.4 `core/solver.py`

`solve(network, source, sink) -> dict` valida los terminales, llama a `edmonds_karp`, `min_cut` y `verify`, y arma el diccionario de resultado del §4 de la Fase 0.

### 7.5 Casos borde que el motor debe manejar

| Caso | Comportamiento |
| --- | --- |
| $s = t$ o terminal inexistente | No llega al motor: `solve` devuelve el error `E_ST_EQUAL` / `E_UNKNOWN_NODE`. |
| $t$ no alcanzable desde $s$ | `max_flow_value = 0`, `iterations = []`, $S$ = alcanzables desde $s$, `cut.arcs = []`, `cut.capacity = 0`. Sigue cumpliéndose $\lvert x\rvert = c(S,T)$. |
| Arcos desactivados | No se cargan en la red residual. No aparecen en `flows` ni en el corte. |
| Nodo que quedó sin arcos activos | Sigue en $V$. Queda en $T$ (salvo que sea $s$). |
| Arcos que entran a $s$ o salen de $t$ | Permitidos. $\lvert x\rvert$ se calcula como salida **neta** de $s$. |
| Ciclos dirigidos | Permitidos (solo se prohíben los de longitud 2). No requieren tratamiento especial. |

## 8. Plan de pruebas (`tests/`, con `unittest`)

1. **Casos con resultado conocido** (valores en `docs/fase1-diseno-redes.md`):

   | Red | $\lvert x\rvert$ | Iteraciones | $S$ |
   | --- | --- | --- | --- |
   | `figura1.json` | 14 | 3 | {O} |
   | `manual_case.json` | 8 | 3 (la tercera usa un arco inverso) | {s, a, c} |
   | `initial_network.json` | 20 | 9 | {STG, RAN, TAL, CHI, CON, LAN} |

2. **Modificaciones candidatas:** sin (CON, TEM) → 13; $c(\text{CON},\text{TEM}) = 9$ → 21; con (CON, VAL) de capacidad 8 → 23.
3. **Invariantes I1–I4** verificados dentro de cada caso anterior.
4. **Casos borde** de §7.5.
5. **Oráculo independiente por fuerza bruta.** Para redes de hasta 12 vértices se pueden enumerar los $2^{|V|-2} \le 1024$ cortes posibles y tomar el de menor capacidad. Ese mínimo debe coincidir con `max_flow_value`. Se aplica a los tres JSON y a redes aleatorias válidas con semilla fija. Es código propio y no usa ninguna librería de grafos.

## 9. Fuentes

Antes de citarlas en el informe, el equipo debe confirmar edición y páginas con el ejemplar que tenga a mano.

- Ford, L. R., & Fulkerson, D. R. (1956). Maximal flow through a network. *Canadian Journal of Mathematics*, 8, 399–404.
- Edmonds, J., & Karp, R. M. (1972). Theoretical improvements in algorithmic efficiency for network flow problems. *Journal of the ACM*, 19(2), 248–264.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3.ª ed.), capítulo 26 "Maximum Flow". MIT Press. (En la 4.ª ed., 2022, es el capítulo 24.)
- Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). *Network Flows: Theory, Algorithms, and Applications*. Prentice Hall.
- Kleinberg, J., & Tardos, É. (2006). *Algorithm Design*, capítulo 7 "Network Flow". Addison-Wesley.
- Dinic, E. A. (1970). Algorithm for solution of a problem of maximum flow in networks with power estimation. *Soviet Mathematics Doklady*, 11, 1277–1280.

## 10. Preguntas probables del docente

| Pregunta | Respuesta corta |
| --- | --- |
| ¿Por qué BFS y no DFS? | La cota $O(\lvert V\rvert\lvert E\rvert^2)$ no depende de las capacidades, y los caminos más cortos hacen reproducible el cálculo manual. |
| ¿DFS no termina? | Con capacidades enteras sí termina. El problema es que su número de iteraciones depende de $\lvert x^*\rvert$. |
| ¿Para qué sirven los arcos inversos si el enunciado prohíbe los recíprocos? | La prohibición es sobre $G$. Los inversos existen solo en la red residual y representan flujo que se puede cancelar. |
| ¿Cómo sabe el programa que el flujo es máximo? | Porque exhibe un corte de igual capacidad, y ningún flujo puede superar la capacidad de un corte. |
| ¿El corte mínimo es único? | No siempre. La Figura 1 tiene dos. El programa entrega el más cercano al origen. |
| ¿Dónde está la librería de grafos? | No hay. `core/` solo importa la biblioteca estándar. |
