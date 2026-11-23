# 6. Referencias

> Apartado 6 del informe (tarea R11, redacta: Rodrigo Pedraza). Todas las referencias bibliográficas de `docs/fase2-algoritmo.md` §9 fueron verificadas en autoría, año, edición, capítulos, páginas y códigos de identificación (DOI/ISBN).

## 6.1 Fuentes académicas

- Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). *Network Flows: Theory, Algorithms, and Applications* (caps. 6 y 7, pp. 166–249). Prentice Hall. ISBN 978-0-13-617549-0.
  *Consultada para el teorema de integralidad, algoritmos de camino aumentante más corto y marco general de algoritmos polinomiales de flujo máximo.*

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3.ª ed., cap. 26 "Maximum Flow", pp. 708–768; §26.1 "Flow networks", pp. 709–714; §26.2 "The Ford-Fulkerson method", pp. 714–732). The MIT Press. ISBN 978-0-262-03384-8. *(En la 4.ª ed., 2022, corresponde al cap. 24, pp. 670–703.)*
  *Consultada para la formalización de redes residuales, demostración del teorema de flujo máximo–corte mínimo, análisis de Edmonds–Karp y ejemplo del peor caso de Ford–Fulkerson.*

- Dinic, E. A. (1970). Algorithm for solution of a problem of maximum flow in networks with power estimation. *Soviet Mathematics Doklady*, 11, 1277–1280.
  *Consultada para contextualizar alternativas polinomiales de flujo máximo basadas en redes por niveles y flujos bloqueantes en $O(\lvert V\rvert^2 \cdot \lvert E\rvert)$.*

- Edmonds, J., & Karp, R. M. (1972). Theoretical improvements in algorithmic efficiency for network flow problems. *Journal of the ACM*, 19(2), 248–264. https://doi.org/10.1145/321694.321699
  *Fuente original del algoritmo de Edmonds–Karp y de la demostración de su complejidad polinomial $O(\lvert V\rvert \cdot \lvert E\rvert^2)$ independiente de las capacidades.*

- Ford, L. R., Jr., & Fulkerson, D. R. (1956). Maximal flow through a network. *Canadian Journal of Mathematics*, 8, 399–404. https://doi.org/10.4153/CJM-1956-045-5
  *Fuente original del método de caminos aumentantes y del teorema de flujo máximo–corte mínimo.*

- Kleinberg, J., & Tardos, É. (2006). *Algorithm Design* (cap. 7 "Network Flow", pp. 337–450). Addison-Wesley. ISBN 978-0-321-29535-4.
  *Consultada para el análisis de terminación con capacidades enteras, dualidad débil/fuerte e interpretación de cortes mínimos.*

## 6.2 Fuentes técnicas

- Python Software Foundation. *The Python Standard Library — `collections`: Container datatypes (`deque`)*. https://docs.python.org/3/library/collections.html
  *Documentación oficial de la cola de doble extremo empleada en la búsqueda en anchura de `core/max_flow.py` y `core/min_cut.py`.*

- Streamlit Inc. *Streamlit Documentation — `st.graphviz_chart`*. https://docs.streamlit.io/develop/api-reference/charts/st.graphviz_chart
  *Documentación oficial del componente de visualización de grafos en la interfaz `app.py`.*

- Graphviz. *DOT Language Specification*. https://graphviz.org/doc/info/lang.html
  *Referencia de la sintaxis DOT utilizada para describir vértices, arcos, etiquetas y estilos del corte mínimo en la interfaz.*
