import os
import sys
import sqlite3

# Ajouter le répertoire parent du dossier 'tests' au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database.bddmanager import DatabaseManager, creer_base_de_donnees
from src.core.personnage import Personnage, sauvegarder_personnages, charger_personnages
from src.core.equipe_joueur import selectionner_equipe
from src.combat.combat import boucle_combat
from src.core.adversaire import Adversaire, ajouter_adversaires, sauvegarder_adversaires
from src.core.equipe_adverse import EquipeAdverse

def inserer_donnees_de_test():
    """Insère des données de test dans la base de données"""
    # Données de test pour les adversaires
    adversaires_test = [
        ("Gobelin", 50, 50, 30, 30, 15, 10, 8, 5, 5, 1, 0),  # hp, hp_total, mana, mana_total, force, defense, magie, resistance, agilite, niveau, experience
        ("Orc", 80, 80, 20, 20, 20, 15, 5, 10, 7, 2, 0)
    ]

    with DatabaseManager() as cursor:
        # Insérer les adversaires de test s'ils n'existent pas déjà
        for data in adversaires_test:
            cursor.execute('''
            SELECT 1 FROM Adversaire WHERE pseudo = ?
            ''', (data[0],))
            
            if not cursor.fetchone():
                cursor.execute('''
                INSERT INTO Adversaire (
                    pseudo, hp, hp_total, mana, mana_total, 
                    force, defense, magie, resistance, agilite, 
                    niveau, experience
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)

def tester_jeu():
    """Fonction principale de test"""
    try:
        print("Création de la base de données...")
        creer_base_de_donnees()
        print("Insertion des données de test...")
        inserer_donnees_de_test()
        
        # Charger les personnages depuis la base de données
        personnages = charger_personnages()
        
        # Si aucun personnage n'est trouvé, créer des personnages par défaut
        if not personnages:
            # Merlin : Humain (race_id=1) Mage (classe_id=1)
            merlin = Personnage(1, "Merlin cliché", 50, 50, 100, 100, 20, 15, 30, 10, 12, 
                              niveau=1, points_de_stats=0, experience=0, race_id=1, classe_id=1)
            
            # Artxis : Orc (race_id=2) Guerrier (classe_id=2)
            artxis = Personnage(2, "Artxis le troll", 200, 200, 150, 150, 5, 25, 5, 20, 8,
                              niveau=1, points_de_stats=0, experience=0, race_id=2, classe_id=2)
            
            # Pedro : Elfe (race_id=3) Archer (classe_id=3)
            pedro = Personnage(3, "Pedro", 225000, 225000, 20000, 20000, 20000, 20000, 20000, 20000, 20000,
                             niveau=1, points_de_stats=0, experience=0, race_id=3, classe_id=3)
            
            personnages = [merlin, artxis, pedro]
            sauvegarder_personnages(personnages)

        # Sélectionner les équipes
        equipe1 = selectionner_equipe(1)
        equipe2 = selectionner_equipe(2)

        # Combiner les équipes
        liste_combattant = equipe1 + equipe2

        # Lancer la boucle de combat
        boucle_combat(liste_combattant, equipe1, equipe2)

        # Réinitialiser les stats des adversaires après le combat
        for adversaire in equipe2:
            if isinstance(adversaire, Adversaire):
                adversaire.reinitialiser_stats()

        # Sauvegarder les personnages après le combat
        sauvegarder_personnages(equipe1)

        # Sauvegarder les adversaires après le combat
        sauvegarder_adversaires(equipe2)

    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        raise

# Fonction pour charger les adversaires depuis la base de données
def charger_adversaires():
    conn = sqlite3.connect('jeu.db')
    cursor = conn.cursor()

    # Charger les adversaires
    cursor.execute('SELECT * FROM Adversaire')
    adversaires_data = cursor.fetchall()
    adversaires = [Adversaire(*data) for data in adversaires_data]

    conn.close()
    return adversaires

if __name__ == "__main__":
    tester_jeu()
