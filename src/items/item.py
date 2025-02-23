from enum import Enum
from src.database.bddmanager import sauvegarder_objets, charger_donnees

class Item:
    def __init__(self, nom, code_item, categorie, description, valeur,
                 bonus_hp, bonus_mp, bonus_force, bonus_defense,
                 bonus_magie, bonus_resistance, bonus_agilite,
                 est_equipable, est_consommable, est_empilable, pile_max,
                 quantite=1, id_item=None):
        self.id_item = id_item
        self.nom = nom
        self.code_item = code_item
        self.categorie = categorie
        self.description = description
        self.valeur = valeur
        self.bonus_hp = bonus_hp
        self.bonus_mp = bonus_mp
        self.bonus_force = bonus_force
        self.bonus_defense = bonus_defense
        self.bonus_magie = bonus_magie
        self.bonus_resistance = bonus_resistance
        self.bonus_agilite = bonus_agilite
        self.est_equipable = est_equipable
        self.est_consommable = est_consommable
        self.est_empilable = est_empilable
        self.pile_max = pile_max
        self.quantite = quantite

    def utiliser(self, personnage):
        """Utilise l'item sur un personnage"""
        if self.quantite <= 0:
            print(f"Vous ne possédez pas de {self.nom}")
            return False

        if not self.est_consommable:
            print(f"{self.nom} n'est pas un objet consommable")
            return False

        # Application des bonus
        if self.bonus_hp > 0:
            hp_actuel = personnage.hp
            hp_max = personnage.hp_total
            # Calcul du soin en pourcentage des HP max
            soin = int(hp_max * (self.bonus_hp / 100))
            nouvelle_valeur = min(hp_actuel + soin, hp_max)
            personnage.hp = nouvelle_valeur
            print(f"{self.nom} restaure {soin} HP à {personnage.pseudo}!")
            print(f"HP : {hp_actuel} -> {nouvelle_valeur}")

        if self.bonus_mp > 0:
            mp_actuel = personnage.mana
            mp_max = personnage.mana_total
            # Calcul du soin en pourcentage des MP max
            restauration = int(mp_max * (self.bonus_mp / 100))
            nouvelle_valeur = min(mp_actuel + restauration, mp_max)
            personnage.mana = nouvelle_valeur
            print(f"{self.nom} restaure {restauration} MP à {personnage.pseudo}!")
            print(f"MP : {mp_actuel} -> {nouvelle_valeur}")

        # Réduire la quantité
        self.quantite -= 1
        return True

    def ajouter(self, quantite=1):
        """Ajoute une quantité d'items à l'inventaire"""
        self.quantite += quantite
        print(f"{quantite} {self.nom} ajouté(s) à l'inventaire")

    def retirer(self, quantite=1):
        """Retire une quantité d'items de l'inventaire"""
        if self.quantite >= quantite:
            self.quantite -= quantite
            print(f"{quantite} {self.nom} retiré(s) de l'inventaire")
            return True
        else:
            print(f"Pas assez de {self.nom} dans l'inventaire")
            return False

    def afficher_details(self):
        """Affiche les détails de l'item"""
        print(f"=== {self.nom} ===")
        print(f"Quantité : {self.quantite}")
        print(f"Effet : {self.bonus_hp}% HP, {self.bonus_mp}% MP, {self.bonus_force} Force, {self.bonus_defense} Défense, {self.bonus_magie} Magie, {self.bonus_resistance} Résistance, {self.bonus_agilite} Agilité")

def sauvegarder_items(items):
    """Sauvegarde les items dans la base de données"""
    sauvegarder_objets('Item', items)

def charger_items():
    """Charge les items depuis la base de données"""
    return charger_donnees('Item', Item)

def creer_items_base():
    """Crée les items de base du jeu"""
    items = [
        Item("Petite potion de soin", "POT_SOIN_P", "Consommables",
             "Une petite potion qui restaure 10% des HP max",
             25, 10, 0, 0, 0, 0, 0, 0, 0, 1, 1, 10),
        
        Item("Potion de soin", "POT_SOIN_M", "Consommables",
             "Une potion qui restaure 25% des HP max",
             50, 25, 0, 0, 0, 0, 0, 0, 0, 1, 1, 5),
        
        Item("Potion de soin puissante", "POT_SOIN_G", "Consommables",
             "Une grande potion qui restaure 50% des HP max",
             100, 50, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3),
        
        Item("Potion de soin surpuissante", "POT_SOIN_S", "Consommables",
             "Une potion légendaire qui restaure 100% des HP max",
             250, 100, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1)
    ]
    sauvegarder_items(items)
    return items 