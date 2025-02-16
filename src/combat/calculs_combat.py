"""Fonctions de calcul pour le combat"""

def calculer_degats(attacker, target, type_degats, pourcentage_defense_ignore):
    """Calcule les dégâts en fonction du type d'attaque et du pourcentage de défense ignoré"""
    if type_degats == "physique":
        defense_effective = target.defense * (1 - pourcentage_defense_ignore)
        degats = max(0, attacker.force - defense_effective)
    else:  # magique
        resistance_effective = target.resistance * (1 - pourcentage_defense_ignore)
        degats = max(0, attacker.magie - resistance_effective)
    return int(degats) 