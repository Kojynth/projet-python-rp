import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
from src.core.personnage import Personnage
from src.core.adversaire import Adversaire
from src.combat.combat import boucle_combat
from src.database.bddmanager import DatabaseManager, creer_base_de_donnees
from src.core.gestion_stats import attribuer_points_apres_niveau
from src.items.item import Item

class TestMannequinEntrainement(unittest.TestCase):
    def setUp(self):
        """Initialisation avant chaque test"""
        # Créer et initialiser la base de données
        creer_base_de_donnees()
        
        # Créer un personnage de test si la BDD est vide
        with DatabaseManager() as cursor:
            cursor.execute('SELECT COUNT(*) FROM Personnage')
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Créer un personnage de test
                self.personnage_test = Personnage(
                    id=1,
                    pseudo="Hero1",
                    hp=100, hp_total=100,
                    mana=50, mana_total=50,
                    force=20, defense=10,
                    magie=15, resistance=10,
                    agilite=12, niveau=1,
                    points_de_stats=0,
                    experience=0
                )
                
                # Sauvegarder dans la BDD
                cursor.execute('''
                    INSERT INTO Personnage (id, pseudo, hp, hp_total, mana, mana_total, 
                    force, defense, magie, resistance, agilite, niveau, points_de_stats, experience)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.personnage_test.id, self.personnage_test.pseudo, 
                      self.personnage_test.hp, self.personnage_test.hp_total,
                      self.personnage_test.mana, self.personnage_test.mana_total,
                      self.personnage_test.force, self.personnage_test.defense,
                      self.personnage_test.magie, self.personnage_test.resistance,
                      self.personnage_test.agilite, self.personnage_test.niveau,
                      self.personnage_test.points_de_stats, self.personnage_test.experience))
        
        # Charger Hero1 depuis la BDD
        with DatabaseManager() as cursor:
            cursor.execute('SELECT * FROM Personnage WHERE pseudo = "Hero1"')
            row = cursor.fetchone()
            if row:
                self.hero = Personnage(
                    id=row[0], pseudo=row[1],
                    hp=row[2], hp_total=row[3],
                    mana=row[4], mana_total=row[5],
                    force=row[6], defense=row[7],
                    magie=row[8], resistance=row[9],
                    agilite=row[10], niveau=row[11],
                    points_de_stats=row[12], experience=row[13]
                )
        
        # Créer un mannequin d'entraînement initial
        self.mannequin = Adversaire(
            id=999,
            pseudo="Mannequin d'entraînement XP",
            hp=1, hp_total=1,
            mana=0, mana_total=0,
            force=0, defense=0,
            magie=0, resistance=0,
            agilite=0,
            niveau=1,
            experience=10
        )

    def test_entrainement_xp(self):
        """Test d'entraînement contre des mannequins avec XP croissante"""
        print("\n=== Début de l'entraînement ===")
        print(f"\nPersonnage actuel: {self.hero.pseudo} (Niveau {self.hero.niveau})")
        
        # Proposer le reset du niveau
        while True:
            choix_reset = input("\nVoulez-vous réinitialiser le niveau et les stats du héros? (oui/non): ").lower()
            if choix_reset == "oui":
                # Reset des stats
                self.hero.niveau = 1
                self.hero.experience = 0
                self.hero.hp = 100
                self.hero.hp_total = 100
                self.hero.mana = 50
                self.hero.mana_total = 50
                self.hero.force = 20
                self.hero.defense = 10
                self.hero.magie = 15
                self.hero.resistance = 10
                self.hero.agilite = 12
                self.hero.points_de_stats = 0
                
                # Sauvegarder le reset dans la BDD
                with DatabaseManager() as cursor:
                    cursor.execute('''
                        UPDATE Personnage 
                        SET niveau=1, experience=0,
                            hp=100, hp_total=100,
                            mana=50, mana_total=50,
                            force=20, defense=10,
                            magie=15, resistance=10,
                            agilite=12, points_de_stats=0
                        WHERE id=?
                    ''', (self.hero.id,))
                print("\nPersonnage réinitialisé au niveau 1!")
                break
            elif choix_reset == "non":
                print("\nContinuation avec le niveau actuel.")
                break
            else:
                print("Veuillez répondre par 'oui' ou 'non'")
        
        print("\nÉtat initial:")
        self.hero.afficher_fiche()
        
        xp_accumulee = 0
        combat_count = 1
        
        while True:
            print(f"\nCombat {combat_count} contre un mannequin donnant {self.mannequin.experience} XP")
            print(f"XP accumulée: {xp_accumulee}")
            print("(Entrez 410 pour arrêter l'entraînement)")
            
            # Créer les équipes
            equipe_joueur = [self.hero]
            equipe_mannequin = [self.mannequin]
            liste_combattants = equipe_joueur + equipe_mannequin
            
            # Vérifier si on veut arrêter
            choix = input("Votre choix (410 pour quitter): ")
            if choix == "410":
                print("\nFin de l'entraînement!")
                print(f"\nXP totale accumulée: {xp_accumulee}")
                
                # Appliquer l'XP et proposer d'attribuer les points
                niveau_initial = self.hero.niveau
                self.hero.gagner_experience(xp_accumulee)
                
                # Si le personnage a gagné au moins un niveau
                if self.hero.niveau > niveau_initial:
                    attribuer_points_apres_niveau(self.hero)
                break
            
            # Lancer le combat
            boucle_combat(liste_combattants, equipe_joueur, equipe_mannequin)
            
            # Accumuler l'XP sans monter de niveau
            xp_accumulee += self.mannequin.experience
            
            # Augmenter l'XP du prochain mannequin
            self.mannequin.experience += 12
            
            # Réinitialiser les HP du mannequin pour le prochain combat
            self.mannequin.hp = 1
            
            print("\nÉtat actuel:")
            print(f"XP accumulée: {xp_accumulee}")
            self.hero.afficher_fiche()
            
            combat_count += 1

        # Sauvegarder l'état final du héros dans la BDD
        with DatabaseManager() as cursor:
            cursor.execute('''
                UPDATE Personnage 
                SET hp=?, hp_total=?, mana=?, mana_total=?, 
                    force=?, defense=?, magie=?, resistance=?, agilite=?,
                    niveau=?, points_de_stats=?, experience=?
                WHERE id=?
            ''', (self.hero.hp, self.hero.hp_total, 
                  self.hero.mana, self.hero.mana_total,
                  self.hero.force, self.hero.defense, 
                  self.hero.magie, self.hero.resistance, 
                  self.hero.agilite, self.hero.niveau,
                  self.hero.points_de_stats, self.hero.experience,
                  self.hero.id))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False) 