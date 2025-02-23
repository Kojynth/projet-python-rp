"""Gestion de la connexion à la base de données"""
import sqlite3
import os

class DatabaseConnection:
    def __init__(self, db_name='jeu.db'):
        # Obtenir le chemin absolu vers le dossier data
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(project_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        self.db_path = os.path.join(data_dir, db_name)
        
        # Vérifier si la base de données existe déjà
        self.db_exists = os.path.exists(self.db_path)
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn.cursor()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    @property
    def exists(self):
        """Vérifie si la base de données existe déjà"""
        return self.db_exists

