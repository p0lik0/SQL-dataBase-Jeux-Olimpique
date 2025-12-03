import sqlite3, pandas
from sqlite3 import IntegrityError

# Fonction permettant de lire le fichier Excel des JO et d'insérer les données dans la base
def read_excel_file_V0(data:sqlite3.Connection, file):
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête

    df_sportifs = pandas.read_excel(file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')
    df_sportifs = df_sportifs.drop_duplicates(subset=['numSp'])

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert into V1_LesSportifs values ({},'{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Lecture de l'onglet LesEpreuves du fichier excel, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert into V1_LesEpreuves values ({},'{}','{}','{}','{}',".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['categorieEp'], row['nbSportifsEp'])

            if row['dateEp'] != 'null':
                query = query + "'{}')".format(row['dateEp'])
            else:
                query = query + "null)"
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    # Supprimer les doublons sur la colonne numEq
    df_sportifs_sans_dupl_numEq = df_sportifs.drop_duplicates(subset=['numEq'])

    cursor = data.cursor()
    for ix, row in df_sportifs_sans_dupl_numEq.iterrows():
        try:
            if row['numEq']!='null':
                query = "insert into V1_LesEq values ({})".format(row['numEq'])
                print(query)
                cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    # cursor = data.cursor()
    # cursor.execute("SELECT * FROM V1_LesEq;")
    # print(cursor.fetchall())
    for ix, row in df_sportifs.iterrows():
        try:
            if row['numEq']!='null' and row['numEq']!='nan':
                query ="insert into V1_CompositionEq(numSp,numEq) values ({},{})".format(
                    row['numSp'], row['numEq'])
                print(query)
                cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    df_nomDi_nomEp = df_epreuves.drop_duplicates(subset=['nomDi', 'nomEp'])

    cursor = data.cursor()
    for ix, row in df_nomDi_nomEp.iterrows():
        try:
            query = "insert into V1_LesDisciplines values ('{}','{}')".format(row['nomDi'], row['nomEp'])
            print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    df_inscriptions = pandas.read_excel(file, sheet_name='LesInscriptions', dtype=str)
    df_resultats = pandas.read_excel(file, sheet_name='LesResultats', dtype=str)
    df_inscriptions_indiv = df_inscriptions[df_inscriptions['numIn'].isin(df_sportifs['numSp'])]
    # Résultats en format long : (numEp, typeM, numSp)
    df_results_long = df_resultats.melt(
        id_vars=['numEp'],
        value_vars=['gold','silver','bronze'],
        var_name='typeMedaille',
        value_name='numSp'
    )

    # Jointure sur numEp pour garder tous les inscrits
    df_participations_indiv = pandas.merge(
        df_inscriptions_indiv,
        df_results_long,
        left_on=['numIn','numEp'],
        right_on=['numSp','numEp'],
        how='left'   # on garde tous les inscrits, si il n y a pas de medaille correspondant, on met NULL dans typeMedaille
    )
    df_participations_indiv = df_participations_indiv.where(pandas.notnull(df_participations_indiv), 'null')
    # df_participations_indiv = df_participations_indiv.drop_duplicates(subset=['numEp','numSp'])

    for ix, row in df_participations_indiv.iterrows():
        try :
                valMedaille = "NULL" if row['typeMedaille']=='null' else f"'{row['typeMedaille']}'"
                query = "insert into V1_ParticipationsIndiv values ({},{},{})".format(
                    row['numEp'], row['numIn'], valMedaille
                )
                print(query)
                cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    df_inscriptions_eq = df_inscriptions[df_inscriptions['numIn'].isin(df_sportifs_sans_dupl_numEq['numEq'])]
    
    # Jointure sur numEp pour garder tous les inscrits
    df_participations_eq = pandas.merge(
        df_inscriptions_eq,
        df_results_long,
        left_on=['numIn','numEp'],
        right_on=['numSp','numEp'],
        how='left'   # on garde tous les inscrits, si il n y a pas de medaille correspondant, on met NULL dans typeMedaille
    )
    df_participations_eq = df_participations_eq.where(pandas.notnull(df_participations_eq), 'null')

    for ix, row in df_participations_eq.iterrows():
        try :
                valMedaille = "NULL" if row['typeMedaille']=='null' else f"'{row['typeMedaille']}'"
                query = "insert into V1_ParticipationsEq values ({},{},{})".format(
                    row['numEp'], row['numIn'], valMedaille
                )
                print(query)
                cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    