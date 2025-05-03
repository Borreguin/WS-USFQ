## Taller 2 de inteligencia artificial

- **Grupo 1**
- **Integrantes del grupo**:
  * Patricia Lema
  * Ana Navas
  * Diana Córdova
  * Sebastián Ruiz

## 1. Uso de Algoritmos de Búsqueda

El objetivo de esta tarea es utilizar cualquier algoritmo de búsqueda para resolver los 3 laberintos propuestos, 
el reto es poder visualizar/representar los resultados, adicionalmente poder comparar al menos 2 algoritmos de búsqueda 
y mirar cómo se comportan para cada laberinto

### A. Leer el laberinto y representarlo como un grafo.

En el punto C se puede ver la estrucutra que se usó para representar el laberinto como un grafo. La función recorre todas las celdas del laberinto qy agrega nodos a aquellas que no son muro, procede a buscar otras celdas sin muros. 

### B. Aplicar algoritmos de búsqueda

Se utilizaron cuatro algoritmos diferentes para los 3 laberintos en el caso de estudio número 1. El primer algoritmo que se corrió fue el Breadth-First Search. La lógica detrás de este laberinto es buscar el camino a través de los vecinos más cercanos. En general, esto funciona bastante bien para grafos en donde no hay ponderación. El segundo fue el Depth-Frist Search, que explora cada rama hasta llegar a su nodo más profundo antes de retroceder. El tercer algoritmo fue el Djistra, es un algoritmo de costo uniforme que explora la ruta de menor costo acumulado, es un algoritmo voraz que garantiza la ruta óptima si los costos son positivos. El cuarto algoritmo es el A estrella, que usa la heurística (o información adicional que ayuda a encontrar la solución óptima)

#### B.1 Tipos de parámetros de evaluación

Para la evaluación usamos la información que se contiene en el artículo de Tomás, Nuñez y Hernández (n.d) en donde medir la distancia que recorre el camino y el tiempo que demora el algoritmo puede indicar cuál elegir. El artículo destaca que BFS recorre más espacio, DFS es más directo pero no óptimo, Dijkstra garantiza soluciones mínimas de costo acumulado y A estrella usa la heurística para garantizar la mejor solución en el menor espacio de búsqueda posible. 

RESULTADOS: 
En el caso del laberinto 3 notamos que: 
Cuando se compara el tiempo y las distancias de los 4 algoritmos vemos que todos, excepto el DFS, obtienen rutas igualmente cortas. El DFS, al explorar cada rama en su profundidad, aumenta la distancia del camino recorrido, aunque no aumentó el tiempo significativamente (tiene un tiempo de 4.0ms, incluso menor al de A estrella). El algoritmo Dijkstra fue el más rápido, seguido por BFS y A estrella.

En el caso del laberinto 1 notamos que: 
Cuando se compara el tiempo y las distancias de los 4 algoritmos vemos que el DFS es el más rápido y encuentra una rota tan corta como la hallada por los otros 3 algoritmos. El BFS y el Dijkstra son los algoritmos que más tiempo demoraron, casi tres veces el tiempo del DFS. 

En el caso del laberinto 2 notamos que: 

El algoritmo A estrella fue el más rápido, seguido por el DFS. Mientras tanto, el algoritmo Dijkstra y BFS fueron más lentos. No obstante, los 4 algoritmos encontraron caminos con la misma distancia. 

##En este caso, se agregaron pesos a los laberintos para probar los algoritmos Dijkstra y A estrella, que responden a grafos con costo de una mejor manera. Encontramos lo siguiente

En el laberinto 1 notamos que: 
Es un laberinto simple, o sea un grafo pequeño, por lo que no vale la pena sobrecargar computacionalmente al calcular A estrella (heurística) porque no da una ganancia significativa en eficiencia. Por lo tanto, Dijkstra encuentra la mejor solución al ser ligeramente más rápido. 

En el laberinto 2 notamos que: 
Quizás por la simplicidad del laberinto no hay gran diferencia, dado que el camino encontrado tiene la misma distancia para ambos algoritmos. El A esgtrella fue el más rápido, lo que puede explicarse por el uso de heurística con distancia Manhattan. Djikstra, al ser un algoritmo voraz que no usa heurística, puede haber evaluado nodos innecesarios. 

En el laberinto 3 notamos que: 
A pesar de lo que se hubiera esperado, el algoritmo Dijkstra fue el más rápido. Ambos algoritmos encontraron el camino con la misma distancia. Gracias a un poco de investigación más profunda, podemos suponer que esto se debe a que el A estrella debe calcular las heurísticas en cada nodo, para decidir cuál explorar primero, quizás en este caso de laberinto más complejo, el tiempo de cada cálculo se acumuló de manera que resultó un poco más lento que el Djisktra, que no tiene que explorar heurística y evita sobrecarga computacional. Este trade-off es importante tenerlo en cuenta. 

### C. Describir los parámetros del modelo.

Los laberintos se cargaron desde Github a Google Colab y las celdas se representaron mediante los siguientes caracteres: 

#: muro 
espacio vacío: celda sin obstáculos
E: entrada
S: salida

Parámetros de los algoritmos de búsqueda

Cada algoritmo devuelve:

Una ruta (lista de coordenadas).
Un tiempo de ejecución (en segundos).
Variables de salida:
bfs_path, bfs_time
dfs_path, dfs_time
dijkstra_path, dijkstra_time
a_star_path, a_star_time

