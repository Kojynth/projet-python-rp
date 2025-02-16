import sqlite3
from src.core.personnage import Personnage, sauvegarder_personnages, charger_personnages
from src.core.equipe_joueur import selectionner_equipe
from src.combat.combat import boucle_combat
from src.core.adversaire import Adversaire, ajouter_adversaires, sauvegarder_adversaires
from src.core.equipe_adverse import EquipeAdverse


# Fonction pour créer la base de données et les tables nécessaires
def creer_base_de_donnees():
    conn = sqlite3.connect('jeu.db')
    cursor = conn.cursor()

    # Créer les tables
    cursor.execute('''
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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Adversaire (
        id INTEGER PRIMARY KEY,
        pseudo TEXT,
        hp INTEGER,
        hp_total INTEGER,
        mana INTEGER,
        mana_total INTEGER,
        attaque INTEGER,
        experience INTEGER,
        points_de_stats INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

# Fonction pour insérer des données de test si elles n'existent pas déjà
def inserer_donnees_de_test():
    conn = sqlite3.connect('jeu.db')
    cursor = conn.cursor()

    # Données de test pour les personnages
    personnages_test = [
        ("Merlin cliché", 50, 50, 100, 100, 20, 1, 1, 0),
        ("Artxis le troll de Skyrim avec la montagne des Grisebarbes", 200, 200, 150, 150, 5, 1, 1, 0),
        ("Pedro", 225000, 225000, 20000, 20000, 20000, 1, 1, 0),
        ("Conan", 100, 100, 100, 100, 10, 1, 1, 0)
    ]

    # Données de test pour les adversaires
    adversaires_test = [
        ("Adversaire 1", 100, 100, 50, 50, 10, 1, 0, 0),
        ("Adversaire 2", 150, 150, 75, 75, 15, 1, 0, 0)
    ]

    # Insérer les personnages de test s'ils n'existent pas déjà
    for data in personnages_test:
        cursor.execute('''
        SELECT 1 FROM Personnage WHERE pseudo = ? AND hp = ? AND hp_total = ? AND mana = ? AND mana_total = ? AND attaque = ? AND niveau = ? AND points_de_stats = ? AND experience = ?
        ''', data)
        if not cursor.fetchone():
            cursor.execute('''
            INSERT INTO Personnage (pseudo, hp, hp_total, mana, mana_total, attaque, niveau, points_de_stats, experience)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

    # Insérer les adversaires de test s'ils n'existent pas déjà
    for data in adversaires_test:
        cursor.execute('''
        SELECT 1 FROM Adversaire WHERE pseudo = ? AND hp = ? AND hp_total = ? AND mana = ? AND mana_total = ? AND attaque = ? AND niveau = ? AND experience = ? AND points_de_stats = ?
        ''', data)
        if not cursor.fetchone():
            cursor.execute('''
            INSERT INTO Adversaire (pseudo, hp, hp_total, mana, mana_total, attaque, niveau, experience, points_de_stats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data)

    conn.commit()
    conn.close()

# Fonction principale pour tester le jeu
def tester_jeu():
    # Créer la base de données et insérer des données de test si elles n'existent pas déjà
    creer_base_de_donnees()
    inserer_donnees_de_test()

    # Charger les personnages depuis la base de données
    personnages = charger_personnages()

    # Si aucun personnage n'est trouvé, créer des personnages par défaut
    if not personnages:
        merlin = Personnage(1, "Merlin cliché", 50, 50, 100, 100, 20, niveau=1, points_de_stats=0, experience=0)
        artxis = Personnage(2, "Artxis le troll de Skyrim avec la montagne des Grisebarbes", 200, 200, 150, 150, 5, niveau=1, points_de_stats=0, experience=0)
        pedro_le_singe = Personnage(3, "Pedro", 225000, 225000, 20000, 20000, 20000, niveau=1, points_de_stats=0, experience=0)
        conan_guerrier = Personnage(4, "Conan", 100, 100, 100, 100, 10, niveau=1, points_de_stats=0, experience=0)
        personnages = [merlin, artxis, pedro_le_singe, conan_guerrier]
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

# Exécuter le test
if __name__ == "__main__":
    tester_jeu()
