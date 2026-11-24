# 2. Investigación, comparación y selección del algoritmo

> Apartado 2 del informe (tarea R9, redacta: Rodrigo Pedraza). Base: `docs/fase2-algoritmo.md` §1–§5.
> Notación: `docs/informe/00-notacion.md`.

## 2.1 Formulación del problema de flujo máximo

Dada la red dirigida $G = (V, E)$ del apartado 1, con capacidades enteras $c: E \to \{1, 2, \dots, 12\}$, un origen $s \in V$ y un destino $t \in V$ ($s \ne t$), se busca un flujo $x$ que asigne a cada arco $(u,v) \in E$ una cantidad $x(u,v)$ de paquetes por hora cumpliendo dos restricciones:

- **Capacidad:** $0 \le x(u,v) \le c(u,v)$ para todo $(u,v) \in E$.
- **Conservación:** para todo vértice intermedio $v \in V \setminus \{s, t\}$,

$$\sum_{(u,v)\in E} x(u,v) = \sum_{(v,w)\in E} x(v,w).$$

El objetivo es maximizar el valor del flujo, definido como la cantidad neta que sale del origen:

$$\lvert x\rvert = \sum_{(s,v)\in E} x(s,v) - \sum_{(u,s)\in E} x(u,s).$$

Un flujo que alcanza el mayor valor posible se denota $x^*$, y su valor se escribe $\lvert x^*\rvert$.

## 2.2 Conceptos comunes: red residual y caminos aumentantes

Las estrategias clásicas basadas en caminos aumentantes comparten la noción de **red residual** $G_x$ asociada a un flujo factible $x$ (Ford y Fulkerson, 1956; Cormen et al., 2009, §26.2). Para cada arco original $(u,v) \in E$ se definen dos capacidades residuales:

- **Directa:** $c_x(u,v) = c(u,v) - x(u,v)$, que mide cuántos paquetes por hora caben todavía por $(u,v)$.
- **Inversa:** $c_x(v,u) = x(u,v)$, que mide cuánto flujo ya enviado por $(u,v)$ puede cancelarse o redirigirse.

Un **camino aumentante** es un camino simple de $s$ a $t$ en $G_x$ que utiliza únicamente arcos con capacidad residual positiva ($c_x > 0$). Su **cuello de botella** $\delta$ es la menor capacidad residual a lo largo del camino. Al aumentar el flujo en $\delta$ paquetes por hora sobre ese camino —sumando $\delta$ en los arcos directos y restando $\delta$ en los originales recorridos en sentido inverso— se obtiene un nuevo flujo factible de valor $\lvert x\rvert + \delta$.

**Por qué son indispensables los arcos inversos.** Sin arcos inversos, el procedimiento se reduce a una heurística voraz que puede quedar bloqueada en un flujo subóptimo. En el caso de verificación manual del apartado 5 (`data/manual_case.json`), si primero se envían 3 paquetes por hora por $s \to b \to a \to t$ y luego 2 paquetes por hora por $s \to b \to d \to t$, el flujo queda en $\lvert x\rvert = 5$ y no existe ningún otro camino directo desde $s$ hasta $t$ con capacidad disponible. Sin embargo, el óptimo es $\lvert x^*\rvert = 8$ paquetes por hora y solo se alcanza al cancelar el flujo previamente asignado a $(b,a)$ mediante su arco inverso en $G_x$.

**Consecuencia de prohibir arcos recíprocos en $G$.** Como el modelo prohíbe que coexistan $(u,v)$ y $(v,u)$ en $E$, el arco inverso residual de $(u,v)$ nunca coincide con un arco original de $G$. En consecuencia, se mantiene siempre la relación $c_x(u,v) + c_x(v,u) = c(u,v)$ y el flujo de cada ruta original se recupera directamente como $x(u,v) = c(u,v) - c_x(u,v)$.

## 2.3 Alternativa A: método de Ford–Fulkerson con búsqueda en profundidad (DFS)

