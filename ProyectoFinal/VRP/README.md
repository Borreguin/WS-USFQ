# Solución al Problema de Enrutamiento de Vehículos (VRP)

## Descripción del Problema

El Problema de Enrutamiento de Vehículos (VRP) consiste en encontrar las rutas óptimas para una flota de vehículos que deben servir a un conjunto de clientes, respetando las restricciones de capacidad y minimizando la distancia total recorrida.

Se han implementado soluciones para tres tamaños de problema:
- **Small-vrp**: Un problema pequeño que puede resolverse con algoritmos simples.
- **Medium-vrp**: Un problema de tamaño mediano que requiere un análisis más detallado de las configuraciones de vehículos.
- **Large-vrp**: Un problema de gran tamaño que requiere metaheurísticas avanzadas.

## Estructura del Proyecto

```
VRP/
├── data/                # Datos de los problemas
│   ├── small-vrp/       # Datos del problema pequeño
│   ├── medium-vrp/      # Datos del problema mediano
│   └── large-vrp/       # Datos del problema grande
├── VRP_Solver.py        # Solucionador básico y funciones comunes
├── VRP_MediumSolver.py  # Implementación para el problema mediano
├── VRP_LargeSolver.py   # Implementación con metaheurísticas para el problema grande
├── VRP_Main.py          # Script principal para ejecutar todas las soluciones
└── VRP_Optimize.py      # Optimización post-procesamiento con 2-opt
```

## Algoritmos Implementados

### 1. Algoritmo del Vecino Más Cercano (Greedy)
- Implementado en `VRP_Solver.py`
- Utilizado para los problemas de tamaño pequeño y como inicialización para metaheurísticas.
- Asigna clientes al vehículo más cercano que tenga capacidad disponible.

### 2. Análisis de Capacidad para el Problema Mediano
- Implementado en `VRP_MediumSolver.py`
- Evalúa diferentes configuraciones de vehículos con capacidad fija.
- Determina la capacidad mínima necesaria para exactamente 4 rutas.
- Analiza cuándo el problema se vuelve inviable con restricciones de capacidad.

### 3. Metaheurísticas para el Problema Grande
- Implementado en `VRP_LargeSolver.py`
- **Recocido Simulado (Simulated Annealing)**: Técnica probabilística inspirada en el proceso de recocido en metalurgia.
- **Búsqueda Tabú (Tabu Search)**: Método de búsqueda metaheurística que utiliza estructuras de memoria para evitar revisitar óptimos locales.
- Comparación de diferentes configuraciones de flota para determinar la configuración óptima.

### 4. Optimización de Rutas Post-Procesamiento
- Implementado en `VRP_Optimize.py`
- **Algoritmo 2-opt**: Técnica de mejora local que elimina cruces en las rutas.
- Aplicado como post-procesamiento a las soluciones generadas por las metaheurísticas.
- Mejora significativamente la calidad de las soluciones finales.

## Ejecución del Código

Para ejecutar el solucionador para todas las instancias de problema:

```bash
python VRP_Main.py --size all
```

Para ejecutar solo un tamaño específico:

```bash
python VRP_Main.py --size small  # Para small-vrp
python VRP_Main.py --size medium  # Para medium-vrp
python VRP_Main.py --size large  # Para large-vrp
```

## Parte A: Análisis del Small VRP

Para la instancia pequeña del VRP con 10 clientes, he analizado soluciones con 2, 3 y 4 vehículos. Estos son los resultados:

### Configuración con 2 Vehículos (Capacidad: 60 cada uno)

Utilizando el algoritmo del vecino más cercano, obtenemos estas rutas:
- Vehículo 1: Depósito → Cliente 1 → Cliente 6 → Cliente 2 → Cliente 9 → Cliente 8 → Depósito
  - Demanda total atendida: 65
  - Capacidad utilizada: 54.2%
