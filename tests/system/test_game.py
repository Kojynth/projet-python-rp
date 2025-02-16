import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.personnage import Personnage
from src.core.adversaire import Adversaire
from src.combat.combat import boucle_combat
from tests.data.test_data import create_test_teams

# Créer des instances de Personnage et Adversaire
personnage = Personnage(
    1,  # ID du personnage
    "Personnage",  # Nom du personnage
    100,  # Points de vie (HP) actuels
    100,  # Points de vie (HP) max
    100,  # Points de mana actuels
    100,  # Points de mana max
    20,  # Force du personnage
    10,  # Défense du personnage
    10,  # Magie du personnage
    10,  # Résistance du personnage
    10,  # Agilité du personnage
    1,  # Niveau du personnage
    0,  # Points de stats du personnage
    0  # Expérience du personnage
)
adversaire = Adversaire(
    2,  # ID de l'adversaire
    "Adversaire",  # Nom de l'adversaire
    120,  # Points de vie (HP) actuels
    120,  # Points de vie (HP) max
    100,  # Points de mana actuels
    100,  # Points de mana max
    10,  # Force de l'adversaire
    10,  # Défense de l'adversaire
    10,  # Magie de l'adversaire
    10,  # Résistance de l'adversaire
    10,  # Agilité de l'adversaire
    10,  # Niveau de l'adversaire
    10  # Expérience de l'adversaire
)

# Lancer la boucle de combat
liste_combattant = [personnage, adversaire]
boucle_combat(liste_combattant, [personnage], [adversaire])