**Funcionamiento.** Parte del flujo nulo ($x(u,v) = 0$ para todo $(u,v) \in E$). Mientras exista un camino aumentante de $s$ a $t$ en $G_x$, lo busca mediante una búsqueda en profundidad (DFS) desde $s$, calcula su cuello de botella $\delta$ y actualiza $x$ y $G_x$. El algoritmo finaliza cuando $t$ deja de ser alcanzable desde $s$ en $G_x$.

**Características principales:**

- **Método general:** Ford y Fulkerson (1956) lo formulan como un *método*, no como un algoritmo único, porque no imponen una regla para escoger el camino aumentante; emplear DFS es una instanciación concreta (Cormen et al., 2009, §26.2).
- **Terminación:** con capacidades enteras —como exige este proyecto— cada aumento aporta al menos $\delta \ge 1$ paquete por hora, de modo que **el método siempre termina** en a lo más $\lvert x^*\rvert$ iteraciones. Solo con capacidades irracionales pueden construirse redes en las que el método no termina, situación que no aplica a este modelo (Kleinberg y Tardos, 2006, §7.1).
- **Complejidad:** cada búsqueda en profundidad cuesta $O(\lvert E\rvert)$, por lo que la cota temporal es $O(\lvert E\rvert \cdot \lvert x^*\rvert)$. Esta cota es **pseudo-polinomial**, ya que depende del valor numérico de las capacidades y no solo del tamaño topológico de la red.
- **Dependencia del orden:** la DFS puede seleccionar caminos largos con cuellos de botella pequeños, y la secuencia de iteraciones cambia según el orden de exploración de los vecinos.

**Ejemplo del peor caso adaptado al rango del proyecto.** Considérese una red con arcos $(s,a)$, $(s,b)$, $(a,t)$ y $(b,t)$ de capacidad 12 paquetes por hora y un arco central $(a,b)$ de capacidad 1 paquete por hora (variante del ejemplo clásico de Cormen et al., 2009, §26.2). El flujo máximo es $\lvert x^*\rvert = 24$ paquetes por hora. Si la DFS elige alternadamente $s \to a \to b \to t$ y luego $s \to b \to a \to t$ (usando el arco inverso de $(a,b)$), cada iteración aporta $\delta = 1$ y se requieren **24 iteraciones**; con búsqueda en anchura bastan **2 iteraciones** ($s \to a \to t$ y $s \to b \to t$).

## 2.4 Alternativa B: algoritmo de Edmonds–Karp (BFS)

**Funcionamiento.** El algoritmo de Edmonds–Karp es una variante específica del método de Ford–Fulkerson que fija la regla de selección del camino aumentante: en cada iteración se busca un camino con el **menor número de arcos** en $G_x$ mediante una búsqueda en anchura (BFS) desde $s$ con una cola FIFO (Edmonds y Karp, 1972).

**Características principales:**

- **Terminación:** garantizada para cualquier capacidad positiva, entera o real (Edmonds y Karp, 1972).
- **Complejidad:** $O(\lvert V\rvert \cdot \lvert E\rvert^2)$, estrictamente polinomial en el tamaño de la red e independiente de las capacidades (Cormen et al., 2009, §26.2; Ahuja, Magnanti y Orlin, 1993, cap. 7).
- **Idea de la demostración de complejidad** (Edmonds y Karp, 1972; Cormen et al., 2009, §26.2):
  1. La distancia mínima en arcos desde $s$ hasta cada vértice $v \in V$ en $G_x$ nunca disminuye entre iteraciones.
  2. En cada aumento queda saturado al menos un arco del camino aumentante (llamado *arco crítico*), que desaparece de $G_x$. Para que ese mismo arco vuelva a aparecer y ser crítico otra vez, la distancia desde $s$ hasta su extremo inicial debe aumentar en al menos 2.
  3. Como la distancia máxima en un camino simple es menor que $\lvert V\rvert$, cada arco puede ser crítico a lo más $\lvert V\rvert / 2$ veces. Al existir $O(\lvert E\rvert)$ arcos residuales, el total de aumentos es $O(\lvert V\rvert \cdot \lvert E\rvert)$, y como cada BFS cuesta $O(\lvert E\rvert)$, la complejidad total es $O(\lvert V\rvert \cdot \lvert E\rvert^2)$.
