# Tareas de Sebastián — verificación, pruebas, escenarios y QA

**Leer antes:** `docs/fase1-diseno-redes.md` (§2 caso manual, §1.6 y §1.7 valores esperados), `docs/fase2-algoritmo.md` (§7.3 y §8) y las convenciones de `docs/tareas/README.md`.

**Archivos propios:** `core/verify.py`, `tests/`, `data/mod1.json`, `data/mod2.json`.
**Imports permitidos:** biblioteca estándar (`unittest`, `itertools`, `random`, `copy`) y los módulos de `core/`.

Regla de `verify.py`: calcula todo desde `flows` y la red, **sin usar la red residual ni el motor**. Su trabajo es comprobar al motor, así que no puede depender de él.

`flows` es un diccionario `{arc_id: flujo}` con los arcos activos.

---

## Cálculo manual

### S1 — Resolver a mano el caso manual
Con `data/manual_case.json` y **sin mirar** `docs/fase1-diseno-redes.md` §2.2–§2.4:
- Aplicar Edmonds–Karp (BFS, vecinos en orden alfabético) y anotar en cada iteración el camino, el cuello de botella y $|x|$.
- Dibujar la red residual después de cada iteración.
- Obtener el flujo final por arco, el corte $(S,T)$ y $c(S,T)$.

**Listo cuando:** el resultado coincide con §2.3 y §2.4 (flujo 8, $S=\{s,a,c\}$), o se informa al equipo la diferencia. Los dibujos quedan guardados para el informe.

---

## Verificación — `core/verify.py`

### S2 — `check_capacity(network, flows) -> bool`
`True` si para cada arco activo el flujo es un entero y `0 <= flows[id] <= capacity`.

**Listo cuando:** da `True` con el flujo de la Figura 1 y `False` si se cambia un flujo a `capacity + 1` o a `-1`.

### S3 — `check_conservation(network, flows, s, t) -> tuple[bool, list]`
Para cada nodo distinto de `s` y `t`: suma lo que entra y lo que sale por arcos activos.
- Devuelve `(ok, tabla)`, donde `tabla` es una lista de `{"node": id, "in": int, "out": int}` ordenada por id.
- `ok` es `True` si `in == out` en todas las filas.

**Listo cuando:** con el flujo de `docs/fase1-diseno-redes.md` §2.3 devuelve `True` y la fila de `a` es `in=3, out=3`.

### S4 — `flow_value(network, flows, s) -> int`
$|x|$ según el enunciado: suma de flujos que salen de `s` menos suma de flujos que entran a `s`.

**Listo cuando:** devuelve 14 para la Figura 1 y 8 para el caso manual.

### S5 — `cut_capacity(network, S) -> int`
Suma de capacidades de los arcos activos con `from` en `S` y `to` fuera de `S`.

**Listo cuando:** en la red inicial con $S = \{\text{STG, RAN, TAL, CHI, CON, LAN}\}$ devuelve 20; con $S = \{\text{STG}\}$ devuelve 28.

### S6 — `verify_all(network, flows, S, s, t) -> dict`
Une S2–S5 y devuelve el bloque `checks` del contrato:

```python
{
  "capacity_ok": bool,
  "conservation_ok": bool,
  "conservation_table": list,
  "duality_ok": bool,   # flow_value == cut_capacity, s está en S y t no está en S
}
```

**Listo cuando:** con el flujo y el corte del caso manual los tres valores son `True`; con un $S$ equivocado (por ejemplo `{"s"}`), `duality_ok` es `False`. **Rodrigo necesita esta función para R8.**

---

## Pruebas — `tests/` (con `unittest`)

Todas se ejecutan con `python -m unittest`.

### S7 — `tests/test_known_cases.py`
Un test por red que compare `solve` con los valores esperados:

| Red | $\lvert x\rvert$ | Iteraciones | $S$ |
| --- | --- | --- | --- |
| `figura1.json` | 14 | 3 | `["O"]` |
| `manual_case.json` | 8 | 3 | `["a", "c", "s"]` |
| `initial_network.json` | 20 | 9 | `["CHI", "CON", "LAN", "RAN", "STG", "TAL"]` |

En cada uno comprobar además que los tres `checks` son `True` y que `max_flow_value == cut["capacity"]`.

**Listo cuando:** los tres tests pasan.

