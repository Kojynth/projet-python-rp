import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
from src.core.personnage import Personnage

class TestMonteeNiveau(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        self.personnage = Personnage(
            id=1,
            pseudo="TestHero",
            hp=100, hp_total=100,
            mana=50, mana_total=50,
            force=20, defense=10,
            magie=15, resistance=10,
            agilite=12, niveau=1,
            points_de_stats=0,
            experience=0
        )

    def test_montee_niveau_basique(self):
        """Test basique de montée de niveau"""
        print("\nÉtat initial:")
        self.personnage.afficher_fiche()
        
        print("\nMontée de niveau:")
        self.personnage.gagner_experience(20)  # XP nécessaire pour niveau 1->2

    def test_montee_niveau_simple(self):
        """Test d'une seule montée de niveau avec vérification des gains"""
        # Enregistrer les valeurs initiales
        hp_initial = self.personnage.hp_total
        mana_initial = self.personnage.mana_total
        points_stats_initial = self.personnage.points_de_stats
        niveau_initial = self.personnage.niveau

        # Donner juste assez d'XP pour monter d'un niveau
        xp_necessaire = self.personnage.calculer_xp_necessaire()
        self.personnage.gagner_experience(xp_necessaire)

        # Vérifier la montée de niveau
        self.assertEqual(self.personnage.niveau, niveau_initial + 1)

        # Vérifier les gains de stats
        self.assertEqual(self.personnage.points_de_stats, points_stats_initial + 5)  # 5 points au niveau 1
        self.assertEqual(self.personnage.hp_total, hp_initial + 75)  # 75 HP aux premiers niveaux
        self.assertEqual(self.personnage.mana_total, mana_initial + 20)  # 20 mana jusqu'au niveau 100

    def test_gains_differents_niveaux(self):
        """Test des gains de points de stats à différents niveaux"""
        # Test niveau 20->21 (passage à 10 points)
        self.personnage.niveau = 20
        points_avant = self.personnage.points_de_stats
        self.personnage.gagner_experience(1000)  # Assez pour monter d'un niveau
        self.assertEqual(self.personnage.niveau, 21)
        gain = self.personnage.points_de_stats - points_avant
        self.assertEqual(gain, 10)  # Devrait gagner 10 points

        # Test niveau 40->41 (passage à 15 points)
        self.personnage.niveau = 40
        points_avant = self.personnage.points_de_stats
        self.personnage.gagner_experience(1000)
        self.assertEqual(self.personnage.niveau, 41)
        gain = self.personnage.points_de_stats - points_avant
        self.assertEqual(gain, 15)  # Devrait gagner 15 points

    def test_attribution_points_stats(self):
        """Test de l'attribution des points de stats gagnés"""
        # Donner des points de stats
        self.personnage.points_de_stats = 10
        
        # Test augmentation force
        force_initiale = self.personnage.force
        self.personnage.augmenter_statistique("force")
        self.assertEqual(self.personnage.force, force_initiale + 2)
        self.assertEqual(self.personnage.points_de_stats, 9)

        # Test augmentation défense
        defense_initiale = self.personnage.defense
        self.personnage.augmenter_statistique("defense")
        self.assertEqual(self.personnage.defense, defense_initiale + 2)
        self.assertEqual(self.personnage.points_de_stats, 8)

    def test_choix_attribution_points(self):
        """Test du choix d'attribution des points à la montée de niveau"""
        from unittest.mock import patch
        
        # Simuler une réponse 'non' à l'attribution des points
        with patch('builtins.input', return_value='n'):
            points_avant = self.personnage.points_de_stats
            xp_necessaire = self.personnage.calculer_xp_necessaire()
            self.personnage.gagner_experience(xp_necessaire)
            # Vérifier que les points sont conservés
            self.assertEqual(self.personnage.points_de_stats, points_avant + 5)

        # Simuler une séquence d'inputs pour attribuer des points
        # 'o' pour oui, puis '1' pour force, puis '0' pour quitter
        with patch('builtins.input', side_effect=['o', '1', '0', 'o']):
            force_avant = self.personnage.force
            points_avant = self.personnage.points_de_stats
            xp_necessaire = self.personnage.calculer_xp_necessaire()
            self.personnage.gagner_experience(xp_necessaire)
            # Vérifier que la force a augmenté et les points ont été déduits
            self.assertEqual(self.personnage.force, force_avant + 2)
            self.assertEqual(self.personnage.points_de_stats, points_avant + 5 - 1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False) 