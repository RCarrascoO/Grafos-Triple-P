## Proyecto 2. Simulador de una red de distribución de paquetes

Teoría de Grafos – INFO1158

Ver plataforma Educa para los grupos de trabajo. Presentación: 26 de noviembre de 2026.

## Planteamiento del problema

Una empresa de distribución de paquetes opera una red de centros logísticos conectados por rutas de transporte. Cada ruta tiene un sentido de circulación y una capacidad máxima de traslado, expresada en paquetes por hora. Los paquetes pueden pasar por diferentes centros intermedios antes de llegar a su destino. La cantidad máxima que puede transportarse depende de las conexiones disponibles y de sus capacidades. Una ruta con capacidad elevada puede resultar insuficiente si los enlaces posteriores admiten un flujo menor. De igual manera, la interrupción de una ruta o la incorporación de una conexión puede modificar la capacidad total de la red. La Figura 1 representa una red ilustrativa de seis centros. El vértice O corresponde al origen, T al destino y A, B, C y D a centros intermedios. Los valores sobre los arcos indican sus capacidades de transporte.

Figura 1: Red de ejemplo. Las flechas indican el sentido de transporte y las etiquetas señalan capacidades máximas, en paquetes por hora.

En este ejemplo, los arcos que salen de O admiten en conjunto hasta 14 paquetes por hora. Para determinar cuánto puede llegar efectivamente a T también es necesario considerar las capacidades intermedias. Una distribución factible utiliza los trayectos O A C T, O A D T y O B D T, transportando respectivamente 5, 3 y 6 paquetes por hora. Así se alcanzan 14 paquetes por hora sin superar ninguna capacidad. La empresa requiere examinar redes de mayor tamaño, identificar sus restricciones de transporte y comparar configuraciones en las que se modifiquen conexiones o capacidades. El proyecto consiste en construir una aplicación que permita realizar ese análisis y mostrar sus resultados mediante una

representación interactiva.

## Desarrollo solicitado

- 1. Modelación matemática de la red.

Represente la configuración inicial mediante un grafo dirigido G = (V, E) y una función de capacidad c que asigne a cada arco su capacidad máxima:

10

Cada vértice representará un centro logístico y cada arco una ruta. El grafo no podrá contener lazos, arcos repetidos ni arcos recíprocos entre un mismo par de centros. Ningún vértice quedará aislado.

12, 15

20,

c : E

2, . . . , 12}.


Se elegirán dos vértices diferentes, origen s y destino t, para los que existan al menos dos caminos dirigidos distintos de s a t.

Identifique los conjuntos V y E, los valores de c y el significado de los elementos del modelo.

Los intervalos de vértices y arcos se exigirán en la configuración inicial.

- 2. Investigación, selección e implementación del algoritmo.

Investigue al menos dos estrategias algorítmicas para resolver el problema de flujo máximo en redes dirigidas con capacidades.

Puede comparar, por ejemplo, el método de Ford–Fulkerson utilizando búsqueda en profundidad

IA

IA

para seleccionar caminos aumentantes y el algoritmo de Edmonds–Karp, que utiliza búsqueda en anchura para esa selección.

Considere que Edmonds–Karp es una variante del método de Ford–Fulkerson.

Describa el funcionamiento de las alternativas, compare sus características y justifique cuál selecciona para resolver el problema planteado.

La argumentación deberá apoyarse en fuentes académicas o técnicas identificables.

Implemente mediante código el algoritmo seleccionado, junto con los procedimientos auxiliares que requiera.

La solución deberá calcular un flujo x que respete las restricciones de capacidad:

Asimismo, deberá cumplir la conservación del flujo en cada vértice intermedio:

El valor de un flujo se obtiene mediante la cantidad neta que sale del origen:

La aplicación deberá determinar el valor máximo posible y mostrar el flujo asignado a cada arco original junto con su capacidad.

- 3. Corte mínimo y visualización interactiva.

Investigue el teorema de flujo máximo–corte mínimo.

Para una partición V = S T, con S T = ∅, s S y t T, la capacidad del corte se define mediante:

A partir del flujo máximo calculado, identifique un corte mínimo y compruebe que su capacidad coincide con el valor de ese flujo.

Señale los conjuntos S y T y los arcos que van desde S hacia T.

La interfaz deberá representar los centros logísticos, las rutas, sus direcciones y capacidades.

Deberá permitir seleccionar un origen y un destino, ejecutar el algoritmo implementado y visualizar el valor del flujo máximo, el flujo y la capacidad de cada arco, y la partición correspondiente a un corte mínimo.

No se requiere desarrollar animaciones ni una interfaz gráfica compleja.


## 4. Simulación y análisis de modificaciones.

La aplicación deberá permitir realizar las siguientes modificaciones desde la interfaz, sin editar el código fuente:

- Desactivar una ruta existente.

- Modificar la capacidad de una ruta.

- Agregar una nueva conexión.

No se admitirán lazos, arcos repetidos ni arcos recíprocos.

