# Instrucciones para agentes de IA

Si eres un agente de IA (Codex, Claude, Copilot, etc.) trabajando en este repositorio, estas reglas son obligatorias.

### Antes de escribir

1. Lee la tarea que te pidieron en `docs/tareas/` y el documento de fase que cita.
2. Haz **solo esa tarea**. No adelantes otras ni toques archivos de otro integrante.
3. Respeta los nombres y las firmas de función de la tarea. Otros módulos dependen de ellos.

### Modo "ponytail": el mínimo código que resuelve la tarea completa

Actúa como un desarrollador senior flojo: el mejor código es el que no se escribe. Toma la primera opción que funcione por completo:

1. ¿Hace falta que exista? Si nadie lo pidió, no lo escribas. Nombra en una línea lo que omitiste.
2. ¿Ya existe en este repositorio? Úsalo (por ejemplo `active_arcs`, `valid_capacity`).
3. ¿Lo resuelve la biblioteca estándar de Python? Úsala.
4. ¿Cabe en una línea que se entiende de un vistazo? Una línea.
5. Si no: el mínimo código que funcione.

Reglas concretas:

- **Sin dependencias nuevas.** La única es `streamlit`, y solo se importa en `app.py`. Nunca importes `networkx`, `scipy`, `numpy`, `pandas`, `matplotlib` ni similares, aunque estén instalados.
- **Sin abstracciones que nadie pidió:** nada de clases, herencia, dataclasses, patrones, wrappers, archivos de configuración, opciones ni código "para después". La red es el diccionario del JSON y las funciones son funciones simples.
- **Sin manejo de errores decorativo.** Las funciones de validación devuelven un código de error o `None`. No agregues `try/except` salvo al leer archivos desde la interfaz.
- **El diff más corto gana**, pero una línea que hay que descifrar no es corta.
- **Flojo con la solución, nunca con la tarea:** termina todo lo que la tarea exige, incluido su "listo cuando".
- **Entre dos opciones del mismo tamaño**, elige la que es correcta en los casos borde.
- **Lógica nueva con ramas o bucles deja una comprobación:** un test pequeño en `tests/` o el "listo cuando" de la tarea convertido en `assert`.
- **Un atajo con límite conocido** lleva un comentario: `# atajo: <el límite>, <cuándo mejorarlo>`.

Lo que **nunca** se recorta:

- Los invariantes de la red: sin lazos, sin arcos repetidos, sin arcos recíprocos, capacidades enteras de 1 a 12.
- La validación de todo lo que el usuario ingresa en la interfaz.
- El **docstring de cada función** (propósito, entradas, salida). Es un requisito del enunciado, así que aquí no aplica "comentar lo mínimo". Fuera del docstring, comenta solo el porqué que el código no muestra.
- Las comprobaciones de `core/verify.py`.

### Separación de capas

- `core/` y `tests/` no importan `streamlit` ni `app.py`: solo biblioteca estándar.
- `app.py` no calcula ni valida: llama a `core/` y muestra. A `st.table` se le pasan listas de diccionarios.
- `core/verify.py` no usa la red residual ni el motor.

### Al terminar

Cierra tu respuesta con una o dos líneas: qué omitiste o no comprobaste, y cualquier riesgo que el integrante deba conocer. No hagas commits: los hace cada integrante.
