# Tareas de Renato — validación, ediciones, interfaz y repositorio

**Leer antes:** `docs/fase0-stack-y-contrato.md` (§3 contrato de red, §4 contrato de resultado, §5 reglas y códigos de error) y las convenciones de `docs/tareas/README.md`.

**Archivos propios:** `app.py`, `requirements.txt`, `core/validacion.py`, `core/ediciones.py`.
**Frontend:** Streamlit (decisión del equipo). `app.py` importa solo `streamlit` y los módulos de `core/`.

Regla de la interfaz: `app.py` **no calcula ni valida nada**. Solo llama a funciones de `core/` y muestra lo que devuelven.

---

## Base

### N1 — Esqueleto del proyecto [COMPLETO]
- [x] Crear las carpetas `core/` y `tests/` con un `__init__.py` vacío en cada una.
- [x] Crear `requirements.txt` con una sola línea: `streamlit`.
- [x] Crear `app.py` en la raíz con `import streamlit as st` y `st.title(...)`. Va en la raíz para que `from core... import ...` funcione sin configurar rutas.

**Listo cuando:** `streamlit run app.py` abre la página con el título y `python -m unittest` corre sin errores de importación.


---

## Validación — `core/validacion.py`

### N2 — `capacidad_valida(valor) -> bool` [COMPLETO]
- [x] `True` solo si `value` es `int` (no `bool`, no `float`) y `1 <= value <= 12`.

**Listo cuando:** `1` y `12` dan `True`; `0`, `13`, `2.5`, `"5"` y `True` dan `False`.

### N3 — `validar_arco_nuevo(red, u, v, capacidad) -> str | None` [COMPLETO]
- [x] Revisa si se puede agregar el arco $(u,v)$. Mira **todos** los arcos de `network["arcs"]`, activos o no (decisión D1). Devuelve el primer código que aplique, en este orden:
1. `"E_UNKNOWN_NODE"` si `u` o `v` no son nodos.
2. `"E_LOOP"` si `u == v`.
3. `"E_DUPLICATE"` si ya existe $(u,v)$.
4. `"E_RECIPROCAL"` si ya existe $(v,u)$.
5. `"E_CAPACITY"` si `not capacidad_valida(capacidad)`.
6. `None` si se puede agregar.

**Listo cuando:** sobre `figura1.json`: `("A","O",5)` → `E_RECIPROCAL`; `("A","A",5)` → `E_LOOP`; `("O","A",5)` → `E_DUPLICATE`; `("O","C",13)` → `E_CAPACITY`; `("O","C",5)` → `None`.

### N4 — `contar_caminos(red, s, t, limite=2) -> int` [COMPLETO]
- [x] Cuenta caminos dirigidos simples de `s` a `t` usando arcos activos, con una DFS recursiva. Deja de contar al llegar a `limit`.

**Listo cuando:** en `figura1.json` de `O` a `T` devuelve `2` (hay 3, pero se detiene en el límite). De `T` a `O` devuelve `0`.

### N5 — `validar_red(red) -> list[str]` [COMPLETO]
- [x] Valida una red completa. Devuelve la lista de códigos encontrados (vacía si es válida).
- Siempre: lazos, repetidos, recíprocos, capacidades, extremos inexistentes, y `E_ST_EQUAL` si `source == sink`.
- Si `profile == "initial"`: `E_V_RANGE` (10–12 nodos), `E_E_RANGE` (15–20 arcos activos), `E_ISOLATED` (algún nodo sin arcos activos), `E_PATHS` (`contar_caminos < 2`).
- Si `profile == "manual"`: `E_V_RANGE_MANUAL` (4–6 nodos).
- Si `profile == "modified"`: nada adicional.

**Listo cuando:** los tres JSON de `data/` devuelven `[]`. `figura1.json` con el perfil cambiado a `"initial"` devuelve `E_V_RANGE` y `E_E_RANGE`.

---

## Ediciones — `core/ediciones.py`

Cada función modifica `network` **solo si la edición es válida** y devuelve `None`. Si no es válida, no cambia nada y devuelve el código de error.

