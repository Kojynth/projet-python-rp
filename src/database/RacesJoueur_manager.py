import sqlite3
import os
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_name: str = "raceJoueur.db"):
        """Initialise la connexion à la base de données"""
        # Créer le dossier data s'il n'existe pas
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        # Définir le chemin complet de la base de données
        self.db_path = os.path.join(data_dir, db_name)
        self.conn = None
        self.cursor = None

    def connect(self):
        """Établit la connexion à la base de données"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()

    def create_tables(self):
        """Crée la table des races"""
        # Supprime la table si elle existe
        self.cursor.execute('DROP TABLE IF EXISTS races')
        
        # Crée la nouvelle table
        self.cursor.execute('''
            CREATE TABLE races (
                race_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                race_code VARCHAR(10) UNIQUE NOT NULL,
                category VARCHAR(50) NOT NULL,  -- 'Nocturne' ou 'Non-Nocturne'
                description TEXT,
                hp INTEGER DEFAULT 0,
                mp INTEGER DEFAULT 0,
                force INTEGER DEFAULT 0,
                defense INTEGER DEFAULT 0,
                magie INTEGER DEFAULT 0,
                resistance INTEGER DEFAULT 0,
                agilite INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def initialize_data(self):
        """Initialise les données de base"""
        races = [
            # Non-Nocturnes
            ('Humain', 'HUM', 'Non-Nocturne', 'Race présente un peu partout dans le monde surtout à Médonia, il existe diverses factions d\'humains luttant pour le pouvoir et le contrôle.', 
             20, 20, 12, 12, 12, 12, 12),
            ('Elfe', 'ELF', 'Non-Nocturne', 'Race peu présente à Médonia. Ils se trouvent dans de lointaines régions notamment dans les forêts L\'on dit qu\'une forte population d\'elfes vit dans les forêts de Sylster', 
             15, 25, 10, 8, 15, 15, 15),
            ('Nain', 'NAI', 'Non-Nocturne', 'Race robuste spécialisée très présent dans les montagnes du nord du Rochefort. Ils subissent de nombreuses représailles de la part de l\'Empire dersien qui a récemment asservit la ville de Nérys. Il existe aujourd\'hui une forte diaspora naine au sein de Prospit', 
             30, 5, 25, 25, 5, 5, 5),
            ('Argoniens', 'ARG', 'Non-Nocturne', 'Race reptilienne dont la catégorisation est régulièrement soumis à divers débats parmi les raciologues pour déterminer leur classification Loup-Garou ou non. Ils sont très présents dans des régions marécageuses ou proche de points d\'eau. Ils sont peu présent à Médonia et préfèrent rester dans des régions éloignées tel que les Marais de Solz\'Ômm.', 
             20, 10, 15, 15, 5, 10, 25),
            # Nocturnes
            ('Vampire', 'VAM', 'Nocturne', 'Créature dont l\'origine est méconnu. A toujours existé tout au long de l\'histoire. Il est dit qu\ils étaient d\'ancien humains ayant sombré face à une malédiction mais nous ignorons si cela est vrai ou non.', 
             20, 20, 12, 12, 12, 12, 12),
            ('Loup-Garou', 'LOU', 'Nocturne', 'Créature avec des traits d\'animaux sans écailles ne rappelant pas forcément un canidé. Les kemonomimi, les kitsunes et autres créatures bipèdes avec des traits animaux sont dénommé comme des loups-garous.', 
             15, 10, 25, 15, 5, 25, 25),
            ('Youkai', 'YOU', 'Nocturne', 'Esprit la plupart du temps l\'esprit d\'un défunt n\'ayant pas trouvé la paix.', 
             10, 25, 5, 5, 25, 25, 5),
            ('Squelette', 'SQU', 'Nocturne', 'Mort-vivant squelettique souvent le fruit et victime de la magie d\'un nécromancien.', 
             10, 30, 5, 5, 20, 20, 10)
        ]
        self.cursor.executemany('''
            INSERT INTO races 
            (name, race_code, category, description, hp, mp, force, defense, magie, resistance, agilite)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', races)
        self.conn.commit()

    def get_all_races(self) -> List[Dict]:
        """Récupère toutes les races avec leurs statistiques"""
        self.cursor.execute('SELECT * FROM races')
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_race_by_code(self, race_code: str) -> Optional[Dict]:
        """Récupère une race par son code"""
        self.cursor.execute('SELECT * FROM races WHERE race_code = ?', (race_code,))
        columns = [description[0] for description in self.cursor.description]
        row = self.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def get_races_by_category(self, category: str) -> List[Dict]:
        """Récupère toutes les races d'une catégorie"""
        self.cursor.execute('SELECT * FROM races WHERE category = ?', (category,))
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

# Exemple d'utilisation
if __name__ == "__main__":
    db = DatabaseManager()
    db.connect()
    
    # Création des tables et initialisation des données
    db.create_tables()
    db.initialize_data()
    
    print("\nToutes les races par catégorie:")
    for category in ['Non-Nocturne', 'Nocturne']:
        print(f"\n=== {category} ===")
        races = db.get_races_by_category(category)
        for race in races:
            print(f"\n{race['name']} ({race['race_code']}) - {race['description']}")
            stats = []
            if race['hp']: stats.append(f"HP: {race['hp']}")
            if race['mp']: stats.append(f"MP: {race['mp']}")
            if race['force']: stats.append(f"Force: {race['force']}")
            if race['defense']: stats.append(f"Défense: {race['defense']}")
            if race['magie']: stats.append(f"Magie: {race['magie']}")
            if race['resistance']: stats.append(f"Résistance: {race['resistance']}")
            if race['agilite']: stats.append(f"Agilité: {race['agilite']}")
            print(", ".join(stats))
    
    db.disconnect()
