# Presentación — parte de Daniel: problema y modelo (tarea D6)

Criterio 1 de la rúbrica de la presentación: "Exposición del problema y de su representación matemática mediante grafos".
Tiempo: unos 2 minutos y medio de los 12. Va primero; después sigue Rodrigo con el algoritmo.

## Diapositiva 1 — El problema (30 s)

En pantalla: título del proyecto, integrantes y un mapa o dibujo del corredor Santiago → Puerto Montt.

Qué decir:
- Una empresa mueve paquetes entre centros logísticos unidos por rutas de sentido único. Cada ruta admite un máximo de paquetes por hora.
- La pregunta: ¿cuántos paquetes por hora pueden llegar, como máximo, de Santiago a Puerto Montt, y qué rutas lo limitan?
- No basta mirar lo que sale del origen: una ruta grande no sirve si las que siguen son más chicas.

## Diapositiva 2 — El modelo (60 s)

En pantalla: la red inicial dibujada por la aplicación, con las capacidades sobre los arcos.

Qué decir:
- Es una red dirigida $G = (V, E)$. Cada vértice es un centro y cada arco $(u,v)$ es una ruta de $u$ a $v$.
- $\lvert V\rvert = 11$ centros y $\lvert E\rvert = 19$ rutas. El enunciado pide entre 10 y 12, y entre 15 y 20.
- La capacidad $c(u,v)$ es un entero entre 1 y 12 paquetes por hora. Usamos de 3 a 12.
- Origen $s$ = Santiago, destino $t$ = Puerto Montt.
- Un flujo $x$ dice cuánto se envía por cada ruta: no supera la capacidad, y en cada centro intermedio lo que entra es igual a lo que sale.

## Diapositiva 3 — Restricciones (45 s)

En pantalla: la tabla de auditoría de `01-modelacion.md` §1.5, resumida.

Qué decir:
- Sin lazos, sin arcos repetidos y sin arcos recíprocos: todas las rutas van de norte a sur.
- Ningún centro queda aislado: todos tienen grado 2 o más. Temuco es el de mayor grado, con 6.
- Hay al menos dos caminos de $s$ a $t$; mostramos dos que no comparten ninguna ruta: STG–CON–LAN–VAL–PMO y STG–RAN–CHI–TEM–OSO–PMO.
- La aplicación valida estas reglas en cada edición, no solo en la red inicial.

## Cierre y paso a Rodrigo (15 s)

- De Santiago pueden salir 28 paquetes por hora y a Puerto Montt pueden entrar 23. El máximo real es menor que ambos, y para encontrarlo hace falta un algoritmo.

## Preguntas probables del docente

| Pregunta | Respuesta corta |
| --- | --- |
| ¿Por qué se prohíben los arcos recíprocos? | Así el arco inverso de la red residual nunca se mezcla con un arco original, y el flujo de cada ruta se recupera sin ambigüedad. |
| ¿Qué significa "caminos distintos"? | Que difieren en al menos un arco. Los nuestros además no comparten ninguno. |
| ¿Qué pasa con una ruta desactivada? | Sale de $E$ y no lleva flujo, pero sigue ocupando el par de centros: no se puede crear la misma ruta ni la recíproca hasta eliminarla. |
| ¿Por qué no se permite capacidad 0? | Porque $c: E \to \{1,\dots,12\}$. Cortar una ruta se modela desactivándola. |
| ¿Por qué la suma de grados de salida es 19? | Cada arco aporta exactamente una salida y una entrada, así que ambas sumas valen $\lvert E\rvert$. |
| ¿La red tiene ciclos? | No. Todos los arcos van de norte a sur. |
