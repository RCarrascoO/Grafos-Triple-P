# Guion del video de presentación (Evaluación 3)

Requisitos del profesor (anuncio del 23-nov): participan los 4, duración de 10 a 20 min, video público, un solo integrante sube el enlace a EDUCA, plazo **lunes 30-nov, 17:00**. Se evalúa con la rúbrica de presentación del enunciado.

**Diseño:** 12 turnos, 3 rondas en el orden Daniel → Sebastián → Rodrigo → Renato. Ningún turno pasa de 1:30. Cada uno habla unos **4:00** (entre 3:50 y 4:15). Duración total estimada: **15 a 16 min** (el texto suma ~1.950 palabras, ~15 min a 130 palabras por minuto; los turnos con demo llevan menos texto porque hay clics en pantalla). Los tiempos son orientativos: midan cada turno con cronómetro en el ensayo y ajusten.

| # | Habla | Tiempo | Tema | Criterio de rúbrica |
|---|-------|--------|------|---------------------|
| 1 | Daniel | 1:15 | Problema y modelo | 1 |
| 2 | Sebastián | 1:15 | Restricciones y validación en vivo | 1 |
| 3 | Rodrigo | 1:30 | Algoritmos y por qué Edmonds–Karp | 2 |
| 4 | Renato | 1:30 | Código propio, tests y red en pantalla | 2 y 3 |
| 5 | Daniel | 1:30 | Cálculo en vivo: flujo máximo 20 | 3 |
| 6 | Sebastián | 1:15 | Corte mínimo en pantalla | 3 |
| 7 | Rodrigo | 1:15 | Teorema flujo máximo–corte mínimo | 2 y 3 |
| 8 | Renato | 1:15 | Modificación 1 en vivo: 13 | 4 |
| 9 | Daniel | 1:15 | Modificación 2 en vivo: 23 | 4 |
| 10 | Sebastián | 1:30 | Comparación de las 3 configuraciones | 4 |
| 11 | Rodrigo | 1:30 | Verificación con el caso manual | 3 y 4 |
| 12 | Renato | 1:15 | Conclusión y cierre | 5 |

**Criterio 5 (participación y preguntas del docente):** en video no hay preguntas en vivo. Para cubrirlo, cada turno responde una pregunta probable del profesor dentro del guion (marcadas con ❓) y todos hablan lo mismo.

---

## Antes de grabar (los 4)

1. Cada uno graba **sus 3 turnos por separado**: pantalla + micrófono (OBS, o Grabar de Teams/Meet). Lo más simple: una videollamada con cámara encendida donde habla quien tiene el turno; así se ven las caras y se evita editar. Si prefieren editar, graben cada turno suelto y únanlos en orden.
2. Quien habla es **quien maneja el programa** en ese turno. Así se nota que los 4 dominan la aplicación.
3. Resolución 1080p, zoom del navegador al 110–125 % para que se lean los números. Cierren notificaciones.
4. Antes de cada turno con demo: recarguen la página (F5) y elijan la red indicada. La app usa `st.session_state`: si recargan, vuelve a "Red inicial".
5. Comando para abrir el programa: `streamlit run app.py`. Ensayen todo una vez con cronómetro.
6. Subir a YouTube como **Público** (no "privado"). Abrir el enlace en una ventana de incógnito para comprobar que se ve. Un solo integrante pega el enlace en EDUCA.

**Datos que se usan en pantalla** (todos salieron del código real del repo el 23-nov):

| Red | Flujo máximo | Corte S | Arcos del corte |
|-----|--------------|---------|-----------------|
| Red inicial | 20 | STG, RAN, TAL, CHI, CON, LAN | CHI-TEM 4 + CON-TEM 7 + LAN-TEM 3 + LAN-VAL 6 = 20 |
| Modificación 1 (sin CON-TEM) | 13 | igual que la inicial | CHI-TEM 4 + LAN-TEM 3 + LAN-VAL 6 = 13 |
| Modificación 2 (CON-TEM = 9 y nueva CON-VAL = 8) | 23 | todo menos PMO | VAL-PMO 12 + OSO-PMO 11 = 23 |
| Caso manual (6 vértices) | 8 | s, a, c | s-b 5 + a-t 3 = 8 |

