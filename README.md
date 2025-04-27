![USFQ-LOGO](/Taller1/images/usfq-red.png)
# Taller 1
## Inteligencia artificial

- **Nombre del grupo**: Grupo 1
- **Integrantes del grupo**:

    • Patricia Lema

    • Ana Navaz

    • Diana Córdova
    
    • Sebastián Ruiz
 
## 1. Uso de la Inteligencia Artificial - Low Code Engineering

### [A. TSP – Traveling Salesman Problem – Problema del vendedor viajante](/Taller1/P1_TSP/TSP.ipynb)

Este problema presentaba dos casos a resolver: un caso con 10 ciudades, y otro con 100 ciudades.

* TSP (10 Ciudades) Se usa fuerza bruta Para cada ruta generada, se calcula la distancia total recorrida sumando las distancias entre cada par de ciudades consecutivas en la ruta. Se compara la distancia de cada ruta con la distancia mínima encontrada hasta el momento. Si se encuentra una ruta con una distancia menor, se actualiza la distancia mínima y se guarda la ruta correspondiente como la mejor ruta. Este método garantiza encontrar la solución óptima, ya que evalúa todas las posibilidades. El tiempo de ejecución crece exponencialmente con el número de ciudades, haciéndolo inviable para problemas con muchas ciudades.

* Para el caso de 100 ciudades no es posible utilizar un método de fuerza bruta, ya que el espacio de búsqueda es demasiado amplio. Por lo tanto, buscamos métodos alternativos que son computacionalmente más eficientes. Al principio tratamos de utilizar programación dinámica, utilizando el algoritmo Held-Karp. La programación dinámica busca encontrar la mejor solución, almacenando soluciones parciales con el fin de utilizarlas para construír soluciones más grandes. Este método hubise garantizado la solución más óptima, pero debido al alto número de ciudades, el algoritmo no finalizaba en un tiempo razonable. Posteriormente se implementó un algoritmo genético, el cual imita el proceso evolutivo con el fin de llegar a mejores soluciones. El algoritmo inicializa caminos al azar, y durante subsecuentes iteraciones -o generaciones- busca preservar las mejores soluciones, mutarlas al azar, y combinar distintas partes de las mismas.Se lo implementó con 1000, 1500, y finalmente 2500 generaciones. A pesar de que no garantiza la mejor solución al problema, mediante inspección visual del camino graficado se puede observar que la solución alcanzada es suficientemente adecuada, y el algoritmo tomó un minuto en llegar a ella.

**Conclusiones**

* Se utiliza un método de fuerza bruta para `n=10` debido a que el tiempo para computar la solución ideal no es muy alto.

* Este es un problema cuya complejidad incrementa en base al número de ciudades. Para el caso de 100 ciudades, tratar de resolverlo por fuerza bruta tiene una complejidad de **`O(99!)`**, usando programación dinámica la complejidad baja a **`O(100*2^100)`**, y usando el algoritmo genético su complejidad baja al número de ciudades por el número de generaciones, en este caso **`O(100*2500)`**.

* Podemos ver que a pesar de ser más eficiente, la programación dinámica aún puede tener costos muy altos, por lo que deja de ser práctica para un número de ciudades mayor a 25. Por lo tanto, utilizar métodos estocásticos como algoritmos genéticos es más eficiente para `n=100`.

* La función para graficar el resultado ayudó bastante a identificar que tan óptima era la solución del algoritmo genético, ya que visualmente es fácil identificar segmentos en la ruta que aún podrían ser optimizados.

### [B. El acertijo del granjero y el bote](/Taller1/P2_Granjero/DesafíoGranjero.ipynb)

**Justificación**: el algoritmo que se aplicó es de búsqueda. En su proceso, aunque se haya hecho de manera manual, se parece más a una búsqueda por anchura que por profundidad. 

Se exploró cada camino por sus nodos vecinos en lugar de un solo camino antes de pasar a otro. 

**Justificación de gráfico por nodos**: El uso de nodos además permitió que una operación prohibida se detenga porque detiene las aristas.

### [C. La torre de Hanoi](/Taller1/P3_Torres/TorreHanoi.ipynb)

Para el ejercicio de la Torre de Hanoi se utilizó un algoritmo de búsqueda en anchura (BFS) para encontrar la ruta más corta para poder resolver el ejercicio planteado. El BFS explora todos los puntos cercanos al inicio antes de ir más lejos, asegurando que la primera solución que encuentra sea la más corta en movimientos.
Se utilizo un tipo de gráfico para dibujar todos estos puntos y flechas, mostrando cómo están conectados todos los posibles estados del juego. El resultado que se presenta es una lista de los pasos exactos para resolver el rompecabezas y una imagen que muestra todos los estados posibles y resalta el camino de la solución más corta.

**Conclusiones**

Se decidió por usar grafos dentro de todos los ejercicios ya que estos nos ayudan a entender de mejor manera como se pueden resolver los problemas anteriores. 

## 2. Uso de la Inteligencia Artificial - Planeamiento de Tareas

Se utilizó ClickUp para estructurar el TSP en base a subproblemas o hitos a cumplir. Con el fin de hacer esto, se exploró la creación de una [versión alternativa del TSP](/Taller1/P1_TSP/TSP_Ciudades.ipynb) que utiliza las coordenadas geográficas de ciudades del Ecuador como espacio a explorar. Se calcula la ruta óptima y se la muestra en un mapa real.

[Link de ClickUp](https://sharing.clickup.com/90131170985/t/h/86a85bdh6/S53FL6XO4NTTE1P)

## 3. La Evolución de la Inteligencia Artificial

[Link al ensayo.](/Ensayo%20de%20chips%20analógicos.pdf)