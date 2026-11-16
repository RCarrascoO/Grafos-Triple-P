# 1. Modelación matemática de la red

> Apartado 1 del informe (tarea D3, redacta: Daniel Prado). Fuente: `docs/fase1-diseno-redes.md` §1 y `data/initial_network.json`.
> Notación: `docs/informe/00-notacion.md`.

## 1.1 Significado del modelo

La empresa distribuye paquetes a lo largo del corredor **Santiago → Puerto Montt**. La configuración inicial se modela como una red dirigida $G = (V, E)$ con una función de capacidad $c$, un origen $s$ y un destino $t$:

| Elemento del modelo | Significado en el problema |
| --- | --- |
| Vértice $v \in V$ | Un centro logístico, ubicado en una ciudad. |
| Arco $(u,v) \in E$ | Una ruta de transporte de sentido único, del centro $u$ al centro $v$. |
| Capacidad $c(u,v)$ | Máximo de paquetes por hora que admite la ruta $(u,v)$. |
| Origen $s$ | Centro desde el que se despachan los paquetes: Santiago. |
| Destino $t$ | Centro al que deben llegar: Puerto Montt. |
| Flujo $x(u,v)$ | Paquetes por hora que efectivamente se envían por la ruta $(u,v)$. |
| Valor $\lvert x\rvert$ | Paquetes por hora que salen de $s$ y llegan a $t$. |

Los centros intermedios no almacenan ni generan paquetes: todo lo que entra a un centro sale de él (conservación del flujo, apartado 2).

## 1.2 Conjunto de vértices

$$V = \{\text{STG}, \text{RAN}, \text{TAL}, \text{CHI}, \text{CON}, \text{LAN}, \text{TEM}, \text{VIL}, \text{VAL}, \text{OSO}, \text{PMO}\}, \qquad \lvert V\rvert = 11$$

| Id | Centro logístico | Rol |
| --- | --- | --- |
| STG | Santiago | Origen $s$ |
| RAN | Rancagua | Intermedio |
| TAL | Talca | Intermedio |
| CHI | Chillán | Intermedio |
| CON | Concepción | Intermedio |
| LAN | Los Ángeles | Intermedio |
| TEM | Temuco | Intermedio |
| VIL | Villarrica | Intermedio |
| VAL | Valdivia | Intermedio |
| OSO | Osorno | Intermedio |
| PMO | Puerto Montt | Destino $t$ |

## 1.3 Conjunto de arcos y función de capacidad

$E$ tiene $\lvert E\rvert = 19$ arcos. La función $c: E \to \{1, 2, \dots, 12\}$ asigna a cada uno su capacidad en paquetes por hora:

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

La capacidad mínima usada es 3 y la máxima es 12.

<!-- FIGURA 1.1: dibujo de la red inicial con sus capacidades (captura de la aplicación, la toma Renato en N19). -->

## 1.4 Grados de los vértices

$\deg^+(v)$ es el número de arcos que salen de $v$ y $\deg^-(v)$ el número de arcos que entran:

| $v$ | STG | RAN | TAL | CHI | CON | LAN | TEM | VIL | VAL | OSO | PMO | Suma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $\deg^+(v)$ | 3 | 1 | 2 | 2 | 2 | 2 | 3 | 1 | 2 | 1 | 0 | 19 |
| $\deg^-(v)$ | 0 | 1 | 1 | 2 | 2 | 2 | 3 | 1 | 2 | 3 | 2 | 19 |
| Total | 3 | 2 | 3 | 4 | 4 | 4 | 6 | 2 | 4 | 4 | 2 | 38 |

Comprobación: $\sum_{v} \deg^+(v) = \sum_{v} \deg^-(v) = \lvert E\rvert = 19$, porque cada arco aporta una salida y una entrada.

El origen no tiene arcos de entrada ($\deg^-(\text{STG}) = 0$) y el destino no tiene arcos de salida ($\deg^+(\text{PMO}) = 0$). Temuco es el centro de mayor grado (6): recibe tres rutas y despacha tres.

## 1.5 Auditoría de las restricciones del enunciado

| Restricción | Verificación | Cumple |
| --- | --- | --- |
| $10 \le \lvert V\rvert \le 12$ | $\lvert V\rvert = 11$ | Sí |
| $15 \le \lvert E\rvert \le 20$ | $\lvert E\rvert = 19$ | Sí |
| $c: E \to \{1,\dots,12\}$ | Las 19 capacidades son enteras y están entre 3 y 12 | Sí |
| Sin lazos | Ningún arco tiene la forma $(u,u)$ | Sí |
| Sin arcos repetidos | Los 19 pares ordenados $(u,v)$ son distintos | Sí |
| Sin arcos recíprocos | Para ningún $(u,v) \in E$ existe $(v,u) \in E$. Todos los arcos van de norte a sur, así que la red es acíclica | Sí |
| Ningún vértice aislado | $\deg^+(v) + \deg^-(v) \ge 2$ para todo $v$ (tabla de §1.4) | Sí |
| $s \ne t$ | $s = \text{STG}$, $t = \text{PMO}$ | Sí |
| Al menos dos caminos dirigidos distintos de $s$ a $t$ | $P_1$ y $P_2$, abajo | Sí |

Dos caminos dirigidos de $s$ a $t$:

- $P_1$: STG → CON → LAN → VAL → PMO
- $P_2$: STG → RAN → CHI → TEM → OSO → PMO

$P_1$ y $P_2$ no comparten ningún arco ni ningún vértice intermedio, de modo que son distintos bajo cualquier lectura de "caminos distintos".

La aplicación comprueba estas mismas restricciones con código (`validate_network` en `core/validation.py`): para `data/initial_network.json` no reporta ningún error.

## 1.6 Interpretación

- **Sentido único.** Todas las rutas avanzan de norte a sur. Un paquete nunca retrocede, y por eso la red no tiene ciclos ni arcos recíprocos.
- **Rutas alternativas.** Entre Santiago y Puerto Montt hay muchos caminos. Si una ruta se interrumpe, los paquetes pueden desviarse por otros centros; cuánto se pierde depende de las capacidades de las rutas que quedan. Eso es lo que se analiza en el apartado 4.
- **Cotas inmediatas.** De Santiago pueden salir a lo más $10 + 12 + 6 = 28$ paquetes por hora, y a Puerto Montt pueden entrar a lo más $12 + 11 = 23$. Por lo tanto ningún flujo puede superar 23. El valor exacto no se lee de los extremos: depende también de las capacidades intermedias, y es lo que calcula el algoritmo del apartado 2 y explica el corte mínimo del apartado 3.