---

## Turno 1 — Daniel (1:15): problema y modelo

**Pantalla:** diapositiva de título (nombres de los 4, "Teoría de Grafos INFO1158"). Luego la app con "Red inicial" cargada, **sin calcular**.

**Decir:**
> Hola, somos Daniel Prado, Sebastián Pereda, Rodrigo Pedraza y Renato Carrasco, y presentamos el Proyecto 2: un simulador de una red de distribución de paquetes.
>
> El problema es este. Una empresa mueve paquetes por rutas de sentido único entre centros logísticos, y cada ruta admite un máximo de paquetes por hora. Nosotros usamos el corredor Santiago–Puerto Montt. La pregunta es: ¿cuántos paquetes por hora pueden llegar como máximo de Santiago a Puerto Montt, y qué rutas lo limitan?
>
> No basta con mirar lo que sale del origen. De Santiago pueden salir 28 paquetes por hora y a Puerto Montt pueden entrar 23, pero una ruta grande no sirve si las que siguen son más chicas.
>
> Lo modelamos con un grafo dirigido G igual a V, E. Cada vértice es un centro logístico y cada arco es una ruta. La función c asigna a cada arco su capacidad, un entero entre 1 y 12. El origen es Santiago y el destino es Puerto Montt. Un flujo dice cuántos paquetes van por cada ruta. Ahora Sebastián explica las restricciones.

**Mostrar:** señalar con el cursor Santiago (origen), Puerto Montt (destino) y una capacidad sobre un arco.

---

## Turno 2 — Sebastián (1:15): restricciones y validación en vivo

**Pantalla:** la red inicial. Barra lateral → "Agregar ruta".

**Decir:**
> Nuestra red tiene 11 centros y 19 rutas. El enunciado pide entre 10 y 12 centros y entre 15 y 20 rutas. Las capacidades van de 3 a 12 paquetes por hora.
>
> El enunciado prohíbe lazos, rutas repetidas y rutas recíprocas, y que ningún centro quede aislado. Nuestra red cumple todo eso: todas las rutas van de norte a sur y todos los centros tienen al menos dos rutas. Además existen al menos dos caminos de origen a destino que no comparten ninguna ruta, por ejemplo Santiago, Concepción, Los Ángeles, Valdivia, Puerto Montt, y Santiago, Rancagua, Chillán, Temuco, Osorno, Puerto Montt.
>
> La aplicación aplica estas reglas en cada edición. Lo demuestro: intento agregar una ruta de Puerto Montt a Valdivia, que es recíproca de una existente. *(hacerlo)* La app la rechaza con un mensaje. Intento una de Santiago a Santiago, un lazo. *(hacerlo)* También la rechaza. ❓ ¿Por qué se prohíben las recíprocas? Para que el arco inverso de la red residual nunca se mezcle con uno original. Sigue Rodrigo.

**Grabar:** en "Agregar ruta": Desde PMO, Hasta VAL, capacidad 5, "Agregar" → aparece el aviso de ruta en sentido contrario. Luego Desde STG, Hasta STG → aviso de lazo (los mensajes de la app son: "Ya existe la ruta en sentido contrario. Elimínela antes de crear esta." y "No se permiten lazos…"). La capacidad fuera de 1–12 ni se puede escribir en el campo.

---

## Turno 3 — Rodrigo (1:30): algoritmos y elección

**Pantalla:** una diapositiva con la tabla comparativa (abajo). No hace falta demo.

| | Ford–Fulkerson + DFS | Edmonds–Karp (BFS) |
|---|---|---|
| Camino elegido | el primero que encuentre la DFS | el más corto en arcos |
| Complejidad | O(\|E\|·\|x\*\|), depende de las capacidades | O(\|V\|·\|E\|²), no depende de ellas |
| Reproducible a mano | poco | sí, caminos cortos y orden fijo |