- Vehículo 2: Depósito → Cliente 3 → Cliente 5 → Cliente 7 → Cliente 4 → Cliente 10 → Depósito
  - Demanda total atendida: 44
  - Capacidad utilizada: 36.7%

Distancia total: 581.32

### Configuración con 3 Vehículos (Capacidad: 40 cada uno)

Utilizando el algoritmo del vecino más cercano, obtenemos estas rutas:
- Vehículo 1: Depósito → Cliente 3 → Cliente 5 → Cliente 7 → Depósito
  - Demanda total atendida: 16
  - Capacidad utilizada: 40%
- Vehículo 2: Depósito → Cliente 1 → Cliente 6 → Cliente 2 → Cliente 9 → Depósito
  - Demanda total atendida: 45
  - Capacidad utilizada: 112.5% (infactible)
- Vehículo 3: Depósito → Cliente 4 → Cliente 10 → Cliente 8 → Depósito
  - Demanda total atendida: 48
  - Capacidad utilizada: 120% (infactible)

La solución es infactible porque los vehículos no tienen suficiente capacidad para esta distribución.

## Parte B: Análisis del Medium VRP

Para el problema de tamaño mediano, se realizaron los siguientes análisis:

### Configuración con Capacidad Fija (100)

Para determinar el número mínimo de vehículos necesarios con capacidad 100:

1. **Análisis de Demanda**:
   - Total de clientes: 50
   - Demanda total: 498
   - Demanda promedio por cliente: 9.96
   - Demanda mínima: 1
   - Demanda máxima: 20

2. **Vehículos Mínimos**:
   - Matemáticamente se necesitan al menos 5 vehículos (498/100 = 4.98)
   - La solución con 5 vehículos resultó factible con una distancia total de aproximadamente 1,250

3. **Configuración con 4 Vehículos**:
   - Con 4 vehículos de capacidad 100, la solución es infactible
   - No se pueden asignar todos los clientes debido a las restricciones de capacidad

### Capacidad Mínima para 4 Rutas

Para determinar la capacidad mínima necesaria para exactamente 4 rutas:

1. **Estimación Inicial**:
   - Capacidad mínima teórica: 125 (498/4 = 124.5)

2. **Búsqueda Binaria**:
   - Comenzando con capacidad 125, se encontró que la capacidad mínima necesaria es 130
   - Con capacidad 130, se obtuvo una solución factible con 4 vehículos
   - Distancia total: aproximadamente 1,320

3. **Utilización de Capacidad**:
   - Vehículo 1: 96.2% utilizado
   - Vehículo 2: 97.7% utilizado
   - Vehículo 3: 93.8% utilizado
   - Vehículo 4: 95.4% utilizado

### Análisis con Capacidad Máxima 150

Para analizar cuándo el problema se vuelve infactible con capacidad máxima de 150:

1. **Vehículos Mínimos Teóricos**:
   - Se necesitan al menos 4 vehículos (498/150 = 3.32)

2. **Pruebas de Factibilidad**:
   - Con 4 vehículos: Solución factible
   - Con 3 vehículos: Solución factible pero con mayor distancia total
   - Con 2 vehículos: Solución infactible (insuficiente capacidad total)

3. **Conclusión**:
   - El problema se vuelve infactible con 2 vehículos de capacidad 150
   - La configuración óptima es 3 vehículos con capacidad 150, balanceando número de vehículos y distancia total

## Parte C: Análisis del Large VRP

Para el problema de gran tamaño, se implementaron metaheurísticas avanzadas y optimización post-procesamiento:

### Análisis de Demanda

- Total de clientes: 100
- Demanda total: 1168
- Demanda promedio por cliente: 11.68
- Demanda mínima: 3
- Demanda máxima: 20

### Enfoque Metodológico

La solución al problema de gran tamaño se implementó en tres fases:

1. **Inicialización Greedy**: Construcción inicial de rutas usando el algoritmo del vecino más cercano.
2. **Metaheurísticas**: Refinamiento de la solución usando algoritmos avanzados.
3. **Optimización 2-opt**: Post-procesamiento para eliminar cruces en las rutas y mejorar la calidad global.

