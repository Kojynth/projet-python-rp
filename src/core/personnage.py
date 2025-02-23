from src.database.bddmanager import sauvegarder_objets, charger_donnees
from src.core.ressources import *

class Personnage:
    def __init__(self, id, pseudo, hp, hp_total, mana, mana_total, force, defense, magie, 
                 resistance, agilite, niveau=1, points_de_stats=0, experience=0, 
                 race_id=None, classe_id=None, sexe=None, alignement=None, 
                 orientation=None, taille=None, poids=None):
        """Initialise un personnage avec ses attributs"""
        self.id = id
        self.pseudo = pseudo
        self.hp = hp
        self.hp_total = hp_total
        self.mana = mana
        self.mana_total = mana_total
        self.force = force
        self.defense = defense
        self.magie = magie
        self.resistance = resistance
        self.agilite = agilite
        self.niveau = niveau
        self.points_de_stats = points_de_stats
        self.experience = experience
        self.race_id = race_id
        self.classe_id = classe_id
        self.sexe = sexe
        self.alignement = alignement
        self.orientation = orientation
        self.taille = taille
        self.poids = poids
        self.degats_infliges = 0  # Pour le suivi des dégâts

    def calculer_hp(self):
        """
        Calcule les HP totaux du personnage en fonction de son niveau.

        Retourne la différence entre les anciens et les nouveaux HP totaux.
        """
        ancien_hp_total = self.hp_total
        hp_total = self.hp
        if self.niveau >= 2:
            hp_total += 75 * min(self.niveau - 1, 9)
        hp_par_niveau = 90
        if self.niveau >= 11:
            for i in range(11, self.niveau + 1):
                hp_total += hp_par_niveau
                if i % 10 == 0:
                    hp_par_niveau += 15

        self.hp_total = hp_total
        return hp_total - ancien_hp_total

    def calculer_stat(self):
        """
        Calcule les points de stats totaux du personnage en fonction de son niveau.

        Retourne la différence entre les anciens et les nouveaux points de stats totaux.
        """
        ancien_stat_total = self.points_de_stats
        stat_total = 0  # Variable pour accumuler les points de stats

        # Initialiser les points de stats par niveau
        stat_par_niveau = 5

        for i in range(2, self.niveau + 1):  # On commence à partir du niveau 2
            stat_total += stat_par_niveau  # Ajouter les points de stats pour ce niveau

            # Augmenter les points de stats tous les 20 niveaux
            if i % 20 == 0:
                stat_par_niveau += 5

        self.points_de_stats = stat_total
        return stat_total - ancien_stat_total

    def calculer_gain_hp(self):
        """
        Calcule le gain de HP en fonction du niveau
        Returns:
            int: Nombre de HP à gagner pour le niveau actuel
        """
        tranche = (self.niveau - 1) // 10
        gain_hp = 75 + (tranche * 15)
        return gain_hp

    def calculer_xp_necessaire(self):
        """
        Calcule l'expérience nécessaire pour le prochain niveau
        Returns:
            int: Quantité d'XP nécessaire
        """
        return (self.niveau + 1) * 10  # Revenir à la formule originale

    def calculer_gain_mana(self):
        """
        Calcule le gain de mana en fonction du niveau
        Returns:
            int: Nombre de points de mana à gagner
        """
        if self.niveau <= 100:
            return 20  # 20 mana par niveau jusqu'au niveau 100
        else:
            return 5   # 5 mana par niveau après le niveau 100

    def monter_niveau(self):
        """Gère la montée de niveau du personnage"""
        # Gain de HP selon le niveau
        gain_hp = self.calculer_gain_hp()
        self.hp_total += gain_hp
        self.hp += gain_hp

        # Gain de Mana selon le niveau
        gain_mana = self.calculer_gain_mana()
        self.mana_total += gain_mana
        self.mana += gain_mana

        # Gain de points de stats selon le niveau
        gain_stats = self.calculer_gain_points_stats()
        self.points_de_stats += gain_stats

        # Augmentation du niveau
        self.niveau += 1
        
        # Afficher les gains
        print(f"\n{self.pseudo} atteint le niveau {self.niveau}!")
        print(f"Gain de {gain_hp} HP!")
        print(f"Gain de {gain_mana} Mana!")
        print(f"Gain de {gain_stats} points de statistiques!")

        # Proposer d'attribuer les points maintenant
        choix = input("\nVoulez-vous attribuer vos points de stats maintenant? (o/n): ")
        if choix.lower() == 'o':
            self.menu_attribution_points()
        else:
            print(f"Vous avez {self.points_de_stats} points de stats en réserve.")

        print(f"XP nécessaire pour le niveau suivant: {self.calculer_xp_necessaire()}")

    def gagner_experience(self, experience_gagnee):
        """
        Gère le gain d'expérience et la montée de niveau
        Args:
            experience_gagnee (int): Quantité d'expérience gagnée
        """
        niveau_initial = self.niveau
        self.experience += experience_gagnee
        
        while self.experience >= self.calculer_xp_necessaire():
            xp_necessaire = self.calculer_xp_necessaire()
            self.experience -= xp_necessaire
            self.niveau += 1
            
            # Gain de HP
            gain_hp = self.calculer_gain_hp()
            self.hp_total += gain_hp
            self.hp += gain_hp
            
            # Gain de Mana
            gain_mana = self.calculer_gain_mana()
            self.mana_total += gain_mana
            self.mana += gain_mana
            
            # Gain de points de stats selon le niveau
            gain_stats = self.calculer_gain_points_stats()
            self.points_de_stats += gain_stats

            print(f"\n{self.pseudo} atteint le niveau {self.niveau}!")
            print(f"Gain de {gain_hp} HP!")
            print(f"Gain de {gain_mana} Mana!")
            print(f"Gain de {gain_stats} points de statistiques!")
            print(f"XP nécessaire pour le niveau suivant: {self.calculer_xp_necessaire()}")
        
        # Si le personnage a gagné au moins un niveau, afficher sa fiche
        if self.niveau > niveau_initial:
            self.afficher_fiche()

    def afficher_fiche(self):
        """Affiche la fiche complète du personnage"""
        print(f"\n{'='*40}")
        print(f"Fiche de {self.pseudo} - Niveau {self.niveau}")
        print(f"{'='*40}")
        print(f"HP: {self.hp}/{self.hp_total}")
        print(f"Mana: {self.mana}/{self.mana_total}")
        print(f"Force: {self.force}")
        print(f"Défense: {self.defense}")
        print(f"Magie: {self.magie}")
        print(f"Résistance: {self.resistance}")
        print(f"Agilité: {self.agilite}")
        print(f"Points de stats disponibles: {self.points_de_stats}")
        xp_necessaire = self.calculer_xp_necessaire()
        print(f"Expérience: {self.experience}/{xp_necessaire}")
        print(f"{'='*40}\n")

    def afficher_fiche_lvlup(self, hp_gagnes, stats_gagnes):
        xp_restant = (self.niveau + 1) * 10 - self.experience
        print(f"Nom: {self.pseudo}")
        print(f"HP: {self.hp}/{self.hp_total} (+{hp_gagnes} HP gagnés)")
        print(f"Mana: {self.mana}/{self.mana_total}")
        print(f"Force: {self.force}/{self.force_total}")
        print(f"Defense: {self.defense}/{self.defense_total}")
        print(f"Magie: {self.magie}/{self.magie_total}")
        print(f"Résistance: {self.resistance}/{self.resistance_total}")
        print(f"Agilité: {self.agilite}/{self.agilite_total}")
        print(f"Niveau: {self.niveau}")
        print(f"Expérience: {self.experience} ({xp_restant} XP restant avant le lvl up)")
        print(f"Total des points de stats gagnés: {self.points_de_stats} (+{stats_gagnes} points de stats gagnés)")

    def afficher_fiche_stat_actuel(self):
        print(f"Nom: {self.pseudo}")
        print(f"HP: {self.hp}/{self.hp_total}")  # Affiche les HP actuels et les HP totaux
        print(f"Mana: {self.mana}/{self.mana_total}")
        print(f"Force: {self.force}")
        print(f"Defense: {self.defense}")
        print(f"Magie: {self.magie}")
        print(f"Résistance: {self.resistance}")
        print(f"Agilité: {self.agilite}")
        print(f"Niveau: {self.niveau}")
        print(f"Expérience: {self.experience}")
        print(f"Total des points de stats actuels: {self.points_de_stats}")  # Affiche les points de stats actuels

    def subir_attaque(self, degats):
        """Méthode qui gère les dégâts subis par le personnage"""
        self.hp = max(0, self.hp - degats)
        print(f"{self.pseudo} subit {degats} de dégâts. Il lui reste {self.hp} HP.")

        # Vérifier si le personnage est mort
        if self.hp <= 0:
            print(f"{self.pseudo} est mort !")

    def est_vivant(self):
        """
        Vérifie si le personnage est vivant
        Returns:
            bool: True si vivant, False sinon
        """
        return self.hp > 0

    def calculer_gain_points_stats(self):
        """
        Calcule le nombre de points de stats gagnés en fonction du niveau
        Returns:
            int: Nombre de points de stats à gagner
        
        Logique :
        - Niveaux 1-20 : 5 points par niveau
        - Niveaux 21-40 : 10 points par niveau
        - Niveaux 41-60 : 15 points par niveau
        - Niveaux 61-80 : 20 points par niveau
        - Niveaux 81-100 : 25 points par niveau
        etc.
        """
        # Déterminer la tranche de niveau (0 pour 1-20, 1 pour 21-40, etc.)
        tranche = (self.niveau - 1) // 20
        
        # Le gain de base est de 5 points, augmenté de 5 par tranche
        points_par_niveau = 5 * (tranche + 1)
        
        return points_par_niveau

    def augmenter_statistique(self, statistique):
        """
        Augmente la statistique choisie si des points sont disponibles
        Args:
            statistique (str): Nom de la statistique à augmenter
        Returns:
            bool: True si l'augmentation a réussi, False sinon
        """
        from src.core.gestion_stats import augmenter_statistique
        return augmenter_statistique(self, statistique)

    def menu_attribution_points(self):
        """Affiche le menu d'attribution des points de stats"""
        from src.core.gestion_stats import menu_attribution_points
        menu_attribution_points(self)

# Fonction pour charger les personnages depuis la base de données
def charger_personnages():
    return charger_donnees('Personnage', Personnage)

# Fonction pour sauvegarder les personnages dans la base de données
def sauvegarder_personnages(personnages):
    sauvegarder_objets('Personnage', personnages)
