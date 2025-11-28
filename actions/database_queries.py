# Fonction permettant lister les épreuves d'une discipline donnée
# def liste_epreuves(data, discipline):
#     print("\nListe des épreuves de " + discipline + " :")
#     try:
#         cursor = data.cursor()
#         result = cursor.execute(
#             """
#                 SELECT DISTINCT nomEp, formeEp
#                 FROM V1_LesEpreuves
#                 WHERE nomDi = ?
#                 ORDER BY nomEp
#             """,
#             [discipline])
#     except Exception as e:
#         print("Impossible d'afficher les résultats : " + repr(e))
#     else:
#         for epreuve in result:
#             print(epreuve[0] + " - " + epreuve[1])

def LesAgesSportifs(data):
    print("\nLes ages de sportifs :")
    try:
        cursor = data.cursor()
        result = cursor.execute(
            """
                SELECT * FROM LesAgesSportifs
            """)
    except Exception as e:
        print("Impossible d'afficher les ages : " + repr(e))
    else:
        for row in result:
            print(row[0],row[1],row[2],row[3],"(",row[4],")",row[5],row[6],"ans")

def LesNbsEquipiers(data):
    print("\nLes nmbr d'équipiers par équipe :")
    try:
        cursor = data.cursor()
        result = cursor.execute(
            """
                SELECT * FROM LesNbsEquipiers
            """)
    except Exception as e:
        print("Impossible d'afficher les nmbr d'équipiers par équipe  : " + repr(e))
    else:
        for row in result:
            print("Groupe",row[0]," - ",row[1], "sportifs")

def AgeMoyEqOr(data):
    try:
        cursor = data.cursor()
        result = cursor.execute(
            """
                SELECT * FROM AgeMoyEqOr
            """)
    except Exception as e:
        print("Impossible d'afficher l'age moyen : " + repr(e))
    else:
        for row in result:
            print("Age moyen :",row[0], "ans")

def ClassementPays(data):
    print("\nClassement des pays selon leur nombre de médailles :")
    try:
        cursor = data.cursor()
        result = cursor.execute(
            """
                SELECT * FROM ClassementPays
            """)
    except Exception as e:
        print("Impossible d'afficher le classement des pays selon leur nombre de médailles: " + repr(e))
    else:
        for row in result:
            print(row[0], "- ", row[1], "(or)", row[2], "(argent)", row[3], "(bronze)")