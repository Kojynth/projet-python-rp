#testbdd.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import sqlite3
from src.database.bddmanager import DatabaseManager

# Connexion à la base de données
conn = sqlite3.connect('jeu.db')
cursor = conn.cursor()

# Récupérer les données des personnages

cursor.execute('SELECT * FROM Personnage')
personnages = cursor.fetchall()

# Récupérer les données des adversaires
cursor.execute('SELECT * FROM Adversaire')
adversaires = cursor.fetchall()

# Fermeture de la connexion
conn.close()

# Afficher les données récupérées
print("Personnages:")
for personnage in personnages:
    print(personnage)

print("\nAdversaires:")
for adversaire in adversaires:
    print(adversaire)
