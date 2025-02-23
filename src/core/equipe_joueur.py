import sqlite3
from src.core.personnage import Personnage
from src.core.ressources import *
from src.database.bddmanager import *
from src.core.adversaire import Adversaire
from ..database.bddmanager import DatabaseManager


def afficher_combattants(combattants):
    for idx, combattant in enumerate(combattants, start=1):
        print(f"{idx}. {combattant[1]} - HP: {combattant[2]}/{combattant[3]}, Mana: {combattant[4]}/{combattant[5]}, Attaque: {combattant[6]}")

def selectionner_equipe(equipe_num):
    """Sélectionne une équipe de combattants"""
    with DatabaseManager() as db:
        # Sélectionner tous les personnages
        db.execute('''
            SELECT id, pseudo, hp, hp_total, mana, mana_total, force, defense, magie, 
                   resistance, agilite, niveau, points_de_stats, experience, 
                   race_id, classe_id, sexe, alignement, orientation, taille, poids
            FROM Personnage
            WHERE hp > 0
        ''')
        personnages = db.fetchall()

        # Sélectionner tous les adversaires
        db.execute('''
            SELECT id, pseudo, hp, hp_total, mana, mana_total, force, defense, magie, 
                   resistance, agilite, niveau, experience
            FROM Adversaire
            WHERE hp > 0
        ''')
        adversaires = db.fetchall()

        # Combiner les résultats
        combattants = []
        
        # Ajouter les personnages
        for p in personnages:
            combattants.append({
                'id': p[0],
                'pseudo': p[1],
                'hp': p[2],
                'hp_total': p[3],
                'mana': p[4],
                'mana_total': p[5],
                'force': p[6],
                'defense': p[7],
                'magie': p[8],
                'resistance': p[9],
                'agilite': p[10],
                'niveau': p[11],
                'points_de_stats': p[12],
                'experience': p[13],
                'type': 'Personnage'
            })
        
        # Ajouter les adversaires
        for a in adversaires:
            combattants.append({
                'id': a[0],
                'pseudo': a[1],
                'hp': a[2],
                'hp_total': a[3],
                'mana': a[4],
                'mana_total': a[5],
                'force': a[6],
                'defense': a[7],
                'magie': a[8],
                'resistance': a[9],
                'agilite': a[10],
                'niveau': a[11],
                'experience': a[12],
                'points_de_stats': 0,
                'type': 'Adversaire'
            })

    # Afficher les combattants disponibles
    print(f"\nSélectionnez l'équipe {equipe_num}:")
    for i, combattant in enumerate(combattants, 1):
        print(f"{i}. {combattant['pseudo']} ({combattant['type']}) - "
              f"HP: {combattant['hp']}/{combattant['hp_total']}, "
              f"Force: {combattant['force']}")

    # Sélectionner les combattants pour l'équipe
    selection = input("Sélectionnez les combattants pour l'équipe (entrez les numéros séparés par des espaces): ").split()
    equipe = []

    for i in selection:
        combattant = combattants[int(i) - 1]
        clone_pseudo = combattant['pseudo']
        clone_count = 0
        while any(clone_pseudo in c['pseudo'] for c in equipe):
            clone_count += 1
            clone_pseudo = f"Clône de {combattant['pseudo']}" if clone_count == 1 else f"Clône de {'Clône de ' * (clone_count - 1)}{combattant['pseudo']}"
        clone_pseudo += f" (équipe {equipe_num})"

        if combattant['type'] == 'Personnage':
            personnage = Personnage(combattant['id'], clone_pseudo, combattant['hp'], combattant['hp_total'], combattant['mana'], combattant['mana_total'], combattant['force'], combattant['defense'], combattant['magie'], combattant['resistance'], combattant['agilite'], combattant['niveau'], combattant['points_de_stats'], combattant['experience'], combattant['race_id'], combattant['classe_id'], combattant['sexe'], combattant['alignement'], combattant['orientation'], combattant['taille'], combattant['poids'])
        else:
            personnage = Adversaire(combattant['id'], clone_pseudo, combattant['hp'], combattant['hp_total'], combattant['mana'], combattant['mana_total'], combattant['force'], combattant['defense'], combattant['magie'], combattant['resistance'], combattant['agilite'], combattant['niveau'], combattant['experience'], combattant['points_de_stats'])

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

def selectionner_equipe_joueurs():
    """Sélectionne une équipe de personnages joueurs"""
    equipe = []
    
    with DatabaseManager() as cursor:
        cursor.execute('SELECT * FROM Personnage WHERE hp > 0 ORDER BY id')
        personnages = cursor.fetchall()
        
        print("\nSélectionnez vos personnages:")
        for i, perso in enumerate(personnages, 1):
            print(f"{i}. {perso[1]} - HP: {perso[2]}/{perso[3]}, Force: {perso[6]}")
        
        selection = input("Sélectionnez les personnages (entrez les numéros séparés par des espaces): ").split()
        
        for i in selection:
            perso = personnages[int(i) - 1]
            clone_pseudo = perso[1] + " (héros)"
            
            # Création avec tous les champs de la table Personnage
            personnage = Personnage(
                pseudo=clone_pseudo,
                hp=perso[2],
                force=perso[6],
                niveau=perso[11],
                mana=perso[4]
            )
            # On définit les HP totaux après la création
            personnage.hp_total = perso[3]
            
            # On définit les autres attributs après la création
            personnage.mana_total = perso[5]
            personnage.defense = perso[7]
            personnage.magie = perso[8]
            personnage.resistance = perso[9]
            personnage.agilite = perso[10]
            personnage.points_de_stats = perso[12]
            personnage.experience = perso[13]
            personnage.race_id = perso[14]
            personnage.classe_id = perso[15]
            personnage.sexe = perso[16]
            personnage.alignement = perso[17]
            personnage.orientation = perso[18]
            personnage.taille = perso[19]
            personnage.poids = perso[20]
            
            equipe.append(personnage)
    
    return equipe

def selectionner_equipe_adversaires():
    """Sélectionne une équipe d'adversaires"""
    equipe = []
    
    with DatabaseManager() as cursor:
        cursor.execute('SELECT * FROM Adversaire WHERE hp > 0 ORDER BY id')
        adversaires = cursor.fetchall()
        
        print("\nAdversaires disponibles:")
        for i, adv in enumerate(adversaires, 1):
            print(f"{i}. {adv[1]} - HP: {adv[2]}/{adv[3]}, Force: {adv[6]}")
        
        selection = input("Sélectionnez les adversaires (entrez les numéros séparés par des espaces): ").split()
        
        for i in selection:
            adv = adversaires[int(i) - 1]
            clone_pseudo = adv[1] + " (ennemi)"
            
            adversaire = Adversaire(
                adv[0],  # id
                clone_pseudo,  # pseudo
                adv[2],  # hp
                adv[3]   # hp_total
            )
            equipe.append(adversaire)
    
    return equipe

