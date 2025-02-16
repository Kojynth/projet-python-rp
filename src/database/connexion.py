"""Gestion de la connexion à la base de données"""
import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='jeu.db'):
        self.db_name = db_name
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn.cursor()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

# Connexion à la base de données (ou création si elle n'existe pas)
conn = sqlite3.connect('jeu.db')
cursor = conn.cursor()

# Supprimer les tables existantes si elles existent
cursor.execute('DROP TABLE IF EXISTS Personnage')
cursor.execute('DROP TABLE IF EXISTS Adversaire')

# Création de la table Personnage avec les nouvelles colonnes hp_total et mana_total
cursor.execute('''
CREATE TABLE Personnage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT NOT NULL,
    hp INTEGER NOT NULL,
    hp_total INTEGER NOT NULL,
    mana INTEGER NOT NULL,
    mana_total INTEGER NOT NULL,
    attaque INTEGER NOT NULL,
    niveau INTEGER NOT NULL,
    experience INTEGER NOT NULL
    points_de_stats INTEGER NOT NULL,
)
''')

# Création de la table Adversaire avec les nouvelles colonnes hp_total et mana_total
cursor.execute('''
CREATE TABLE Adversaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT NOT NULL,
    hp INTEGER NOT NULL,
    hp_total INTEGER NOT NULL,
    mana INTEGER NOT NULL,
    mana_total INTEGER NOT NULL,
    attaque INTEGER NOT NULL,
    niveau INTEGER NOT NULL,
    experience INTEGER NOT NULL
)
''')

# Commit et fermeture de la connexion
conn.commit()
conn.close()
