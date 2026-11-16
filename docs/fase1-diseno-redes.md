# Fase 1 — Diseño formal de la red inicial y del caso de verificación manual

> Estado: **propuesta para revisión del equipo** (redacta: Daniel Prado).
> Datos: `data/initial_network.json` y `data/manual_case.json`, según el contrato de `docs/fase0-stack-y-contrato.md`.
> Notación: la del enunciado ($G=(V,E)$, $c$, $x$, $|x|$, $S$, $T$, $c(S,T)$).

**Sobre los valores "esperados" de este documento.** Los flujos máximos, iteraciones y cortes se calcularon con un prototipo desechable de Edmonds-Karp (BFS con vecinos en orden lexicográfico) que **no** forma parte del repositorio. Son la referencia contra la que se probará el motor de Rodrigo. El caso manual además está resuelto a mano en §2.

---

## 1. Red principal inicial $G_{\text{inicial}}$

### 1.1 Contexto del modelo

La red representa el corredor de distribución **Santiago → Puerto Montt**:
- Cada **vértice** es un centro logístico (una ciudad).
- Cada **arco** $(u,v)$ es una ruta de transporte con sentido único de $u$ a $v$.
- $c(u,v)$ es la cantidad máxima de paquetes por hora que admite esa ruta.
- Un **flujo** $x(u,v)$ es la cantidad de paquetes por hora que efectivamente se envía por la ruta.
- $|x|$ es el total de paquetes por hora que sale de Santiago y llega a Puerto Montt.

### 1.2 Conjunto de vértices: $|V| = 11$

$$V = \{\text{STG}, \text{RAN}, \text{TAL}, \text{CHI}, \text{CON}, \text{LAN}, \text{TEM}, \text{VIL}, \text{VAL}, \text{OSO}, \text{PMO}\}$$

| Id | Centro logístico | Rol |
| --- | --- | --- |
| STG | Santiago | **Origen** $s$ |
| RAN | Rancagua | Intermedio |
| TAL | Talca | Intermedio |
| CHI | Chillán | Intermedio |
| CON | Concepción | Intermedio |
| LAN | Los Ángeles | Intermedio |
| TEM | Temuco | Intermedio (nodo de mayor grado) |
| VIL | Villarrica | Intermedio |
| VAL | Valdivia | Intermedio |
| OSO | Osorno | Intermedio |
| PMO | Puerto Montt | **Destino** $t$ |

### 1.3 Conjunto de arcos y función de capacidad: $|E| = 19$

| # | Arco $(u,v)$ | $c(u,v)$ | | # | Arco $(u,v)$ | $c(u,v)$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (STG, RAN) | 10 | | 11 | (LAN, TEM) | 3 |
| 2 | (STG, TAL) | 12 | | 12 | (LAN, VAL) | 6 |
| 3 | (STG, CON) | 6 | | 13 | (TEM, VIL) | 5 |
| 4 | (RAN, CHI) | 7 | | 14 | (TEM, VAL) | 6 |
| 5 | (TAL, CHI) | 5 | | 15 | (TEM, OSO) | 4 |
| 6 | (TAL, CON) | 6 | | 16 | (VIL, OSO) | 5 |
| 7 | (CHI, LAN) | 8 | | 17 | (VAL, OSO) | 3 |
| 8 | (CHI, TEM) | 4 | | 18 | (VAL, PMO) | 12 |
| 9 | (CON, LAN) | 5 | | 19 | (OSO, PMO) | 11 |
| 10 | (CON, TEM) | 7 | | | | |

$c: E \to \{1,\dots,12\}$. El mínimo usado es 3 y el máximo es 12.

### 1.4 Auditoría de las restricciones del enunciado

