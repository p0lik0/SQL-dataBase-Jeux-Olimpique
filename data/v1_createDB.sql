PRAGMA foreign_keys = ON;

CREATE TABLE V1_LesSportifs
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SP_PK PRIMARY KEY (numSp),
  CONSTRAINT SP_CK1 CHECK(numSp > 0),
  CONSTRAINT SP_CK2 CHECK(categorieSp IN ('feminin','masculin'))
);

CREATE TABLE V1_LesEpreuves
(
  numEp NUMBER(3),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  dateEp DATE,
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 0)
);

CREATE TABLE V1_LesEq
(
  numEq NUMBER(4),
  CONSTRAINT EQ_PK PRIMARY KEY (numEq),
  CONSTRAINT EQ_CK1 CHECK(numEq > 0)
);

CREATE TABLE V1_LesDisciplines
(
  nomDi VARCHAR2(25),
  nomEp NUMBER(3),
  CONSTRAINT DI_PK PRIMARY KEY (nomDi,nomEp)
  -- CONSTRAINT DI_FK FOREIGN KEY (numEp) REFERENCES V1_LesEpreuves(numEp)
);

CREATE TABLE V1_ParticipationsIndiv
(
  numEp NUMBER(3),
  numSp NUMBER(4),
  typeMedaille VARCHAR2(7),
  CONSTRAINT PI_PK PRIMARY KEY (numEp, numSp),
  CONSTRAINT PI_CK1 CHECK (typeMedaille IN ('gold','silver','bronze')),
  CONSTRAINT PI_FK1 FOREIGN KEY (numEp) REFERENCES V1_LesEpreuves(numEp),
  CONSTRAINT PI_FK2 FOREIGN KEY (numSp) REFERENCES V1_LesSportifs(numSp)
);

CREATE TABLE V1_ParticipationsEq
(
  numEp NUMBER(3),
  numEq NUMBER(4),
  typeMedaille VARCHAR2(7),
  CONSTRAINT PE_PK PRIMARY KEY (numEp, numEq),
  CONSTRAINT PE_CK1 CHECK (typeMedaille IN ('gold','silver','bronze')),
  CONSTRAINT PE_FK1 FOREIGN KEY (numEp) REFERENCES V1_LesEpreuves(numEp),
  CONSTRAINT PE_FK2 FOREIGN KEY (numEq) REFERENCES V1_LesEq(numEq)
);

CREATE TABLE V1_CompositionEq
(
  numEq NUMBER(4),
  numSp NUMBER(4),
  CONSTRAINT CE_PK PRIMARY KEY (numSp, numEq),
  CONSTRAINT CE_FK1 FOREIGN KEY (numEq) REFERENCES V1_LesEq(numEq),
  CONSTRAINT CE_FK2 FOREIGN KEY (numSp) REFERENCES V1_LesSportifs(numSp)
);

-- CREATE TABLE V1_Medailles
-- (
--   numEp NUMBER(3),
--   gold NUMBER(4),
--   silver NUMBER(4),
--   bronze NUMBER(4),
--   CONSTRAINT M_PK PRIMARY KEY (numEp),
-- )