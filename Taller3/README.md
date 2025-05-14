# Taller 3 de inteligencia artificial

## P1: Unsupervised Machine Learning

## P2: Linear Programming

## P3: Algoritmos Genéticos

### 1. Ejecute los dos casos de estudio y explique los resultados de ejecución de cada caso de estudio.

- **Caso 1:** Este caso siempre converge a la frase objetivo en la generación 982. Esto se debe a que al generar los individuos "aleatoriamente", utiliza una constante predefinida en `constants.py` como semilla para el RNG.

- **Caso 2:** Este caso no converge al objetivo esperado, sino hacia una frase llena de espacios con una aptitud de `-869`, por lo que podemos inferir que hay algún problema en la manera en la cual el algoritmo calcula la distancia, la cual no debería permitir valores negativos. 

### 2. Cuál sería una posible explicación para que el caso 2 no finalice como lo hace el caso 1? Revisar el archivo util.py función distance

Existe un problema con la función `distance` en `utils.py`. El algoritmo intenta siempre minimizar la distancia entre el individuo y el objetivo. Idealmente, con la meta de que la distancia entre cada par de caracteres sea 0 (es decir, que estos sean iguales). Sin embargo, al comparar los valores ASCII de los caracteres, el algoritmo realiza una resta sin calcular el valor absoluto. Por lo tanto, se favorecen valores que minimizan la operación `caracter_del_individuo - caracter_del_objetivo`. En este caso, los caracteres del objetivo ya están definidos, por lo que el algoritmo trata de encontrar el valor más pequeño para el caracter del individuo, lo cual lo lleva a elegir el espacio (`' '`), ya que es el caracter posible (determinado por `all_possible_gens`) con el menor código ASCII. 

### 3. Realice una correcta implementación para obtener la distancia/diferencia correcta entre los dos individuos en el archivo ***util.py*** función ***distance***. (Por ejemplo, considerar la Levenshtein distance)

Se trató de implementar la distancia Levenshtein, pero el algoritmo no logró converger al objetivo dentro de las 1000 generaciones. Para este problema la distancia Levenshtein debería resolver los problemas que genera el método de calcular distancia original (el cual converge en una frase llena de espacios). El que no lo haga podría ser indicativo de que tal vez la manera en la que el algoritmo está seleccionando a los padres no es óptima, o el `mutation_rate` podría ser muy bajo. También puede ser posible que para incorporar la distancia Levenshtein sea necesario introducir más aleatoriedad al algoritmo, ya que parece atorarse en mínimos locales. Esto es aparente ya que alcanza una aptitud baja pronto, pero en las generaciones subsecuentes existe muy poca o nada de diferencia entre el mejor candidato de cada generación.

Se optó por tomar la manera de calcular distancia del algoritmo y hacer un par de pequeñas correcciones. En lugar de calcular la diferencia entre los valores ASCII de cada par de caracteres, se calcula el valor absoluto de esta, lo cual ayudará a que el algoritmo converja hacia 0. También se eliminó el cálculo de `n_size`, y para considerar frases de distintas distancias, se compara longitud y se añade los valores ASCII de los caracteres excedentes. Sin embargo, cabe recalcar que en base a la manera que el algoritmo está programado, frases con una longitud distinta al objetivo no son posibles, ya que la poblacion se inicializa con frases con la misma longitud del objetivo, y ninguna de las operaciones que se realizan sobre los individuos para crear generaciones subsecuentes altera la longitud de la frase.  

### 4. Sin alterar el parámetro de mutación ***mutation_rate***, se puede implementar algo para mejorar la convergencia y que esta sea más rápida? Implemente cualquier mejora que permita una rápida convergencia. Pista: Tal vez elegir de manera diferente los padres? Realizar otro tipo de mutación o cruce?

Se creó un nuevo caso `case_study_3`, donde se escogió alterar dos parámetros:

1. **La manera en la que se seleccionan los padres:** se optó por un método de selección por torneo, el cual incrementa la movilidad hacia el objetivo al seleccionar el mejor candidato de un subconjunto.

2. **La manera en la que se realiza el cruce:** Previamente el algoritmo seleccionaba un punto aleatorio para el cruce, por lo cual uno de los hijos tenía el prefijo del padre 1, y el sufijo del padre 2, mientras que el otro tiene el prefijo del padre 2 y el sufijo del padre 1. Entonces para un par de padres `AAAAAAAAAA` y `BBBBBBBBBB` sus hijos podrían verse así: `AAAAAABBBB` y `BBBBBBAAAA`. Se implementó un cruce de dos puntos, donde el algoritmo selecciona dos coordenadas a lo largo del candidato, e intercambia el segmento entre esas dos coordenadas para producir los hijos. Este método funciona mejor porque preserva grupos de genes que funcionan juntos, ya que el método anterior tiende a separar los extremos de los candidatos. También produce opciones más diversas.