**Decir:**
> Investigamos dos estrategias para flujo máximo. Ambas parten de flujo cero y buscan un camino aumentante en la red residual: un camino de origen a destino con capacidad sobrante. Envían por él su cuello de botella y repiten hasta que no queden caminos.
>
> La primera es Ford–Fulkerson con búsqueda en profundidad. Funciona, pero su número de pasos depende del valor de las capacidades, orden O de E por flujo máximo, y el resultado depende del orden en que explora la DFS.
>
> La segunda es Edmonds–Karp, que es Ford–Fulkerson eligiendo siempre el camino con menos arcos, con búsqueda en anchura. Su cota es O de V por E al cuadrado y no depende de las capacidades.
>
> Elegimos Edmonds–Karp por tres razones. Primero, la aplicación permite editar capacidades y su garantía no cambia. Segundo, es determinista: el apartado de verificación exige comparar con un cálculo manual y así se puede reproducir paso a paso. Tercero, la misma búsqueda final entrega el corte mínimo. ❓ No decimos que DFS no termine: con enteros termina; la elección es por garantías y trazabilidad, no por velocidad. Las fuentes son Ford y Fulkerson, 1956, Edmonds y Karp, 1972, y Cormen, capítulo 26. Sigue Renato.

---

## Turno 4 — Renato (1:30): código propio, tests y red en pantalla

**Pantalla:** primero VS Code, luego terminal, luego la app.

**Decir:**
> El algoritmo está programado por nosotros. El proyecto no importa ninguna librería de grafos ni de cálculo: no hay networkx, scipy ni numpy. La única dependencia es Streamlit, y solo para la interfaz. Lo pueden ver en `requirements.txt`.
>
> El código está separado en dos capas. La carpeta `core` tiene el motor: validación, ediciones, flujo máximo, corte mínimo y verificación, solo con biblioteca estándar de Python. `app.py` solo muestra y llama a `core`; no calcula nada. Cada función tiene su docstring con propósito, entradas y salida, como pide el enunciado. Por ejemplo, `buscar_camino` es la búsqueda en anchura que devuelve el camino más corto con residual positivo.
>
> Tenemos 31 pruebas automáticas. Las corro. *(ejecutar)* Pasan todas. Incluyen un oráculo por fuerza bruta que enumera todos los cortes posibles y comprueba que el menor coincide con nuestro flujo máximo.
>
> Ahora la aplicación. Aquí está la red inicial con sus 11 centros, las rutas con su dirección en la flecha y la capacidad sobre cada una. A la izquierda se elige origen y destino y se calcula. Eso lo muestra Daniel.

**Grabar:**
1. VS Code: abrir `core/flujo_maximo.py`, mostrar el docstring de `buscar_camino` y `edmonds_karp` (5 s).
2. Terminal: `python -m unittest` → "Ran 31 tests … OK".
3. Navegador: la app con la red inicial; recorrer con el cursor flecha → capacidad → barra lateral.
4. Mostrar el enlace del repositorio: https://github.com/RCarrascoO/Grafos-Triple-P

---

## Turno 5 — Daniel (1:30): cálculo en vivo, flujo máximo 20

**Pantalla:** app, red inicial, origen STG, destino PMO.

**Decir:**
> Selecciono origen Santiago, destino Puerto Montt, y presiono Calcular. *(hacerlo)* El flujo máximo es **20 paquetes por hora**, menos que los 23 que podrían entrar a Puerto Montt.
>
> En el grafo cada arco muestra flujo sobre capacidad. Por ejemplo, Valdivia–Puerto Montt va 12 de 12, completamente usado, y Osorno–Puerto Montt va 8 de 11, con holgura.
>
> Abajo está la tabla con el flujo y la capacidad de cada ruta. El programa comprueba tres cosas, con un módulo de verificación que no usa el motor. Una: ningún flujo supera su capacidad, `capacity_ok` verdadero. Dos: en cada centro intermedio lo que entra es igual a lo que sale, y esta tabla lo muestra, `conservation_ok` verdadero. Tres: el valor del flujo, lo que sale neto de Santiago, es igual a la capacidad del corte, `duality_ok` verdadero.
>
> Esta última tabla son las iteraciones de Edmonds–Karp: nueve caminos aumentantes. El primero fue Santiago, Concepción, Los Ángeles, Valdivia, Puerto Montt, con cuello de botella 5. Al sumar los cuellos de botella se llega a 20. Sebastián muestra el corte.

