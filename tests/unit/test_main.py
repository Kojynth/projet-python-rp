import unittest
import sqlite3
import os
import sys

# Ajouter le répertoire racine du projet au PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from src.core.main import DatabaseManager, creer_base_de_donnees, sauvegarder_objets, charger_donnees, inserer_donnees_de_test, tester_jeu
from src.core.personnage import Personnage

class TestMain(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        creer_base_de_donnees()

    def tearDown(self):
        self.conn.close()

    def test_creer_base_de_donnees(self):
        with DatabaseManager() as db:
            db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Personnage'")
            result = db.fetchone()
            self.assertIsNotNone(result, "La table Personnage n'a pas été créée.")

            db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Adversaire'")
            result = db.fetchone()
            self.assertIsNotNone(result, "La table Adversaire n'a pas été créée.")

    def test_inserer_donnees_de_test(self):
        inserer_donnees_de_test()
        with DatabaseManager() as db:
            db.execute("SELECT COUNT(*) FROM Personnage")
            count_personnage = db.fetchone()[0]
            self.assertEqual(count_personnage, 4, "Le nombre de personnages insérés n'est pas correct.")

            db.execute("SELECT COUNT(*) FROM Adversaire")
            count_adversaire = db.fetchone()[0]
            self.assertEqual(count_adversaire, 2, "Le nombre d'adversaires insérés n'est pas correct.")

    def test_charger_donnees(self):
        inserer_donnees_de_test()
        personnages = charger_donnees('Personnage', Personnage)
        self.assertEqual(len(personnages), 4, "Le nombre de personnages chargés n'est pas correct.")

        adversaires = charger_donnees('Adversaire', Personnage)
        self.assertEqual(len(adversaires), 2, "Le nombre d'adversaires chargés n'est pas correct.")

    def test_sauvegarder_objets(self):
        personnages = [
            Personnage(1, "Merlin cliché", 50, 50, 100, 100, 20, 1, 1, 0),
            Personnage(2, "Artxis le troll de Skyrim avec la montagne des Grisebarbes", 200, 200, 150, 150, 5, 1, 1, 0)
        ]
        sauvegarder_objets('Personnage', personnages)
        with DatabaseManager() as db:
            db.execute("SELECT COUNT(*) FROM Personnage")
            count_personnage = db.fetchone()[0]
            self.assertEqual(count_personnage, 2, "Le nombre de personnages sauvegardés n'est pas correct.")

if __name__ == '__main__':
    unittest.main()