- **Determinismo:** al recorrer los vecinos de cada vértice en orden lexicográfico fijo, la secuencia de caminos aumentantes, cuellos de botella y flujos intermedios es completamente determinista y reproducible.

## 2.5 Comparación y selección del algoritmo

| Criterio | Ford–Fulkerson + DFS | Edmonds–Karp (BFS) |
| --- | --- | --- |
| Elección del camino aumentante | El primero que encuentra la DFS | El más corto en número de arcos |
| Estructura auxiliar principal | Pila o recursión | Cola FIFO (`collections.deque`) |
| Complejidad temporal | $O(\lvert E\rvert \cdot \lvert x^*\rvert)$ | $O(\lvert V\rvert \cdot \lvert E\rvert^2)$ |
| ¿Depende del valor de las capacidades? | Sí (pseudo-polinomial) | No (fuertemente polinomial) |
| Terminación con capacidades enteras | Sí | Sí |
| Terminación con capacidades reales cualesquiera | No siempre | Sí |
| Reproducibilidad para verificación manual | Baja: sensible al orden de la DFS | Alta: caminos más cortos y orden fijo |
| Reutilización para el corte mínimo | Requiere definir una búsqueda adicional | La misma BFS sobre $G_x$ entrega $S$ |

**Algoritmo seleccionado: Edmonds–Karp.** La elección se justifica por cuatro motivos directamente ligados a los requisitos del proyecto:

1. **Garantía independiente de las capacidades.** La aplicación permite modificar capacidades y agregar nuevas rutas desde la interfaz. La cota $O(\lvert V\rvert \cdot \lvert E\rvert^2)$ de Edmonds–Karp no se degrada al aumentar las capacidades ni sufre el comportamiento oscilatorio del peor caso de DFS.
2. **Determinismo y trazabilidad para el contraste manual.** El apartado 5 exige contrastar el cálculo manual con la ejecución del código. Al elegir siempre caminos de menor longitud y recorrer vecinos en orden lexicográfico, cualquier integrante puede reproducir a mano las mismas iteraciones del programa.
3. **Integración natural con el corte mínimo.** La misma búsqueda en anchura desde $s$ en la red residual final —aquella que confirma que $t$ ya no es alcanzable— identifica directamente el conjunto $S$ del corte mínimo $(S, T)$.
4. **Respaldo bibliográfico sólido.** Es la variante de referencia en los textos clásicos de algoritmos y flujos en redes, con demostraciones completas de corrección y complejidad (Edmonds y Karp, 1972; Cormen et al., 2009; Kleinberg y Tardos, 2006; Ahuja, Magnanti y Orlin, 1993).

**Precisión sobre el alcance de la justificación.** A la escala de este proyecto ($\lvert V\rvert \le 12$ vértices y $c(u,v) \le 12$ paquetes por hora), tanto Ford–Fulkerson con DFS como Edmonds–Karp ejecutan de forma prácticamente instantánea. De hecho, en la red inicial el límite de aumentos de DFS ($\lvert x^*\rvert = 20$) es numéricamente menor que la cota asintótica $\lvert V\rvert \cdot \lvert E\rvert = 11 \times 19 = 209$ de Edmonds–Karp (aunque en la ejecución real Edmonds–Karp solo requiere 9 iteraciones). Por ello, la selección no se fundamenta en velocidad medida en esta red ni en una supuesta falta de terminación de DFS, sino en las garantías teóricas independientes de la capacidad, el determinismo y la trazabilidad.

**Otras alternativas existentes.** En la literatura existen algoritmos asintóticamente más eficientes para redes grandes, como el algoritmo de Dinic (1970), que construye redes por niveles y calcula flujos bloqueantes en $O(\lvert V\rvert^2 \cdot \lvert E\rvert)$, y los algoritmos de preflujo (*push–relabel*) (Ahuja, Magnanti y Orlin, 1993, cap. 7; Cormen et al., 2009, §26.4–§26.5). No se implementaron porque su mayor complejidad estructural no aporta ventajas prácticas con 12 vértices y dificulta el seguimiento iteración a iteración respecto del cálculo manual.
