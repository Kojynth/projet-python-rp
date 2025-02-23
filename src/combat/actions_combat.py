import random
from src.core.ressources import *
from src.core.personnage import *
from src.core.adversaire import *
from src.combat.menu_combat import menu_combat  # Changement de l'import


# Fonction pour gérer les dégâts subis par la cible
def subir_attaque(target, degats):
    # Réduire les HP de la cible en fonction des dégâts subis
    target.hp = max(0, target.hp - degats)
    # Afficher un message indiquant les dégâts subis et les HP restants
    print(f"{target.pseudo} subit {degats} de dégâts. Il lui reste {target.hp} HP.")

# Fonction pour gérer l'attaque d'un combattant sur une cible
def attaquer(attacker, target, equipe1, equipe2, is_super_contre=False, is_contre=False):
    degats = 0
    type_degats = None
    
    while True:
        if isinstance(attacker, Personnage):
            # Demander au joueur de choisir le type d'attaque
            print("\nChoisissez le type d'attaque :")
            print("1. Dégâts physiques")
            print("2. Dégâts magiques")
            print("0. Retour au menu principal")
            try:
                type_degats = int(input("Type de dégâts : "))
                if type_degats == 0:
                    return "retour"  # Retour au menu principal
                elif type_degats == 1:
                    type_degats = "physique"
                    break
                elif type_degats == 2:
                    type_degats = "magique"
                    break
                else:
                    print("Choix invalide. Veuillez réessayer.")
            except ValueError:
                print("Entrée invalide. Veuillez réessayer.")
        else:
            # Pour les adversaires, on choisit le type d'attaque qui fait le plus de dégâts
            type_degats = "physique" if calculer_degats(attacker, target, "physique", 0) > calculer_degats(attacker, target, "magique", 0) else "magique"
            break

    # Si c'est une contre-attaque, pas de jet d'esquive
    if is_contre:
        # Réduire temporairement la défense/résistance de la cible pour le super contre
        if is_super_contre:
            if type_degats == "physique":
                defense_originale = target.defense
                target.defense = int(target.defense * 0.75)  # Réduction de 25% de la défense
            else:
                resistance_originale = target.resistance
                target.resistance = int(target.resistance * 0.75)  # Réduction de 25% de la résistance
            
            print(f"Super contre ! La {'défense' if type_degats == 'physique' else 'résistance'} de {target.pseudo} est temporairement réduite de 25% !")

        # Calculer les dégâts
        degats = calculer_degats(attacker, target, type_degats, 0)
        print(f"Contre-attaque ! {target.pseudo} ne peut pas esquiver !")
        subir_attaque(target, degats)

        # Restaurer la défense/résistance originale si c'était un super contre
        if is_super_contre:
            if type_degats == "physique":
                target.defense = defense_originale
            else:
                target.resistance = resistance_originale

        return True

    # Jet d'esquive normal pour les attaques standards
    jet_esquive = random.randint(1, 100)
    print(f"Jet d'esquive : {jet_esquive}")

    # Vérifier l'esquive et les critiques
    if jet_esquive <= target.agilite:
        print(f"{target.pseudo} esquive l'attaque !")
        
        # Gestion des contres
        if 6 <= jet_esquive <= 10:  # Contre basique
            print(f"{target.pseudo} effectue une contre-attaque basique !")
            contre_attaque(target, attacker, "basique", equipe1, equipe2)
        elif 2 <= jet_esquive <= 5:  # Super contre
            print(f"{target.pseudo} effectue une super contre-attaque !")
            contre_attaque(target, attacker, "super", equipe1, equipe2)
        elif jet_esquive == 1:  # Ultra contre
            print(f"{target.pseudo} effectue une ultra contre-attaque !")
            contre_attaque(target, attacker, "ultra", equipe1, equipe2)
    else:
        # Gestion des critiques
        if 91 <= jet_esquive <= 95:  # Critique
            print(f"{attacker.pseudo} effectue une attaque critique !")
            degats = calculer_degats(attacker, target, type_degats, 0.25)
        elif 96 <= jet_esquive <= 99:  # Super critique
            print(f"{attacker.pseudo} effectue une super attaque critique !")
            degats = calculer_degats(attacker, target, type_degats, 0.50)
        elif jet_esquive == 100:  # Ultra critique
            print(f"{attacker.pseudo} effectue une ultra attaque critique !")
            degats = calculer_degats(attacker, target, type_degats, 0.50)
            degats = int(degats * 1.25)  # 25% de dégâts bonus
        else:  # Attaque normale ou super contre
            pourcentage_defense_ignore = 0.25 if is_super_contre else 0
            degats = calculer_degats(attacker, target, type_degats, pourcentage_defense_ignore)

        # Appliquer les dégâts
        subir_attaque(target, degats)