**Grabar:** clic en Calcular; zoom a la métrica "Flujo máximo (|x|) = 20", a la tabla flujo/capacidad (bajar con scroll), a la tabla de conservación y a las tres líneas `*_ok`, y a la tabla de iteraciones.

---

## Turno 6 — Sebastián (1:15): corte mínimo en pantalla

**Pantalla:** la misma vista con el resultado calculado (arriba, el grafo coloreado).

**Decir:**
> Veamos el corte mínimo. Los nodos azules son el conjunto S: Santiago, Rancagua, Talca, Chillán, Concepción y Los Ángeles. Los amarillos son T: Temuco, Villarrica, Valdivia, Osorno y Puerto Montt.
>
> Los arcos rojos son los que van de S a T. Son cuatro: Chillán–Temuco con capacidad 4, Concepción–Temuco con 7, Los Ángeles–Temuco con 3 y Los Ángeles–Valdivia con 6. Sumo: 4 más 7 más 3 más 6 igual a **20**. La capacidad del corte coincide con el flujo máximo.
>
> Eso significa que el flujo no puede ser mayor: todo lo que cruza de S a T pasa por esas cuatro rutas y las cuatro van llenas. Es el cuello de botella real: está entre el norte de la red y la zona Temuco–Valdivia, no a la salida de Santiago ni a la llegada a Puerto Montt. ❓ ¿Es único el corte? No siempre; el programa entrega el más cercano al origen. Rodrigo explica por qué esto prueba que 20 es el máximo.

**Grabar:** zoom al grafo coloreado y a la línea "S = …; T = …; arcos de corte: …". Resaltar con el cursor los cuatro arcos rojos y sus etiquetas 4/4, 7/7, 3/3, 6/6.

---

## Turno 7 — Rodrigo (1:15): teorema flujo máximo–corte mínimo

**Pantalla:** diapositiva con el enunciado del teorema y, después, `core/corte_minimo.py`.

**Decir:**
> Esto es el teorema de flujo máximo–corte mínimo de Ford y Fulkerson. Para un corte S, T, todo flujo vale a lo más la capacidad del corte, porque cada paquete tiene que cruzar de S a T. Entonces si encontramos un flujo y un corte con el mismo valor, ambos son óptimos. Por eso 20 es el máximo y 20 es el mínimo.
>
> Nuestro código lo usa así. Cuando Edmonds–Karp termina, hacemos una última búsqueda desde Santiago en la red residual. Los centros que alcanza forman S y el resto forma T. En ese corte todos los arcos de S a T están saturados y los de T a S llevan flujo cero. Esa búsqueda es la función `alcanzables_desde`.
>
> Además, como las capacidades son enteras, existe un flujo máximo entero: los paquetes no se parten. El valor del flujo máximo es único, pero el flujo por arco no necesariamente. Sigue Renato con la primera modificación.

**Grabar:** diapositiva (5 s), luego `core/corte_minimo.py` mostrando el docstring de `alcanzables_desde` (5 s).

---

## Turno 8 — Renato (1:15): modificación 1 en vivo (cierre de Concepción–Temuco)

**Pantalla:** app. Cargar "Red inicial" (selector Red → Cargar). Barra lateral → "Editar ruta existente".

