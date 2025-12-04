CREATE TRIGGER CheckOnlyIndiv
BEFORE INSERT ON V1_ParticipationsIndiv
WHEN (SELECT formeEp FROM V1_LesEpreuves WHERE numEp = NEW.numEp)='par equipe'
BEGIN
  SELECT RAISE(ABORT, 'Cette épreuve est par équipe, pas de sportifs individuels autorisés');
END;/

CREATE TRIGGER CheckOnlyEq
BEFORE INSERT ON V1_ParticipationsEq
WHEN (SELECT formeEp FROM V1_LesEpreuves WHERE numEp = NEW.numEp)='individuelle'
BEGIN
  SELECT RAISE(ABORT, 'Cette épreuve est individuelle, pas d équipes autorisées');
END;/

CREATE TRIGGER CheckOnlyCouple
BEFORE INSERT ON V1_ParticipationsEq
WHEN (SELECT formeEp FROM V1_LesEpreuves WHERE numEp = NEW.numEp)='par couple'
  AND (SELECT nbEquipiersEq FROM LesNbsEquipiers WHERE numEq = NEW.numEq)!=2
BEGIN
  SELECT RAISE(ABORT, 'Cette épreuve est par couple, mais l effectif de cet equipe != 2');
END;/

CREATE TRIGGER CheckOnlyMenOnlyWomen
BEFORE INSERT ON V1_ParticipationsIndiv
WHEN ((SELECT categorieEp FROM V1_LesEpreuves WHERE numEp = NEW.numEp)='masculin'
  AND (SELECT categorieSp FROM V1_LesSportifs WHERE numSp = NEW.numSp)='feminin')
  OR ((SELECT categorieEp FROM V1_LesEpreuves WHERE numEp = NEW.numEp)='feminin'
  AND (SELECT categorieSp FROM V1_LesSportifs WHERE numSp = NEW.numSp)='masculin')
BEGIN
  SELECT RAISE(ABORT, 'La categorie de l epreuve n est pas compatible avec le sex du sportif');
END;/

-- triggers pour vérifier qu'un sportif n'est pas inscrit dans plusieurs équipes pour la même épreuve
CREATE TRIGGER trig_verif_sportif_unique_par_epreuve
BEFORE INSERT ON V1_CompositionEq
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT,'Le sportif est déjà inscrit dans une autre équipe pour cette épreuve')
    WHERE EXISTS (
        SELECT 1
        FROM V1_CompositionEq ce
        JOIN V1_ParticipationsEq pe ON ce.numEq = pe.numEq
        WHERE ce.numSp = NEW.numSp
          AND pe.numEp IN (
              SELECT numEp
              FROM V1_ParticipationsEq
              WHERE numEq = NEW.numEq
          )
          AND ce.numEq <> NEW.numEq
    );
END;/

CREATE TRIGGER CheckPaysSportifEq
BEFORE INSERT ON V1_CompositionEq
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT,'Les sportifs qui viennent de pays differents peuvent pas être dans la même équipe')
    WHERE EXISTS (
        SELECT 1 FROM V1_LesSportifs WHERE numSp IN (SELECT numSp FROM V1_CompositionEq WHERE numEq = NEW.numEq)
          AND pays != (SELECT pays FROM V1_LesSportifs WHERE numSp=NEW.numSp)
    );
END;/

CREATE TRIGGER trig_verif_2_equipiers_au_moins 
BEFORE INSERT ON V1_ParticipationsEq
WHEN (SELECT nbEquipiersEq FROM LesNbsEquipiers WHERE numEq=NEW.numEq)<2
BEGIN
    SELECT RAISE(ABORT,'L équipe doit avoir au moins 2 équipiers pour participer à une épreuve par équipe ou par couple');
END;/