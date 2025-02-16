import sqlite3

# Connexion à la base de données
conn = sqlite3.connect('jeu.db')
cursor = conn.cursor()

# Supprimer les doublons dans la table Personnage
cursor.execute('''
DELETE FROM Personnage
WHERE id NOT IN (
    SELECT MIN(id)
    FROM Personnage
    GROUP BY pseudo, hp, hp_total, mana, mana_total, attaque, niveau, points_de_stats, , experience
)
''')

# Supprimer les doublons dans la table Adversaire
cursor.execute('''
DELETE FROM Adversaire
WHERE id NOT IN (
    SELECT MIN(id)
    FROM Adversaire
    GROUP BY pseudo, hp, hp_total, mana, mana_total, attaque, niveau, experience, points_de_stats
)
''')

# Commit et fermeture de la connexion
conn.commit()
conn.close()
