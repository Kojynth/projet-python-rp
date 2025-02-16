"""Données de test communes pour tous les tests"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.personnage import Personnage
from src.core.adversaire import Adversaire

def create_test_personnage():
    """Crée un personnage de test standard"""
    return Personnage(
        id=1,
        pseudo="Test Hero",
        hp=100, hp_total=100,
        mana=50, mana_total=50,
        force=20, defense=10,
        magie=15, resistance=10,
        agilite=20,
        niveau=1,
        points_de_stats=0,
        experience=0
    )

def create_test_adversaire():
    """Crée un adversaire de test standard"""
    return Adversaire(
        id=1,
        pseudo="Test Enemy",
        hp=80, hp_total=80,
        mana=30, mana_total=30,
        force=15, defense=8,
        magie=8, resistance=8,
        agilite=15,
        niveau=1,
        experience=10
    )

def create_test_teams():
    """Crée des équipes de test"""
    hero = create_test_personnage()
    enemy = create_test_adversaire()
    return [hero], [enemy], [hero, enemy] 