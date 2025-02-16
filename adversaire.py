from bddmanager import sauvegarder_objets, charger_donnees

class Adversaire:
    def __init__(self, id, pseudo, hp, hp_total, mana, mana_total, attaque, niveaux, experience, points_de_stats=0):
        self.id = id
        self.pseudo = pseudo
        self.hp = hp  # HP actuels
        self.hp_total = hp_total  # HP totaux
        self.mana = mana  # Mana actuel
        self.mana_total = mana_total  # Mana total
        self.attaque = attaque
        self.niveaux = niveaux
        self.experience = experience
        self.points_de_stats = points_de_stats

    def attaquer(self, cible):
        """Méthode pour attaquer un autre adversaire"""
        print(f"{self.pseudo} attaque {cible.pseudo} avec {self.attaque} de dégâts.")
        cible.subir_attaque(self.attaque)

    def subir_attaque(self, degats):
        """Méthode qui permet à l'adversaire de subir une attaque"""
        self.hp = max(0, self.hp - degats)  # Ensure HP does not go below 0
        print(f"{self.pseudo} subit {degats} de dégâts. Il lui reste {self.hp} HP.")

        # Vérifier si l'adversaire est mort
        if self.hp <= 0:
            self.mourir()

    def mourir(self):
        """Méthode qui gère la mort de l'adversaire et déclenche un gain d'expérience pour l'équipe adverse"""
        print(f"{self.pseudo} est mort !")
        self.gagner_experience_adversaire()

    def gagner_experience_adversaire(self):
        """Attribution de l'XP pour toute l'équipe adverse au moment de la mort d'un adversaire"""
        print(f"{self.pseudo} déclenche un gain d'expérience pour l'équipe adverse.")
        if hasattr(self, 'equipe_adverse'):
            # Attribution de l'XP personnalisée par le développeur, ici on utilise l'expérience définie dans le constructeur
            xp_a_gagner = self.experience  # Utilisation de l'XP propre à chaque adversaire
            self.equipe_adverse.gagner_experience(xp_a_gagner)  # Attribution de l'XP à toute l'équipe

    def reinitialiser_stats(self):
        """Méthode pour réinitialiser les stats de l'adversaire après le combat"""
        self.hp = self.hp_total
        self.mana = self.mana_total
        self.experience = 0
        self.points_de_stats = 0

# Fonction pour ajouter des adversaires à la base de données
def ajouter_adversaires(adversaires):
    sauvegarder_objets('Adversaire', adversaires)

# Fonction pour sauvegarder les adversaires dans la base de données
def sauvegarder_adversaires(adversaires):
    sauvegarder_objets('Adversaire', adversaires)
