# snake.py
import random
import numpy as np
from neural_network import NeuralNetwork
from config import GRID_WIDTH, GRID_HEIGHT

DIRECTIONS = [(0,-1), (1,0), (0,1), (-1,0)]

class Snake:
    def __init__(self, network=None):
        self.network = network or NeuralNetwork()
        self.reset()

    def reset(self):
        self.direction = random.choice(DIRECTIONS)
        self.length = 3
        # Initialiser le serpent avec 3 positions alignées dans la direction
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        self.positions = []
        for i in range(self.length):
            # Créer les positions en reculant de la direction
            pos_x = (start_x - i * self.direction[0]) % GRID_WIDTH
            pos_y = (start_y - i * self.direction[1]) % GRID_HEIGHT
            self.positions.append((pos_x, pos_y))
        self.alive = True
        self.score = 0
        self.steps = 0
        self.steps_without_food = 0
        self.fitness = 0

    def get_head(self):
        return self.positions[0]

    def turn(self, d):
        if (-d[0], -d[1]) != self.direction:
            self.direction = d

    def move(self, food):
        if not self.alive:
            return False

        x, y = self.get_head()
        nx = (x + self.direction[0]) % GRID_WIDTH
        ny = (y + self.direction[1]) % GRID_HEIGHT
        new = (nx, ny)

        if new in self.positions:
            self.alive = False
            return False

        # Ajouter la nouvelle position de la tête
        self.positions.insert(0, new)

        if new == food:
            # Le serpent a mangé : augmenter le score et la taille
            self.score += 1
            self.length += 1  # Augmente la taille du serpent
            self.steps_without_food = 0
            # Ne pas tronquer : la liste a maintenant self.length éléments (ancienne longueur + 1 nouvelle position)
            return True

        # Si le serpent n'a pas mangé, tronquer pour garder exactement self.length éléments
        # On garde les self.length premières positions (la tête + le corps)
        self.positions = self.positions[:self.length]
        
        self.steps += 1
        self.steps_without_food += 1

        # Augmenter la limite pour donner plus de chances au serpent d'apprendre
        if self.steps_without_food > 300:
            self.alive = False

        return False

    def get_vision(self, food):
        hx, hy = self.get_head()
        fx, fy = food

        # Distance normalisée à la nourriture (avec wrap-around)
        dx = min(abs(fx - hx), GRID_WIDTH - abs(fx - hx))
        dy = min(abs(fy - hy), GRID_HEIGHT - abs(fy - hy))
        vision = [
            dx / GRID_WIDTH,
            dy / GRID_HEIGHT
        ]
        
        # Direction vers la nourriture (normalisée)
        if fx != hx or fy != hy:
            dir_x = (fx - hx + GRID_WIDTH // 2) % GRID_WIDTH - GRID_WIDTH // 2
            dir_y = (fy - hy + GRID_HEIGHT // 2) % GRID_HEIGHT - GRID_HEIGHT // 2
            vision.append(dir_x / GRID_WIDTH)
            vision.append(dir_y / GRID_HEIGHT)
        else:
            vision.append(0)
            vision.append(0)

        # Détection d'obstacles dans les 4 directions (corps du serpent)
        for dx, dy in DIRECTIONS:
            distance = 0
            found = False
            for i in range(1, max(GRID_WIDTH, GRID_HEIGHT)):
                nx = (hx + dx * i) % GRID_WIDTH
                ny = (hy + dy * i) % GRID_HEIGHT
                if (nx, ny) in self.positions:
                    distance = i
                    found = True
                    break
            vision.append(distance / max(GRID_WIDTH, GRID_HEIGHT) if found else 1.0)

        # Direction actuelle (one-hot encoding)
        for d in DIRECTIONS:
            vision.append(1 if self.direction == d else 0)

        # Informations supplémentaires
        vision.append(self.length / (GRID_WIDTH * GRID_HEIGHT))
        vision.append(self.steps_without_food / 200.0)  # Normalisé
        
        # Distance euclidienne à la nourriture (normalisée)
        distance_euclidean = np.sqrt(dx**2 + dy**2) / np.sqrt(GRID_WIDTH**2 + GRID_HEIGHT**2)
        vision.append(distance_euclidean)
        
        # Position normalisée de la tête
        vision.append(hx / GRID_WIDTH)
        vision.append(hy / GRID_HEIGHT)
        
        # Position normalisée de la nourriture
        vision.append(fx / GRID_WIDTH)
        vision.append(fy / GRID_HEIGHT)

        return vision

    def think(self, food):
        out = self.network.forward(self.get_vision(food))
        self.turn(DIRECTIONS[np.argmax(out)])

    def calculate_fitness(self):
        # Fonction de fitness améliorée qui récompense mieux les bons comportements
        # Bonus exponentiel pour les scores élevés
        score_bonus = self.score * 200
        if self.score > 0:
            score_bonus += (self.score ** 2) * 50  # Bonus quadratique pour encourager les scores élevés
        
        # Récompense pour la survie (mais moins que le score)
        survival_bonus = self.steps * 0.5
        
        # Pénalité pour ne pas avoir mangé (mais moins sévère)
        starvation_penalty = self.steps_without_food * 0.1
        
        # Bonus pour avoir mangé récemment
        if self.score > 0:
            efficiency_bonus = (self.score / max(self.steps, 1)) * 100
        else:
            efficiency_bonus = 0
        
        self.fitness = (
            score_bonus
            + survival_bonus
            - starvation_penalty
            + efficiency_bonus
        )
        return max(0, self.fitness)
