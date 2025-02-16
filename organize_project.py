import os
import shutil

def create_directory_structure():
    """Crée la structure des dossiers"""
    directories = [
        'src',
        'src/core',
        'src/combat',
        'src/items',
        'src/database',
        'tests/unit',
        'tests/integration',
        'tests/system',
        'tests/data',
        'data',
        'docs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # Créer __init__.py dans les packages Python
        if directory.startswith(('src', 'tests')):
            with open(os.path.join(directory, '__init__.py'), 'w') as f:
                pass
        print(f"Créé: {directory}/")

def move_files():
    """Déplace les fichiers vers leur nouvelle location"""
    moves = {
        # Fichiers source principaux
        'rpg python.py': 'src/core/main.py',
        'combat.py': 'src/combat/combat.py',
        'equipe_adverse.py': 'src/core/equipe_adverse.py',
        'equipe_joueur.py': 'src/core/equipe_joueur.py',
        'ressources.py': 'src/core/ressources.py',
        
        # Fichiers de base de données
        'connexionbdd.py': 'src/database/connexion.py',
        'insérer_données.py': 'src/database/insert_data.py',
        'doublondelete.py': 'src/database/clean_duplicates.py',
        'update.py': 'src/database/update.py',
        
        # Tests existants
        'test_esquive.py': 'tests/integration/test_esquive.py',
        'test_game.py': 'tests/system/test_game.py',
        'test_data.py': 'tests/data/test_data.py',
        'test_database.py': 'tests/data/test_database.py',
        'test_personnage.py': 'tests/unit/test_personnage.py',
    }
    
    print("\nFichiers présents dans le répertoire courant:")
    for file in os.listdir('.'):
        print(f"- {file}")
    
    for source, destination in moves.items():
        print(f"\nTentative de déplacement de {source} vers {destination}")
        if os.path.exists(source):
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            try:
                shutil.move(source, destination)
                print(f"✓ Déplacé: {source} → {destination}")
            except Exception as e:
                print(f"✗ Erreur: {str(e)}")
        else:
            print(f"✗ Non trouvé: {source}")

def create_requirements():
    """Crée un fichier requirements.txt basique"""
    with open('requirements.txt', 'w') as f:
        f.write('# Liste des dépendances du projet\n')

def create_readme():
    """Crée un README.md basique"""
    with open('docs/README.md', 'w') as f:
        f.write('# Projet de Jeu\n\n')
        f.write('Documentation du projet...\n')

def main():
    print("=== Réorganisation du projet ===\n")
    
    print("Création de la structure des dossiers...")
    create_directory_structure()
    
    print("\nDéplacement des fichiers...")
    move_files()
    
    print("\nCréation des fichiers de base...")
    create_requirements()
    create_readme()
    
    print("\n=== Réorganisation terminée! ===")

if __name__ == "__main__":
    main() 