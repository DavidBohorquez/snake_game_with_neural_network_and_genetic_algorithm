# genetic_algorithm.py
import random
import numpy as np
from snake import Snake
from neural_network import NeuralNetwork
from game import Game

class GeneticAlgorithm:
    def __init__(self, size=50):
        """
        Initialise l'algorithme génétique avec des paramètres équilibrés.
        """
        self.size = size
        self.population = [Snake() for _ in range(size)]
        self.generation = 1
        self.best_fitness = 0
        self.history = []
        # Paramètres équilibrés de l'algorithme génétique
        self.mutation_rate = 0.1  # Taux standard
        self.crossover_rate = 0.7  # Taux standard
        self.elite_size = int(size * 0.1)  # 10% de la population
        self.tournament_size = 5  # Taille standard du tournoi

    def evaluate(self):
        """
        Évalue chaque serpent de la population en le faisant jouer.
        Calcule la fitness de chaque individu et met à jour les statistiques.
        """
        for snake in self.population:
            snake.reset()
            game = Game(snake)
            
            # Faire jouer le serpent jusqu'à ce qu'il meure
            max_steps = 2000  # Limite pour éviter les boucles infinies
            steps = 0
            while snake.alive and steps < max_steps:
                game.update()
                steps += 1
            
            # Calculer la fitness
            snake.calculate_fitness()
        
        # Trier la population par fitness (meilleur en premier)
        self.population.sort(key=lambda s: s.fitness, reverse=True)
        
        # Mettre à jour la meilleure fitness
        current_best = self.population[0].fitness
        if current_best > self.best_fitness:
            self.best_fitness = current_best
        
        # Enregistrer la meilleure fitness de cette génération
        self.history.append(current_best)
        
        print(f"Génération {self.generation} - Meilleure fitness: {current_best:.2f}, Score: {self.population[0].score}")
        
        return True

    def select(self):
        """
        Sélectionne les meilleurs serpents pour la reproduction.
        Utilise élitisme + sélection par tournoi (méthode simple et efficace).
        """
        selected = []
        
        # Élitisme : garder les meilleurs individus
        for i in range(self.elite_size):
            selected.append(self.population[i])
        
        # Sélection par tournoi pour le reste
        while len(selected) < self.size:
            tournament = random.sample(self.population, min(self.tournament_size, len(self.population)))
            winner = max(tournament, key=lambda s: s.fitness)
            selected.append(winner)
        
        return selected

    def reproduce(self, selected):
        """
        Crée une nouvelle génération à partir des serpents sélectionnés.
        Applique crossover et mutation.
        """
        new_population = []
        
        # Garder les élites sans modification
        for i in range(self.elite_size):
            new_population.append(selected[i])
        
        # Créer le reste de la population par reproduction
        while len(new_population) < self.size:
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child_network = NeuralNetwork.crossover(parent1.network, parent2.network)
            else:
                child_network = NeuralNetwork(weights=parent1.network.get_weights())
            
            # Mutation
            if random.random() < self.mutation_rate:
                child_network.mutate(rate=self.mutation_rate)
            
            new_population.append(Snake(network=child_network))
        
        self.population = new_population
        self.generation += 1
        return new_population