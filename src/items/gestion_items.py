"""Gestion des items"""
from .item import Item

def utiliser_item(item, cible):
    """Utilise un item sur une cible"""
    if item.quantite <= 0:
        return False
        
    item.quantite -= 1
    item.effet(cible)
    return True 