### N6 — `agregar_arco(red, u, v, capacidad) -> str | None` [COMPLETO]
- [x] Llama a `validar_arco_nuevo`. Si pasa, agrega `{"id": f"{u}-{v}", "from": u, "to": v, "capacity": capacity, "active": True}`.

**Listo cuando:** agregar `("CON","VAL",8)` a la red inicial deja 20 arcos; agregar `("TEM","CON",5)` devuelve `E_RECIPROCAL` y la red sigue con 19.

### N7 — `cambiar_capacidad(red, id_arco, capacidad) -> str | None` [COMPLETO]
- [x] Cambia la capacidad del arco si `capacidad_valida`. Si no, `"E_CAPACITY"`.

**Listo cuando:** `cambiar_capacidad(red, "CON-TEM", 9)` cambia el valor; con `0` o `13` devuelve `E_CAPACITY` y no cambia nada.

### N8 — `cambiar_estado(red, id_arco, activo) -> None` [COMPLETO]
- [x] Pone `active` en `True` o `False`. No necesita validar: por la decisión D1, reactivar nunca rompe una regla.

**Listo cuando:** tras `cambiar_estado(red, "CON-TEM", False)`, `arcos_activos(red)` tiene 18 arcos.

### N9 — `eliminar_arco(red, id_arco) -> None` [COMPLETO]
- [x] Elimina el arco de `network["arcs"]`. Es la única forma de liberar el par de nodos para crear la ruta en sentido contrario.

**Listo cuando:** tras eliminar `"CON-TEM"`, `agregar_arco(red, "TEM", "CON", 5)` devuelve `None`.

---

## Interfaz — `app.py` (Streamlit)

Cómo funciona Streamlit, en una línea: **cada clic vuelve a ejecutar `app.py` completo, de arriba hacia abajo**. Lo que debe sobrevivir entre clics se guarda en `st.session_state`.

Orden obligatorio dentro de `app.py`:
1. Estado (N10).
2. Barra lateral con todos los controles y botones (N13, N15, N16, N17). Los botones modifican el estado **aquí**.
3. Zona principal: dibujo (N11, N12) y resultados (N14).

Así el dibujo siempre refleja el estado ya actualizado por el clic.

### N10 — Página base y estado [COMPLETO]
- [x] `st.set_page_config(layout="wide")`.
- [x] Si `"network"` no está en `st.session_state`: cargar `data/initial_network.json` con `cargar_red` y poner `st.session_state.result = None`.
- [x] Dos zonas: `st.sidebar` para los controles y la zona principal para el dibujo y los resultados.

**Listo cuando:** la página abre con la barra lateral y, al interactuar con cualquier control, la red no se vuelve a cargar desde el archivo.

### N11 — `red_a_dot(red, resultado=None) -> str` [COMPLETO]
- [x] Devuelve la red como texto en lenguaje DOT de Graphviz. Se muestra con `st.graphviz_chart(red_a_dot(...))`.
- [x] Encabezado: `digraph { rankdir=LR; node [shape=circle, style=filled, fillcolor=white];`
- [x] Una línea por nodo: `"STG" [label="STG\nSantiago"];`
- [x] Una línea por arco: `"STG" -> "RAN" [label="10"];` con la capacidad como etiqueta cuando `result` es `None`.

**Listo cuando:** `initial_network.json` se ve completa, de izquierda a derecha, con las 19 flechas en el sentido correcto y sus capacidades.

### N12 — Mostrar el resultado sobre el dibujo
Ampliar `red_a_dot` para cuando `result` no es `None`:
- Etiqueta de arco `x/c` (por ejemplo `7/10`), con `result["flows"]`.
- Nodos de $S$ con un `fillcolor` y nodos de $T$ con otro. Explicar los colores con un `st.caption` debajo del dibujo.
- Arcos del corte (`result["cut"]["arcs"]`): `color=red, penwidth=3`.
- Arcos desactivados: `style=dashed, color=gray`, con la capacidad como etiqueta y sin flujo. Se dibujan siempre, con o sin resultado.

**Listo cuando:** en la red inicial se distinguen a simple vista los 6 nodos de $S$, los 5 de $T$ y los 4 arcos del corte.

