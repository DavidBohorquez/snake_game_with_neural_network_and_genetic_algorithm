# genetic_algorithm.py
import random
import numpy as np
from snake import Snake
from neural_network import NeuralNetwork
from game import Game

class GeneticAlgorithm:
    def __init__(self, size=50):
        self.size = size
        self.population = [Snake() for _ in range(size)]
        self.generation = 1
        self.best_fitness = 0
        self.history = []
        # Param├¿tres de l'algorithme g├®n├®tique
        self.mutation_rate = 0.1
        self.crossover_rate = 0.7
        self.elite_size = int(size * 0.1)  # 10% de la population pour l'├®litisme
        self.tournament_size = 5

    def evaluate(self):
        """
        ├ëvalue chaque serpent de la population en le faisant jouer.
        Calcule la fitness de chaque individu et met ├á jour les statistiques.
        """
        for snake in self.population:
            snake.reset()
            game = Game(snake)
            
            # Faire jouer le serpent jusqu'├á ce qu'il meure
            max_steps = 2000  # Limite pour ├®viter les boucles infinies
            steps = 0
            while snake.alive and steps < max_steps:
                game.update()
                steps += 1
            
            # Calculer la fitness
            snake.calculate_fitness()
        
        # Trier la population par fitness (meilleur en premier)
        self.population.sort(key=lambda s: s.fitness, reverse=True)
        
        # Mettre ├á jour la meilleure fitness
        current_best = self.population[0].fitness
        if current_best > self.best_fitness:
            self.best_fitness = current_best
        
        # Enregistrer la meilleure fitness de cette g├®n├®ration
        self.history.append(current_best)
        
        print(f"G├®n├®ration {self.generation} - Meilleure fitness: {current_best:.2f}, Score: {self.population[0].score}")
        
        return True

    def select(self):
        """
        S├®lectionne les meilleurs serpents pour la reproduction.
        Utilise une combinaison d'├®litisme et de s├®lection par tournoi.
        """
        selected = []
        
        # ├ëlitisme : garder les meilleurs individus
        for i in range(self.elite_size):
            selected.append(self.population[i])
        
        # S├®lection par tournoi pour le reste
        while len(selected) < self.size:
            # Tournoi : choisir k individus al├®atoires et prendre le meilleur
            tournament = random.sample(self.population, min(self.tournament_size, len(self.population)))
            winner = max(tournament, key=lambda s: s.fitness)
            selected.append(winner)
        
        return selected

    def reproduce(self, selected):
        """
        Cr├®e une nouvelle g├®n├®ration ├á partir des serpents s├®lectionn├®s.
        Applique crossover et mutation.
        """
        new_population = []
        
        # Garder les ├®lites (sans modification)
        for i in range(self.elite_size):
            new_population.append(selected[i])
        
        # Cr├®er le reste de la population par reproduction
        while len(new_population) < self.size:
            # S├®lectionner deux parents
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child_network = NeuralNetwork.crossover(parent1.network, parent2.network)
            else:
                # Pas de crossover, copier un parent
                child_network = NeuralNetwork(weights=parent1.network.get_weights())
            
            # Mutation
            if random.random() < self.mutation_rate:
                child_network.mutate(rate=self.mutation_rate)
            
            # Cr├®er le nouveau serpent
            new_population.append(Snake(network=child_network))
        
        # Mettre ├á jour la population
        self.population = new_population
        self.generation += 1
        
        return new_population
