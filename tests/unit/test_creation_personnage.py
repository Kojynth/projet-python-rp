import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
from src.core.creation_personnage import CreationPersonnage
from src.database.bddmanager import DatabaseManager, creer_base_de_donnees
from src.database.RacesJoueur_manager import DatabaseManager as RacesManager
from src.database.ClasseJoueur_manager import ClassesManager

def initialiser_bases_donnees():
    """Initialise toutes les bases de données nécessaires"""
    try:
        # Création de la base principale et de toutes les tables
        print("Création de la base de données principale...")
        with DatabaseManager() as cursor:
            # Table Personnage
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Personnage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pseudo TEXT NOT NULL,
                hp INTEGER,
                hp_total INTEGER,
                mana INTEGER,
                mana_total INTEGER,
                force INTEGER,
                defense INTEGER,
                magie INTEGER,
                resistance INTEGER,
                agilite INTEGER,
                niveau INTEGER,
                points_de_stats INTEGER,
                experience INTEGER,
                race_id INTEGER,
                classe_id INTEGER,
                sexe TEXT,
                alignement TEXT,
                orientation TEXT,
                taille REAL,
                poids REAL,
                FOREIGN KEY (race_id) REFERENCES races(race_id),
                FOREIGN KEY (classe_id) REFERENCES classes(class_id)
            )
            ''')
        
        # Initialisation des races
        print("Initialisation des races...")
        races_manager = RacesManager()
        races_manager.connect()
        races_manager.create_tables()
        races_manager.initialize_data()
        races_manager.disconnect()
        
        # Initialisation des classes
        print("Initialisation des classes...")
        classes_manager = ClassesManager()
        classes_manager.connect()
        classes_manager.create_tables()
        classes_manager.initialize_data()
        classes_manager.disconnect()
        
        print("Toutes les tables ont été initialisées avec succès!")
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation des bases de données: {e}")
        raise

class TestCreationPersonnage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialisation une seule fois avant tous les tests"""
        initialiser_bases_donnees()

    def setUp(self):
        """Initialisation avant chaque test"""
        self.createur = CreationPersonnage()

    def tearDown(self):
        """Nettoyage après chaque test"""
        if hasattr(self, 'createur'):
            del self.createur

    def test_creation_personnage(self):
        """Test de la création d'un nouveau personnage"""
        print("\n=== Test de création de personnage ===")
        
        # Créer un nouveau personnage
        nouveau_personnage = self.createur.creer_personnage()
        
        # Vérifier que le personnage a été créé et sauvegardé
        with DatabaseManager() as cursor:
            cursor.execute('SELECT * FROM Personnage WHERE pseudo = ?', (nouveau_personnage.pseudo,))
            personnage_db = cursor.fetchone()
            
            self.assertIsNotNone(personnage_db, "Le personnage n'a pas été sauvegardé dans la base de données")
            if personnage_db:
                print("\nPersonnage trouvé dans la base de données:")
                print(f"ID: {personnage_db[0]}")
                print(f"Nom: {personnage_db[1]}")
                print(f"Niveau: {personnage_db[11]}")
                print(f"Race: {personnage_db[14]}")
                print(f"Classe: {personnage_db[15]}")
                print(f"Sexe: {personnage_db[16]}")
                print(f"Alignement: {personnage_db[17]}")
                print(f"Orientation: {personnage_db[18]}")
                print(f"Taille: {personnage_db[19]} cm")
                print(f"Poids: {personnage_db[20]} kg")

def main():
    print("Initialisation du système...")
    try:
        # Initialiser les bases de données
        initialiser_bases_donnees()
        
        # Créer une instance du créateur de personnages
        createur = CreationPersonnage()
        
        while True:
            print("\n=== Menu de test ===")
            print("1. Créer un nouveau personnage")
            print("0. Quitter")
            
            choix = input("\nVotre choix: ")
            
            if choix == "1":
                nouveau_personnage = createur.creer_personnage()
            elif choix == "0":
                print("Au revoir!")
                break
            else:
                print("Choix invalide!")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        raise

if __name__ == "__main__":
    # Si on veut lancer les tests unitaires
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    # Sinon, on lance le menu de test
    else:
        main() 