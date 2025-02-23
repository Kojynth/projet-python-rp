import sqlite3
import os
from src.database.connexion import DatabaseConnection

class DatabaseManager:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(project_root, 'data')
        
        # Créer le dossier data s'il n'existe pas
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        self.db_path = os.path.join(data_dir, 'jeu.db')
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            self.cursor.close()
            self.connection.close()

    @classmethod
    def get_db_path(cls):
        """Retourne le chemin de la base de données"""
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(project_root, 'data', 'jeu.db')

def creer_base_de_donnees(force=False):
    """
    Crée toutes les tables nécessaires
    
    Args:
        force (bool): Si True, recrée les tables même si la base existe déjà
    """
    db_connection = DatabaseConnection()
    
    # Si la base existe et qu'on ne force pas la recréation, on sort
    if db_connection.exists and not force:
        print("La base de données existe déjà. Utilisation de la base existante.")
        return

    with db_connection as cursor:
        # Suppression des tables existantes si nécessaire
        if force:
            cursor.execute('DROP TABLE IF EXISTS Personnage')
            cursor.execute('DROP TABLE IF EXISTS Adversaire')
            cursor.execute('DROP TABLE IF EXISTS races')
            cursor.execute('DROP TABLE IF EXISTS classes')
            cursor.execute('DROP TABLE IF EXISTS Item')
            cursor.execute('DROP TABLE IF EXISTS inventaire')
        
        # Création de la table Personnage
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Personnage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            hp INTEGER NOT NULL,
            hp_total INTEGER NOT NULL,
            mana INTEGER NOT NULL,
            mana_total INTEGER NOT NULL,
            force INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            magie INTEGER NOT NULL,
            resistance INTEGER NOT NULL,
            agilite INTEGER NOT NULL,
            niveau INTEGER NOT NULL,
            points_de_stats INTEGER NOT NULL,
            experience INTEGER NOT NULL,
            race_id INTEGER,
            classe_id INTEGER,
            sexe TEXT,
            alignement TEXT,
            orientation TEXT,
            taille REAL,
            poids REAL,
            FOREIGN KEY (race_id) REFERENCES races(race_id),
            FOREIGN KEY (classe_id) REFERENCES classes(classe_id)
        )
        ''')

        # Création de la table Adversaire
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Adversaire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            hp INTEGER NOT NULL,
            hp_total INTEGER NOT NULL,
            mana INTEGER NOT NULL,
            mana_total INTEGER NOT NULL,
            force INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            magie INTEGER NOT NULL,
            resistance INTEGER NOT NULL,
            agilite INTEGER NOT NULL,
            niveau INTEGER NOT NULL,
            experience INTEGER NOT NULL
        )
        ''')
    
        # Ajout de la table classes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_code TEXT UNIQUE,
            category TEXT,
            description TEXT,
            hp INTEGER,
            mp INTEGER,
            force INTEGER,
            defense INTEGER,
            magie INTEGER,
            resistance INTEGER,
            agilite INTEGER
        )
        ''')

        # Création de la table Item
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            item_code VARCHAR(10) UNIQUE NOT NULL,
            category VARCHAR(50) NOT NULL,
            description TEXT,
            value INTEGER DEFAULT 0,
            hp_bonus INTEGER DEFAULT 0,
            mp_bonus INTEGER DEFAULT 0,
            force_bonus INTEGER DEFAULT 0,
            defense_bonus INTEGER DEFAULT 0,
            magie_bonus INTEGER DEFAULT 0,
            resistance_bonus INTEGER DEFAULT 0,
            agilite_bonus INTEGER DEFAULT 0,
            is_equipable BOOLEAN DEFAULT 0,
            is_consumable BOOLEAN DEFAULT 0,
            is_stackable BOOLEAN DEFAULT 0,
            max_stack INTEGER DEFAULT 1
        )
        ''')

        # Création de la table inventaire
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventaire (
            inventaire_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            quantity INTEGER DEFAULT 1,
            is_equipped BOOLEAN DEFAULT 0,
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        )
        ''')

def sauvegarder_objets(table, objets):
    """Sauvegarde une liste d'objets dans la base de données"""
    with DatabaseManager() as cursor:
        for obj in objets:
            if table == 'Personnage':
                cursor.execute('''
                INSERT OR REPLACE INTO Personnage 
                (id, pseudo, hp, hp_total, mana, mana_total, force, defense, magie, 
                resistance, agilite, niveau, points_de_stats, experience, race_id, 
                classe_id, sexe, alignement, orientation, taille, poids)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (obj.id, obj.pseudo, obj.hp, obj.hp_total, obj.mana, obj.mana_total,
                     obj.force, obj.defense, obj.magie, obj.resistance, obj.agilite,
                     obj.niveau, obj.points_de_stats, obj.experience, obj.race_id,
                     obj.classe_id, obj.sexe, obj.alignement, obj.orientation,
                     obj.taille, obj.poids))
            elif table == 'Adversaire':
                cursor.execute('''
                INSERT OR REPLACE INTO Adversaire 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (obj.id, obj.pseudo, obj.hp, obj.hp_total, obj.mana, obj.mana_total,
                     obj.force, obj.defense, obj.magie, obj.resistance, obj.agilite,
                     obj.niveau, obj.experience))

def charger_donnees(table, classe):
    """
    Charge les données d'une table et crée les objets correspondants
    
    Args:
        table (str): Nom de la table ('Personnage', 'Adversaire' ou 'Item')
        classe (class): Classe à utiliser pour créer les objets
    
    Returns:
        list: Liste des objets créés
    """
    objets = []
    with DatabaseConnection() as cursor:
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        
        for row in rows:
            if table == 'Personnage':
                obj = classe(
                    id=row[0], pseudo=row[1], hp=row[2], hp_total=row[3],
                    mana=row[4], mana_total=row[5], force=row[6], defense=row[7],
                    magie=row[8], resistance=row[9], agilite=row[10], niveau=row[11],
                    points_de_stats=row[12], experience=row[13], race_id=row[14],
                    classe_id=row[15], sexe=row[16], alignement=row[17],
                    orientation=row[18], taille=row[19], poids=row[20]
                )
            elif table == 'Adversaire':
                obj = classe(
                    id=row[0], pseudo=row[1], hp=row[2], hp_total=row[3],
                    mana=row[4], mana_total=row[5], force=row[6], defense=row[7],
                    magie=row[8], resistance=row[9], agilite=row[10], niveau=row[11],
                    experience=row[12]
                )
            elif table == 'Item':
                # Récupérer la quantité depuis l'inventaire
                cursor.execute('SELECT quantity FROM inventaire WHERE item_id = ?', (row[0],))
                quantite_row = cursor.fetchone()
                quantite = quantite_row[0] if quantite_row else 0
                
                obj = classe(
                    id_item=row[0],
                    nom=row[1],
                    code_item=row[2],
                    categorie=row[3],
                    description=row[4],
                    valeur=row[5],
                    bonus_hp=row[6],
                    bonus_mp=row[7],
                    bonus_force=row[8],
                    bonus_defense=row[9],
                    bonus_magie=row[10],
                    bonus_resistance=row[11],
                    bonus_agilite=row[12],
                    est_equipable=bool(row[13]),
                    est_consommable=bool(row[14]),
                    est_empilable=bool(row[15]),
                    pile_max=row[16],
                    quantite=quantite
                )
            else:
                raise ValueError(f"Table inconnue: {table}")
                
            objets.append(obj)
    return objets

def initialiser_base_de_donnees():
    """Crée et initialise la base de données avec toutes les tables et données nécessaires"""
    # Import déplacé ici pour éviter l'importation circulaire
    from .RacesJoueur_manager import DatabaseManager as RacesManager
    from .ClasseJoueur_manager import ClassesManager
    
    with DatabaseManager() as cursor:
        # Création de la table races
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race_code TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            hp INTEGER,
            mp INTEGER,
            force INTEGER,
            defense INTEGER,
            magie INTEGER,
            resistance INTEGER,
            agilite INTEGER
        )
        ''')
    
        # Création de la table Personnage
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Personnage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
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
            experience INTEGER,
            race_id INTEGER,
            classe_id INTEGER,
            sexe TEXT,
            alignement TEXT,
            orientation TEXT,
            taille REAL,
            poids REAL,
            FOREIGN KEY (race_id) REFERENCES races(race_id),
            FOREIGN KEY (classe_id) REFERENCES classes(class_id)
        )
        ''')
    
        # Création de la table Adversaire
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Adversaire (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
        # Création de la table classes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_code TEXT UNIQUE,
            category TEXT,
            description TEXT,
            hp INTEGER,
            mp INTEGER,
            force INTEGER,
            defense INTEGER,
            magie INTEGER,
            resistance INTEGER,
            agilite INTEGER
        )
        ''')

        # Création de la table Item
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Item (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            item_code VARCHAR(10) UNIQUE NOT NULL,
            category VARCHAR(50) NOT NULL,
            description TEXT,
            value INTEGER DEFAULT 0,
            hp_bonus INTEGER DEFAULT 0,
            mp_bonus INTEGER DEFAULT 0,
            force_bonus INTEGER DEFAULT 0,
            defense_bonus INTEGER DEFAULT 0,
            magie_bonus INTEGER DEFAULT 0,
            resistance_bonus INTEGER DEFAULT 0,
            agilite_bonus INTEGER DEFAULT 0,
            is_equipable BOOLEAN DEFAULT 0,
            is_consumable BOOLEAN DEFAULT 0,
            is_stackable BOOLEAN DEFAULT 0,
            max_stack INTEGER DEFAULT 1
        )
        ''')

        # Création de la table inventaire
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventaire (
            inventaire_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            quantity INTEGER DEFAULT 1,
            is_equipped BOOLEAN DEFAULT 0,
            FOREIGN KEY (item_id) REFERENCES Item(item_id)
        )
        ''')

        # Initialisation des données des races et des classes
        races_manager = RacesManager()
        races_manager.connect()
        races_manager.create_tables()
        races_manager.initialize_data()
        races_manager.disconnect()
        
        classes_manager = ClassesManager()
        classes_manager.connect()
        classes_manager.create_tables()
        classes_manager.initialize_data()
        classes_manager.disconnect()

        # Initialisation des items de base
        cursor.execute('SELECT COUNT(*) FROM items')
        if cursor.fetchone()[0] == 0:
            items_base = [
                # Armes
                ('Épée courte', 'EPE_CRT', 'Armes', 'Une épée courte basique', 
                 50, 2.0, 0, 0, 5, 0, 0, 0, 2, 1, 0, 0, 1),
                ('Bâton', 'BAT', 'Armes', 'Un bâton de combat basique',
                 30, 1.5, 0, 5, 2, 0, 5, 0, 0, 1, 0, 0, 1),
                
                # Armures
                ('Armure en cuir', 'ARM_CUI', 'Armures', 'Une armure légère en cuir',
                 80, 5.0, 5, 0, 0, 5, 0, 2, 1, 1, 0, 0, 1),
                
                # Consommables
                ('Potion de vie', 'POT_VIE', 'Consommables', 'Restaure 50 points de vie',
                 25, 0.2, 50, 0, 0, 0, 0, 0, 0, 0, 1, 1, 10),
                ('Potion de mana', 'POT_MAN', 'Consommables', 'Restaure 50 points de mana',
                 25, 0.2, 0, 50, 0, 0, 0, 0, 0, 0, 1, 1, 10)
            ]

            cursor.executemany('''
                INSERT INTO Item (
                    name, item_code, category, description, value, hp_bonus,
                    mp_bonus, force_bonus, defense_bonus,
                    magie_bonus, resistance_bonus, agilite_bonus,
                    is_equipable, is_consumable, is_stackable, max_stack
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', items_base)
