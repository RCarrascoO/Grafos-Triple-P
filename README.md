# Grafos-Triple-P — Simulador de una red de distribución de paquetes

Proyecto 2 de Teoría de Grafos (INFO1158). La aplicación calcula el **flujo máximo** y un **corte mínimo** en una red dirigida de centros logísticos, los muestra en una interfaz y permite modificar la red (desactivar rutas, cambiar capacidades, agregar conexiones) para comparar configuraciones.

**Entrega del informe y presentación:** jueves 26 de noviembre de 2026.

**Integrantes:** Daniel Prado, Rodrigo Pedraza, Renato Carrasco y Sebastián Pereda.

## Estado

En desarrollo. El diseño (fases 0 a 2), las redes de datos y las tareas están listos. El código de `core/` y `app.py` se está escribiendo según `docs/tareas/`.

## Requisitos

- Python 3.11 o superior.
- Streamlit, solo para la interfaz. Es la única dependencia.

## Cómo ejecutar

Crear un entorno virtual e instalar Streamlit (recomendado, evita conflictos con Python del sistema):

```bash
python -m venv .venv
```

Activar el entorno según la terminal:

- **bash / zsh (Linux/macOS):** `source .venv/bin/activate`
- **fish (Linux/macOS):** `source .venv/bin/activate.fish`
- **PowerShell (Windows):** `.venv\Scripts\Activate.ps1`

Instalar y ejecutar:

```bash
pip install -r requirements.txt
streamlit run app.py
```

*(Alternativa sin activar el entorno en cualquier shell Linux/macOS: `.venv/bin/streamlit run app.py`.)*

Pruebas (no requieren Streamlit, solo biblioteca estándar):

```bash
python -m unittest
```

## Regla principal del proyecto

El algoritmo de flujo máximo (Edmonds–Karp), el corte mínimo y sus procedimientos auxiliares están programados con código propio. **Ningún archivo del repositorio importa `networkx`, `scipy`, `numpy`, `pandas` ni otra biblioteca de grafos o cálculo.** Streamlit se usa solo para la interfaz; su componente Graphviz solo ubica y dibuja los nodos.

## Estructura

```
app.py           Interfaz Streamlit (solo muestra y llama a core/)
requirements.txt streamlit
core/            Motor: red, validación, ediciones, flujo máximo, corte mínimo, verificación (solo biblioteca estándar)
data/            Redes en JSON: Figura 1, caso manual, red inicial y modificaciones
tests/           Pruebas con unittest
docs/            Diseño por fases y tareas por integrante
```

## Documentación

| Documento | Contenido |
| --- | --- |
| [Enunciado (PDF)](Proyecto%202%20Simulador%20de%20una%20red%20de%20distribución%20de%20paquetes.pdf) | Fuente de verdad del proyecto y rúbricas |
| [Fase 0](docs/fase0-stack-y-contrato.md) | Stack, arquitectura, contrato JSON y reglas de validación |
| [Fase 1](docs/fase1-diseno-redes.md) | Red inicial, caso de verificación manual y valores esperados |
| [Fase 2](docs/fase2-algoritmo.md) | Comparación de algoritmos, teorema de flujo máximo–corte mínimo y diseño del motor |
| [Tareas](docs/tareas/README.md) | Tareas detalladas por integrante, orden y fechas |

## Responsables

| Integrante | Área | Tareas |
| --- | --- | --- |
| Daniel Prado | Modelo matemático, red inicial, contrato de datos, informe | [índice](docs/tareas/README.md) |
| Rodrigo Pedraza | Motor de flujo máximo y corte mínimo | [rodrigo.md](docs/tareas/rodrigo.md) |
| Renato Carrasco | Validación, ediciones, interfaz y repositorio | [renato.md](docs/tareas/renato.md) |
| Sebastián Pereda | Verificación, pruebas, escenarios y QA | [sebastian.md](docs/tareas/sebastian.md) |

## Agentes de IA

Las reglas para trabajar con agentes (Codex, Claude, Copilot, etc.) están en [AGENTS.md](AGENTS.md).
