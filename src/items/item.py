from enum import Enum
from src.database.bddmanager import sauvegarder_objets, charger_donnees

class CaracteristiqueItem(Enum):
    """Énumération des différentes caractéristiques possibles pour un item"""
    HP = "hp"
    MANA = "mana"
    FORCE = "force"
    DEFENSE = "defense"
    MAGIE = "magie"
    RESISTANCE = "resistance"
    AGILITE = "agilite"

class Item:
    def __init__(self, nom, effet, quantite=1):
        self.nom = nom
        self.effet = effet
        self.quantite = quantite

    def utiliser(self, personnage):
        """
        Utilise l'item sur un personnage.
        
        Args:
            personnage (Personnage): Le personnage sur lequel utiliser l'item
            
        Returns:
            bool: True si l'item a été utilisé avec succès, False sinon
        """
        if self.quantite <= 0:
            print(f"Vous ne possédez pas de {self.nom}")
            return False

        # Récupérer la valeur actuelle de la caractéristique
        valeur_actuelle = getattr(personnage, self.effet)
        
        # Si c'est HP ou MANA, on ne dépasse pas le total
        if self.effet in [CaracteristiqueItem.HP, CaracteristiqueItem.MANA]:
            valeur_max = getattr(personnage, f"{self.effet}_total")
            nouvelle_valeur = min(valeur_actuelle + self.effet, valeur_max)
        else:
            nouvelle_valeur = valeur_actuelle + self.effet

        # Appliquer la nouvelle valeur
        setattr(personnage, self.effet, nouvelle_valeur)
        
        # Réduire la quantité
        self.quantite -= 1
        
        print(f"{self.nom} utilisé sur {personnage.pseudo}!")
        print(f"{self.effet} : {valeur_actuelle} -> {nouvelle_valeur}")
        
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
        print(f"Effet : {self.effet}")

def sauvegarder_items(items):
    """Sauvegarde les items dans la base de données"""
    sauvegarder_objets('Item', items)

def charger_items():
    """Charge les items depuis la base de données"""
    return charger_donnees('Item', Item)

def potion_full_heal(personnage):
    """Restaure tous les HP du personnage"""
    hp_manquants = personnage.hp_total - personnage.hp
    personnage.hp = personnage.hp_total
    print(f"{personnage.pseudo} récupère {hp_manquants} HP! (HP: {personnage.hp}/{personnage.hp_total})") 