**Decir:**
> Ahora la simulación. Primera modificación: se cierra la ruta Concepción–Temuco, por ejemplo por un temporal. Selecciono esa ruta y presiono Desactivar. *(hacerlo)* Queda en gris punteado. Los resultados anteriores se borran, así que presiono Calcular de nuevo. *(hacerlo)*
>
> El flujo máximo baja de 20 a **13**. El corte ahora tiene tres arcos: Chillán–Temuco 4, Los Ángeles–Temuco 3 y Los Ángeles–Valdivia 6, que suman 13. Perdimos 7 paquetes por hora, exactamente la capacidad de la ruta cerrada. Eso pasa porque esa ruta estaba en el corte mínimo.
>
> Todo se hizo desde la interfaz, sin tocar el código. Daniel sigue con la segunda modificación.

**Grabar:** Red → "Red inicial" → Cargar → Ruta `CON-TEM` → Desactivar → Calcular → mostrar métrica 13 y los tres arcos rojos.
*(Esto equivale a cargar `Modificación 1` del selector; es preferible hacerla a mano para que se vea que se edita desde la interfaz.)*

---

## Turno 9 — Daniel (1:15): modificación 2 en vivo (ampliar y agregar ruta)

**Pantalla:** app. Cargar "Red inicial" de nuevo.

**Decir:**
> Segunda modificación: invertir en infraestructura. Primero amplío Concepción–Temuco de 7 a 9. Selecciono la ruta, pongo capacidad 9, Cambiar capacidad y Calcular. *(hacerlo)* El flujo sube solo a **21**: mejoró poco, porque el cuello de botella se movió.
>
> Segundo paso: agrego una ruta nueva de Concepción a Valdivia con capacidad 8. Desde Concepción, hasta Valdivia, capacidad 8, Agregar y Calcular. *(hacerlo)* Ahora el flujo máximo es **23**. El corte cambió por completo: S es toda la red y T es solo Puerto Montt. Los arcos del corte son Valdivia–Puerto Montt 12 y Osorno–Puerto Montt 11, que suman 23.
>
> Es el máximo posible para esta red: no se puede enviar más de lo que entra a Puerto Montt. Para subir más habría que ampliar esas dos últimas rutas. Sebastián compara las tres configuraciones.

**Grabar:** Red inicial → Cargar → Ruta `CON-TEM` → Capacidad 9 → Cambiar capacidad → Calcular (21) → Agregar: Desde CON, Hasta VAL, capacidad 8 → Agregar → Calcular (23) → mostrar los dos arcos rojos hacia PMO.

---

## Turno 10 — Sebastián (1:30): comparación de las tres configuraciones

**Pantalla:** una diapositiva con esta tabla (y, si se puede, tres capturas de las redes).

| Configuración | Flujo máximo | Arcos del corte mínimo | Capacidad del corte |
|---|---|---|---|
| Red inicial | 20 | CHI-TEM, CON-TEM, LAN-TEM, LAN-VAL | 4+7+3+6 = 20 |
| Modificación 1 (cierre CON-TEM) | 13 | CHI-TEM, LAN-TEM, LAN-VAL | 4+3+6 = 13 |
| Modificación 2 (CON-TEM = 9 y CON-VAL nueva) | 23 | VAL-PMO, OSO-PMO | 12+11 = 23 |

**Decir:**
> Esta es la comparación. La red inicial entrega 20, la modificación 1 baja a 13 y la modificación 2 sube a 23. En las tres, el flujo máximo es igual a la capacidad del corte mínimo.
>
> ¿Qué interpretamos? Primero, el cuello de botella se desplaza. Al inicio está en la zona de Temuco y Valdivia. Con la ruta cerrada seguía ahí pero con un arco menos, y con la ampliación se movió hasta el final de la red, a las dos rutas que llegan a Puerto Montt.
>
> Segundo, solo importa la capacidad de los arcos que están en el corte. Cerrar Concepción–Temuco costó exactamente 7, su capacidad, porque estaba en el corte. En cambio, ampliar esa ruta de 7 a 9 sumó solo 1 por sí sola, porque aparecieron otros arcos saturados.
>
> Tercero, la red inicial perdía 3 paquetes por hora respecto del tope teórico de 23, y la nueva ruta Concepción–Valdivia los recupera. Sigue Rodrigo con la verificación.

