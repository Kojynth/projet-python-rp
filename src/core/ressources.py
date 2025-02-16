# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:31:48 2024

@author: dsmic
"""
# personnage.py

import random
import time
import os
import sys
from colorama import init, Fore, Back, Style
init()

class Personnage:
    def __init__(self, pseudo, hp, attaque, niveau=1, mana=100):
        self.pseudo = pseudo
        self.hp = hp
        self.attaque = attaque
        self.niveau = niveau
        self.degats_infliges = 0
        self.experience = 0
        self.mana = mana
        self.calculer_hp()

    def calculer_hp(self):
        hp_total = self.hp
        hp_gagnes = 0  # Réinitialiser le nombre de HP gagnés à chaque montée de niveau

        if self.niveau >= 2:
            hp_total += 75 * min(self.niveau - 1, 9)
        hp_par_niveau = 90
        if self.niveau >= 11:
            for i in range(11, self.niveau + 1):
                hp_total += hp_par_niveau
                if i % 10 == 0:
                    hp_par_niveau += 15

        # Calculer les HP gagnés à chaque montée de niveau
        hp_gagnes = hp_total - self.hp_precedent
        self.hp_gagnes_total += hp_gagnes

        self.hp = hp_total
        self.hp_precedent = hp_total  # Mettre à jour les HP précédents pour le prochain calcul

    def gagner_experience(self, quantite):
        self.experience += quantite
        print(f"{self.pseudo} gagne {quantite} points d'expérience.")
        while self.experience >= 10 * self.niveau:
            self.experience -= 10 * self.niveau
            self.niveau += 1
            print(f"{self.pseudo} passe au niveau {self.niveau}!")
            self.calculer_hp()

    def afficher_fiche(self):
        xp_restant = (self.niveau + 1) * 10 - self.experience
        print(f"Nom: {self.pseudo}")
        print(f"HP: {self.hp}")
        print(f"Attaque: {self.attaque}")
        print(f"Niveau: {self.niveau}")
        print(f"Mana: {self.mana}")
        print(f"Expérience: {self.experience} ({xp_restant} XP restant avant le lvl up)")
        print(f"Dégâts infligés: {self.degats_infliges}")
        print(f"HP total gagnés depuis le dernier niveau: {self.hp_gagnes_total}")  # Affiche les HP gagnés depuis le dernier niveau

