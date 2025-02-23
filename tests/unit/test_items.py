import unittest
import os
import sys
from pathlib import Path

# Ajouter le chemin du projet au PYTHONPATH
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.database.bddmanager import creer_base_de_donnees
from src.database.connexion import DatabaseConnection

class TestItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialisation une seule fois avant tous les tests"""
        print("Initialisation de la base de données...")
        creer_base_de_donnees(force=True)  # Force la recréation des tables

    def test_ajouter_potions(self):
        """Test l'ajout de différentes potions de soin"""
        with DatabaseConnection() as cursor:
            # Ajout des potions de soin
            potions = [
                ('Petite potion de soin', 'POT_SOIN_P', 'Consommables', 
                 'Une petite potion qui restaure 10% des HP max', 
                 25, 10, 0, 0, 0, 0, 0, 0, 0, 1, 1, 10),
                
                ('Potion de soin', 'POT_SOIN_M', 'Consommables',
                 'Une potion qui restaure 25% des HP max',
                 50, 25, 0, 0, 0, 0, 0, 0, 0, 1, 1, 5),
                
                ('Potion de soin puissante', 'POT_SOIN_G', 'Consommables',
                 'Une grande potion qui restaure 50% des HP max',
                 100, 50, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3),
                
                ('Potion de soin surpuissante', 'POT_SOIN_S', 'Consommables',
                 'Une potion légendaire qui restaure 100% des HP max',
                 250, 100, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1)
            ]

            cursor.executemany('''
                INSERT INTO Item (
                    name, item_code, category, description, value,
                    hp_bonus, mp_bonus, force_bonus, defense_bonus,
                    magie_bonus, resistance_bonus, agilite_bonus,
                    is_equipable, is_consumable, is_stackable, max_stack
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', potions)

            # Vérification que les potions ont bien été ajoutées
            cursor.execute('SELECT name, item_code FROM Item WHERE category = "Consommables"')
            resultats = cursor.fetchall()
            
            self.assertEqual(len(resultats), 4)
            noms_attendus = [
                'Petite potion de soin',
                'Potion de soin',
                'Potion de soin puissante',
                'Potion de soin surpuissante'
            ]
            noms_trouves = [r[0] for r in resultats]
            for nom in noms_attendus:
                self.assertIn(nom, noms_trouves)

    def test_ajouter_item_inventaire(self):
        """Test l'ajout d'items dans l'inventaire"""
        with DatabaseConnection() as cursor:
            # Ajouter une potion à l'inventaire
            cursor.execute('''
                INSERT INTO inventaire (item_id, quantity)
                SELECT item_id, 3
                FROM Item 
                WHERE item_code = 'POT_SOIN_M'
            ''')

            # Vérifier que l'item est bien dans l'inventaire
            cursor.execute('''
                SELECT i.quantity, it.name
                FROM inventaire i
                JOIN Item it ON i.item_id = it.item_id
            ''')
            
            resultat = cursor.fetchone()
            self.assertIsNotNone(resultat)
            self.assertEqual(resultat[0], 3)  # Vérifie la quantité
            self.assertEqual(resultat[1], 'Potion de soin')  # Vérifie le nom

def main():
    """Fonction principale pour les tests manuels"""
    print("Initialisation du système...")
    try:
        # Forcer la recréation des tables
        creer_base_de_donnees(force=True)
        
        # Créer une instance de test
        test = TestItems()
        test.test_ajouter_potions()
        test.test_ajouter_item_inventaire()
        
        print("Tests terminés avec succès!")
        
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        raise

if __name__ == '__main__':
    # Si des arguments de test sont fournis, lancer les tests unitaires
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    # Sinon, on lance le test manuel
    else:
        main() 