from typing import List


def distance(s1: str, s2: str) -> int:
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j

    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # Eliminación
                dp[i][j - 1] + 1,        # Inserción
                dp[i - 1][j - 1] + cost  # Sustitución
            )

    return dp[len_s1][len_s2]

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



# print(word_distance("abc", "abc"))
# print(word_distance("abc", "abd"))
# print(word_distance("abc", "abz"))
# print(word_distance("abc", "cba"))
# print(word_distance("abc", "cbad"))