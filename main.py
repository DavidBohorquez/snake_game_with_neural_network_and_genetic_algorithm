# main.py
import pygame
from config import *
from genetic_algorithm import GeneticAlgorithm
from game import Game
from utils import plot_fitness

def main():
    # Initialisation de Pygame : création de la fenêtre et du contrôleur de FPS
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Création de l'algorithme génétique avec une population plus grande pour meilleur apprentissage
    ga = GeneticAlgorithm(size=100)  # Population augmentée de 50 à 100
    
    # MODIFIÉ : Définition du nombre maximum de générations à exécuter
    # Augmenté à 500 générations pour permettre un meilleur apprentissage
    max_generations = 500

    running = True
    # MODIFIÉ : Boucle principale qui s'exécute jusqu'à 100 générations
    # Au lieu de jouer un seul serpent, on fait évoluer toute la population
    while running and ga.generation <= max_generations:
        # Gestion des événements Pygame (fermeture de la fenêtre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # MODIFIÉ : Évaluation de toute la population
        # Cette méthode fait jouer chaque serpent de la population jusqu'à sa mort,
        # calcule leur fitness (score, durée de vie, efficacité) et les trie par performance
        # Affiche un message pour indiquer le début de l'évaluation
        print(f"Évaluation de la génération {ga.generation}...")
        ga.evaluate()
        
        # MODIFIÉ : Récupération et affichage du meilleur serpent de la génération
        # Après l'évaluation, la population est triée par fitness décroissante,
        # donc le premier élément est le meilleur individu
        best_snake = ga.population[0]
        
        # Réinitialisation du meilleur serpent pour pouvoir le visualiser
        # (remet le serpent à sa position initiale, score à 0, etc.)
        best_snake.reset()
        
        # Création d'un nouveau jeu avec le meilleur serpent pour visualisation
        game = Game(best_snake)
        
        # MODIFIÉ : Boucle de visualisation du meilleur serpent
        # Affiche le meilleur serpent de chaque génération pour observer l'évolution
        while best_snake.alive:
            # Gestion des événements pendant le jeu (permet de fermer la fenêtre)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            # Si l'utilisateur a fermé la fenêtre, on sort de la boucle
            if not running:
                break
                
            # Mise à jour du jeu : le serpent réfléchit et se déplace
            game.update()
            
            # Affichage du jeu à l'écran (serpent et nourriture)
            game.draw(screen)
            pygame.display.flip()
            
            # Contrôle de la vitesse du jeu (60 FPS)
            clock.tick(FPS)
        
        # MODIFIÉ : Sélection et reproduction pour créer la prochaine génération
        # Sélection : choisit les meilleurs serpents (élitisme + tournoi)
        selected = ga.select()
        
        # Reproduction : crée une nouvelle génération à partir des sélectionnés
        # Applique crossover (combinaison des réseaux neuronaux) et mutation
        # Incrémente automatiquement le compteur de générations
        ga.reproduce(selected)

    # MODIFIÉ : Affichage du graphique de progression de la fitness
    # Trace l'évolution de la meilleure fitness à travers les générations
    # Permet de visualiser l'amélioration de l'algorithme génétique
    plot_fitness(ga.history)
    
    # Fermeture propre de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