| Restricción | Verificación | Cumple |
| --- | --- | --- |
| $10 \le \lvert V\rvert \le 12$ | $\lvert V\rvert = 11$ | Sí |
| $15 \le \lvert E\rvert \le 20$ | $\lvert E\rvert = 19$ | Sí |
| $c(u,v) \in \{1,\dots,12\}$ | Todas las capacidades son enteras y están entre 3 y 12 | Sí |
| Sin lazos | Ningún arco tiene la forma $(u,u)$ | Sí |
| Sin arcos repetidos | Los 19 pares ordenados son distintos | Sí |
| Sin arcos recíprocos | Para ningún $(u,v) \in E$ existe $(v,u) \in E$. La red es acíclica: todos los arcos van de norte a sur. | Sí |
| Ningún vértice aislado | Tabla de grados (abajo): $\deg^+(v)+\deg^-(v) \ge 2$ para todo $v$ | Sí |
| $s \ne t$ y al menos 2 caminos dirigidos distintos | Ver §1.5 | Sí |

**Tabla de grados** ($\deg^+$ = arcos que salen, $\deg^-$ = arcos que entran):

| $v$ | STG | RAN | TAL | CHI | CON | LAN | TEM | VIL | VAL | OSO | PMO | Suma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\deg^+(v)$ | 3 | 1 | 2 | 2 | 2 | 2 | 3 | 1 | 2 | 1 | 0 | 19 |
| $\deg^-(v)$ | 0 | 1 | 1 | 2 | 2 | 2 | 3 | 1 | 2 | 3 | 2 | 19 |
| Total | 3 | 2 | 3 | 4 | 4 | 4 | 6 | 2 | 4 | 4 | 2 | 38 |

Comprobación: $\sum \deg^+ = \sum \deg^- = |E| = 19$.

### 1.5 Origen, destino y caminos

$s = \text{STG}$, $t = \text{PMO}$. Hay muchos caminos dirigidos de $s$ a $t$. Basta exhibir dos que **no comparten ningún arco** (ni vértices intermedios):

- $P_1$: STG → CON → LAN → VAL → PMO
- $P_2$: STG → RAN → CHI → TEM → OSO → PMO

Como son arco-disjuntos, son distintos bajo cualquier lectura de "caminos distintos" (decisión D2 de la Fase 0).

### 1.6 Resultado esperado (referencia para el motor)

- **Flujo máximo:** $|x| = 20$ paquetes/hora.
- **Corte mínimo:** $S = \{\text{STG}, \text{RAN}, \text{TAL}, \text{CHI}, \text{CON}, \text{LAN}\}$, $T = \{\text{TEM}, \text{VIL}, \text{VAL}, \text{OSO}, \text{PMO}\}$.
- **Arcos del corte:** (CHI, TEM), (CON, TEM), (LAN, TEM), (LAN, VAL).
- $c(S,T) = 4 + 7 + 3 + 6 = 20 = |x|$. Este corte mínimo es **único**.

**Interpretación:** el cuello de botella no está en Santiago (de donde pueden salir $10+12+6 = 28$) ni en Puerto Montt (donde pueden entrar $12+11 = 23$). Está en el **paso de la zona del Biobío hacia La Araucanía y Los Ríos**: las cuatro rutas que cruzan hacia Temuco y Valdivia suman solo 20.

**Flujo de referencia** (el que produce Edmonds-Karp con orden lexicográfico; cualquier flujo factible de valor 20 es igualmente máximo):

| Arco | $x/c$ | | Arco | $x/c$ | | Arco | $x/c$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| (STG, RAN) | 7/10 | | (CHI, TEM) | 4/4 | | (TEM, VAL) | 6/6 |
| (STG, TAL) | 7/12 | | (CON, LAN) | 5/5 | | (TEM, OSO) | 4/4 |
| (STG, CON) | 6/6 | | (CON, TEM) | 7/7 | | (VIL, OSO) | 4/5 |
| (RAN, CHI) | 7/7 | | (LAN, TEM) | 3/3 | | (VAL, OSO) | 0/3 |
| (TAL, CHI) | 1/5 | | (LAN, VAL) | 6/6 | | (VAL, PMO) | 12/12 |
| (TAL, CON) | 6/6 | | (TEM, VIL) | 4/5 | | (OSO, PMO) | 8/11 |
| (CHI, LAN) | 4/8 | | | | | | |

