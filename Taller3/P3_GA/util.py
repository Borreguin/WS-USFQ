from typing import List
import Levenshtein



def word_to_array(word: str):
    return [ord(w) for w in word]

# Algo no está bien con esta función de distancia
"""
def distance(list1:List[int], list2:List[int]):
    #print("Lista 1:", list1)
    #print("Lista 2:", list2)

    acc = 0 #
    for e1, e2 in zip(list1, list2):
        acc += abs(e1 - e2)
        #print(f"e1 - e2 = acc, {e1} - {e2} = {acc}")

    n_size = min(len(list1), len(list2))
    if n_size == 0:
        return None
    return acc #+ (len(list1) - len(list2))
"""
def distance(list1: List[int], list2: List[int]) -> int:
    str1 = ''.join(chr(i) for i in list1)
    str2 = ''.join(chr(i) for i in list2)
    return Levenshtein.distance(str1, str2)


def distancia_lev(word1:str, word2:str):
    return Levenshtein.distance(word1, word2)

def word_distance(word1:str, word2:str):
    #print(word1, word2)
    return distance(word_to_array(word1), word_to_array(word2))
    #return distancia_lev(word1, word2)


def choose_best_individual_by_distance(population, aptitudes):
    best_individual = population[0]
    best_aptitude = aptitudes[0]
    for ind, apt in zip(population, aptitudes):
        if apt < best_aptitude:
            best_aptitude = apt
            best_individual = ind
    return best_individual



#print(word_distance("abf", "abc"))
# print(word_distance("abc", "abd"))
# print(word_distance("abc", "abz"))
# print(word_distance("abc", "cba"))
# print(word_distance("abc", "cbad"))