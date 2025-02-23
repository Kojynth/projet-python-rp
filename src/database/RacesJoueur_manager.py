import sqlite3
import os
from typing import Dict, List, Optional
from src.database.connexion import DatabaseConnection

class RacesManager:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def create_tables(self):
        """Crée la table des races si elle n'existe pas"""
        with self.db_connection as cursor:
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

    def initialize_data(self):
        """Initialise les données de base des races"""
        races_data = [
            # Non-Nocturnes
            {
                'name': 'Humain',
                'race_code': 'HUM',
                'category': 'Non-Nocturne',
                'description': 'Race présente un peu partout dans le monde surtout à Médonia, il existe diverses factions d\'humains luttant pour le pouvoir et le contrôle.',
                'hp': 20,
                'mp': 20,
                'force': 12,
                'defense': 12,
                'magie': 12,
                'resistance': 12,
                'agilite': 12
            },
            {
                'name': 'Elfe',
                'race_code': 'ELF',
                'category': 'Non-Nocturne',
                'description': 'Race peu présente à Médonia. Ils se trouvent dans de lointaines régions notamment dans les forêts L\'on dit qu\'une forte population d\'elfes vit dans les forêts de Sylster',
                'hp': 15,
                'mp': 25,
                'force': 10,
                'defense': 8,
                'magie': 15,
                'resistance': 15,
                'agilite': 15
            },
            {
                'name': 'Nain',
                'race_code': 'NAI',
                'category': 'Non-Nocturne',
                'description': 'Race robuste spécialisée très présent dans les montagnes du nord du Rochefort. Ils subissent de nombreuses représailles de la part de l\'Empire dersien qui a récemment asservit la ville de Nérys. Il existe aujourd\'hui une forte diaspora naine au sein de Prospit',
                'hp': 30,
                'mp': 5,
                'force': 25,
                'defense': 25,
                'magie': 5,
                'resistance': 5,
                'agilite': 5
            },
            {
                'name': 'Argoniens',
                'race_code': 'ARG',
                'category': 'Non-Nocturne',
                'description': 'Race reptilienne dont la catégorisation est régulièrement soumis à divers débats parmi les raciologues pour déterminer leur classification Loup-Garou ou non. Ils sont très présents dans des régions marécageuses ou proche de points d\'eau. Ils sont peu présent à Médonia et préfèrent rester dans des régions éloignées tel que les Marais de Solz\'Ômm.',
                'hp': 20,
                'mp': 10,
                'force': 15,
                'defense': 15,
                'magie': 5,
                'resistance': 10,
                'agilite': 25
            },
            # Nocturnes
            {
                'name': 'Vampire',
                'race_code': 'VAM',
                'category': 'Nocturne',
                'description': 'Créature dont l\'origine est méconnu. A toujours existé tout au long de l\'histoire. Il est dit qu\ils étaient d\'ancien humains ayant sombré face à une malédiction mais nous ignorons si cela est vrai ou non.',
                'hp': 20,
                'mp': 20,
                'force': 12,
                'defense': 12,
                'magie': 12,
                'resistance': 12,
                'agilite': 12
            },
            {
                'name': 'Loup-Garou',
                'race_code': 'LOU',
                'category': 'Nocturne',
                'description': 'Créature avec des traits d\'animaux sans écailles ne rappelant pas forcément un canidé. Les kemonomimi, les kitsunes et autres créatures bipèdes avec des traits animaux sont dénommé comme des loups-garous.',
                'hp': 15,
                'mp': 10,
                'force': 25,
                'defense': 15,
                'magie': 5,
                'resistance': 25,
                'agilite': 25
            },
            {
                'name': 'Youkai',
                'race_code': 'YOU',
                'category': 'Nocturne',
                'description': 'Esprit la plupart du temps l\'esprit d\'un défunt n\'ayant pas trouvé la paix.',
                'hp': 10,
                'mp': 25,
                'force': 5,
                'defense': 5,
                'magie': 25,
                'resistance': 25,
                'agilite': 5
            },
            {
                'name': 'Squelette',
                'race_code': 'SQU',
                'category': 'Nocturne',
                'description': 'Mort-vivant squelettique souvent le fruit et victime de la magie d\'un nécromancien.',
                'hp': 10,
                'mp': 30,
                'force': 5,
                'defense': 5,
                'magie': 20,
                'resistance': 20,
                'agilite': 10
            }
        ]

        with self.db_connection as cursor:
            for race in races_data:
                cursor.execute('''
                INSERT OR IGNORE INTO races 
                (name, race_code, category, description, hp, mp, force, defense, magie, resistance, agilite)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    race['name'], race['race_code'], race['category'], race['description'],
                    race['hp'], race['mp'], race['force'], race['defense'],
                    race['magie'], race['resistance'], race['agilite']
                ))

    def get_all_races(self) -> List[Dict]:
        """Récupère toutes les races"""
        with self.db_connection as cursor:
            cursor.execute('SELECT * FROM races')
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_race_by_id(self, race_id: int) -> Optional[Dict]:
        """Récupère une race par son ID"""
        with self.db_connection as cursor:
            cursor.execute('SELECT * FROM races WHERE race_id = ?', (race_id,))
            row = cursor.fetchone()
            if row:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
            return None

    def get_races_by_category(self, category: str) -> List[Dict]:
        """Récupère toutes les races d'une catégorie donnée"""
        with self.db_connection as cursor:
            cursor.execute('SELECT * FROM races WHERE category = ?', (category,))
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
