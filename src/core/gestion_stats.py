"""Module de gestion des statistiques des personnages"""

from src.database.bddmanager import DatabaseManager

def afficher_stats_actuelles(personnage):
    """Affiche les statistiques actuelles du personnage"""
    print("\n=== Statistiques actuelles ===")
    print(f"Points disponibles: {personnage.points_de_stats}")
    print(f"1. Force: {personnage.force}")
    print(f"2. Défense: {personnage.defense}")
    print(f"3. Magie: {personnage.magie}")
    print(f"4. Résistance: {personnage.resistance}")
    print(f"5. Agilité: {personnage.agilite} (max 40)")
    print("0. Quitter")

def menu_attribution_points(personnage):
    """
    Menu d'attribution des points de stats
    Args:
        personnage: Instance de la classe Personnage
    """
    stats_map = {
        "1": "force",
        "2": "defense",
        "3": "magie",
        "4": "resistance",
        "5": "agilite"
    }

    while personnage.points_de_stats > 0:
        afficher_stats_actuelles(personnage)
        choix = input("\nQuelle statistique voulez-vous augmenter? (0-5): ")
        
        if choix == "0":
            confirmation = input("Êtes-vous sûr de vouloir quitter? (o/n): ")
            if confirmation.lower() == 'o':
                break
            continue

        if choix in stats_map:
            personnage.augmenter_statistique(stats_map[choix])
        else:
            print("Choix invalide!")

def augmenter_statistique(personnage, statistique):
    """
    Augmente la statistique choisie si des points sont disponibles
    """
    if personnage.points_de_stats <= 0:
        print("Vous n'avez plus de points de stats disponibles!")
        return False

    # Vérifier la limite d'agilité avant l'augmentation
    if statistique == "agilite":
        if personnage.agilite >= 40:
            print("L'agilité ne peut pas dépasser 40!")
            return False

    # Augmenter la statistique choisie
    if statistique == "force":
        personnage.force += 1
        print(f"Force augmentée! ({personnage.force})")
    elif statistique == "defense":
        personnage.defense += 1
        print(f"Défense augmentée! ({personnage.defense})")
    elif statistique == "magie":
        personnage.magie += 1
        print(f"Magie augmentée! ({personnage.magie})")
    elif statistique == "resistance":
        personnage.resistance += 1
        print(f"Résistance augmentée! ({personnage.resistance})")
    elif statistique == "agilite":
        if personnage.agilite + 1 <= 40:
            personnage.agilite += 1
            print(f"Agilité augmentée! ({personnage.agilite})")
        else:
            print("L'agilité ne peut pas dépasser 40!")
            return False
    else:
        print("Statistique invalide!")
        return False

    personnage.points_de_stats -= 1
    return True

def attribuer_points_apres_niveau(personnage):
    """
    Fonction dédiée à l'attribution des points de stats après une montée de niveau
    Args:
        personnage: Instance de la classe Personnage
    """
    while True:
        choix_attribution = input("\nVoulez-vous attribuer vos points de stats maintenant ? (oui/non): ").lower()
        if choix_attribution == "oui":
            while personnage.points_de_stats > 0:
                print("\n=== Attribution des points de stats ===")
                print(f"Points disponibles: {personnage.points_de_stats}")
                print("\nStatistiques actuelles:")
                print(f"1. Force: {personnage.force}")
                print(f"2. Défense: {personnage.defense}")
                print(f"3. Magie: {personnage.magie}")
                print(f"4. Résistance: {personnage.resistance}")
                print(f"5. Agilité: {personnage.agilite} (max 40)")
                print("0. Conserver les points pour plus tard")

                choix = input("\nQuelle statistique voulez-vous augmenter? (0-5): ")
                
                if choix == "0":
                    while True:
                        confirmation = input("Voulez-vous vraiment garder les points pour plus tard? (oui/non): ").lower()
                        if confirmation == "oui":
                            print(f"\nPoints conservés: {personnage.points_de_stats}")
                            break
                        elif confirmation == "non":
                            break
                        else:
                            print("Veuillez répondre par 'oui' ou 'non'")
                    if confirmation == "oui":
                        break

                stats_map = {
                    "1": "force",
                    "2": "defense",
                    "3": "magie",
                    "4": "resistance",
                    "5": "agilite"
                }

                if choix in stats_map:
                    personnage.augmenter_statistique(stats_map[choix])
                else:
                    print("Choix invalide!")
            break
        elif choix_attribution == "non":
            print(f"Points de stats conservés: {personnage.points_de_stats}")
            break
        else:
            print("Veuillez répondre par 'oui' ou 'non'")

    # Sauvegarder les modifications dans la BDD
    with DatabaseManager() as cursor:
        cursor.execute('''
            UPDATE Personnage 
            SET force=?, defense=?, magie=?, resistance=?, agilite=?,
                points_de_stats=?
            WHERE id=?
        ''', (personnage.force, personnage.defense, 
              personnage.magie, personnage.resistance, 
              personnage.agilite, personnage.points_de_stats,
              personnage.id))
        
    print("\nStatistiques sauvegardées!") 