Ambos parámetros se implementaron dentro de `TOURNAMENT_TWO_POINT`. Se corrió `case_study_2` y `case_study_3` juntos. El caso 2 alcanza el objetivo en la generación 378, mientras que el caso 3 lo hizo en la generación 209, demostrando una mejora significativa.

### 5. Cree un **nuevo caso de estudio 3**. Altere el parámetro de mutación **mutation_rate**. Ha beneficiado en algo la convergencia? Qué valores son los más adecuados para este parámetro? Qué conclusión se puede obtener de este cambio?

Se creó `new_case_study_3`, el cual itera a traves de distintos mutation rates y corre el algoritmo genético para cada uno de ellos. Ya que todos arrancan con la misma población inicial, decidimos establecer 3 puntos de interés para cada caso: la aptitud en la generación 10, la generación en la que alcanza una aptitud de 1, y la generación donde alcanza el objetivo.

| Mutation Rate | Aptitud 10º Generación | Generación Aptitud = 1 | Generación Aptitud = 0 |
|----------|----------|----------|----------|
|    0.02      |    150      |    79      |     104     |
|     0.07     |     49     |     73     |    91      |
|     0.1     |     69     |     118     |     196     |

En base a estos resultados, parece que un `mutation_rate` de 0.07 funciona bastante bien. Valores muy bajos demoran mucho en aproximarse a un espacio de soluciones óptimo (como se ve en la columna "Aptitud 10º Generación"), mientras que valores muy altos tienen problemas en converger hacia la solución una vez alcanzada una aptitud baja (como se puede ver en las últimas dos columnas de la tabla). Alternativamente, podría utilizarse un `mutation_rate` adaptivo, que inicia con un valor alto que ayude al algoritmo a minimizar rápidamente su espacio de búsqueda, y luego disminuye para ayudarlo a explorar ese espacio sin mutaciones muy radicales que entorpezcan la convergencia.

### 6. Cree un **nuevo caso de estudio 4**. Altere el tamaño de la población. Es beneficioso o no aumentar la población?

Se creó `case_study_4`, el cual itera `case_study_2` para distintos tamaños de población. Es intuitivo que el aumentar el tamaño de la población resultará generalmente en un número menor de generaciones necesarias para alcanzar el objetivo, pero esto no se puede explotar indefinidamente ya que para objetivos más complejos o tamaños de población muy altos, aumenta el costo computacional de cada generación.

No siempre se cumplió la relación de que para poblaciones más grandes, el número de generaciones para alcanzar el objetivo sería menor. Esto se debe a la naturaleza estocástica del algoritmo. Pero si se evaluase repetidas veces para distintas semillas y distintos objetivos, se cumpliría que en general, las poblaciones iniciales más grandes alcanzarían el objetivo en un número menor de generaciones.

### 7. De todo lo aprendido, cree que el caso de estudio definitivo (caso de estudio 5) el cual tiene lo mejor de los items 4, 5, 6.

Se implementó `case_study_5`, el cual utiliza el método `TOURNAMENT_TWO_POINT` mencionado en la pregunta 4, un mutation rate de 0.06, y una población inicial de 500 individuos. Este caso logró alcanzar el objetivo en 22 generaciones.

Se puede observar como el valor de mutación intermedio ayuda al algoritmo a converger rápidamente hacia un espacio de búsqueda óptimo, sin introducir demasiada variedad a bajas aptitudes, cuando el algoritmo necesita realizar cambios mínimos.

También podemos ver como el número de individuos de la población ayuda al algoritmo a explorar más de su espacio de búsqueda, lo cual en combinación con el método de selección y el cruce de dos puntos, mejoran la camada de candidatos de cada generación.

## GLPK package:
The GLPK (GNU Linear Programming Kit) package is intended for solving large-scale linear programming (LP), mixed integer programming (MIP), and other related problems. It is a set of routines written in ANSI C and organized in the form of a callable library.
This project uses this Linear Programming Kit to solve large-scale problems related to Logistics. 

The installation of this package depends on the Operating System:

Windows: https://winglpk.sourceforge.net/

Linux: apt-get install -y -qq glpk-utils

Mac:  brew install glpk