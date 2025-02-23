import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.creation_personnage import CreationPersonnage
from src.database.bddmanager import DatabaseManager, creer_base_de_donnees
from src.database.RacesJoueur_manager import RacesManager
from src.database.ClasseJoueur_manager import ClassesManager

def initialiser_bases_donnees(force=False):
    """
    Initialise toutes les bases de données nécessaires
    
    Args:
        force (bool): Si True, force la recréation des tables
    """
    try:
        print("Création de la base de données principale...")
        creer_base_de_donnees(force=force)
        
        print("Initialisation des races...")
        races_manager = RacesManager()
        races_manager.create_tables()
        races_manager.initialize_data()
        
        print("Initialisation des classes...")
        classes_manager = ClassesManager()
        classes_manager.create_tables()
        classes_manager.initialize_data()
        
    except Exception as e:
        print(f"Erreur lors de l'initialisation des bases de données: {e}")
        raise

class TestCreationPersonnage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialisation une seule fois avant tous les tests"""
        initialiser_bases_donnees(force=True)  # Force la recréation pour les tests
        
    def setUp(self):
        """Initialisation avant chaque test"""
        self.createur = CreationPersonnage()
    
    def test_creation_personnage(self):
        """Test la création d'un personnage"""
        # TODO: Ajouter les tests spécifiques
        pass

def main():
    """Fonction principale pour les tests manuels"""
    print("Initialisation du système...")
    try:
        # Initialiser les bases de données sans forcer la recréation
        initialiser_bases_donnees(force=False)
        
        # Créer une instance du créateur de personnages
        createur = CreationPersonnage()
        
        # Créer un nouveau personnage
        nouveau_personnage = createur.creer_personnage()
        
        print("\nPersonnage créé avec succès!")
        print(f"ID: {nouveau_personnage.id}")
        print(f"Nom: {nouveau_personnage.pseudo}")
        print(f"Niveau: {nouveau_personnage.niveau}")
        
    except Exception as e:
        print(f"Une erreur est survenue: {e}")
        raise

if __name__ == '__main__':
    # Si des arguments de test sont fournis, lancer les tests unitaires
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    # Sinon, on lance le menu de test
    else:
        main() 