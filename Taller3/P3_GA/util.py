from typing import List


def word_to_array(word: str):
    return [ord(w) for w in word]

# Algo no está bien con esta función de distancia
def distance(list1:List[int], list2:List[int]):

    # Si no existen, se devuelve 0
    if not list1 and not list2:
        return 0
    
    acc = 0
    for e1, e2 in zip(list1, list2):
        # Utilizamos el valor absoluto de la diferencia entre los caracteres
        # para evitar que la distancia sea negativa
        acc += abs(e1 - e2)
    # Reemplacemos n_size por ifs que comparen la longitud de las listas y añadan la diferencia
    # de longitud a la distancia para penalizar diferencias de longitud
    #n_size = min(len(list1), len(list2))
    if len(list1) > len(list2):
        for i in range(len(list2), len(list1)):
            acc += list1[i] 
    elif len(list2) > len(list1):
        for i in range(len(list1), len(list2)):
            acc += list2[i] 
    
    return acc

def word_distance(word1:str, word2:str):
    return distance(word_to_array(word1), word_to_array(word2))

def choose_best_individual_by_distance(population, aptitudes):
    best_individual = population[0]
    best_aptitude = aptitudes[0]
    for ind, apt in zip(population, aptitudes):
        if apt < best_aptitude:
            best_aptitude = apt
            best_individual = ind
    return best_individual



# print(word_distance("abc", "abc"))
# print(word_distance("abc", "abd"))
# print(word_distance("abc", "abz"))
# print(word_distance("abc", "cba"))
# print(word_distance("abc", "cbad"))