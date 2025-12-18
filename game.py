# game.py
import random
import pygame
from config import *

class Game:
    def __init__(self, snake):
        self.snake = snake
        self.food = self.spawn_food()

    def spawn_food(self):
        while True:
            p = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if p not in self.snake.positions:
                return p

    def update(self):
        self.snake.think(self.food)
        if self.snake.move(self.food):
            self.food = self.spawn_food()

    def draw(self, screen):
        screen.fill(BLACK)

        # Dessiner toutes les positions du serpent (le serpent grandit avec self.length)
        for i, (x, y) in enumerate(self.snake.positions):
            pygame.draw.rect(
                screen, GREEN,
                (x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

        # Dessiner la nourriture
        fx, fy = self.food
        pygame.draw.rect(
            screen, RED,
            (fx*GRID_SIZE, fy*GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )
        
        # Afficher le score et la longueur pour debug
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.snake.score} | Longueur: {self.snake.length}", True, WHITE)
        screen.blit(score_text, (10, 10))
