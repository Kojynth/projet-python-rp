import sys
import os
import sqlite3

# Obtenir le chemin absolu du répertoire racine du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Ajouter le chemin au PYTHONPATH
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Supprimer la base de données existante si elle existe
db_path = os.path.join(project_root, 'game.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print("Base de données existante supprimée.")

# Vérifier que le chemin est correct
print(f"Project root: {project_root}")
print(f"Sys.path: {sys.path}")

try:
    from src.core.personnage import Personnage
    from src.database.bddmanager import creer_base_de_donnees
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print(f"Contenu du dossier src: {os.listdir(os.path.join(project_root, 'src'))}")
    print(f"Contenu du dossier src/core: {os.listdir(os.path.join(project_root, 'src', 'core'))}")
    raise

def test_progression():
    # S'assurer que la base de données est créée
    creer_base_de_donnees()
    
    # Créer un personnage
    hero = Personnage(1, "TestHero", 100, 100, 50, 50, 20, 10, 15, 10, 12, 1, 0, 0)
    
    # Afficher état initial
    print("\nÉtat initial:")
    hero.afficher_fiche()
    
    # Test niveau 1-5 (gain de 20 mana par niveau et 5 points de stats)
    print("\nTest des niveaux 1-5:")
    xp_totale = sum([(i+1)*10 for i in range(1, 5)])
    hero.gagner_experience(xp_totale)
    
    # Test niveau 99-101 (changement de gain de mana et points de stats)
    print("\nTest des niveaux 99-101 (pour voir les changements de gains):")
    # Calculer l'XP nécessaire pour atteindre le niveau 101
    xp_totale = sum([(i+1)*10 for i in range(5, 101)])
    hero.gagner_experience(xp_totale)

if __name__ == '__main__':
    test_progression()