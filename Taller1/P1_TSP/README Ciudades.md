Grupo 1

### Resumen
- TSP Ciudades
  Se usa fuerza bruta
  Para cada ruta generada, se calcula la distancia total recorrida sumando las distancias entre cada par de ciudades consecutivas en la ruta.
  Se compara la distancia de cada ruta con la distancia mínima encontrada hasta el momento. Si se encuentra una ruta con una distancia menor, se actualiza la distancia mínima y se guarda la ruta correspondiente como la mejor ruta.
  Este método garantiza encontrar la solución óptima, ya que evalúa todas las posibilidades.
  El tiempo de ejecución crece exponencialmente con el número de ciudades, haciéndolo inviable para problemas con muchas ciudades.

### Conclusiones
Se usa fuerza bruta porque solo se quiere analizar 10 ciudades
Pero si se quisiera usar más puntos se debería usar:
  * Algoritmo genético
  * Simulated annealing
  * Algoritmo de colonia de hormigas
  * Christofides algorithm

