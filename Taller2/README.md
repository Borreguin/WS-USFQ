# WorkShop-USFQ
## Taller 2 de inteligencia artificial

- **Nombre del grupo**: Grupo 2

- **Integrantes del grupo**:
  * Daniel Arias
  * André Ramirez
  * Santiago Rodríguez


El objetivo de esta tarea es utilizar cualquier algoritmo de búsqueda para resolver los 3 laberintos propuestos, 
el reto es poder visualizar/representar los resultados, adicionalmente poder comparar al menos 2 algoritmos de búsqueda 
y mirar cómo se comportan para cada laberinto
![Maze1](/Taller2/images/maze1.jpg) 

## Parte 1
### Laberinto 3
#### Resultados
![Maze3ney](/Taller2/images/maze_3_nay.png)
**Figura 5.** Resultados obtenidos después de aplicar el algoritmo de Nayfeth
![Maze3astar](/Taller2/images/maze_3_astar.png)
**Figura 6.** Resultados obtenidos después de aplicar el algoritmo de A*.

A partir de los resultados obtenidos, se observó que, al aumentar el ancho del laberinto en 
comparación con el Laberinto 1, el algoritmo de Nayfeth no logra simplificar de manera efectiva la 
estructura. Esto se debe a que, al haber más celdas vecinas, muchos corredores no cumplen la 
condición para ser transformados en paredes, lo que dificulta la limpieza del laberinto y puede 
impedir la obtención de una ruta óptima.

En contraste, el algoritmo A* fue capaz de encontrar consistentemente el camino más corto desde 
el punto de entrada (E) hasta el punto de salida (S), siempre que se respetara la condición de no 
permitir movimientos en diagonal. Esto confirma la eficacia de A* como algoritmo de búsqueda óptima 
incluso en laberintos amplios y con estructuras complejas.

Link del doc en línea
https://docs.google.com/document/d/1Dpq9p_8Z5-TfOHjl7bSqWfcLgUXnPAQVSKNZZCWwWLU/edit?usp=sharing

