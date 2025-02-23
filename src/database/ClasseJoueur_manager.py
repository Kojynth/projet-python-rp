import sqlite3
import os
from typing import Dict, List, Optional
from src.database.connexion import DatabaseConnection

class ClassesManager:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def create_tables(self):
        """Crée la table des classes"""
        with self.db_connection as cursor:
            # On supprime d'abord la table existante
            cursor.execute('DROP TABLE IF EXISTS classes')
            
            # Puis on la recrée avec la nouvelle structure
            cursor.execute('''
            CREATE TABLE classes (
                class_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                class_code VARCHAR(10) UNIQUE NOT NULL,
                category VARCHAR(50) NOT NULL,
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

    def initialize_data(self):
        """Initialise les données de base des classes"""
        classes_data = [
            # Physiques
            {
                'name': 'Guerrier',
                'class_code': 'GUE',
                'category': 'Physiques',
                'description': 'Combattant polivalent pouvant se défendre et attaquer',
                'hp': 15, 'mp': 0, 'force': 5, 'defense': 3,
                'magie': 0, 'resistance': 2, 'agilite': 0
            },
            {
                'name': 'Berserker',
                'class_code': 'BER',
                'category': 'Physiques',
                'description': 'Guerrier se concentrant sur l\'attaque avec une grande violence',
                'hp': 5, 'mp': 0, 'force': 15, 'defense': 0,
                'magie': 0, 'resistance': 0, 'agilite': 5
            },
            {
                'name': 'Chevalier',
                'class_code': 'CHE',
                'category': 'Physiques',
                'description': 'Combattant se préoccupant de la protection de ses alliés avec une forte défense',
                'hp': 5, 'mp': 0, 'force': 5, 'defense': 15,
                'magie': 0, 'resistance': 0, 'agilite': 0
            },
            # Mages
            {
                'name': 'Sorcier',
                'class_code': 'SOR',
                'category': 'Mages',
                'description': 'Mage polyvalent pouvant aussi bien se défendre et attaquer',
                'hp': 0, 'mp': 5, 'force': 0, 'defense': 5,
                'magie': 10, 'resistance': 5, 'agilite': 0
            },
            {
                'name': 'Mage noir',
                'class_code': 'MGN',
                'category': 'Mages',
                'description': 'Spécialiste de la magie offensive avec des sorts destructeurs',
                'hp': 0, 'mp': 5, 'force': 2, 'defense': 2,
                'magie': 15, 'resistance': 0, 'agilite': 0
            },
            {
                'name': 'Enchanteur',
                'class_code': 'ENC',
                'category': 'Mages',
                'description': 'Mage défensif se concentrant sur la protection de ses alliés avec une forte résistance',
                'hp': 0, 'mp': 5, 'force': 0, 'defense': 7,
                'magie': 5, 'resistance': 5, 'agilite': 0
            },
            # Alterations
            {
                'name': 'Alchimiste',
                'class_code': 'ALC',
                'category': 'Alterations',
                'description': 'Manie des potions afin d\'améliorer ses statistiques sur une courte durée. Seule classe pouvant se spécialiser dans l\'invocation',
                'hp': 5, 'mp': 10, 'force': 0, 'defense': 5,
                'magie': 0, 'resistance': 5, 'agilite': 0
            },
            {
                'name': 'Voleur',
                'class_code': 'VOL',
                'category': 'Alterations',
                'description': 'Combattant se concentrant sur son agilité avec de multiples attaques et altérations destiné à ignorer la défense et résistance de l\'adversaire',
                'hp': 2, 'mp': 0, 'force': 2, 'defense': 1,
                'magie': 0, 'resistance': 5, 'agilite': 15
            },
            {
                'name': 'Mage Blanc',
                'class_code': 'MGB',
                'category': 'Alterations',
                'description': 'Mage soutenant son équipe grâce à divers sort de soutiens',
                'hp': 0, 'mp': 5, 'force': 0, 'defense': 0,
                'magie': 5, 'resistance': 15, 'agilite': 0
            },
            # Equilibré
            {
                'name': 'Equilibré',
                'class_code': 'EQU',
                'category': 'Equilibré',
                'description': 'Capable d\'un peu tout faire. Jack of all trades master of nothing',
                'hp': 0, 'mp': 5, 'force': 5, 'defense': 5,
                'magie': 5, 'resistance': 5, 'agilite': 0
            }
        ]

        with self.db_connection as cursor:
            for classe in classes_data:
                cursor.execute('''
                INSERT OR IGNORE INTO classes 
                (name, class_code, category, description, hp, mp, force, defense, magie, resistance, agilite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    classe['name'], classe['class_code'], classe['category'], 
                    classe['description'], classe['hp'], classe['mp'], 
                    classe['force'], classe['defense'], classe['magie'], 
                    classe['resistance'], classe['agilite']
                ))

    def get_all_classes(self):
        """Récupère toutes les classes"""
        with self.db_connection as cursor:
            cursor.execute('SELECT * FROM classes')
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_class_by_id(self, class_id):
        """Récupère une classe par son ID"""
        with self.db_connection as cursor:
            cursor.execute('SELECT * FROM classes WHERE class_id = ?', (class_id,))
            row = cursor.fetchone()
            if row:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
            return None

    def get_class_by_code(self, class_code: str) -> Optional[Dict]:
        """Récupère une classe par son code"""
        with self.db_connection as cursor:
            cursor.execute('SELECT * FROM classes WHERE class_code = ?', (class_code,))
            columns = [description[0] for description in cursor.description]
            row = cursor.fetchone()
            return dict(zip(columns, row)) if row else None

    def get_classes_by_category(self, category: str) -> List[Dict]:
        """Récupère toutes les classes d'une catégorie"""
        with self.db_connection as cursor:
            cursor.execute('SELECT * FROM classes WHERE category = ?', (category,))
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def create_table(self):
        """Crée la table des classes si elle n'existe pas"""
        with self.db_connection as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                taille INTEGER CHECK (taille >= 20 AND taille <= 500),
                poids INTEGER CHECK (poids >= 20 AND poids <= 1000)
            )
            """)

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