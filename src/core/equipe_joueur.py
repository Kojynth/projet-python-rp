import sqlite3
from src.core.personnage import Personnage
from src.core.ressources import *
from src.database.bddmanager import *
from src.core.adversaire import Adversaire


def afficher_combattants(combattants):
    for idx, combattant in enumerate(combattants, start=1):
        print(f"{idx}. {combattant[1]} - HP: {combattant[2]}/{combattant[3]}, Mana: {combattant[4]}/{combattant[5]}, Attaque: {combattant[6]}")

def selectionner_equipe(equipe_num):


    with DatabaseManager() as db:
        # Sélectionner tous les combattants de la vue Combattants
        db.execute('SELECT id, pseudo, hp, hp_total, mana, mana_total, attaque, niveau, experience, points_de_stats, type FROM Combattants')
        combattants = db.fetchall()

    # Afficher les combattants disponibles
    print(f"Sélectionnez les membres de l'équipe {equipe_num} :")
    afficher_combattants(combattants)

    # Sélectionner les combattants pour l'équipe
    selection = input("Sélectionnez les combattants pour l'équipe (entrez les numéros séparés par des espaces): ").split()
    equipe = []

    for i in selection:
        combattant = combattants[int(i) - 1]
        clone_pseudo = combattant[1]
        clone_count = 0
        while any(clone_pseudo in c.pseudo for c in equipe):
            clone_count += 1
            clone_pseudo = f"Clône de {combattant[1]}" if clone_count == 1 else f"Clône de {'Clône de ' * (clone_count - 1)}{combattant[1]}"
        clone_pseudo += f" (équipe {equipe_num})"

        if combattant[-1] == 'Personnage':
            personnage = Personnage(combattant[0], clone_pseudo, combattant[2], combattant[3], combattant[4], combattant[5], combattant[6], combattant[7], combattant[8], combattant[9])
        else:
         personnage = Adversaire(combattant[0], clone_pseudo, combattant[2], combattant[3], combattant[4], combattant[5], combattant[6], combattant[7], combattant[8], combattant[9])


        equipe.append(personnage)

    return equipe

def afficher_stats_equipe(equipe):
    hp_total = 0
    combattants_vivants = []

    for combattant in equipe:
        if combattant.hp > 0:
            hp_total += combattant.hp
            combattants_vivants.append(combattant.pseudo)

    print(f"L'équipe victorieuse a {hp_total} HP restants.")
    print(f"{combattant.pseudo} - HP: {combattant.hp}")
    print(f"Combattants encore en vie : {', '.join(combattants_vivants)}")