# Fonction pour calculer les dégâts en fonction du type d'attaque et du pourcentage de défense ignoré
def calculer_degats(attacker, target, type_degats, pourcentage_defense_ignore):
    """
    Calcule les dégâts en fonction du type d'attaque et du pourcentage de défense ignoré.
    
    Args:
        attacker: L'attaquant
        target: La cible
        type_degats: "physique" ou "magique"
        pourcentage_defense_ignore: Pourcentage de défense/résistance ignoré (0 à 1)
    """
    if type_degats == "physique":
        defense_effective = target.defense * (1 - pourcentage_defense_ignore)
        degats = max(0, attacker.force - defense_effective)
    else:  # magique
        resistance_effective = target.resistance * (1 - pourcentage_defense_ignore)
        degats = max(0, attacker.magie - resistance_effective)
    return int(degats)

# Fonction pour gérer les contre-attaques
def contre_attaque(target, attacker, type_contre, equipe1, equipe2):
    """
    Gère les contre-attaques avec leurs effets spéciaux.
    Les contre-attaques ne peuvent pas être esquivées.
    """
    if type_contre == "basique":
        if isinstance(target, Personnage):
            print("Choisissez le type de contre-attaque :")
            print("1. Contre physique")
            print("2. Contre magique")
            try:
                choix = int(input("Type : "))
                type_degats = "physique" if choix == 1 else "magique"
            except ValueError:
                print("Entrée invalide. Contre physique par défaut.")
                type_degats = "physique"
        else:
            type_degats = "physique" if target.force > target.magie else "magique"
            
        # Calculer et appliquer les dégâts directement, sans jet d'esquive
        degats = calculer_degats(target, attacker, type_degats, 0)
        print(f"{target.pseudo} effectue une contre-attaque basique non-esquivable !")
        subir_attaque(attacker, degats)
        
    elif type_contre == "super":
        print(f"\n{target.pseudo} peut effectuer une action complète avec bonus !")
        print("Si vous choisissez d'attaquer, l'attaque sera non-esquivable et ignorera 25% de la défense/résistance de la cible")
        if isinstance(target, Personnage):
            menu_combat(target, equipe1, equipe2, is_super_contre=True, is_contre=True)
            
    elif type_contre == "ultra":
        print(f"\n{target.pseudo} peut effectuer deux actions complètes avec bonus !")
        print("Les attaques seront non-esquivables et ignoreront 25% de la défense/résistance de la cible !")
        if isinstance(target, Personnage):
            for i in range(2):
                print(f"\nAction {i+1}/2 :")
                menu_combat(target, equipe1, equipe2, is_super_contre=True, is_contre=True)

# Fonction pour permettre au joueur de fuir le combat
def fuite(combattant):
    # Générer un nombre aléatoire pour déterminer si la fuite est réussie
    chance_fuite = random.randint(1, 100)
    print(f"Nombre aléatoire pour la fuite: {chance_fuite}")
    if chance_fuite <= combattant.agilite:
        # Si la fuite est réussie, afficher un message et retourner True
        print(f"{combattant.pseudo} a réussi à fuir le combat !")
        return True
    else:
        # Si la fuite échoue, afficher un message et retourner False
        print(f"{combattant.pseudo} n'a pas réussi à fuir le combat !")
        return False
