from src.core.adversaire import *
from src.core.ressources import *
from src.database.bddmanager import *

class EquipeAdverse:
    def __init__(self):
        self.personnages = []  # Liste des Adversaires dans l'équipe

    def ajouter_adversaire(self, adversaire):
        """Ajoute un Adversaire à l'équipe"""
        self.personnages.append(adversaire)
        adversaire.equipe_adverse = self  # Associer l'équipe à chaque Adversaire

    def attaquer(self, cible, degats):
        """Méthode d'attaque qui applique les dégâts à l'Adversaire"""
        cible.subir_attaque(degats)

    def __iter__(self):  # Crée un itérateur pour permettre une itération sur l'équipe adverse
        return iter(self.personnages)

    def afficher_fiche(self):
        """Affiche les informations de tous les Adversaires de l'équipe"""
        print("Informations de l'équipe adverse:")
        for adversaire in self.personnages:
            print(f"\nNom: {adversaire.pseudo}")
            print(f"HP: {adversaire.hp}")
            print(f"Attaque: {adversaire.attaque}")
            print(f"Niveaux: {adversaire.niveau}")
            print(f"Mana: {adversaire.mana}")
            print(f"Expérience: {adversaire.experience}")
