import random
from src.database.bddmanager import sauvegarder_objets, charger_donnees
from src.core.ressources import *
from src.core.personnage import Personnage


class Adversaire:
    def __init__(self, id, pseudo, hp, hp_total, mana, mana_total, force, defense, magie, resistance, agilite, niveau, experience):
        self.id = id
        self.pseudo = pseudo
        self.hp = hp
        self.hp_total = hp_total
        self.mana = mana
        self.mana_total = mana_total
        self.force = force
        self.defense = defense
        self.magie = magie
        self.resistance = resistance
        self.agilite = agilite
        self.niveau = niveau
        self.experience = experience

    def subir_attaque(self, degats):
        self.hp = max(0, self.hp - degats)
        print(f"{self.pseudo} subit {degats} de dégâts. Il lui reste {self.hp} HP.")

        # Vérifier si l'adversaire est mort
        if self.hp <= 0:
            self.mourir()

    def mourir(self):
        """Méthode qui gère la mort de l'adversaire et déclenche un gain d'expérience pour l'équipe adverse"""
        print(f"{self.pseudo} est mort !")
        self.gagner_experience_adversaire()

    def gagner_experience_adversaire(self):
        """Attribution de l'XP pour toute l'équipe adverse au moment de la mort d'un adversaire"""
        print(f"{self.pseudo} déclenche un gain d'expérience pour l'équipe adverse.")
        if hasattr(self, 'equipe_adverse'):
            # Attribution de l'XP personnalisée par le développeur, ici on utilise l'expérience définie dans le constructeur
            xp_a_gagner = self.experience  # Utilisation de l'XP propre à chaque adversaire
            self.equipe_adverse.gagner_experience(xp_a_gagner)  # Attribution de l'XP à toute l'équipe

    def reinitialiser_stats(self):
        """Méthode pour réinitialiser les stats de l'adversaire après le combat"""
        self.hp = self.hp_total
        self.mana = self.mana_total
        self.experience = 0
        self.points_de_stats = 0

# Fonction pour ajouter des adversaires à la base de données
def ajouter_adversaires(adversaires):
    sauvegarder_objets('Adversaire', adversaires)

# Fonction pour sauvegarder les adversaires dans la base de données
def sauvegarder_adversaires(adversaires):
    sauvegarder_objets('Adversaire', adversaires)