Cada ruta activa tendrá una capacidad entera entre 1 y 12 paquetes por hora.

Compare tres configuraciones: la red inicial y dos modificaciones elegidas por el grupo.

Para cada una, calcule el flujo máximo y un corte mínimo, e interprete las diferencias.

Las modificaciones podrán alterar el número inicial de arcos.

Los cálculos podrán actualizarse mediante una acción de recálculo.

## 5. Verificación de resultados.

Construya un caso de comprobación de entre cuatro y seis vértices, con capacidades enteras, que permita resolver manualmente el problema.

Determine un flujo factible y un corte con capacidades coincidentes, de manera que quede justificada la optimalidad de ambos resultados.

Compare el cálculo manual con los resultados del código, identifique los valores obtenidos en cada procedimiento y explique cualquier diferencia encontrada.

Para la red principal y sus dos modificaciones, compruebe que los flujos respetan las capacidades de los arcos, que se conserva el flujo en los vértices intermedios y que el valor máximo coincide con la capacidad del corte mínimo.

## Condiciones de implementación y documentación

- Implementar con código propio el algoritmo de flujo máximo seleccionado y sus procedimientos auxiliares.

- No utilizar bibliotecas que realicen los cálculos algorítmicos solicitados. Se permiten las estructuras básicas del lenguaje y las bibliotecas para gráficos e interfaz.

- Incluir comentarios que expliquen las funciones principales, sus entradas y sus resultados.

- Identificar las fuentes académicas y técnicas consultadas para fundamentar la selección e imple- mentación del algoritmo.


## Entrega y presentación

El informe técnico y la presentación tendrán una ponderación de 50% cada uno.

Ambos se calificarán sobre 20 puntos, con un total de 40.

Cada grupo deberá entregar, a través de Educa, un informe técnico en formato PDF el jueves 26 de noviembre de 2026, hasta las 23:00 horas.

El documento incluirá la formulación matemática de la red, la investigación y comparación de alternativas algorítmicas, la justificación de la solución seleccionada, la explicación de su implementación y los resultados de las tres configuraciones analizadas.

Deberá incorporar el desarrollo matemático de la verificación solicitada en el apartado 5 y, cuando corresponda,

imágenes o capturas que permitan contrastar las salidas del código con los resultados obtenidos manualmente. El informe deberá contener un enlace accesible al repositorio o carpeta donde se encuentre alojado el código fuente completo, acompañado de sus dependencias e instrucciones de ejecución.

Se identificarán las fuentes académicas y técnicas utilizadas.

## Informe técnico (50%).

## Rúbrica del informe técnico.

Cada criterio se calificará de 0 a 4 puntos. Se marcará el nivel correspondiente y se registrará el puntaje en la última columna.

Escala: 0 = sin evidencia; 1 = insuficiente; 2 = desarrollo parcial; 3 = satisfactorio con observaciones menores; 4 = completo, correcto y fundamentado.

| Criterio | 0 1 2 3 4 Puntaje |
| --- | --- |
| 1. Formulación matemática: vértices, arcos, capacidades, restricciones y | □ □ □ □ □ |
| significado del modelo. |   |
| 2. Investigación y selección: comparación de alternativas y justificación | □ □ □ □ □ |
| documentada del algoritmo. |   |
| 3. Implementación propia: código del algoritmo, funciones | □ □ □ □ □ |
| documentadas y enlace accesible al código fuente. |   |
| 4. Resultados y análisis: flujo máximo, corte mínimo y comparación de | □ □ □ □ □ |
| las tres configuraciones. |   |
| 5. Verificación: resolución manual, comprobaciones matemáticas y | □ □ □ □ □ |
| evidencia de contraste con el código. |   |

Puntaje total del informe:

/20.

Presentación (50 %).

La presentación presencial se realizará el jueves 26 de noviembre de 2026, con una duración máxima de 12 minutos por grupo.

Los tres integrantes deberán participar y demostrar el funcionamiento de la aplicación mediante la visualización de la red, la ejecución del cálculo de flujo máximo, la identificación de un corte mínimo y una modificación interactiva que permita comparar resultados.

El docente podrá formular preguntas sobre el modelo, el algoritmo y el código.

## Rúbrica de la presentación.

Se utilizará la misma escala de 0 a 4 puntos.

| Criterio | 0 1 2 3 4 Puntaje |
| --- | --- |
| 1. Exposición del problema y de su representación matemática | □ □ □ □ □ |
| mediante grafos. |   |
| 2. Explicación y fundamento de la elección del algoritmo | □ □ □ □ □ |
| implementado. |   |
| 3. Demostración funcional de la aplicación y visualización de los | □ □ □ □ □ |
| resultados. |   |
| 4. Simulación interactiva, comparación e interpretación de cambios en | □ □ □ □ □ |
| la red. |   |
| 5. Participación de los integrantes y respuestas a las preguntas del | □ □ □ □ □ |
| docente. |   |

Puntaje total de la presentación:

/20.

Puntaje total del proyecto:

/40.