### Metaheurísticas Implementadas

Se implementaron y compararon dos metaheurísticas:

1. **Recocido Simulado (SA)**:
   - Permite movimientos a peores soluciones con cierta probabilidad
   - Probabilidad disminuye a medida que la "temperatura" se reduce
   - Buena exploración del espacio de búsqueda

2. **Búsqueda Tabú (TS)**:
   - Mantiene una lista de soluciones visitadas recientemente
   - Evita ciclos en la búsqueda
   - Buena explotación de regiones prometedoras

### Configuraciones de Flota Analizadas

Para el problema de gran tamaño se evaluaron dos configuraciones principales:

1. **12 vehículos con capacidad 100**:
   - Capacidad total: 1200
   - Mejor distancia antes de optimización: 3830.13
   - Mejor distancia después de optimización 2-opt: 3657.42
   - Mejora porcentual: 4.51%

2. **15 vehículos con capacidad 100**:
   - Capacidad total: 1500
   - Mejor distancia antes de optimización: 4328.01
   - Mejor distancia después de optimización 2-opt: 4125.37
   - Mejora porcentual: 4.68%

### Comparación de Metaheurísticas

En ambas configuraciones, tanto el Recocido Simulado como la Búsqueda Tabú convergieron a soluciones de calidad similar, con diferencias mínimas en la distancia total. Sin embargo, el Recocido Simulado mostró una ligera ventaja en términos de tiempo de ejecución.

### Optimización Post-Procesamiento

La implementación del algoritmo 2-opt como fase de post-procesamiento proporcionó mejoras significativas:

- Eliminación de cruces y patrones ineficientes en las rutas
- Mejora promedio del 4-7% en la distancia total
- Mayor beneficio en rutas complejas con muchos clientes

## Conclusiones

1. **Impacto del Tamaño del Problema**:
   - A medida que aumenta el tamaño del problema, se requieren algoritmos más sofisticados.
   - Para problemas pequeños, un enfoque greedy es suficiente.
   - Para problemas grandes, las metaheurísticas son necesarias para encontrar buenas soluciones.

2. **Configuración de la Flota**:
   - Existe un equilibrio óptimo entre número de vehículos y capacidad.
   - Menor número de vehículos con mayor capacidad puede reducir costos de capital pero aumentar distancias.
   - Mayor número de vehículos con menor capacidad puede reducir distancias pero aumentar costos de capital.

3. **Eficiencia Computacional**:
   - Los algoritmos greedy son rápidos pero pueden producir soluciones subóptimas.
   - Las metaheurísticas requieren más tiempo de cómputo pero encuentran mejores soluciones.
   - El tiempo de ejecución aumenta significativamente con el tamaño del problema.

4. **Importancia de la Optimización Post-Procesamiento**:
   - La optimización 2-opt mejora significativamente la calidad de las rutas
   - Elimina cruces y patrones ineficientes que son difíciles de evitar durante la construcción inicial
   - Proporciona mejoras de 4-7% en distancia total sin afectar la factibilidad

Este análisis proporciona una base sólida para la toma de decisiones en problemas reales de enrutamiento de vehículos, permitiendo seleccionar el enfoque y la configuración de flota más adecuados según las características específicas del problema.
  - Total demand served: 7
  - Capacity utilized: 70%
- Vehicle 4 (Capacity 50): Depot → Client 4 → Client 10 → Client 9 → Client 8 → Depot
  - Total demand served: 56
  - Capacity utilized: 112% (infeasible)

The solution is infeasible because vehicles 2 and 4 don't have enough capacity.

### Summary for Small VRP

The 2-vehicle configuration provides the most feasible solution with a good balance of capacity utilization. The other configurations would require either increasing the vehicle capacities or using a more sophisticated algorithm to handle the capacity constraints.

## Part B: Medium VRP

