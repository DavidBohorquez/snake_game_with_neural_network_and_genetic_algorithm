# main.py
import pygame
from config import *
from genetic_algorithm import GeneticAlgorithm
from game import Game
from utils import plot_fitness

def main():
    # Initialisation de Pygame : cr├®ation de la fen├¬tre et du contr├┤leur de FPS
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Cr├®ation de l'algorithme g├®n├®tique avec une population par d├®faut (50 serpents)
    ga = GeneticAlgorithm()
    
    # MODIFI├ë : D├®finition du nombre maximum de g├®n├®rations ├á ex├®cuter
    # Permet de limiter l'├®volution ├á 100 g├®n├®rations pour observer les r├®sultats
    max_generations = 100

    running = True
    # MODIFI├ë : Boucle principale qui s'ex├®cute jusqu'├á 100 g├®n├®rations
    # Au lieu de jouer un seul serpent, on fait ├®voluer toute la population
    while running and ga.generation <= max_generations:
        # Gestion des ├®v├®nements Pygame (fermeture de la fen├¬tre)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # MODIFI├ë : ├ëvaluation de toute la population
        # Cette m├®thode fait jouer chaque serpent de la population jusqu'├á sa mort,
        # calcule leur fitness (score, dur├®e de vie, efficacit├®) et les trie par performance
        ga.evaluate()
        
        # MODIFI├ë : R├®cup├®ration et affichage du meilleur serpent de la g├®n├®ration
        # Apr├¿s l'├®valuation, la population est tri├®e par fitness d├®croissante,
        # donc le premier ├®l├®ment est le meilleur individu
        best_snake = ga.population[0]
        
        # R├®initialisation du meilleur serpent pour pouvoir le visualiser
        # (remet le serpent ├á sa position initiale, score ├á 0, etc.)
        best_snake.reset()
        
        # Cr├®ation d'un nouveau jeu avec le meilleur serpent pour visualisation
        game = Game(best_snake)
        
        # MODIFI├ë : Boucle de visualisation du meilleur serpent
        # Affiche le meilleur serpent de chaque g├®n├®ration pour observer l'├®volution
        while best_snake.alive:
            # Gestion des ├®v├®nements pendant le jeu (permet de fermer la fen├¬tre)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            # Si l'utilisateur a ferm├® la fen├¬tre, on sort de la boucle
            if not running:
                break
                
            # Mise ├á jour du jeu : le serpent r├®fl├®chit et se d├®place
            game.update()
            
            # Affichage du jeu ├á l'├®cran (serpent et nourriture)
            game.draw(screen)
            pygame.display.flip()
            
            # Contr├┤le de la vitesse du jeu (60 FPS)
            clock.tick(FPS)
        
        # MODIFI├ë : S├®lection et reproduction pour cr├®er la prochaine g├®n├®ration
        # S├®lection : choisit les meilleurs serpents (├®litisme + tournoi)
        selected = ga.select()
        
        # Reproduction : cr├®e une nouvelle g├®n├®ration ├á partir des s├®lectionn├®s
        # Applique crossover (combinaison des r├®seaux neuronaux) et mutation
        # Incr├®mente automatiquement le compteur de g├®n├®rations
        ga.reproduce(selected)

    # MODIFI├ë : Affichage du graphique de progression de la fitness
    # Trace l'├®volution de la meilleure fitness ├á travers les g├®n├®rations
    # Permet de visualiser l'am├®lioration de l'algorithme g├®n├®tique
    plot_fitness(ga.history)
    
    # Fermeture propre de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
