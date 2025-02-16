import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.personnage import Personnage
from src.core.adversaire import Adversaire
from src.combat.actions_combat import attaquer
from src.database.bddmanager import creer_base_de_donnees
from tests.data.test_data import create_test_personnage, create_test_adversaire, create_test_teams

def creer_combattants_test():
    """Crée des combattants avec des stats spécifiques pour les tests"""
    # Personnage avec haute agilité pour tester les esquives
    perso_agile = Personnage(
        id=1,
        pseudo="Ninja",
        hp=100, hp_total=100,
        mana=50, mana_total=50,
        force=20, defense=10,
        magie=15, resistance=10,
        agilite=40,  # Haute agilité pour tester les esquives (40% de chance)
        niveau=1, points_de_stats=0,
        experience=0
    )

    # Personnage avec stats équilibrées pour tester les contre-attaques
    perso_normal = Personnage(
        id=2,
        pseudo="Guerrier",
        hp=120, hp_total=120,
        mana=40, mana_total=40,
        force=25, defense=15,
        magie=10, resistance=15,
        agilite=20,
        niveau=1, points_de_stats=0,
        experience=0
    )

    # Adversaire pour les tests
    adversaire = Adversaire(
        id=1,
        pseudo="Gobelin",
        hp=80, hp_total=80,
        mana=30, mana_total=30,
        force=15, defense=8,
        magie=8, resistance=8,
        agilite=15,
        niveau=1,
        experience=10
    )

    return perso_agile, perso_normal, adversaire

def test_esquive():
    """Test des mécaniques d'esquive et de contre-attaque"""
    print("=== Test des mécaniques d'esquive et de contre-attaque ===")
    
    # Créer la base de données
    creer_base_de_donnees()
    
    # Créer les combattants de test
    perso_agile, perso_normal, adversaire = creer_combattants_test()
    
    # Créer les équipes
    equipe1 = [perso_agile, perso_normal]
    equipe2 = [adversaire]
    
    print("\nTest 1: Personnage agile (40% d'esquive)")
    print(f"Stats de {perso_agile.pseudo}:")
    print(f"HP: {perso_agile.hp}/{perso_agile.hp_total}")
    print(f"Agilité: {perso_agile.agilite}")
    
    # Faire 10 attaques pour voir les différents résultats
    print("\nLancement de 10 attaques sur le personnage agile...")
    for i in range(10):
        print(f"\nAttaque {i+1}:")
        attaquer(adversaire, perso_agile, equipe1, equipe2)
        
    print("\nTest 2: Personnage normal (20% d'esquive)")
    print(f"Stats de {perso_normal.pseudo}:")
    print(f"HP: {perso_normal.hp}/{perso_normal.hp_total}")
    print(f"Agilité: {perso_normal.agilite}")
    
    # Faire 10 attaques pour voir les différents résultats
    print("\nLancement de 10 attaques sur le personnage normal...")
    for i in range(10):
        print(f"\nAttaque {i+1}:")
        attaquer(adversaire, perso_normal, equipe1, equipe2)

def test_critique():
    """Test des attaques critiques"""
    print("\n=== Test des attaques critiques ===")
    
    # Créer les combattants de test
    perso_agile, perso_normal, adversaire = creer_combattants_test()
    
    # Créer les équipes
    equipe1 = [perso_normal]
    equipe2 = [adversaire]
    
    print(f"\nStats de l'attaquant ({perso_normal.pseudo}):")
    print(f"Force: {perso_normal.force}")
    print(f"Magie: {perso_normal.magie}")
    
    print(f"\nStats de la cible ({adversaire.pseudo}):")
    print(f"HP: {adversaire.hp}/{adversaire.hp_total}")
    print(f"Défense: {adversaire.defense}")
    print(f"Résistance: {adversaire.resistance}")
    
    # Faire 20 attaques pour voir les différents types de critiques
    print("\nLancement de 20 attaques pour tester les critiques...")
    for i in range(20):
        print(f"\nAttaque {i+1}:")
        attaquer(perso_normal, adversaire, equipe1, equipe2)
        # Réinitialiser les HP de l'adversaire après chaque attaque
        adversaire.hp = adversaire.hp_total

if __name__ == "__main__":
    print("=== Début des tests ===\n")
    test_esquive()
    test_critique()
    print("\n=== Fin des tests ===") 