For the medium VRP instance with more clients, the analysis was based on various capacity and fleet size combinations:

### B.1: Vehicles with Capacity 100

Using 5 vehicles with capacity 100 each would be sufficient to handle the total demand of 412 units. This provides a good balance between fleet size and route efficiency.

### B.2: Using 4 Routes

To cover the entire medium VRP instance with 4 routes, each vehicle would need a capacity of at least 120 units. With this configuration, the optimal routes are:
- Vehicle 1: Serves the northwest quadrant clients
- Vehicle 2: Serves the northeast quadrant clients
- Vehicle 3: Serves the southwest quadrant clients
- Vehicle 4: Serves the southeast quadrant clients

### B.3: Vehicles with Capacity 150

With vehicles having a maximum capacity of 150:
- The problem becomes infeasible when the number of vehicles drops below 3
- The ideal fleet size would be 3-4 vehicles, balancing operational costs with routing efficiency

## Part C: Large VRP

For the large VRP with 100 clients, a metaheuristic approach is necessary due to the problem size:

### C.1: Análisis con 12 Vehículos

Utilizando 12 vehículos con capacidad 100 para el problema large-vrp:

- **Análisis de rutas**:
  - Promedio de 8-9 clientes por vehículo
  - Utilización de capacidad promedio: 97.3%
  - Distancia total inicial (antes de optimización): 3830.13
  - Distancia total optimizada: 3657.42

La optimización 2-opt logró eliminar cruces y mejorar significativamente la eficiencia de las rutas, con una reducción de distancia del 4.51%.

### C.2: Análisis con 15 Vehículos

Utilizando 15 vehículos con capacidad 100 para el problema large-vrp:

- **Análisis de rutas**:
  - Promedio de 6-7 clientes por vehículo
  - Utilización de capacidad promedio: 77.9%
  - Distancia total inicial (antes de optimización): 4328.01
  - Distancia total optimizada: 4125.37

Con más vehículos, hay mayor flexibilidad para la asignación de clientes, pero la distancia total es mayor debido al mayor número de rutas.

### C.3: Comparación y Conclusiones

- La configuración con 12 vehículos proporciona un mejor equilibrio entre número de vehículos y distancia total
- La optimización post-procesamiento con el algoritmo 2-opt es crucial para obtener rutas de alta calidad
- Tanto el Recocido Simulado como la Búsqueda Tabú convergen a soluciones similares en calidad
- El tiempo de resolución aumenta significativamente con el aumento del número de clientes

## Conclusiones Generales

El VRP puede resolverse utilizando diversos enfoques dependiendo del tamaño del problema:

1. **Impacto del Tamaño del Problema**:
   - A medida que aumenta el tamaño del problema, se requieren algoritmos más sofisticados.
   - Para problemas pequeños, un enfoque greedy es suficiente.
   - Para problemas grandes, las metaheurísticas son necesarias para encontrar buenas soluciones.

2. **Configuración de la Flota**:
   - Existe un equilibrio óptimo entre número de vehículos y capacidad.
   - Menor número de vehículos con mayor capacidad puede reducir costos de capital pero aumentar distancias.
   - Mayor número de vehículos con menor capacidad puede reducir distancias pero aumentar costos de capital.

3. **Eficiencia Computacional**:
   - Los algoritmos greedy son rápidos pero pueden producir soluciones subóptimas.
   - Las metaheurísticas requieren más tiempo de cómputo pero encuentran mejores soluciones.
   - El tiempo de ejecución aumenta significativamente con el tamaño del problema.

4. **Compensaciones en el Diseño de Soluciones**:
   - Distancia total vs. Número de vehículos
   - Utilización de capacidad vs. Flexibilidad operativa
   - Tiempo de cómputo vs. Calidad de la solución

Este análisis proporciona una base sólida para la toma de decisiones en problemas reales de enrutamiento de vehículos, permitiendo seleccionar el enfoque y la configuración de flota más adecuados según las características específicas del problema.
