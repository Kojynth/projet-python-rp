import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('jeu.db')
cursor = conn.cursor()

# Insérer un personnage
cursor.execute('''
INSERT INTO Personnage (pseudo, hp, attaque, niveau, mana, points_de_stats, experience)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', ("Test Personnage", 100, 20, 1, 100, 0, 0))

# Insérer un adversaire
cursor.execute('''
INSERT INTO Adversaire (pseudo, hp, attaque, niveau, mana, points_de_stats, experience)
VALUES (?, ?, ?, ?, ?, ?, ?)
''', ("Test Adversaire", 100, 20, 1, 100, 0, 0))

# Commit et fermeture de la connexion
conn.commit()
conn.close()

