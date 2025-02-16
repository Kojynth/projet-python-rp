import sqlite3

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
    """Crée la base de données et les tables nécessaires"""
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    
    # Création de la table Personnage
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Personnage (
        id INTEGER PRIMARY KEY,
        pseudo TEXT,
        hp INTEGER,
        hp_total INTEGER,
        mana INTEGER,
        mana_total INTEGER,
        force INTEGER,
        defense INTEGER,
        magie INTEGER,
        resistance INTEGER,
        agilite INTEGER,
        niveau INTEGER,
        points_de_stats INTEGER,
        experience INTEGER
    )
    ''')
    
    # Création de la table Adversaire
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Adversaire (
        id INTEGER PRIMARY KEY,
        pseudo TEXT,
        hp INTEGER,
        hp_total INTEGER,
        mana INTEGER,
        mana_total INTEGER,
        force INTEGER,
        defense INTEGER,
        magie INTEGER,
        resistance INTEGER,
        agilite INTEGER,
        niveau INTEGER,
        experience INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

def sauvegarder_objets(table, objets):
    """Sauvegarde une liste d'objets dans la base de données"""
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    
    for obj in objets:
        if table == 'Personnage':
            cursor.execute('''
            INSERT OR REPLACE INTO Personnage 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (obj.id, obj.pseudo, obj.hp, obj.hp_total, obj.mana, obj.mana_total,
                 obj.force, obj.defense, obj.magie, obj.resistance, obj.agilite,
                 obj.niveau, obj.points_de_stats, obj.experience))
        elif table == 'Adversaire':
            cursor.execute('''
            INSERT OR REPLACE INTO Adversaire 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (obj.id, obj.pseudo, obj.hp, obj.hp_total, obj.mana, obj.mana_total,
                 obj.force, obj.defense, obj.magie, obj.resistance, obj.agilite,
                 obj.niveau, obj.experience))
    
    conn.commit()
    conn.close()

def charger_donnees(table, classe):
    """Charge les données depuis la base de données"""
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()
    
    objets = []
    for row in rows:
        if table == 'Personnage':
            obj = classe(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                        row[7], row[8], row[9], row[10], row[11], row[12], row[13])
        elif table == 'Adversaire':
            obj = classe(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                        row[7], row[8], row[9], row[10], row[11], row[12])
        objets.append(obj)
    
    conn.close()
    return objets

def creer_vue_combattants():
    with DatabaseManager() as db:
        db.execute('''
        CREATE VIEW IF NOT EXISTS Combattants AS
        SELECT id, pseudo, hp, hp_total, mana, mana_total, force, niveau, experience, points_de_stats, 'Personnage' AS type
        FROM Personnage
        UNION ALL
        SELECT id, pseudo, hp, hp_total, mana, mana_total, force, niveau, experience, points_de_stats, 'Adversaire' AS type
        FROM Adversaire
        ''')
