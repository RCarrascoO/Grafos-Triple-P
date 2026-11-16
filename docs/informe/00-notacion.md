# Notación común del informe

> Tarea D4 (redacta: Daniel Prado). Las cinco secciones del informe usan estos símbolos, que son los del enunciado. Si una sección necesita un símbolo nuevo, se agrega aquí primero.

| Símbolo | Significado |
| --- | --- |
| $G = (V, E)$ | Red dirigida: $V$ es el conjunto de vértices (centros logísticos) y $E$ el de arcos (rutas activas). |
| $(u,v)$ | Arco dirigido de $u$ a $v$. Siempre como par ordenado, no "$u \to v$" ni "$uv$". |
| $\lvert V\rvert$, $\lvert E\rvert$ | Número de vértices y de arcos. |
| $c$ | Función de capacidad $c: E \to \{1, 2, \dots, 12\}$. $c(u,v)$ es la capacidad del arco $(u,v)$, en paquetes por hora. |
| $s$, $t$ | Origen y destino, con $s \ne t$. |
| $\deg^+(v)$, $\deg^-(v)$ | Número de arcos que salen de $v$ y que entran a $v$. |
| $x$ | Flujo: asigna a cada arco un valor $x(u,v)$. Se escribe $x$, **no** $f$. |
| $x(u,v)/c(u,v)$ | Etiqueta "flujo/capacidad" de un arco en tablas y figuras, por ejemplo 4/5. |
| $\lvert x\rvert$ | Valor del flujo: cantidad neta que sale del origen. |
| $x^*$ | Un flujo máximo. $\lvert x^*\rvert$ es el valor del flujo máximo. |
| $S$, $T$ | Partición de $V$ que define un corte: $V = S \cup T$, $S \cap T = \emptyset$, $s \in S$, $t \in T$. |
| $c(S,T)$ | Capacidad del corte $(S,T)$. |
| $G_x$ | Red residual de $G$ respecto del flujo $x$. |
| $c_x(u,v)$ | Capacidad residual de $(u,v)$ en $G_x$. Se escribe $c_x$, **no** $c_f$. |
| $\delta$ | Cuello de botella de un camino aumentante: su menor capacidad residual. |

## Definiciones

**Flujo factible.** $x$ es factible si cumple:

- Capacidad: $0 \le x(u,v) \le c(u,v)$ para todo $(u,v) \in E$.
- Conservación: $\displaystyle\sum_{(u,v)\in E} x(u,v) = \sum_{(v,w)\in E} x(v,w)$ para todo $v \in V \setminus \{s,t\}$.

**Valor del flujo.** $\displaystyle\lvert x\rvert = \sum_{(s,v)\in E} x(s,v) - \sum_{(u,s)\in E} x(u,s)$.

**Capacidad de un corte.** $\displaystyle c(S,T) = \sum_{\substack{(u,v)\in E \\ u\in S,\ v\in T}} c(u,v)$. Solo cuentan los arcos que van de $S$ hacia $T$.

**Red residual.** Para cada arco $(u,v) \in E$, $G_x$ tiene:

- un arco directo con $c_x(u,v) = c(u,v) - x(u,v)$: lo que aún cabe por la ruta;
- un arco inverso con $c_x(v,u) = x(u,v)$: el flujo ya enviado que se puede cancelar.

Un **camino aumentante** es un camino de $s$ a $t$ en $G_x$ formado solo por arcos con capacidad residual positiva.

## Vocabulario

| Se usa | No se usa |
| --- | --- |
| vértice, arco | nodo, arista (salvo al citar nombres del código, como `nodes`) |
| origen, destino | fuente, sumidero |
| arco recíproco | arco antiparalelo |
| arco repetido | arco paralelo |
| arco saturado ($x(u,v) = c(u,v)$) | arco lleno |
| paquetes por hora | unidades |

## Revisión de las secciones (pendiente hasta que estén escritas)

- [ ] Sección 2 y 3 (Rodrigo, R9–R10): usa $x$, $\lvert x\rvert$, $G_x$, $c_x$, $\delta$, $c(S,T)$.
- [ ] Secciones 4 y 5 (Sebastián, S13): usa $x(u,v)/c(u,v)$, $S$, $T$, $c(S,T)$ y $c_x$ en la resolución manual.

Estado de los documentos base: `docs/fase2-algoritmo.md` ya usa $G_x$ y $c_x$. `docs/fase0-stack-y-contrato.md` §6 y `docs/fase1-diseno-redes.md` §2.2 usaban $c_f$ y se corrigieron a $c_x$.
