from src.core.ressources import *
from src.core.personnage import *
from src.core.adversaire import *
from src.combat.actions_combat import *

def menu_combat(combattant, equipe1, equipe2, is_super_contre=False, is_contre=False):
    """Affiche le menu de combat et gère les choix du joueur"""
    while True:
        print("\nChoisissez une action :")
        print("1. Attaquer")
        print("2. Items")
        print("3. Compétences")
        print("4. Actions")
        
        try:
            choix = int(input("Votre choix : "))
            
            if choix == 1:  # Attaquer
                while True:  # Boucle pour la sélection de cible
                    # Déterminer l'équipe adverse
                    if combattant in equipe1:
                        cibles_valides = [c for c in equipe2 if c.hp > 0]
                    else:
                        cibles_valides = [c for c in equipe1 if c.hp > 0]
                    
                    if not cibles_valides:
                        print("Aucun adversaire vivant. Choisissez une autre action.")
                        break
                    
                    # Afficher et choisir la cible
                    print("\nChoisissez votre cible :")
                    for idx, cible in enumerate(cibles_valides, start=1):
                        print(f"{idx}. {cible.pseudo} (HP: {cible.hp}/{cible.hp_total})")
                    print("0. Retour au menu principal")
                    
                    try:
                        choix_cible = int(input("Cible : "))
                        if choix_cible == 0:
                            break  # Retour au menu principal
                        
                        choix_cible -= 1  # Ajuster l'index
                        if 0 <= choix_cible < len(cibles_valides):
                            from src.combat.actions_combat import attaquer
                            resultat = attaquer(combattant, cibles_valides[choix_cible], 
                                              equipe1, equipe2, is_super_contre, is_contre)
                            if resultat == "retour":

                                continue  # Retour à la sélection de cible
                            return "attaque"
                        else:
                            print("Choix invalide. Veuillez réessayer.")
                    except ValueError:
                        print("Entrée invalide. Veuillez réessayer.")
                
            elif choix == 2:  # Items
                from src.items.item import charger_items  # Import local
                items = charger_items()
                items_utilisables = [item for item in items if item.quantite > 0]
                

                if not items_utilisables:
                    print("Vous n'avez aucun item utilisable.")
                    continue
                
                print("\nChoisissez un item à utiliser :")
                for idx, item in enumerate(items_utilisables, start=1):
                    print(f"{idx}. {item.nom} (x{item.quantite})")
                
                choix_item = int(input("Numéro de l'item (0 pour retour) : ")) - 1
                if choix_item == -1:
                    continue
                if 0 <= choix_item < len(items_utilisables):
                    # Choisir sur quelle équipe utiliser l'item
                    print("\nUtiliser sur quelle équipe ?")
                    print("1. Équipe alliée")
                    print("2. Équipe adverse")
                    
                    try:
                        choix_equipe = int(input("Choix de l'équipe : "))
                        if choix_equipe == 1:
                            equipe_cible = equipe1 if combattant in equipe1 else equipe2
                        elif choix_equipe == 2:
                            equipe_cible = equipe2 if combattant in equipe1 else equipe1
                        else:
                            print("Choix invalide.")
                            continue
                            
                        # Afficher les cibles possibles
                        print("\nUtiliser sur qui ?")
                        for idx, cible in enumerate(equipe_cible, start=1):
                            print(f"{idx}. {cible.pseudo} (HP: {cible.hp}/{cible.hp_total})")
                        
                        choix_cible = int(input("Numéro de la cible : ")) - 1
                        if 0 <= choix_cible < len(equipe_cible):
                            items_utilisables[choix_item].utiliser(equipe_cible[choix_cible])
                            return True
                            
                    except ValueError:
                        print("Entrée invalide.")
                        continue
                
            elif choix == 3:  # Compétences
                print("Les compétences ne sont pas encore implémentées.")
                continue
                
            elif choix == 4:  # Actions
                print("\nActions disponibles :")
                print("1. Fuir")
                print("2. Retour")
                
                try:
                    choix_action = int(input("Action : "))
                    if choix_action == 1:
                        from src.combat.actions_combat import fuite  # Import local
                        if fuite(combattant):
                            return "fuite"

                        return True
                    elif choix_action == 2:
                        continue
                    else:
                        print("Choix invalide. Veuillez réessayer.")
                except ValueError:
                    print("Entrée invalide. Veuillez réessayer.")
                    
            else:
                print("Choix invalide. Veuillez réessayer.")
                
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.") 