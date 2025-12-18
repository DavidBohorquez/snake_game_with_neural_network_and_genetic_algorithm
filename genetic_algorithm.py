# genetic_algorithm.py
import random
import numpy as np
from snake import Snake
from neural_network import NeuralNetwork
from game import Game

class GeneticAlgorithm:
    def __init__(self, size=100):
        self.size = size
        self.population = [Snake() for _ in range(size)]
        self.generation = 1
        self.best_fitness = 0
        self.history = []
        # Paramètres de l'algorithme génétique améliorés
        self.mutation_rate = 0.15  # Augmenté pour plus d'exploration
        self.crossover_rate = 0.8  # Augmenté pour plus de combinaison
        self.elite_size = int(size * 0.15)  # 15% de la population pour l'élitisme
        self.tournament_size = 7  # Augmenté pour meilleure sélection

    def evaluate(self):
        """
        Évalue chaque serpent de la population en le faisant jouer.
        Calcule la fitness de chaque individu et met à jour les statistiques.
        """
        for snake in self.population:
            snake.reset()
            game = Game(snake)
            
            # Faire jouer le serpent jusqu'à ce qu'il meure
            max_steps = 5000  # Limite augmentée pour permettre plus d'exploration et d'apprentissage
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
        
        # Afficher plus d'informations pour suivre la progression
        avg_fitness = sum(s.fitness for s in self.population) / len(self.population)
        print(f"Génération {self.generation} - Meilleure fitness: {current_best:.2f}, Score: {self.population[0].score}, "
              f"Fitness moyenne: {avg_fitness:.2f}, Meilleur score global: {max(s.score for s in self.population)}")
        
        return True

    def select(self):
        """
        Sélectionne les meilleurs serpents pour la reproduction.
        Utilise une combinaison d'élitisme et de sélection par tournoi.
        """
        selected = []
        
        # Élitisme : garder les meilleurs individus
        for i in range(self.elite_size):
            selected.append(self.population[i])
        
        # Sélection par tournoi pour le reste
        while len(selected) < self.size:
            # Tournoi : choisir k individus aléatoires et prendre le meilleur
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
        
        # Garder les élites (sans modification)
        for i in range(self.elite_size):
            new_population.append(selected[i])
        
        # Créer le reste de la population par reproduction
        while len(new_population) < self.size:
            # Sélectionner deux parents
            parent1 = random.choice(selected)
            parent2 = random.choice(selected)
            
            # Crossover
            if random.random() < self.crossover_rate:
                child_network = NeuralNetwork.crossover(parent1.network, parent2.network)
            else:
                # Pas de crossover, copier un parent
                child_network = NeuralNetwork(weights=parent1.network.get_weights())
            
            # Mutation (toujours appliquer une petite mutation même si le taux n'est pas atteint)
            mutation_prob = random.random()
            if mutation_prob < self.mutation_rate:
                child_network.mutate(rate=self.mutation_rate)
            elif mutation_prob < self.mutation_rate + 0.05:  # Petite mutation aléatoire
                child_network.mutate(rate=0.05)  # Mutation légère pour maintenir la diversité
            
            # Créer le nouveau serpent
            new_population.append(Snake(network=child_network))
        
        # Mettre à jour la population
        self.population = new_population
        self.generation += 1
        
        return new_population
