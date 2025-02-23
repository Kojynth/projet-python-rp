from src.database.bddmanager import DatabaseManager
from src.core.personnage import Personnage
from src.database.RacesJoueur_manager import RacesManager
from src.database.ClasseJoueur_manager import ClassesManager
from src.database.connexion import DatabaseConnection

class CreationPersonnage:
    def __init__(self):
        self.alignements = [
            "Loyal Bon", "Neutre Bon", "Chaotique Bon",
            "Loyal Neutre", "Neutre", "Chaotique Neutre",
            "Loyal Mauvais", "Neutre Mauvais", "Chaotique Mauvais"
        ]
        self.orientations = [
            "Hétérosexuel(le)", "Homosexuel(le)", "Bisexuel(le)", 'Autres', "Asexuel(le)"   
        ]
        self.sexes = ["Masculin", "Féminin", "Trans"]
        
        # Initialisation des managers
        self.races_manager = RacesManager()
        self.classes_manager = ClassesManager()

        self.db_connection = DatabaseConnection()

    def afficher_races_disponibles(self):
        """Affiche les races disponibles"""
        races = self.races_manager.get_all_races()
        print("\nRaces disponibles:")
        for race in races:
            print(f"{race['race_id']}. {race['name']} ({race['category']})")
            print(f"   {race['description']}")
            stats = []
            if race['hp']: stats.append(f"HP: {race['hp']}")
            if race['mp']: stats.append(f"MP: {race['mp']}")
            if race['force']: stats.append(f"Force: {race['force']}")
            if race['defense']: stats.append(f"Défense: {race['defense']}")
            if race['magie']: stats.append(f"Magie: {race['magie']}")
            if race['resistance']: stats.append(f"Résistance: {race['resistance']}")
            if race['agilite']: stats.append(f"Agilité: {race['agilite']}")
            print(f"   Stats: {', '.join(stats)}")

    def afficher_classes_disponibles(self):
        """Affiche les classes disponibles"""
        classes = self.classes_manager.get_all_classes()
        print("\nClasses disponibles:")
        for classe in classes:
            print(f"{classe['class_id']}. {classe['name']} ({classe['category']})")
            print(f"   {classe['description']}")
            stats = []
            if classe['hp']: stats.append(f"HP: {classe['hp']}")
            if classe['mp']: stats.append(f"MP: {classe['mp']}")
            if classe['force']: stats.append(f"Force: {classe['force']}")
            if classe['defense']: stats.append(f"Défense: {classe['defense']}")
            if classe['magie']: stats.append(f"Magie: {classe['magie']}")
            if classe['resistance']: stats.append(f"Résistance: {classe['resistance']}")
            if classe['agilite']: stats.append(f"Agilité: {classe['agilite']}")
            print(f"   Stats: {', '.join(stats)}")

    def afficher_alignements(self):
        print("\n=== Alignements disponibles ===")
        for i, alignement in enumerate(self.alignements, 1):
            print(f"{i}. {alignement}")

    def get_default_values(self, race_dict):
        """Retourne les valeurs par défaut selon la race"""
        defaults = {
            "orientation": "Hétérosexuel(le)",
            "sexe": "Non spécifié",
            "taille": None,
            "poids": None
        }
        
        # Définition des plages de taille et poids selon la race
        race_ranges = {
            "Humain": {
                "taille": (130, 250),
                "poids": (30, 150)
            },
            "Nain": {
                "taille": (80, 140),
                "poids": (40, 180)
            },
            "Elfe": {
                "taille": (130, 200),
                "poids": (30, 100)
            },
            "Argonien": {
                "taille": (130, 250),
                "poids": (80, 250)
            },
            "Vampire": {
                "taille": (130, 250),
                "poids": (60, 150)
            },
            "Loup-Garou": {
                "taille": (190, 300),
                "poids": (90, 250)
            },
            "Youkai": {
                "taille": (20, 500),
                "poids": (0, 0)
            },
            "Squelette": {
                "taille": (20, 500),
                "poids": (10, 50)
            }
        }
        
        race_name = race_dict['name']  # Utiliser le nom de la race depuis le dictionnaire
        if race_name in race_ranges:
            import random
            taille_min, taille_max = race_ranges[race_name]["taille"]
            poids_min, poids_max = race_ranges[race_name]["poids"]
            
            defaults["taille"] = round(random.uniform(taille_min, taille_max), 1)
            defaults["poids"] = round(random.uniform(poids_min, poids_max), 1)
        
        return defaults

    def get_race_limits(self, race_dict):
        """Retourne les limites de taille et poids selon la race"""
        race_limits = {
            "Humain": {
                "taille": (130, 250),
                "poids": (30, 150),
                "message": "Pour un Humain, la taille doit être entre 130 et 250 cm et le poids entre 30 et 150 kg"
            },
            "Nain": {
                "taille": (80, 140),
                "poids": (40, 180),
                "message": "Pour un Nain, la taille doit être entre 80 et 140 cm et le poids entre 40 et 180 kg"
            },
            "Elfe": {
                "taille": (130, 200),
                "poids": (30, 100),
                "message": "Pour un Elfe, la taille doit être entre 130 et 200 cm et le poids entre 30 et 100 kg"
            },
            "Argonien": {
                "taille": (130, 250),
                "poids": (80, 250),
                "message": "Pour un Argonien, la taille doit être entre 130 et 250 cm et le poids entre 80 et 250 kg"
            },
            "Vampire": {
                "taille": (130, 250),
                "poids": (60, 150),
                "message": "Pour un Vampire, la taille doit être entre 130 et 250 cm et le poids entre 60 et 150 kg"
            },
            "Loup-Garou": {
                "taille": (190, 300),
                "poids": (90, 250),
                "message": "Pour un Loup-Garou, la taille doit être entre 190 et 300 cm et le poids entre 90 et 250 kg"
            },
            "Youkai": {
                "taille": (20, 500),
                "poids": (0, 0),
                "message": "Pour un Youkai, la taille doit être entre 20 et 500 cm et le poids entre 0 et 0 kg"
            },
            "Squelette": {
                "taille": (20, 500),
                "poids": (10, 50),
                "message": "Pour un Squelette, la taille doit être entre 20 et 500 cm et le poids entre 10 et 50 kg"
            }
        }
        return race_limits.get(race_dict['name'])  # Utiliser le nom de la race depuis le dictionnaire

    def valider_nom(self, texte):
        """Valide que le texte contient au moins 3 caractères alphabétiques"""
        if not texte or len(texte.strip()) < 3:
            return False
        return texte.isalpha()

    def demander_nom_valide(self, message):
        """Demande un nom valide à l'utilisateur avec le message spécifié"""
        while True:
            print("\n" + "=" * len(message))
            print(message)
            print("=" * len(message))
            print("Le nom doit contenir au moins 3 lettres, sans chiffres ni caractères spéciaux.")
            
            valeur = input("Votre choix: ").strip()
            
            if self.valider_nom(valeur):
                return valeur.capitalize()
            else:
                print("\nNom invalide! Veuillez réessayer.")
                print("Le nom doit contenir uniquement des lettres et faire au moins 3 caractères.")

    def creer_personnage(self):
        """Interface de création de personnage"""
        # Demande du prénom
        while True:
            prenom = input("\n Quel est le prénom de votre personnage ? ")
            if self.valider_nom(prenom):
                break
            print("\nPrénom invalide! Veuillez réessayer.")
            print("Le prénom doit contenir uniquement des lettres et faire au moins 3 caractères.")

        # Demande du nom
        while True:
            nom = input("\nQuel est le nom de votre personnage ?")
            if self.valider_nom(nom):
                break
            print("\nNom invalide! Veuillez réessayer.")
            print("Le nom doit contenir uniquement des lettres et faire au moins 3 caractères.")

        # Choix du sexe
        print("\nChoisissez le sexe de votre personnage:")
        for i, sexe in enumerate(self.sexes, 1):
            print(f"{i}. {sexe}")
        
        while True:
            try:
                choix_sexe = int(input("Choisissez le sexe (numéro): "))
                if 1 <= choix_sexe <= len(self.sexes):
                    sexe = self.sexes[choix_sexe - 1]
                    break
                print("Choix invalide, veuillez réessayer.")
            except ValueError:
                print("Veuillez entrer un numéro valide!")

        # Choix de la race
        self.afficher_races_disponibles()
        while True:
            try:
                race_id = int(input("\nChoisissez votre race (entrez le numéro): "))
                race = self.races_manager.get_race_by_id(race_id)
                if race:
                    break
                print("Race invalide, veuillez réessayer.")
            except ValueError:
                print("Veuillez entrer un numéro valide!")

        # Choix de la classe
        self.afficher_classes_disponibles()
        while True:
            try:
                classe_id = int(input("\nChoisissez votre classe (entrez le numéro): "))
                if 1 <= classe_id <= len(self.classes_manager.get_all_classes()):
                    classe = self.classes_manager.get_all_classes()[classe_id-1]
                    break
                print("Choix invalide!")
            except ValueError:
                print("Veuillez entrer un numéro valide!")

        # Choix de l'alignement
        self.afficher_alignements()
        while True:
            try:
                choix_alignement = int(input("Choisissez un alignement (numéro): "))
                if 1 <= choix_alignement <= len(self.alignements):
                    alignement = self.alignements[choix_alignement-1]
                    break
                print("Choix invalide!")
            except ValueError:
                print("Veuillez entrer un numéro valide!")

        # Détails optionnels
        details = input("\nSouhaitez-vous ajouter des détails supplémentaires? (oui/non): ").lower()
        orientation = taille = poids = None
        
        if details == "oui":
            # Choix de l'orientation
            print("\n=== Orientation ===")
            for i, ori in enumerate(self.orientations, 1):
                print(f"{i}. {ori}")
            while True:
                try:
                    choix_ori = int(input("Choisissez une orientation (numéro): "))
                    if 1 <= choix_ori <= len(self.orientations):
                        orientation = self.orientations[choix_ori-1]
                        break
                    print("Choix invalide!")
                except ValueError:
                    print("Veuillez entrer un numéro valide!")

            # Taille et poids
            while True:
                try:
                    race_limits = self.get_race_limits(race)
                    taille = float(input("Taille (en cm): "))
                    if race_limits["taille"][0] <= taille <= race_limits["taille"][1]:
                        break
                    print(race_limits["message"])
                except ValueError:
                    print("Veuillez entrer un nombre valide!")

            while True:
                try:
                    poids = float(input("Poids (en kg): "))
                    if race_limits["poids"][0] <= poids <= race_limits["poids"][1]:
                        break
                    print(race_limits["message"])
                except ValueError:
                    print("Veuillez entrer un nombre valide!")

        # Si l'utilisateur n'a pas spécifié ces valeurs
        if not taille or not poids or not orientation or not sexe:
            default_values = self.get_default_values(race)
            
            if not taille:
                taille = default_values["taille"]
            if not poids:
                poids = default_values["poids"]
            if not orientation:
                orientation = default_values["orientation"]
            if not sexe:
                sexe = default_values["sexe"]

        # Création du personnage niveau 1 avec le nom complet et le sexe
        nouveau_personnage = Personnage(
            id=None,  # Sera généré par la BDD
            pseudo=f"{prenom} {nom}",  # Combinaison du prénom et du nom
            hp=race['hp'] + classe['hp'],
            hp_total=race['hp'] + classe['hp'],
            mana=race['mp'] + classe['mp'],
            mana_total=race['mp'] + classe['mp'],
            force=race['force'] + classe['force'],
            defense=race['defense'] + classe['defense'],
            magie=race['magie'] + classe['magie'],
            resistance=race['resistance'] + classe['resistance'],
            agilite=race['agilite'] + classe['agilite'],
            niveau=1,  # Niveau initial
            points_de_stats=0,
            experience=0,
            race_id=race['race_id'],
            classe_id=classe['class_id'],
            sexe=sexe,  # Ajout du sexe
            alignement=alignement,
            orientation=orientation,
            taille=taille,
            poids=poids
        )

        # Sauvegarde dans la BDD
        with self.db_connection as cursor:
            cursor.execute('''
                INSERT INTO Personnage (
                    pseudo, hp, hp_total, mana, mana_total,
                    force, defense, magie, resistance, agilite,
                    niveau, points_de_stats, experience,
                    race_id, classe_id, sexe, alignement, orientation, taille, poids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nouveau_personnage.pseudo, nouveau_personnage.hp,
                nouveau_personnage.hp_total, nouveau_personnage.mana,
                nouveau_personnage.mana_total, nouveau_personnage.force,
                nouveau_personnage.defense, nouveau_personnage.magie,
                nouveau_personnage.resistance, nouveau_personnage.agilite,
                nouveau_personnage.niveau, nouveau_personnage.points_de_stats,
                nouveau_personnage.experience, nouveau_personnage.race_id,
                nouveau_personnage.classe_id, nouveau_personnage.sexe,
                nouveau_personnage.alignement, nouveau_personnage.orientation,
                nouveau_personnage.taille, nouveau_personnage.poids
            ))
            
            # Récupération de l'ID généré
            cursor.execute('SELECT last_insert_rowid()')
            nouveau_personnage.id = cursor.fetchone()[0]

        print("\nPersonnage créé avec succès!")
        return nouveau_personnage 