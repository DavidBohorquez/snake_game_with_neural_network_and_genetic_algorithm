# Partie 1 : Algorithmes génétiques

## Consignes

Implémentation d'un algorithme génétique pour optimiser les paramètres d'un agent jouant au Snake. Le projet se concentre sur trois méthodes principales : **evaluate**, **select**, et **reproduce**.

---

## 🔑 Points clés pour l'implémentation

### 1. Évaluation (`evaluate`)

**Objectif** : Chaque agent (serpent) joue au jeu et calcule sa fitness.

**Implémentation** :
- Chaque serpent de la population joue une partie complète jusqu'à sa mort
- La fitness est calculée en fonction de :
  - **Score** : `score * 100` (chaque nourriture mangée = 100 points)
  - **Durée de vie** : `steps * 0.1` (récompense pour survivre)
  - **Efficacité des mouvements** : `-steps_without_food * 0.2` (pénalité pour tourner sans manger)
- Cette méthode met à jour la valeur de fitness de chaque individu
- La population est triée par fitness décroissante (meilleurs en premier)

**Implémentation** : Voir `genetic_algorithm.py`, méthode `evaluate()`

---

### 2. Sélection (`select`)

**Objectif** : Choisir les meilleurs serpents pour produire la génération suivante.

**Méthodes implémentées** :
- **Élitisme** : Les 10% meilleurs individus (5 serpents) sont conservés directement
- **Tournoi** : Pour le reste de la population, sélection par tournoi
  - Choisir k individus aléatoires (k = 5 par défaut)
  - Prendre le meilleur parmi ces k participants
  - Répéter jusqu'à avoir assez de serpents

**Retour** : Un sous-ensemble des meilleurs individus (taille = taille de la population)

**Implémentation** : Voir `genetic_algorithm.py`, méthode `select()`

---

### 3. Reproduction (`reproduce`)

**Objectif** : Créer une nouvelle population à partir des serpents sélectionnés.

**Implémentation** :
- **Crossover** : Combine les chromosomes (réseaux neuronaux) des parents
  - Taux de crossover : 70%
  - Méthode : Pour chaque poids du réseau neuronal, choisir aléatoirement entre le poids du parent 1 ou du parent 2
  - Si pas de crossover (30%), copier directement un parent
- **Mutation** : Introduit de la variation
  - Taux de mutation : 10%
  - Modifie aléatoirement certains poids du réseau neuronal
  - Permet d'explorer de nouvelles solutions
- **Mise à jour** : 
  - Met à jour la population avec la nouvelle génération
  - Incrémente le compteur de générations

**Implémentation** : Voir `genetic_algorithm.py`, méthode `reproduce()`

---

## 📁 Structure du projet

```
snake_game_with_neural_network_and_genetic_algorithm/
│
├── main.py                    # Point d'entrée principal
├── genetic_algorithm.py       # Implémentation de l'algorithme génétique
│                              #   - evaluate() : Évaluation de la population
│                              #   - select() : Sélection des meilleurs
│                              #   - reproduce() : Reproduction avec crossover et mutation
├── neural_network.py          # Réseau de neurones (feedforward)
├── snake.py                   # Classe Snake avec logique du jeu et calcul de fitness
├── game.py                    # Gestion du jeu et affichage
├── config.py                  # Configuration (taille grille, couleurs, etc.)
├── utils.py                   # Utilitaires (graphiques)
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier
```

---

## ⚙️ Paramètres de l'algorithme génétique

Les paramètres sont définis dans `genetic_algorithm.py` :

- **Taille de la population** : 50 serpents (par défaut)
- **Taux de mutation** : 10% (petit taux pour éviter de détruire les bonnes solutions)
- **Taux de crossover** : 70% (taux élevé pour favoriser la combinaison des bonnes caractéristiques)
- **Élitisme** : 10% de la population (5 meilleurs serpents conservés)
- **Taille du tournoi** : 5 individus
- **Nombre de générations** : 100 (configurable dans `main.py`)

---

## 📊 Remarques pratiques

### Taille de la population
- Quelques dizaines de serpents (50 par défaut)
- Permet un bon équilibre entre diversité et performance

### Nombre de générations
- Assez pour observer l'évolution (50-100 générations)
- Configurable dans `main.py` : `max_generations = 100`

### Taux de mutation et de crossover
- **Mutation** : Petit taux (10%) pour éviter de détruire les bonnes solutions
- **Crossover** : Taux élevé (70%) pour favoriser la combinaison des caractéristiques

### Suivi de la progression
- Stockage de la meilleure fitness de chaque génération dans `self.history`
- Affichage dans la console : `Génération X - Meilleure fitness: Y, Score: Z`
- Graphique de progression à la fin de l'exécution

---

## 🔄 Cycle d'évolution

Le cycle complet de l'algorithme génétique :

1. **Initialisation** → Population de 50 serpents avec réseaux neuronaux aléatoires
2. **Évaluation (evaluate)** → Chaque serpent joue et calcule sa fitness
3. **Sélection (select)** → Choisir les meilleurs serpents (élitisme + tournoi)
4. **Reproduction (reproduce)** → Créer nouvelle génération (crossover + mutation)
5. **Répétition** → Retour à l'étape 2 pour la génération suivante

---

## 📈 Résultats attendus

Au fil des générations, vous devriez observer :

- **Génération 1-10** : Serpents qui meurent rapidement, mangent rarement
- **Génération 10-30** : Serpents qui commencent à se diriger vers la nourriture
- **Génération 30-50** : Serpents qui mangent régulièrement
- **Génération 50-100** : Serpents qui mangent efficacement et survivent plus longtemps

Le graphique de fitness devrait montrer une courbe ascendante, indiquant que les serpents apprennent progressivement à mieux jouer.

---

## 🔧 Dépannage

### Les serpents n'apprennent pas
- Augmentez le nombre de générations dans `main.py`
- Vérifiez que la fitness augmente dans la console
- Ajustez les taux de mutation/crossover si nécessaire

### Performance lente
- Réduisez la taille de la population dans `genetic_algorithm.py`
- Réduisez `max_steps` dans `evaluate()` pour limiter la durée des parties

---

## 📝 Notes

- Le code est documenté avec des commentaires expliquant les concepts clés
- Les trois méthodes principales (`evaluate`, `select`, `reproduce`) sont implémentées selon les consignes
- Le projet suit les principes de l'algorithme génétique classique

