import sqlite3
from src.database.connexion import DatabaseConnection

def ajouter_colonne_niveaux():
    conn = sqlite3.connect('jeu.db')

    cursor = conn.cursor()

    # Créer une nouvelle table avec la colonne 'niveaux'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Personnage_temp (
        id INTEGER PRIMARY KEY,
        pseudo TEXT,
        hp INTEGER,
        hp_total INTEGER,
        mana INTEGER,
        mana_total INTEGER,
        attaque INTEGER,
        niveau INTEGER,
        points_de_stats INTEGER DEFAULT 0,
        degats_infliges INTEGER,
        experience INTEGER
    )
    ''')

    # Copier les données de l'ancienne table vers la nouvelle table
    cursor.execute('''
    INSERT INTO Personnage_temp (id, pseudo, hp, hp_total, mana, mana_total, attaque, niveau, points_de_stats, degats_infliges, experience)
    SELECT id, pseudo, hp, hp_total, mana, mana_total, attaque, niveau, points_de_stats, degats_infliges, experience FROM Personnage
    ''')

    # Supprimer l'ancienne table
    cursor.execute('DROP TABLE Personnage')

    # Renommer la nouvelle table en 'Personnage'
    cursor.execute('ALTER TABLE Personnage_temp RENAME TO Personnage')

    conn.commit()
    conn.close()

def update_personnage(personnage):
    """Met à jour un personnage dans la base de données"""
    with DatabaseConnection() as cursor:
        cursor.execute('''
            UPDATE Personnage 
            SET hp=?, mana=?, niveau=?, experience=?
            WHERE id=?
        ''', (personnage.hp, personnage.mana, personnage.niveau, 
              personnage.experience, personnage.id))

# Appeler la fonction pour ajouter la colonne 'niveaux'
ajouter_colonne_niveaux()
