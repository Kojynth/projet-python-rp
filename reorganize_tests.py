import os
import shutil

# Créer la structure des dossiers
def create_directory_structure():
    directories = [
        'tests',
        'tests/unit',
        'tests/integration',
        'tests/system',
        'tests/data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        init_path = os.path.join(directory, '__init__.py')
        with open(init_path, 'w') as f:
            pass
        print(f"Créé le dossier {directory} et son __init__.py")

# Déplacer les fichiers
def move_files():
    moves = {
        '# main_test.py': 'tests/unit/test_main.py',
        '# main.py': 'tests/unit/test_main_functions.py'
    }
    
    print("\nFichiers présents dans le répertoire courant:")
    for file in os.listdir('.'):
        print(f"- {file}")
    
    for source, destination in moves.items():
        print(f"\nTentative de déplacement de {source} vers {destination}")
        if os.path.exists(source):
            # Créer le dossier de destination s'il n'existe pas
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            try:
                shutil.move(source, destination)
                print(f"✓ Succès: {source} déplacé vers {destination}")
            except Exception as e:
                print(f"✗ Erreur lors du déplacement: {str(e)}")
        else:
            print(f"✗ Fichier source {source} non trouvé")

def main():
    print("=== Début de la réorganisation des tests ===")
    print("\nCréation de la structure des dossiers...")
    create_directory_structure()
    
    print("\nDéplacement des fichiers...")
    move_files()
    
    print("\n=== Réorganisation terminée! ===")

if __name__ == "__main__":
    main() 