### N13 — Selectores de origen y destino, y botón "Calcular"
- Dos `st.selectbox` con los ids de los nodos. Valor inicial: `network["source"]` y `network["sink"]`.
- `st.button("Calcular")`: llama a `resolver(red, s, t)`. Si el resultado trae `"error"`, muestra el mensaje (N18) y deja `result = None`. Si no, lo guarda en `st.session_state.result`.

**Necesita R8.** **Listo cuando:** con la red inicial y STG → PMO se muestra el flujo 20. Elegir el mismo nodo como origen y destino muestra un aviso y no se cae.

### N14 — Panel de resultados
Solo si `result` no es `None`:
- `st.metric` para $|x|$ y para $c(S,T)$, uno al lado del otro.
- Texto con los conjuntos $S$ y $T$ y los arcos del corte.
- Las tres comprobaciones (`capacity_ok`, `conservation_ok`, `duality_ok`).
- `st.table` con el flujo y la capacidad de cada arco.
- `st.table` con `checks["conservation_table"]`.
- `st.table` con `result["iterations"]` (camino, cuello de botella, valor acumulado).

A `st.table` se le pasa una **lista de diccionarios**. No se importa `pandas`.

**Listo cuando:** para la red inicial muestra `20` en ambas métricas y 9 iteraciones.

### N15 — Panel "Editar ruta existente" [EN PROGRESO — falta verificar recálculo con R8]
En la barra lateral:
- [x] `st.selectbox` con los ids de los arcos.
- [x] `st.number_input("Capacidad", min_value=1, max_value=12, step=1)` + botón "Cambiar capacidad" → `cambiar_capacidad`.
- [x] Botón "Desactivar / Reactivar" → `cambiar_estado`.
- [x] Botón "Eliminar" → `eliminar_arco`.
- [x] Después de **cualquier** edición: `st.session_state.result = None`. Así nunca queda en pantalla un resultado que no corresponde a la red.
- [x] Si la función devuelve un código, mostrar el mensaje (N18).

**Listo cuando:** desactivar `CON-TEM` y recalcular da flujo 13.

### N16 — Panel "Agregar ruta" [EN PROGRESO — falta verificar recálculo con R8]
- [x] Dos `st.selectbox` (desde, hasta), un `st.number_input` de capacidad (1 a 12) y el botón "Agregar" → `agregar_arco`. Si devuelve un código, mostrar el mensaje (N18). Si no, `result = None`.

**Listo cuando:** agregar `CON → VAL` con 8 y recalcular da flujo 23. Intentar `TEM → CON` muestra el aviso de arco recíproco. Intentar `CON → CON` muestra el aviso de lazo.

### N17 — Selector de configuraciones [EN PROGRESO — faltan selectores s/t de N13]
- [x] `st.selectbox` con: "Red inicial", "Modificación 1", "Modificación 2", "Caso manual", "Figura 1", y un botón "Cargar". Al cargar: `cargar_red` del JSON correspondiente y `result = None`. Si el archivo no existe todavía, mostrar un aviso con `st.warning`.

**Listo cuando:** se puede pasar de una red a otra sin reiniciar la aplicación, y los selectores de origen y destino muestran los nodos de la red cargada.

### N18 — `MENSAJES_ERROR` [COMPLETO]
- [x] Un diccionario `código → texto en español`. Los avisos se muestran con `st.warning(MENSAJES_ERROR[code])`. Ejemplo: `"E_RECIPROCAL": "Ya existe la ruta en sentido contrario. Elimínela antes de crear esta."`

**Listo cuando:** todos los códigos de `docs/fase0-stack-y-contrato.md` §5 tienen mensaje.

---

## Repositorio y presentación

### N19 — Instrucciones, repositorio y demo
- Mantener al día la sección "Cómo ejecutar" del `README.md`.
- Confirmar que el repositorio es público abriendo el enlace en una ventana de incógnito.
- Tomar las capturas de la interfaz que pida Sebastián.
- Preparar su parte de la presentación: demostración en vivo (cargar la red, elegir origen y destino, calcular, mostrar el corte).
- Antes de la presentación, dejar Streamlit instalado y probado en el computador que se usará. La instalación necesita internet; la ejecución no.

**Listo cuando:** alguien que no es del equipo clona el repositorio y lo ejecuta siguiendo solo el README.