El algoritmo llega a este flujo en 9 iteraciones. Valor neto en el origen: $7+7+6 = 20$.

### 1.7 Por qué esta red sirve para las modificaciones (adelanto de la Fase 3)

Son candidatas para que Sebastián y el equipo elijan las dos configuraciones modificadas. Los valores vienen del mismo prototipo:

| Modificación candidata | $\lvert x\rvert$ | Qué pasa con el corte |
| --- | --- | --- |
| Desactivar (CON, TEM) | 13 | El corte conserva los mismos conjuntos $S$ y $T$, pero pierde su arco más grande: $4+3+6 = 13$. |
| Subir $c(\text{CON},\text{TEM})$ de 7 a 9 (o más, hasta 12) | 21 | El flujo solo sube en 1, porque el cuello de botella **se desplaza** a las salidas de Temuco y Los Ángeles. Aparece más de un corte mínimo. |
| Agregar la ruta (CON, VAL) con capacidad 8 | 23 | El cuello de botella se va al final: el corte pasa a ser $T = \{\text{PMO}\}$, con arcos (VAL, PMO) y (OSO, PMO), $12+11 = 23$. |

---

## 2. Caso de verificación manual $G_{\text{test}}$

### 2.1 Definición

$V = \{s, a, b, c, d, t\}$ ($|V| = 6$), origen $s$, destino $t$, $|E| = 8$:

| Arco | $(s,b)$ | $(s,c)$ | $(b,a)$ | $(b,d)$ | $(c,a)$ | $(d,c)$ | $(a,t)$ | $(d,t)$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $c$ | 5 | 7 | 6 | 6 | 5 | 5 | 3 | 9 |

Cumple los invariantes: sin lazos, sin repetidos, sin recíprocos y con capacidades en $\{1,\dots,12\}$.

**Por qué se eligió este caso.** Es pequeño (3 iteraciones), pero en la tercera el algoritmo necesita **devolver flujo por un arco inverso de la red residual**. Así el caso prueba la parte más delicada del motor, que es la cancelación de flujo. Además, su topología es distinta a la de la Figura 1 del enunciado.

### 2.2 Resolución a mano (Edmonds-Karp, vecinos en orden alfabético)

Notación: $c_f$ es la capacidad residual. Al enviar $\delta$ por un arco $(u,v)$, $c_f(u,v)$ baja en $\delta$ y el arco inverso $c_f(v,u)$ sube en $\delta$.

**Iteración 1.** El BFS desde $s$ encuentra el camino más corto $s \to b \to a \to t$.
- Residuales: $5, 6, 3$. Cuello de botella: $\delta = 3$.
- $|x| = 3$. Queda saturado $(a,t)$.

**Iteración 2.** $(a,t)$ ya no admite más. El BFS encuentra $s \to b \to d \to t$.
- Residuales: $5-3 = 2$, $6$, $9$. Cuello de botella: $\delta = 2$.
- $|x| = 5$. Queda saturado $(s,b)$.

**Iteración 3.** Desde $s$ solo se puede salir por $(s,c)$. El BFS encuentra $s \to c \to a \Rightarrow b \to d \to t$, donde $a \Rightarrow b$ es el **arco inverso** de $(b,a)$.
- Residuales: $c_f(s,c)=7$, $c_f(c,a)=5$, $c_f(a,b)=3$ (el flujo que llevaba $(b,a)$), $c_f(b,d)=6-2=4$, $c_f(d,t)=9-2=7$. Cuello de botella: $\delta = 3$.
- Efecto: se **cancelan** las 3 unidades de $(b,a)$. Ahora $a$ recibe sus 3 unidades desde $c$, y $b$ redirige las suyas hacia $d$.
- $|x| = 8$.

