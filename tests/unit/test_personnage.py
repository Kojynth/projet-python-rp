import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
from src.core.personnage import Personnage
from tests.data.test_data import create_test_personnage


class TestPersonnage(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.personnage = Personnage(1, "TestHero", 100, 100, 50, 50, 20, 10, 15, 10, 12, 1, 0, 0)

    def test_gain_hp_par_niveau(self):
        """Test des gains de HP à différents niveaux"""
        # Test niveau 1-10 (75 HP par niveau)
        self.assertEqual(self.personnage.calculer_gain_hp(), 75)
        
        # Test niveau 11-20 (90 HP par niveau)
        self.personnage.niveau = 15
        self.assertEqual(self.personnage.calculer_gain_hp(), 90)
        
        # Test niveau 21-30 (105 HP par niveau)
        self.personnage.niveau = 25
        self.assertEqual(self.personnage.calculer_gain_hp(), 105)
        
        # Test niveau 31-40 (120 HP par niveau)
        self.personnage.niveau = 35
        self.assertEqual(self.personnage.calculer_gain_hp(), 120)

    def test_montee_niveau_complete(self):
        """Test d'une montée de niveau complète avec gain de HP"""
        hp_initial = self.personnage.hp_total
        
        # Donner assez d'XP pour monter d'un niveau
        self.personnage.gagner_experience(10)
        
        # Vérifier que le niveau a augmenté
        self.assertEqual(self.personnage.niveau, 2)
        # Vérifier que les HP ont augmenté du bon montant
        self.assertEqual(self.personnage.hp_total, hp_initial + 75)
        # Vérifier que les HP actuels ont aussi augmenté
        self.assertEqual(self.personnage.hp, self.personnage.hp_total)

    def test_multiple_montees_niveau(self):
        """Test de plusieurs montées de niveau d'affilée"""
        hp_initial = self.personnage.hp_total
        
        # Donner assez d'XP pour monter de 3 niveaux (30 XP)
        self.personnage.gagner_experience(30)
        
        # Vérifier le niveau final
        self.assertEqual(self.personnage.niveau, 4)
        
        # Calculer le gain total attendu (3 * 75 HP car toujours dans la première tranche)
        gain_total_attendu = 3 * 75
        
        # Vérifier les HP totaux
        self.assertEqual(self.personnage.hp_total, hp_initial + gain_total_attendu)

    def test_gain_hp_niveaux_eleves(self):
        """Test des gains de HP à des niveaux plus élevés"""
        # Test niveau 91-100 (210 HP par niveau)
        self.personnage.niveau = 95
        self.assertEqual(self.personnage.calculer_gain_hp(), 210)
        
        # Test niveau 191-200 (360 HP par niveau)
        self.personnage.niveau = 195
        self.assertEqual(self.personnage.calculer_gain_hp(), 360)

    def test_gain_mana_par_niveau(self):
        """Test des gains de mana à différents niveaux"""
        # Test niveau 1-100 (20 Mana par niveau)
        mana_initial = self.personnage.mana_total
        self.personnage.niveau = 50
        self.assertEqual(self.personnage.calculer_gain_mana(), 20)
        
        # Test niveau 101+ (5 Mana par niveau)
        self.personnage.niveau = 150
        self.assertEqual(self.personnage.calculer_gain_mana(), 5)

    def test_montee_niveau_avec_mana(self):
        """Test d'une montée de niveau complète avec gain de mana"""
        mana_initial = self.personnage.mana_total
        
        # Donner assez d'XP pour monter d'un niveau
        self.personnage.gagner_experience(10)
        
        # Vérifier que le niveau a augmenté
        self.assertEqual(self.personnage.niveau, 2)
        # Vérifier que le mana a augmenté du bon montant
        self.assertEqual(self.personnage.mana_total, mana_initial + 20)
        # Vérifier que le mana actuel a aussi augmenté
        self.assertEqual(self.personnage.mana, self.personnage.mana_total)

    def test_gain_mana_niveaux_eleves(self):
        """Test des gains de mana à des niveaux plus élevés"""
        self.personnage.niveau = 99
        self.assertEqual(self.personnage.calculer_gain_mana(), 20)
        
        self.personnage.niveau = 100
        self.assertEqual(self.personnage.calculer_gain_mana(), 20)
        
        self.personnage.niveau = 101
        self.assertEqual(self.personnage.calculer_gain_mana(), 5)

    def test_gain_points_stats_par_niveau(self):
        """Test des gains de points de stats à différents niveaux"""
        # Test niveau 1-20 (5 points par niveau)
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 5)
        
        # Test niveau 21-40 (10 points par niveau)
        self.personnage.niveau = 21
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 10)
        
        # Test niveau 41-60 (15 points par niveau)
        self.personnage.niveau = 41
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 15)
        
        # Test niveau 61-80 (20 points par niveau)
        self.personnage.niveau = 61
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 20)

    def test_montee_niveau_avec_points_stats(self):
        """Test d'une montée de niveau complète avec gain de points de stats"""
        points_initial = self.personnage.points_de_stats
        
        # Test passage niveau 19->20 (5 points)
        self.personnage.niveau = 19
        self.personnage.gagner_experience(200)  # Assez pour monter d'un niveau
        self.assertEqual(self.personnage.niveau, 20)
        self.assertEqual(self.personnage.points_de_stats, points_initial + 5)
        
        # Test passage niveau 20->21 (10 points)
        points_avant = self.personnage.points_de_stats
        self.personnage.gagner_experience(210)  # Assez pour monter d'un niveau
        self.assertEqual(self.personnage.niveau, 21)
        self.assertEqual(self.personnage.points_de_stats, points_avant + 10)

    def test_gain_points_stats_niveaux_eleves(self):
        """Test des gains de points de stats à des niveaux plus élevés"""
        # Test niveau 39->40 (10 points)
        self.personnage.niveau = 39
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 10)
        
        # Test niveau 40->41 (15 points)
        self.personnage.niveau = 40
        self.personnage.gagner_experience(400)
        self.assertEqual(self.personnage.niveau, 41)
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 15)
        
        # Test niveau 59->60 (15 points)
        self.personnage.niveau = 59
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 15)
        
        # Test niveau 60->61 (20 points)
        self.personnage.niveau = 60
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 20)

    def test_total_points_stats_niveau_101(self):
        """Test du total des points de stats accumulés jusqu'au niveau 101"""
        # Donner assez d'XP pour atteindre le niveau 101
        while self.personnage.niveau < 101:
            self.personnage.gagner_experience(1000)  # Valeur arbitraire assez grande
        
        # Vérifier le total des points de stats
        self.assertEqual(self.personnage.points_de_stats, 1530)
        
        # Vérifier le dernier gain (niveau 101)
        self.assertEqual(self.personnage.calculer_gain_points_stats(), 30)

    def test_augmenter_statistique(self):
        """Test de l'augmentation des statistiques"""
        # Donner des points de stats
        self.personnage.points_de_stats = 5
        
        # Test augmentation force
        self.assertTrue(self.personnage.augmenter_statistique("force"))
        self.assertEqual(self.personnage.force, 22)  # 20 + 2
        self.assertEqual(self.personnage.points_de_stats, 4)
        
        # Test augmentation defense
        self.assertTrue(self.personnage.augmenter_statistique("defense"))
        self.assertEqual(self.personnage.defense, 12)  # 10 + 2
        self.assertEqual(self.personnage.points_de_stats, 3)

    def test_limite_agilite(self):
        """Test de la limite d'agilité à 40"""
        self.personnage.points_de_stats = 20
        self.personnage.agilite = 39
        
        # Premier test : peut augmenter jusqu'à 40
        self.assertTrue(self.personnage.augmenter_statistique("agilite"))
        self.assertEqual(self.personnage.agilite, 40)
        
        # Deuxième test : ne peut pas dépasser 40
        self.assertFalse(self.personnage.augmenter_statistique("agilite"))
        self.assertEqual(self.personnage.agilite, 40)

    def test_points_stats_insuffisants(self):
        """Test quand il n'y a plus de points de stats"""
        self.personnage.points_de_stats = 0
        self.assertFalse(self.personnage.augmenter_statistique("force"))
        self.assertEqual(self.personnage.force, 20)  # Inchangé

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
