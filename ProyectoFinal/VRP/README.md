# Vehicle Routing Problem (VRP)

## Descripción del Problema

Una empresa de entregas dispone de una flota de vehículos con capacidad limitada,y debe repartir paquetes a un conjunto de clientes ubicados en distintas direcciones. Todos los vehículos parten desde un único depósito y deben regresar al mismo al finalizar su ruta.

Cada cliente debe ser visitado exactamente una vez por un solo vehículo, y la cantidad de
paquetes que transporta un vehículo no debe superar su capacidad.

## Objetivo

Diseñar las rutas para todos los vehículos de manera que la distancia total recorrida sea mínima, cumpliendo con todas las restricciones de capacidad y asignación.

## Interpretación

El problema está definido por los siguientes entes:

- **Clientes**: consisten en ubicaciones geográficas en el mapa, que requieren la entrega de uno o más paquetes, representados por su característica de `demanda`. Para obtener la distancia entre clientes se calcula la distancia euclideana entre sus coordenadas.

- **Vehículos**: agentes que recorren el espacio geográfico, saliendo desde un depósito ubicado en el centro del mapa, y regresando al mismo luego de entregar todos los paquetes. Cada vehículo tiene una capacidad (dada por archivo para el caso *small*, variable para el caso *medium*, y con un valor de 100 para el caso *large*). A fin de satisfacer la demanda de los clientes en su ruta, la suma de las demandas de cada cliente en la ruta no puede exceder la capacidad del vehículo.

- **Rutas**: la secuencia de paradas en el mapa que recorre cada vehículo, es necesario que cada ruta inicie y termine en el depósito.

## Estructura

El repositorio provee un dataset estructurado de la siguiente manera:

### Small VRP

Contiene una lista con las coordenadas y la demanda de 11 clientes ubicados en un plano xy. También contiene 3 archivos para cada uno de los casos a resolver. Estos indican la capacidad de cada uno de los vehículos que se utilizaran para repartir en ese caso particular.

### Medium VRP

Igual que el caso anterior contiene una lista con clientes y sus demandas, pero esta vez son 50 clientes. Este caso ya no contiene una lista de vehículos

### Large VRP

También contiene la lista de clientes y demandas. Para este caso existen 100 clientes.

## Propuesta

El objetivo del problema consiste en optimizar las rutas que una flota de vehículos recorrerá con el fin de satisfacer toda la demanda de los clientes de cada caso. Para casos pequeños y medianos el problema no es demasiado complejo, pero para casos grandes se vuelve un poco más difícil explorar minuciosamente el espacio de soluciones para llegar al mínimo global. Nuestra meta es tratar de minimizar la distancia total utilizando una combinación de algoritmos y heurísticas que sean capaces de optimizar a nivel local (restructurando rutas), como a nivel global (iterando con el objetivo de intercambiar segmentos entre rutas). Parte del reto de este problema se debe al restricción dada por la capacidad de cada vehículo.

Con la finalidad de optimizar el caso *Large*, se decidio inicializar el número de vehículos e ir llenando la ruta usando un algoritmo voraz. Esto generaba rutas muy ineficientes, por lo que se trató de complementarlo con 2-opt. Pero esto no dió buenos resultados ya que 2-opt es un algoritmo de búsqueda local, por lo que si las rutas están mal desarrolladas desde su inicialización, 2-opt no podrá reducir la distancia de manera significativa. Debido a esto, se optó por el siguiente método: se realizó una agrupación utilizando K-nearest neighbors a fin de definir grupos de clientes que estén cerca entre sí como parte de una ruta. Posteriormente a esto se aplicó Large Neighborhood Search [1] seguido de crossover exchange con el fin de optimizar globalmente. Una vez hecho esto se utilizaron 2-opt[2] y backward-tracking como métodos para optimizar rutas particulares.

## Dificultades

- El número de posibles rutas crece exponencialmente con el número de clientes y el tamaño de la flota. Esto hace que el costo computacional para encontrar la solución óptima sea demasiado alto. 

- Si la inicialización de las rutas no se realiza con una heurística o algoritmo en mente, se vuelve difícil que métodos de optimización aplicados posteriormente puedan llegar a un espacio óptimo de soluciones, incremenando el costo computacional.

- La restricción de la capacidad del vehículo de entrega hace que sea necesario verificar durante el proceso de optimización que la demanda de los clientes a lo largo de la ruta no exceda la capacidad del vehículo.

- Ciertos casos no eran solvibles debido a que la demanda total de los clientes excedía la capacidad total de la flota.

- El archivo para el subcaso de 4 vehículos dentro del caso small tenía un error de sintaxis que debe ser corregido antes de leer el archivo.

- Existe el riesgo de que el proceso se atore en un mínimo local, por lo que se debe implementar métodos que puedan empujar al algoritmo fuera de esa región para que pueda explorar otra región del espacio de soluciones.

- Parte del proceso de determinar la eficiencia de las rutas consiste en inspeccionar visualmente el gráfico para analizar el resultado y ver donde puede haber mejoras.

- A pesar de que usar el algoritmo de agrupamiento por cercanía para iniciar rutas que recorran clientes que estén cerca entre sí, fue necesario asegurarse de que las rutas generadas no excedan los límites de capacidad de los vehículos.

## Bibliografía

1. https://backend.orbit.dtu.dk/ws/portalfiles/portal/5293785/Pisinger.pdf
2. https://www.researchgate.net/publication/268981882_Comparison_of_Approximate_Approaches_to_Solving_the_Travelling_Salesman_Problem_and_its_Application_to_UAV_Swarming