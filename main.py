import sqlite3
from actions import database_functions
from actions import database_queries

# Connexion à la base de données
data = sqlite3.connect("data/jo.db")

# Fonction permettant de quitter le programme
def quitter():
    print("Au revoir !")
    exit(0)

# Association des actions aux fonctions
actions = {
    "1": lambda: database_functions.database_create(data),
    "2": lambda: database_functions.database_insert(data),
    "3": lambda: database_functions.database_delete(data),
    # "4": lambda: database_queries.liste_epreuves(data, "Ski alpin"),
    "4": lambda: database_queries.LesAgesSportifs(data),
    "5": lambda: database_queries.LesNbsEquipiers(data),
    "6": lambda: database_queries.AgeMoyEqOr(data),
    "7": lambda: database_queries.ClassementPays(data),
    "q": quitter
}

# Fonctions d'affichage du menu
def menu():
    print("\n=== Menu principal ===")
    print("1 - Créer la base de données")
    print("2 - Insérer les données du fichier Excel")
    print("3 - Supprimer la base de données")
    # print("4 - Liste des épreuves de ski alpin")
    print("4 - Liste des les ages de sportifs")
    print("5 - Liste des nmbr d'équipiers par équipe")
    print("6 - L'age moyen des équipes qui ont gagné une médaille d'or")
    print("7 - Classement des pays selon leur nombre de médailles ")
    print("q - Quitter")

# Fonction principale
def main():
     # Appel du menu en boucle et gestion du choix
    while True:
        menu()
        choix = input("Votre choix : ").strip()
        action = actions.get(choix)
        if action:
            action()
        else:
            print("Choix invalide.")

# Appel de la fonction principale
main()