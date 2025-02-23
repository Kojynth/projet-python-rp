import sqlite3
import os

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

def creer_base_de_donnees():
    """Crée la base de données et les tables nécessaires"""
    with DatabaseManager() as cursor:
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
    
        # Ajout de la table races
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race_code TEXT UNIQUE,
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

        # Création de la table items
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            item_code VARCHAR(10) UNIQUE NOT NULL,
            category VARCHAR(50) NOT NULL,
            description TEXT,
            value INTEGER DEFAULT 0,
            weight FLOAT DEFAULT 0,
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

        # Table d'inventaire pour lier les personnages aux items
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventaire (
            inventaire_id INTEGER PRIMARY KEY AUTOINCREMENT,
            personnage_id INTEGER,
            item_id INTEGER,
            quantity INTEGER DEFAULT 1,
            is_equipped BOOLEAN DEFAULT 0,
            FOREIGN KEY (personnage_id) REFERENCES Personnage(id),
            FOREIGN KEY (item_id) REFERENCES items(item_id)
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
    """Charge les données depuis la base de données"""
    with DatabaseManager() as cursor:
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        
        objets = []
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
                obj = classe(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                            row[7], row[8], row[9], row[10], row[11], row[12])
            objets.append(obj)
        return objets

def initialiser_base_de_donnees():
    """Crée et initialise la base de données avec toutes les tables et données nécessaires"""
    # Import déplacé ici pour éviter l'importation circulaire
    from .RacesJoueur_manager import DatabaseManager as RacesManager
    from .ClasseJoueur_manager import ClassesManager
    
    with DatabaseManager() as cursor:
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
    
        # Création de la table races
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS races (
            race_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race_code TEXT UNIQUE,
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

        # Création de la table items
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) NOT NULL,
            item_code VARCHAR(10) UNIQUE NOT NULL,
            category VARCHAR(50) NOT NULL,
            description TEXT,
            value INTEGER DEFAULT 0,
            weight FLOAT DEFAULT 0,
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
            personnage_id INTEGER,
            item_id INTEGER,
            quantity INTEGER DEFAULT 1,
            is_equipped BOOLEAN DEFAULT 0,
            FOREIGN KEY (personnage_id) REFERENCES Personnage(id),
            FOREIGN KEY (item_id) REFERENCES items(item_id)
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
                INSERT INTO items (
                    name, item_code, category, description, value, weight,
                    hp_bonus, mp_bonus, force_bonus, defense_bonus,
                    magie_bonus, resistance_bonus, agilite_bonus,
                    is_equipable, is_consumable, is_stackable, max_stack
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', items_base)