**Iteración 4.** Desde $s$ se alcanza $c$ (residual $7-3 = 4$) y desde $c$ se alcanza $a$ (residual $5-3 = 2$). Desde $a$ no se puede seguir: $(a,t)$ está saturado y el inverso hacia $b$ quedó en 0. No se alcanza $t$, así que el algoritmo termina.

### 2.3 Flujo final

| Arco | $(s,b)$ | $(s,c)$ | $(b,a)$ | $(b,d)$ | $(c,a)$ | $(d,c)$ | $(a,t)$ | $(d,t)$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $x/c$ | 5/5 | 3/7 | 0/6 | 5/6 | 3/5 | 0/5 | 3/3 | 5/9 |

**Capacidad:** $0 \le x(u,v) \le c(u,v)$ en los 8 arcos.

**Conservación en los vértices intermedios:**

| $v$ | Entra | Sale | Diferencia |
| --- | --- | --- | --- |
| $a$ | $x(b,a)+x(c,a) = 0+3 = 3$ | $x(a,t) = 3$ | 0 |
| $b$ | $x(s,b) = 5$ | $x(b,a)+x(b,d) = 0+5 = 5$ | 0 |
| $c$ | $x(s,c)+x(d,c) = 3+0 = 3$ | $x(c,a) = 3$ | 0 |
| $d$ | $x(b,d) = 5$ | $x(d,c)+x(d,t) = 0+5 = 5$ | 0 |

**Valor:** $|x| = x(s,b) + x(s,c) - 0 = 5 + 3 = 8$. Coincide con lo que llega a $t$: $3 + 5 = 8$.

### 2.4 Corte mínimo y optimalidad

Los vértices alcanzables desde $s$ en la red residual final son $S = \{s, c, a\}$, por lo que $T = \{b, d, t\}$.

- Arcos de $S$ hacia $T$: $(s,b)$ y $(a,t)$. Ambos están **saturados**.
- $c(S,T) = c(s,b) + c(a,t) = 5 + 3 = 8$.
- Arcos de $T$ hacia $S$: $(b,a)$ y $(d,c)$. Ambos llevan **flujo 0**. No cuentan en la capacidad del corte.

**Argumento de optimalidad.** Todo flujo factible vale a lo más la capacidad de cualquier corte: $|x| \le c(S,T)$. Aquí se exhibió un flujo de valor 8 y un corte de capacidad 8. Por lo tanto ningún flujo puede superar 8 (el flujo es máximo) y ningún corte puede valer menos de 8 (el corte es mínimo). Este corte mínimo es único.

### 2.5 Qué debe coincidir con el código

| Valor | Manual | Esperado del motor |
| --- | --- | --- |
| $\lvert x\rvert$ | 8 | 8 |
| Iteraciones | 3 | 3, con los mismos caminos y cuellos de botella (3, 2, 3) |
| Flujo por arco | Tabla de §2.3 | Igual |
| $S$ / $T$ | $\{s,a,c\}$ / $\{b,d,t\}$ | Igual |
| $c(S,T)$ | 8 | 8 |

Si el motor recorre los vecinos en otro orden, los caminos pueden diferir, pero $|x|$, $S$, $T$ y $c(S,T)$ deben ser los mismos.

---

## 3. Segundo caso de prueba: Figura 1 del enunciado

`data/figura1.json`. Resultado esperado: $|x| = 14$ en 3 iteraciones (O-A-C-T con 5, O-A-D-T con 3, O-B-D-T con 6), $S = \{O\}$, $c(S,T) = 8 + 6 = 14$.

Esta red tiene **más de un corte mínimo**: también $\{(C,T),(D,T)\}$ suma $5+9 = 14$. El procedimiento por alcanzabilidad desde $s$ siempre entrega el más cercano al origen. Sirve para explicar en el informe por qué se pide "un" corte mínimo y no "el" corte mínimo.

---

## 4. Tareas que se desprenden de esta fase

El detalle por integrante está en `docs/tareas/`.
