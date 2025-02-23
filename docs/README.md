# Projet de Jeu

## Structure du Projet

Le projet est organisé en plusieurs dossiers principaux :

- `src/` : Contient le code source principal
  - `core/` : Fichiers principaux du jeu
  - `combat/` : Système de combat
  - `database/` : Gestion des bases de données avec SQLite
  - `items/` : Gestion des objets du jeu

- `tests/` : Contient les fichiers de tests
  - `unit/` : Tests unitaires
  - `integration/` : Tests d'intégration
  - `system/` : Tests système
  - `data/` : Données de test communes

## Backlog 

### Réalisé : 
- Système de combat 
- Système des esquives
- systèmes de points de statistiques
- BDD Adversaire
- BDD Personnages
- Définir les équipes du personnage
- définir les équipes des adversaires
- Inventaire du joueur
- Système de contres 
- Système de critiques
- Création du personnage
- Gestion des races
- Gestion des classes



### En cours :

###A faire : 
- système de points de compétences à attribuer pour créer/obtenir des  compétences
- Limiter les soins aux personnages encore en vie
- Si un personnage a fuit le commbat alors on ne peut plus interagir avec lui (bug potion de soin utilisable sur le héro ayant fuit)
- Faire une interface graphique pour le menu
- Faire une interface graphique pour le jeu
- Importer la carte de Médonia
- Créer les différents adversaires 
- Penser aux différents points d'intérêts du jeu 
- Créer l'histoire et ses quêtes et tout le parcours du joueur/utilisateur à travers le jeu
- Créer des quêtes intégré au jeu avec de muliples choix et fins
- Rajouter des options dans le menu actions du menu de combat
- Avoir une Interface comportant les onglets suivants :
  - Onglet "Équipes"
  - Onglet "Inventaires"
    - Créer un item "Encyclopédie" achetable et collectable
    - Créer un item "Journal" achetable et dans lequel il sera inscrit des notes au fur et à mesure de l'aventure depuis le moment où il aura acheté le journal (Entrée 1 : J'ai acheté ce journal etc etc)
  - Onglet "Quêtes"
  - Onglet "Carte" 
    - Sélectionner un endroit sur la carte de Médonia (Ville, forêt, montagne, etc...) puis une fois la destination sélectionnée, animation du trajet vers la destination (avec un nombre aléatoire pour indiquer si le trajet se passe bien ou mal en fonction de la valeur obtenue)
    - une fois arrivé à destination l'exploration par le joueur de l'endroit sélectionné (à moi d'aller dans les détails et dans les différents endroits visitable par le joueur)
  - Onglet "Options"

Dans l'onglet "Équipes" :
- Visualiser les différents personnages
  -Ajouter les âges dans le code et dans la BDD personnages
  - Sélectionner leurs équipements 
  - Sélectionner leurs compétences
  - Visualiser leurs backgrounds 
  - Des notes et autres anecdotes en lien avec le personnage sélectionné (Avec ce qu'il apprécie, déteste, caractère, etc...)

- A LA FIN  : s'intéresser au côté graphique avec pygame (voir avec Raphaël Hage pour l'interface graphique)

