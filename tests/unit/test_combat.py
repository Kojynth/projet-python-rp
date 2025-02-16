import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
from src.combat.combat import boucle_combat
from src.core.personnage import Personnage
from src.core.adversaire import Adversaire
from src.database.bddmanager import creer_base_de_donnees, sauvegarder_objets, charger_donnees
from src.items.item import charger_items
from tests.data.test_data import create_test_teams

# Fonction pour créer des personnages
def creer_personnages():
    return [
        Personnage(1, "Hero1", 100, 100, 50, 50, 20, 10, 15, 10, 12, 1, 0, 0),
        Personnage(2, "Hero2", 120, 120, 60, 60, 25, 15, 20, 15, 14, 1, 0, 0)
    ]

# Fonction pour créer des adversaires
def creer_adversaires():
    return [
        Adversaire(1, "Enemy1", 80, 80, 40, 40, 18, 8, 12, 8, 10, 1, 0),
        Adversaire(2, "Enemy2", 90, 90, 45, 45, 22, 12, 18, 12, 13, 1, 0)
    ]

class TestCombat(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        creer_base_de_donnees()
        self.equipe_joueur = creer_personnages()
        self.equipe_adversaire = creer_adversaires()
        
    def test_combat_initialization(self):
        """Test de l'initialisation du combat"""
        # Sauvegarder les équipes dans la base de données
        sauvegarder_objets('Personnage', self.equipe_joueur)
        sauvegarder_objets('Adversaire', self.equipe_adversaire)
        
        # Charger les équipes depuis la base de données
        equipe_joueur = charger_donnees('Personnage', Personnage)
        equipe_adversaire = charger_donnees('Adversaire', Adversaire)
        
        # Vérifier que les équipes sont correctement chargées
        self.assertEqual(len(equipe_joueur), 2)
        self.assertEqual(len(equipe_adversaire), 2)
        
        # Vérifier les stats des personnages
        self.assertEqual(equipe_joueur[0].hp, 100)
        self.assertEqual(equipe_adversaire[0].hp, 80)

def main():
    # Créer la base de données et les tables
    creer_base_de_donnees()

    # Créer les équipes de personnages et d'adversaires
    equipe_joueur = creer_personnages()
    equipe_adversaire = creer_adversaires()

    # Sauvegarder les équipes dans la base de données
    sauvegarder_objets('Personnage', equipe_joueur)
    sauvegarder_objets('Adversaire', equipe_adversaire)

    # Charger les équipes depuis la base de données
    equipe_joueur = charger_donnees('Personnage', Personnage)
    equipe_adversaire = charger_donnees('Adversaire', Adversaire)

    # Liste de tous les combattants
    liste_combattant = equipe_joueur + equipe_adversaire

    # Lancer la boucle de combat
    boucle_combat(liste_combattant, equipe_joueur, equipe_adversaire)

if __name__ == "__main__":
    # Si on veut lancer les tests
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    # Sinon, on lance le combat
    else:
        main()
