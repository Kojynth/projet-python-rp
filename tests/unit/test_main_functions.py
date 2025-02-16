import sqlite3
from src.core.personnage import Personnage, sauvegarder_personnages, charger_personnages
from src.core.equipe_joueur import selectionner_equipe
from src.combat.combat import boucle_combat
from src.core.adversaire import Adversaire, ajouter_adversaires, sauvegarder_adversaires
from src.core.equipe_adverse import EquipeAdverse
from src.database.bddmanager import creer_base_de_donnees, sauvegarder_objets, charger_donnees, creer_vue_combattants

class DatabaseManager:
    def __enter__(self):
        self.conn = sqlite3.connect('jeu.db', timeout=10)  # Ajouter un timeout pour éviter les blocages
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.conn.commit()
        self.conn.close()

def creer_base_de_donnees():
    with DatabaseManager() as db:
        db.execute('''
        CREATE TABLE IF NOT EXISTS Personnage (
            id INTEGER PRIMARY KEY,
            pseudo TEXT,
            hp INTEGER,
            hp_total INTEGER,
            mana INTEGER,
            mana_total INTEGER,
            attaque INTEGER,
            niveau INTEGER,
            points_de_stats INTEGER DEFAULT 0,
            experience INTEGER
        )
        ''')
        db.execute('''
        CREATE TABLE IF NOT EXISTS Adversaire (
            id INTEGER PRIMARY KEY,
            pseudo TEXT,
            hp INTEGER,
            hp_total INTEGER,
            mana INTEGER,
            mana_total INTEGER,
            attaque INTEGER,
            niveau INTEGER DEFAULT 1,
            experience INTEGER,
            points_de_stats INTEGER DEFAULT 0
        )
        ''')

def sauvegarder_objets(table, objets):
    with DatabaseManager() as db:
        for obj in objets:
            columns = ", ".join(obj.__dict__.keys())
            placeholders = ", ".join("?" for _ in obj.__dict__.keys())
            values = tuple(obj.__dict__.values())
            db.execute(f'''
            INSERT OR REPLACE INTO {table} ({columns})
            VALUES ({placeholders})
            ''', values)

def charger_donnees(table, objet_classe):
    with DatabaseManager() as db:
        db.execute(f'SELECT * FROM {table}')
        rows = db.fetchall()
        print(f"Loading data from {table}: {rows}")  # Debug print
        return [objet_classe(*row) for row in rows]

# Fonction pour insérer des données de test si elles n'existent pas déjà
def inserer_donnees_de_test():
    with DatabaseManager() as db:
        # Données de test pour les personnages
        personnages_test = [
            ("Merlin cliché", 50, 50, 100, 100, 20, 1, 0, 0),
            ("Artxis le troll de Skyrim avec la montagne des Grisebarbes", 200, 200, 150, 150, 5, 1, 0, 0),
            ("Pedro", 225000, 225000, 20000, 20000, 20000, 1, 0, 0),
            ("Conan", 100, 100, 100, 100, 10, 1, 0, 0)
        ]

        # Insérer les personnages de test s'ils n'existent pas déjà
        for data in personnages_test:
            db.execute('''
            SELECT 1 FROM Personnage WHERE
            pseudo = ? AND
            hp = ? AND
            hp_total = ? AND
            mana = ? AND
            mana_total = ? AND
            attaque = ? AND
            niveau = ? AND
            points_de_stats = ? AND
            experience = ?
            ''', data)
            if not db.fetchone():
                db.execute('''
                INSERT INTO Personnage (
                    pseudo,
                    hp,
                    hp_total,
                    mana,
                    mana_total,
                    attaque,
                    niveau,
                    points_de_stats,
                    experience
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)

        # Données de test pour les adversaires
        adversaires_test = [
            ("Adversaire 1", 100, 100, 50, 50, 10, 1, 0, 0),
            ("Adversaire 2", 150, 150, 75, 75, 15, 1, 0, 0)
        ]

        # Insérer les adversaires de test s'ils n'existent pas déjà
        for data in adversaires_test:
            db.execute('''
            SELECT 1 FROM Adversaire WHERE
            pseudo = ? AND
            hp = ? AND
            hp_total = ? AND
            mana = ? AND
            mana_total = ? AND
            attaque = ? AND
            niveau = ? AND
            experience = ? AND
            points_de_stats = ?
            ''', data)
            if not db.fetchone():
                db.execute('''
                INSERT INTO Adversaire (
                    pseudo,
                    hp,
                    hp_total,
                    mana,
                    mana_total,
                    attaque,
                    niveau,
                    experience,
                    points_de_stats
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)
                conn.commit()
                conn.close()

# Fonction principale pour tester le jeu
def tester_jeu():
    print("Début de tester_jeu()")
    try:
        creer_base_de_donnees()
        print("Base de données créée")
    except Exception as e:
        print(f"Erreur lors de la création de la base de données : {e}")
        return

    try:
        creer_vue_combattants()
        print("Vue Combattants créée")
    except Exception as e:
        print(f"Erreur lors de la création de la vue Combattants : {e}")
        return

    try:
        inserer_donnees_de_test()
        print("Données de test insérées")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données de test : {e}")
        return

    try:
        personnages = charger_personnages()
        print(f"Personnages chargés : {personnages}")
    except Exception as e:
        print(f"Erreur lors du chargement des personnages : {e}")
        return
    # Si aucun personnage n'est trouvé, créer des personnages par défaut
    if not personnages:
        merlin = Personnage("Merlin cliché", 50, 50, 100, 100, 20, 1, 0, 0)
        artxis = Personnage("Artxis le troll de Skyrim avec la montagne des Grisebarbes", 200, 200, 150, 150, 5, 1, 0, 0)
        pedro_le_singe = Personnage("Pedro", 225000, 225000, 20000, 20000, 20000, 1, 0, 0)
        conan_guerrier = Personnage("Conan", 100, 100, 100, 100, 10, 1, 0, 0)
        personnages = [merlin, artxis, pedro_le_singe, conan_guerrier]
        sauvegarder_personnages(personnages)

    print("Sélection des équipes")
    equipe1 = selectionner_equipe(1)
    equipe2 = selectionner_equipe(2)
    print(f"Équipe 1 : {equipe1}")
    print(f"Équipe 2 : {equipe2}")

    # Combiner les équipes
    liste_combattant = equipe1 + equipe2

    print("Lancement de la boucle de combat")
    boucle_combat(liste_combattant, equipe1, equipe2)
    print("Fin de la boucle de combat")

    print("Fin de tester_jeu()")

    # Réinitialiser les stats des adversaires après le combat
    for adversaire in equipe2:
        if isinstance(adversaire, Adversaire):
            adversaire.reinitialiser_stats()

    # Sauvegarder les personnages après le combat
    sauvegarder_personnages(equipe1)


print("Début du script")
# Exécuter le test
if __name__ == "__main__":
    try:
        print("Avant l'appel de tester_jeu()")
        tester_jeu()
        print("Après l'appel de tester_jeu()")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        import traceback
        traceback.print_exc()