### S8 — `tests/test_modifications.py`
Sobre una copia (`copy.deepcopy`) de la red inicial, usando las funciones de `core/edits.py`:
- `set_active("CON-TEM", False)` → flujo 13.
- `set_capacity("CON-TEM", 9)` → flujo 21.
- `add_arc("CON", "VAL", 8)` → flujo 23 y corte `["OSO-PMO", "VAL-PMO"]`.

**Necesita N6–N8.** **Listo cuando:** los tres tests pasan.

### S9 — `tests/test_edge_cases.py`
- Destino inalcanzable (desactivar `VAL-PMO` y `OSO-PMO`): flujo 0, `iterations == []`, capacidad del corte 0.
- `solve(red, "STG", "STG")` devuelve `{"error": "E_ST_EQUAL"}`.
- Un arco desactivado no aparece en `flows`.

**Listo cuando:** los tres tests pasan.

### S10 — `tests/test_brute_force.py`
- Función auxiliar `brute_force_min_cut(network, s, t) -> int`: prueba todos los subconjuntos de nodos intermedios con `itertools.combinations`, arma $S$ = `{s}` más el subconjunto, y devuelve la menor `cut_capacity`.
- Test: para los tres JSON, ese mínimo es igual a `max_flow_value`.
- Test: lo mismo para 20 redes aleatorias de 6 nodos generadas con `random.seed(1)` y `add_arc` (así salen válidas por construcción).

**Listo cuando:** los tests pasan. Es la prueba más fuerte de que el motor es correcto, porque no usa el algoritmo para comprobarlo.

### S11 — `tests/test_validation.py`
Probar los casos "listo cuando" de las tareas N2, N3, N5, N6 y N7 de Renato (códigos de error de lazos, repetidos, recíprocos y capacidad).

**Necesita N2–N7.** **Listo cuando:** los tests pasan.

---

## Escenarios, informe y QA

### S12 — Elegir y crear las dos modificaciones
- Con el equipo, elegir dos de las candidatas de `docs/fase1-diseno-redes.md` §1.7 (u otras). Conviene que entre las dos usen las tres operaciones: desactivar, cambiar capacidad y agregar.
- Crear `data/mod1.json` y `data/mod2.json` copiando `initial_network.json`, aplicando los cambios a mano y poniendo `"profile": "modified"`.

**Listo cuando:** ambos archivos cargan desde el selector de la interfaz y `validate_network` devuelve `[]`.

### S13 — Resultados, capturas y secciones 4 y 5 del informe
Para el caso manual y las tres configuraciones:
- Ejecutar en la aplicación y tomar una captura de cada una.
- Armar las tablas del apartado 5 a partir de `checks` y `flows`: capacidad por arco, conservación por nodo y $|x| = c(S,T)$.
- Sección 4: tabla comparativa de las tres configuraciones (flujo, corte, arcos del corte) e interpretación de cómo se mueve el cuello de botella.
- Sección 5: resolución manual de S1 contrastada con la salida del programa. Si hay diferencias en caminos o flujos por arco, explicarlas (puede haber más de un flujo máximo o más de un corte mínimo).

**Listo cuando:** cada número de las secciones 4 y 5 se puede rastrear a una captura o a una tabla.

### S14 — Batería de QA sobre la interfaz
Probar a mano, con la aplicación abierta, y anotar el resultado de cada caso:

| Caso | Resultado esperado |
| --- | --- |
| Capacidad 0, −5, 13 o 2.5 | El control no deja ingresarla, o aparece un aviso. La red no cambia |
| Agregar un lazo (mismo nodo en "desde" y "hasta") | Aviso de lazo |
| Agregar una ruta que ya existe | Aviso de ruta repetida |
| Agregar la ruta contraria a una existente | Aviso de ruta recíproca |
| Agregar la ruta contraria a una **desactivada** | Aviso de ruta recíproca |
| Mismo nodo como origen y destino | Aviso, sin cálculo |
| Desactivar rutas hasta aislar el destino | Flujo 0, sin caídas |
| Editar después de calcular | El resultado anterior desaparece hasta recalcular |
| Cambiar de configuración varias veces | Sin caídas ni restos del dibujo anterior |

**Listo cuando:** todos los casos dan el resultado esperado, o cada falla está informada a Renato o Rodrigo. Además, preparar su parte de la presentación: modificación en vivo y comparación.
