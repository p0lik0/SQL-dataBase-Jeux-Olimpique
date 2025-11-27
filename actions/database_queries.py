# Fonction permettant lister les épreuves d'une discipline donnée
def liste_epreuves(data, discipline):
    print("\nListe des épreuves de " + discipline + " :")
    try:
        cursor = data.cursor()
        result = cursor.execute(
            """
                SELECT DISTINCT nomEp, formeEp
                FROM V1_LesEpreuves
                WHERE nomDi = ?
                ORDER BY nomEp
            """,
            [discipline])
    except Exception as e:
        print("Impossible d'afficher les résultats : " + repr(e))
    else:
        for epreuve in result:
            print(epreuve[0] + " - " + epreuve[1])