import sqlite3
import os
from typing import Dict, List, Optional

class ClassesManager:
    def __init__(self, db_name: str = "class.db"):
        """Initialise la connexion à la base de données"""
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        os.makedirs(data_dir, exist_ok=True)
        
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
        """Crée la table des classes"""
        # Supprime la table si elle existe
        self.cursor.execute('DROP TABLE IF EXISTS classes')
        
        # Crée la nouvelle table
        self.cursor.execute('''
            CREATE TABLE classes (
                class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                class_code VARCHAR(10) UNIQUE NOT NULL,
                category VARCHAR(50) NOT NULL,  -- 'Physiques', 'Mages', 'Alterations', 'Equilibré'
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
        classes = [
            # Physiques
            ('Guerrier', 'GUE', 'Physiques', 'Combattant polivalent pouvant se défendre et attaquer', 15, 0, 5, 3, 0, 2, 0),
            ('Berserker', 'BER', 'Physiques', 'Guerrier se concentrant sur l\'attaque avec une grande violence', 5, 0, 15, 0, 0, 0, 5),
            ('Chevalier', 'CHE', 'Physiques', 'Combattant se préoccupant de la protection de ses alliés avec une forte défense', 5, 0, 5, 15, 0, 0, 0),
            # Mages
            ('Sorcier', 'SOR', 'Mages', 'Mage polyvalent pouvant aussi bien se défendre et attaquer', 0, 5, 0, 5, 10, 5, 0),
            ('Mage noir', 'MGN', 'Mages', 'Spécialiste de la magie offensive avec des sorts destructeurs', 0, 5, 2, 2, 15, 0, 0),
            ('Enchanteur', 'ENC', 'Mages', 'Mage défensif se concentrant sur la protection de ses alliés avec une forte résistance', 0, 5, 0, 7, 5, 5, 0),


            # Alterations
            ('Alchimiste', 'ALC', 'Alterations', 'Manie des potions afin d\'améliorer ses statistiques sur une courte durée. Seule classe pouvant se spécialiser dans l\'invocation', 5, 10, 0, 5, 0, 5, 0),
            ('Voleur', 'VOL', 'Alterations', 'Combattant se concentrant sur son agilité avec de multiples attaques destiné à ignorer la défense et résistance de l\'adversaire', 2, 0, 2, 1, 0, 5, 15),
            ('Mage Blanc', 'MGB', 'Mages', 'Mage soutenant son équipe grâce à divers sort de soutiens', 0, 5, 0, 0, 5, 15, 0),


            # Equilibré
            ('Equilibré', 'EQU', 'Equilibré', 'Capable d\'un peu tout faire. Jack of all trades master of nothing', 0, 5, 5, 5, 5, 5, 0)
        ]
        
        self.cursor.executemany('''
            INSERT INTO classes 
            (name, class_code, category, description, hp, mp, force, defense, magie, resistance, agilite)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', classes)
        self.conn.commit()

    def get_all_classes(self) -> List[Dict]:
        """Récupère toutes les classes avec leurs statistiques"""
        self.cursor.execute('SELECT * FROM classes')
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_class_by_code(self, class_code: str) -> Optional[Dict]:
        """Récupère une classe par son code"""
        self.cursor.execute('SELECT * FROM classes WHERE class_code = ?', (class_code,))
        columns = [description[0] for description in self.cursor.description]
        row = self.cursor.fetchone()
        return dict(zip(columns, row)) if row else None

    def get_classes_by_category(self, category: str) -> List[Dict]:
        """Récupère toutes les classes d'une catégorie"""
        self.cursor.execute('SELECT * FROM classes WHERE category = ?', (category,))
        columns = [description[0] for description in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

# Exemple d'utilisation
if __name__ == "__main__":
    db = ClassesManager()
    db.connect()
    
    # Création des tables et initialisation des données
    db.create_tables()
    db.initialize_data()
    
    print("\nToutes les classes par catégorie:")
    for category in ['Physiques', 'Mages', 'Alterations', 'Equilibré']:
        print(f"\n=== {category} ===")
        classes = db.get_classes_by_category(category)
        for classe in classes:
            print(f"\n{classe['name']} ({classe['class_code']}) - {classe['description']}")
            stats = []
            if classe['hp']: stats.append(f"HP: {classe['hp']}")
            if classe['mp']: stats.append(f"MP: {classe['mp']}")
            if classe['force']: stats.append(f"Force: {classe['force']}")
            if classe['defense']: stats.append(f"Défense: {classe['defense']}")
            if classe['magie']: stats.append(f"Magie: {classe['magie']}")
            if classe['resistance']: stats.append(f"Résistance: {classe['resistance']}")
            if classe['agilite']: stats.append(f"Agilité: {classe['agilite']}")
            print(", ".join(stats))
    
    db.disconnect()    