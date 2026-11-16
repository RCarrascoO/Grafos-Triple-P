# Informe técnico — ensamblado (tarea D6)

Ensambla: Daniel Prado. Entrega: PDF en Educa, jueves 26 de noviembre de 2026, hasta las 23:00.

## Secciones y responsables

Cada sección es un archivo Markdown en esta carpeta. Los símbolos son los de [00-notacion.md](00-notacion.md).

| Orden | Archivo | Contenido | Responsable | Tarea | Estado |
| --- | --- | --- | --- | --- | --- |
| 0 | Portada | Título, ramo (INFO1158), los cuatro integrantes, fecha, **enlace al repositorio** | Daniel | D6 | Pendiente |
| 1 | [01-modelacion.md](01-modelacion.md) | Modelación matemática de la red | Daniel | D3 | Listo; falta la figura 1.1 |
| 2 | `02-algoritmo.md` | Investigación, comparación y selección del algoritmo | Rodrigo | R9 | Pendiente |
| 3 | `03-corte-e-implementacion.md` | Teorema de flujo máximo–corte mínimo y explicación del código | Rodrigo | R10 | Pendiente |
| 4 | `04-resultados.md` | Tres configuraciones: flujo máximo, corte mínimo e interpretación | Sebastián | S13 | Pendiente |
| 5 | `05-verificacion.md` | Caso manual, comprobaciones y contraste con el código | Sebastián | S13 | Pendiente |
| 6 | `06-referencias.md` | Fuentes académicas y técnicas confirmadas | Rodrigo | R11 | Pendiente |

El glosario de `00-notacion.md` va como anexo o al inicio de la sección 1, según el espacio.

## Revisión contra la rúbrica (antes de exportar el PDF)

Cada criterio vale de 0 a 4 puntos.

- [ ] **1. Formulación matemática:** $V$, $E$, tabla de $c$, restricciones auditadas y significado del modelo (sección 1).
- [ ] **2. Investigación y selección:** dos alternativas descritas, tabla comparativa, justificación y citas identificables (sección 2).
- [ ] **3. Implementación propia:** explicación de cada función, docstrings en el código y enlace accesible al repositorio, abierto en ventana de incógnito (sección 3 y portada).
- [ ] **4. Resultados y análisis:** flujo máximo, corte mínimo y comparación de las tres configuraciones, con capturas (sección 4).
- [ ] **5. Verificación:** resolución manual, tablas de capacidad y conservación, $\lvert x\rvert = c(S,T)$ y contraste con el código (sección 5).

Además:

- [ ] Las cinco secciones usan los símbolos de `00-notacion.md` (lista de revisión al final de ese archivo).
- [ ] Los valores del informe coinciden con la salida del programa: $\lvert x\rvert$, $S$, $T$ y $c(S,T)$ de las tres configuraciones y del caso manual.
- [ ] El informe incluye dependencias e instrucciones de ejecución, o remite al `README.md` del repositorio.
- [ ] Las fórmulas se ven bien en el PDF exportado.
