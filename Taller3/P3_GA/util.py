from typing import List


def distance(s1: str, s2: str) -> int:
    if len(s1) != len(s2):
        raise ValueError("Las cadenas deben tener la misma longitud.")
    return sum(1 for a, b in zip(s1, s2) if a != b)

def word_distance(word1: str, word2: str) -> int:
    return distance(word1, word2)

def choose_best_individual_by_distance(population, aptitudes):
    best_individual = population[0]
    best_aptitude = aptitudes[0]
    for ind, apt in zip(population, aptitudes):
        if apt < best_aptitude:
            best_aptitude = apt
            best_individual = ind
    return best_individual

# distancia euclideana con strings
#def euclidean_distance(s1: str, s2: str) -> float:
    #if len(s1) != len(s2):
        #raise ValueError("Strings must be of the same length")
    #return sum((ord(a) - ord(b)) ** 2 for a, b in zip(s1, s2)) ** 0.5

# print(word_distance("abc", "abc"))
# print(word_distance("abc", "abd"))
# print(euclidean_distance("abh", "abz"))
# print(word_distance("abc", "cba"))
# print(word_distance("abc", "cbad"))