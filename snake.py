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

        # Vérifier la collision AVANT d'ajouter la nouvelle position
        # La queue (dernière position) va bouger si on ne mange pas,
        # donc on ne la considère pas comme un obstacle
        # On vérifie seulement les positions qui resteront fixes (le corps, pas la queue)
        if len(self.positions) >= self.length:
            # Le serpent a atteint sa longueur maximale
            # La queue (dernière position) va être retirée, donc on l'exclut
            body_positions = self.positions[:-1] if len(self.positions) > 1 else []
        else:
            # Le serpent est encore en train de grandir
            # Toutes les positions actuelles sont fixes et comptent comme obstacles
            body_positions = self.positions
        
        # Vérifier si la nouvelle position entre en collision avec le corps
        if new in body_positions:
            self.alive = False
            return False

        # Ajouter la nouvelle position de la tête
        self.positions.insert(0, new)

        if new == food:
            # Le serpent a mangé : augmenter le score et la taille
            self.score += 1
            self.length += 1  # Augmente la taille du serpent
            self.steps_without_food = 0
            # Ne pas tronquer : on garde toutes les positions car le serpent grandit
            return True

        # Si le serpent n'a pas mangé, tronquer pour garder exactement self.length éléments
        # On garde uniquement les self.length premières positions (la tête + le corps)
        while len(self.positions) > self.length:
            self.positions.pop()  # Retirer la queue
        
        self.steps += 1
        self.steps_without_food += 1

        # Donner plus de temps pour trouver la nourriture (500 steps pour plus de chances)
        # Augmenté pour permettre au serpent de grandir avant de mourir de faim
        if self.steps_without_food > 500:
            self.alive = False

        return False

    def get_vision(self, food):
        """
        Calcule la vision du serpent pour le réseau neuronal.
        Amélioré pour mieux détecter les obstacles et la nourriture.
        """
        hx, hy = self.get_head()
        fx, fy = food

        # Position relative de la nourriture (normalisée)
        vision = [
            (fx - hx) / GRID_WIDTH,
            (fy - hy) / GRID_HEIGHT
        ]

        # Détection d'obstacles dans les 4 directions
        # On ne considère pas la queue comme obstacle car elle va bouger
        body_positions = self.positions[:-1] if len(self.positions) > 1 else []
        for dx, dy in DIRECTIONS:
            nx, ny = (hx + dx) % GRID_WIDTH, (hy + dy) % GRID_HEIGHT
            # Vérifier si c'est un obstacle (corps, pas la queue)
            vision.append(1 if (nx, ny) in body_positions else 0)

        # Direction actuelle encodée (one-hot)
        for d in DIRECTIONS:
            vision.append(1 if self.direction == d else 0)

        # Longueur normalisée
        vision.append(self.length / (GRID_WIDTH * GRID_HEIGHT))
        
        # Direction actuelle (x, y)
        vision += list(self.direction)

        return vision

    def think(self, food):
        out = self.network.forward(self.get_vision(food))
        self.turn(DIRECTIONS[np.argmax(out)])

    def calculate_fitness(self):
        """
        Calcule la fitness du serpent.
        Récompense fortement le score (manger) et la survie.
        """
        # Récompense pour manger : chaque nourriture = 200 points (augmenté)
        # Bonus pour la longueur : plus le serpent est long, mieux c'est
        # Récompense pour survivre : chaque step = 0.1 point
        # Pénalité très légère pour ne pas manger
        self.fitness = (
            self.score * 200  # Récompense principale pour manger (augmentée)
            + self.length * 20  # Bonus pour la taille (augmenté pour encourager la croissance)
            + self.steps * 0.1  # Récompense pour survivre
            - self.steps_without_food * 0.05  # Pénalité très réduite
        )
        return max(0, self.fitness)
