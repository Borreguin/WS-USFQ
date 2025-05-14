import random
from constants import *
from util import *


def parent_selection(_type: ParentSelectionType, population, aptitudes):
    if _type == ParentSelectionType.DEFAULT:
        # Selección de padres por ruleta
        cumulative = sum(aptitudes)
        selection_probability = [aptitude / cumulative for aptitude in aptitudes]
        parents = random.choices(population, weights=selection_probability, k=2)
        return parents
    if _type == ParentSelectionType.MIN_DISTANCE:
        # seleccionando randomicamente dos poblaciones diferentes para cada padre
        # se podria seleccionar de otra manera?
        partition_size = random.randint(1, len(population)-1)
        parent1 = choose_best_individual_by_distance(population[:partition_size], aptitudes[:partition_size])
        parent2 = choose_best_individual_by_distance(population[partition_size:], aptitudes[partition_size:])
        return parent1, parent2
    if _type == ParentSelectionType.TOURNAMENT:
        # Tournament selection - selección por torneo
        # Define tournament size (typical values are 2-5% of population)
        tournament_size = max(3, int(len(population) * 0.05))
        
        # For DEFAULT evaluation type, we want minimum values (0 is perfect match)
        # For distance evaluation, we also want minimum values
        # So in all cases, we're minimizing
        
        # Select the first parent through tournament
        candidates_idx1 = random.sample(range(len(population)), tournament_size)
        # Always choose the smallest aptitude (minimum is best for both methods)
        best_idx = min(candidates_idx1, key=lambda idx: aptitudes[idx])
        parent1 = population[best_idx]
        
        # Select the second parent through another tournament
        candidates_idx2 = random.sample(range(len(population)), tournament_size)
        best_idx = min(candidates_idx2, key=lambda idx: aptitudes[idx])
        parent2 = population[best_idx]
        
        return parent1, parent2
    if _type == ParentSelectionType.NEW:
        print("implement here the new parent selection")
        return None


def crossover(_type: CrossoverType, parent1, parent2):
    if _type == CrossoverType.DEFAULT:
        # Cruce de dos padres para producir descendencia
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    if _type == CrossoverType.TWO_POINT:
        # Two-point crossover - more diverse offspring with preservation of segments
        length = len(parent1)
        # Get two distinct crossover points
        point1 = random.randint(1, length - 2)
        point2 = random.randint(point1 + 1, length - 1)
        
        # Create children by exchanging the middle segment
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        return child1, child2
    if _type == CrossoverType.NEW:
        print("implement here the new crossover")
        return None


def mutate(_type: MutationType, individual, mutation_rate, current_gen=0, max_gen=1000):
    if _type == MutationType.DEFAULT:
        # Mutación de un individuo
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual = individual[:i] + random.choice(all_possible_gens) + individual[i + 1:]
        return individual
    if _type == MutationType.ADAPTIVE:
        # Calculate adaptive rate that decreases over time
        adaptive_rate = mutation_rate * (1 - current_gen / max_gen)
        
        # Apply mutation with adaptive rate
        for i in range(len(individual)):
            if random.random() < adaptive_rate:
                individual = individual[:i] + random.choice(all_possible_gens) + individual[i + 1:]
        return individual
        
        # Apply mutation with adaptive rate
        for i in range(len(individual)):
            if random.random() < adaptive_rate:
                individual = individual[:i] + random.choice(all_possible_gens) + individual[i + 1:]
        return individual
    if _type == MutationType.NEW:
        print("implement here the new mutation")
        return None