---

## Turno 11 — Rodrigo (1:30): verificación con el caso manual

**Pantalla:** app con "Caso manual" cargada y calculada. Opcional: diapositiva con la tabla.

**Decir:**
> Para verificar los resultados construimos un caso de seis vértices que se resuelve a mano: origen s, centros b, c, d, a, y destino t. A mano, tres caminos aumentantes: s, b, a, t con 3; s, b, d, t con 2; y s, c, a, b, d, t con 3. Este último **cancela flujo** del arco b–a usando su inverso residual. Total: 8.
>
> El corte que justifica la optimalidad es S igual a s, a, c y T igual a b, d, t. Los arcos de S a T son s–b con 5 y a–t con 3: suman 8. Los arcos de T a S, b–a y d–c, llevan flujo cero. Flujo 8 y corte 8: ambos son óptimos.
>
> Cargamos el mismo caso en la aplicación. *(cargar y calcular)* Devuelve 8, el mismo corte y el mismo flujo en cada arco. No hubo ninguna diferencia entre el cálculo manual y el código.
>
> Y para la red principal y sus dos modificaciones, el módulo de verificación comprueba que se respetan las capacidades, que se conserva el flujo en los centros intermedios y que el flujo máximo coincide con el corte. Las tres salieron verdaderas. Renato cierra.

**Grabar:** Red → "Caso manual" → Cargar → Calcular → mostrar 8, S/T, arcos rojos (s-b, a-t) y la tabla de iteraciones (3 caminos, el último usa b).

---

## Turno 12 — Renato (1:15): conclusión y cierre

**Pantalla:** diapositiva de cierre con 4 viñetas y el enlace al repositorio.

**Decir:**
> Para cerrar, resumimos lo que cumple el proyecto. Modelamos la red como grafo dirigido con 11 centros, 19 rutas y capacidades enteras, validando las restricciones en cada edición. Comparamos Ford–Fulkerson con Edmonds–Karp y elegimos Edmonds–Karp, implementado con código propio y sin librerías algorítmicas, con 31 pruebas que pasan.
>
> La aplicación calcula el flujo máximo, muestra el flujo y la capacidad de cada arco, e identifica el corte mínimo, cuya capacidad coincide siempre con el flujo. Permite desactivar rutas, cambiar capacidades y agregar conexiones sin editar el código, y con eso comparamos tres configuraciones: 20, 13 y 23 paquetes por hora. Verificamos todo con un caso manual y con las comprobaciones matemáticas.
>
> El código completo, con sus instrucciones de ejecución, está en el repositorio que aparece en pantalla, y el informe técnico está entregado en EDUCA. Quedamos disponibles para cualquier consulta. Gracias por su atención.

**Mostrar:** diapositiva final con nombres de los 4 y enlace https://github.com/RCarrascoO/Grafos-Triple-P. Puede terminar con los 4 diciendo "Gracias" juntos.

---

## Cómo cubre cada criterio de la rúbrica

| Criterio | Dónde se cubre |
|---|---|
| 1. Problema y modelo | Turnos 1 y 2 |
| 2. Algoritmo y fundamento | Turnos 3, 4 y 7 |
| 3. Demostración funcional | Turnos 4, 5, 6, 7 y 11 |
| 4. Simulación, comparación e interpretación | Turnos 8, 9 y 10 |
| 5. Participación y respuestas | Los 4 hablan 4:00 cada uno; preguntas anticipadas marcadas con ❓ dentro de los turnos |

## Qué hacer si el video se pasa o se queda corto

- **Se pasa de 20 min:** recorten del turno 5 la tabla de iteraciones, del turno 10 la tercera conclusión y del turno 4 la parte del oráculo por fuerza bruta.
- **Queda bajo 10 min:** imposible con este guion a ritmo normal. Si pasara, agreguen la tabla de conservación del flujo (turno 5) y la demostración del teorema (turno 7).
