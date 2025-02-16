# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 18:51:22 2022

@author: user
"""
from src.core.equipe_joueur import *
from src.core.equipe_adverse import *
from src.core.personnage import *
from src.core.adversaire import *
from src.core.ressources import *
from src.combat.combat import *
from src.database.bddmanager import *

class Personnage:
    def __init__(self, pseudo, hp, attaque):
        self.pseudo = pseudo
        self.hp = hp
        self.attaque = attaque
        self.degats_infliges = 0  # Initialize damage counter

    def dommage(self, ennemi_attaque):
        self.hp = max(0, self.hp - ennemi_attaque)  # Ensure HP does not go below 0
        print(self.pseudo, "perd", ennemi_attaque, "HP.")
        print("Il lui reste donc", self.hp, "HP")
        if self.hp > 0:
            print("Il lui reste", self.hp, "HP")
        else:
            print(self.pseudo, "est mort")

    def attaquer(self, cible):
        cible.dommage(self.attaque)
        self.degats_infliges += self.attaque  # Update damage counter


"""

PV DE PEDRO LE SINGE : 225 000
attaque Pedro le singe : 20 000

"""


merlin = Personnage("Merlin cliché",50,20)
artxis = Personnage ("Artxis le troll de skyrim avec la montagne des Grisebarbes",200,5 )
pedro_le_singe = Personnage ("Pedro",225000,20000)
conan_guerrier = Personnage("Conan",100,10,)


def afficher_combattants(combattants):
    for idx, combattant in enumerate(combattants, start=1):
        print(f"{idx}. {combattant.pseudo} - HP: {combattant.hp}, Attaque: {combattant.attaque}")

def selectionner_equipe(combattants, equipe_num):
    print(f"Sélectionnez l'équipe {equipe_num} :")
    afficher_combattants(combattants)
    selection = input("Sélectionnez les personnages pour l'équipe (entrez les numéros séparés par des espaces): ").split()
    equipe = []
    for i in selection:
        combattant = combattants[int(i)-1]
        clone_pseudo = combattant.pseudo
        clone_count = 0
        while any(clone_pseudo in c.pseudo for c in equipe):
            clone_count += 1
            clone_pseudo = f"Clône de {combattant.pseudo}" if clone_count == 1 else f"Clône de {'Clône de ' * (clone_count - 1)}{combattant.pseudo}"
        clone_pseudo += f" (équipe {equipe_num})"
        clone = Personnage(clone_pseudo, combattant.hp, combattant.attaque)
        equipe.append(clone)
    return equipe

def afficher_stats_equipe(equipe):
    hp_total = 0
    degats_totaux = 0
    combattants_vivants = []

    for combattant in equipe:
        if combattant.hp > 0:
            hp_total += combattant.hp
            degats_totaux += combattant.degats_infliges
            combattants_vivants.append(combattant.pseudo)

    print(f"L'équipe victorieuse a {hp_total} HP restants.")
    print(f"Dégâts totaux infligés par l'équipe victorieuse : {degats_totaux}")
    print(f"Combattants encore en vie : {', '.join(combattants_vivants)}")


# List of all available combatants
tous_combattants = [conan_guerrier, artxis, merlin, pedro_le_singe]

# Select teams
equipe1 = selectionner_equipe(tous_combattants, 1)
equipe2 = selectionner_equipe(tous_combattants, 2)

# Combine both teams into one list for the combat loop
liste_combattant = equipe1 + equipe2
"""
while merlin.hp > 0 or artxis.hp > 0 or conan_guerrier.hp > 0:
    merlin.dommage(conan_guerrier.attaque)
    merlin.dommage(artxis.attaque)
    conan_guerrier.dommage(merlin.attaque)
    conan_guerrier.dommage(artxis.attaque)  
    artxis.dommage(conan_guerrier.attaque)
    artxis.dommage(merlin.attaque)
    print(conan_guerrier.attaque)
"""

# Combat loop
while True:
    compteur_en_vie_equipe1 = sum(1 for combattant in equipe1 if combattant.hp > 0)
    compteur_en_vie_equipe2 = sum(1 for combattant in equipe2 if combattant.hp > 0)

    if compteur_en_vie_equipe1 == 0:
        print("L'équipe 2 a gagné!")
        afficher_stats_equipe(equipe2)
        break
    elif compteur_en_vie_equipe2 == 0:
        print("L'équipe 1 a gagné!")
        afficher_stats_equipe(equipe1)
        break

    for i in range(len(liste_combattant)):
        if liste_combattant[i].hp > 0:
            print("C'est le tour de", liste_combattant[i].pseudo)

            # Determine the opponent team
            if liste_combattant[i] in equipe1:
                valid_targets = [j for j in range(len(liste_combattant)) if liste_combattant[j] in equipe2 and liste_combattant[j].hp > 0]
            else:
                valid_targets = [j for j in range(len(liste_combattant)) if liste_combattant[j] in equipe1 and liste_combattant[j].hp > 0]

            if not valid_targets:
                print("Aucun adversaire vivant. Passez votre tour.")
                continue

            print("Tapez le numéro correspondant à la cible :")
            for idx, target in enumerate(valid_targets, start=1):
                print(f"{idx} pour attaquer {liste_combattant[target].pseudo}")

            try:
                aa = int(input("Cible : ")) - 1
                if 0 <= aa < len(valid_targets):
                    liste_combattant[i].attaquer(liste_combattant[valid_targets[aa]])
                else:
                    print("Choix invalide. Passez votre tour.")
            except ValueError:
                print("Entrée invalide. Passez votre tour.")