### Soluciones
Laberinto 1: 
Sin pesos: ![image](https://github.com/user-attachments/assets/59de3a40-4d3e-4270-93c5-48a10f887cd9)

Con pesos: ![image](https://github.com/user-attachments/assets/04a26019-4cda-452e-bf46-ecc85e162d2d)

Laberinto 2:
Sin pesos: ![image](https://github.com/user-attachments/assets/15c0e87d-d448-4a19-9384-188901089cbe)

Con pesos: ![image](https://github.com/user-attachments/assets/3636e3ed-a731-43fe-a7a7-f053e7b6820b)


Laberinto 3: 
Sin pesos: ![image](https://github.com/user-attachments/assets/2fdf838a-d030-4678-84b8-cdc315d63ec0)


Con pesos: ![image](https://github.com/user-attachments/assets/60f8b327-11ac-49f1-9b41-6bb6099c3721)


## 2. Optimización de Colonia de Hormigas

Ant	 Colony	 Optimization	 (ACO)	 es una técnica de optimización inspirada en el
comportamiento de las hormigas reales cuando buscan recursos para su colonia. El propósito
de este algoritmo en el campo de la IA es el de simular el comportamiento de las hormigas
para encontrar el mejor camino desde el nido de la colonia a la fuente de recursos.

### A. Correr la implementación planteada. Analizar el código.

Se corrió el programa para el caso de estudio 1 algunas veces. Para algunos de los casos, el camino seleccionado por el algoritmo no llegaba a la meta planteada. Al revisar el código, se observó que en el fragmento del código que hace que la hormiga recorra, cuando la posición siguiente no es válida, el algoritmo termina el trayecto actual, pero a pesar de no haber llegado a la meta lo almacena. Posteriormente, de todos los caminos almacenados, el algoritmo selecciona el más corto, lo que quiere decir que a pesar de haber fallado en el trayecto, si un camino erróneo es más corto que cualquier camino correcto, el algoritmo seleccionará y graficará el camino más corto.

Para resolver esto, se añadió un paso entre el recorrido de todas las hormigas, y la selección del mejor camino. A fin de comparar solamente caminos que llegan a la meta, se creo una lista `valid_paths` que es poblada por los caminos en `all_paths` que han alcanzado la meta.

### B. Que ocurre con el 2do caso de estudio?

En el 2do caso de estudio se hubiesen visto fallas en todas las iteraciones, pero se realizó la corrección detallada en el literal A antes de empezar con el 2do caso.

Sin embargo, se observó una pecularidad en los caminos que se graficaban en el 2do caso: una vez superados los obstáculos, a pesar de tener un camino recto hacia la meta, el camino seleccionado era uno en el cual había una desviación de 45º que era corregida en el siguiente paso. Esto se debe a la naturaleza estocástica del modelo, una vez que las hormigas empiezan a caminar por este tipo de caminos, el camino es reforzado debido a la forman en la que el parámetro de las feromonas influye en la caminata de hormigas subsecuentes.

Con el fin de solucionar esto, se puede incrementar el valor del parámetro `beta` del modelo, el cual controla la influencia de la distancia. Para valores altos de `beta`, hay una atracción mayor hacia la meta.

### C. Describir los parámetros del modelo.

* start: Las coordinadas posición inicial de las hormigas.
* end: Las coordinadas de la ubicación de la meta.
* obstacles: Lista que contiene las coordenadas sobre las cuales las hormigas no pueden moverse.
* grid_size: El tamaño de la cuadrícula (10x10 en este caso)
* num_ants: El número de hormigas que actúan en cada iteración.
* evaporation_rate: un parámetro que define la tasa con la que se disipan las feromonas.
* alpha: el peso del rastro de feromonas en el camino que toman las hormigas subsecuentes.
* beta: el peso que regula la atracción de las hormigas hacia la meta.

### D. Pregunta de investigación: será que se puede utilizar este algoritmo para resolver el TSP Cuales serían sus pasos de implementación?

La Optimización por Colonia de Hormigas (ACO) puede extenderse para abordar el Problema del Viajero (TSP). En esta adaptación, las ciudades del TSP se modelan como nodos de un grafo, y las conexiones entre ellas como aristas con las distancias asociadas. Las "hormigas" construyen gradualmente tours completos, decidiendo la siguiente ciudad a visitar basándose en la cantidad de feromonas depositadas en las aristas por hormigas anteriores y una heurística que favorece las ciudades más cercanas, con este proceso probabilístico se permite a las hormigas explorar diferentes rutas en el espacio de soluciones.

Una vez que todas las hormigas han completado sus tours en una iteración, se actualizan las feromonas en las aristas. Se aplica una evaporación para evitar la convergencia prematura y fomentar la exploración continua. Las hormigas que encontraron tours más cortos depositan una mayor cantidad de feromonas en las aristas que utilizaron, reforzando así los caminos prometedores para las siguientes generaciones de hormigas.

El algoritmo ACO para el TSP se ejecuta durante varias iteraciones, manteniendo un registro del mejor tour encontrado hasta el momento. Aunque no siempre garantiza la solución óptima, esta metaheurística ha demostrado ser eficaz para encontrar soluciones de alta calidad para el TSP en un tiempo razonable, equilibrando la exploración de nuevas rutas con la explotación de las soluciones previamente encontradas.

Por lo tanto, la aplicación de la metáfora del comportamiento de las hormigas a la resolución del Problema del Viajero ofrece una estrategia computacional robusta y adaptable. Al simular la comunicación indirecta a través de feromonas y la toma de decisiones probabilística influenciada por la experiencia colectiva y el conocimiento heurístico, ACO emerge como una técnica valiosa dentro del campo de la inteligencia artificial y la optimización. Su capacidad para explorar un vasto espacio de soluciones y converger hacia resultados de alta calidad, sin la necesidad de un conocimiento exhaustivo del problema, lo convierte en una herramienta poderosa para abordar desafíos complejos de optimización combinatoria como el TSP.
