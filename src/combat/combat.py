from src.core.equipe_joueur import *
from src.core.personnage import *
from src.core.adversaire import *
from src.core.ressources import *
from src.combat.actions_combat import *
from src.items.item import charger_items
from src.combat.menu_combat import menu_combat

# Fonction principale pour la boucle de combat
def afficher_etat_equipes(equipe1, equipe2, numero_tour):
    """Affiche l'état actuel des deux équipes"""
    print(f"\n=== Tour {numero_tour} ===")
    print("=== État des équipes ===")
    print("Votre équipe :")
    for perso in equipe1:
        print(f"- {perso.pseudo}: HP {perso.hp}/{perso.hp_total}, Mana {perso.mana}/{perso.mana_total}")
    print("\nÉquipe adverse :")
    for adv in equipe2:
        print(f"- {adv.pseudo}: HP {adv.hp}/{adv.hp_total}, Mana {adv.mana}/{adv.mana_total}")
    print("=====================\n")

def boucle_combat(liste_combattant, equipe1, equipe2):
    """
    Boucle de combat entre deux équipes.

    La fonction prend en argument une liste de combattants, deux équipes (une équipe de personnages et une équipe d'adversaires)
    et lance une boucle de combat.

    La boucle de combat fonctionne comme suit :
    - À chaque tour, chaque combattant vivant attaque un adversaire aléatoire.
    - Les dégâts sont déterminés en fonction de l'attaque et de la défense du combattant et de la cible.
    - Les dégâts sont appliqués à la cible.
    - Les combattants qui ont perdu tous leurs points de vie sont éliminés.
    - La boucle de combat s'arrête lorsque tous les combattants d'une équipe ont été éliminés.
    - L'équipe qui a gagné est affichée.

    La fonction sauvegarde les combattants de l'équipe gagnante avant de s'arrêter.
    """
    numero_tour = 1  # Initialisation du compteur de tour
    
    while True:
        print(f"\n=== Début du tour {numero_tour} ===")
        
        # Compter le nombre de combattants vivants dans chaque équipe
        compteur_en_vie_equipe1 = sum(1 for combattant in equipe1 if combattant.hp > 0)
        compteur_en_vie_equipe2 = sum(1 for combattant in equipe2 if combattant.hp > 0)

        # Vérifier si une équipe a été éliminée
        if compteur_en_vie_equipe1 == 0:
            print(f"\nCombat terminé au tour {numero_tour}")
            print("Vos ennemis ont gagné!")
            afficher_stats_equipe(equipe2)
            sauvegarder_personnages(equipe1)
            sauvegarder_adversaires(equipe2)
            break
        elif compteur_en_vie_equipe2 == 0:
            print(f"\nCombat terminé au tour {numero_tour}")
            print("L'équipe 1 a gagné!")
            afficher_stats_equipe(equipe1)
            sauvegarder_personnages(equipe1)
            break

        # Boucle sur chaque combattant vivant
        for combattant in liste_combattant:
            if combattant.hp > 0:
                # Afficher l'état des équipes au début de chaque tour
                afficher_etat_equipes(equipe1, equipe2, numero_tour)
                
                print("\nC'est le tour de", combattant.pseudo)
                
                if isinstance(combattant, Personnage):
                    resultat = menu_combat(combattant, equipe1, equipe2)
                    if resultat == "fuite":
                        liste_combattant.remove(combattant)
                        if combattant in equipe1:
                            equipe1.remove(combattant)
                        else:
                            equipe2.remove(combattant)
                        if tous_vaincus(equipe1) or tous_vaincus(equipe2):
                            return
                else:
                    # Logique pour les adversaires (IA)
                    if combattant in equipe1:
                        cibles_valides = [c for c in equipe2 if c.hp > 0]
                    else:
                        cibles_valides = [c for c in equipe1 if c.hp > 0]

                    if cibles_valides:
                        cible = max(cibles_valides, key=lambda c: calculer_degats(combattant, c, "physique", 0))
                        attaquer(combattant, cible, equipe1, equipe2)

                # Sauvegarder après chaque action
                sauvegarder_personnages(equipe1)
                sauvegarder_adversaires(equipe2)
        
        # Incrémenter le compteur de tour à la fin de chaque tour complet
        numero_tour += 1
        print(f"\n=== Fin du tour {numero_tour-1} ===")

# Fonction pour vérifier si tous les membres d'une équipe sont vaincus
def tous_vaincus(equipe):
    return all(combattant.hp <= 0 for combattant in equipe)

# Fonction pour choisir une cible
def choisir_cible(combattant, equipe1, equipe2):
    if combattant in equipe1:
        return equipe2[0]
    else:
        return equipe1[0]
