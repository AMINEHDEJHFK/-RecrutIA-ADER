-- RecrutIA ADER : export complet (structure + données de test), base SQLite recrut.db
-- Toutes les données sont fictives (candidats et évaluations de test).
-- Import : sqlite3 recrut.db < recrutia_dump.sql
BEGIN TRANSACTION;
CREATE TABLE candidat (
	id INTEGER NOT NULL, 
	nom VARCHAR(100), 
	prenom VARCHAR(100), 
	email VARCHAR(120), 
	telephone VARCHAR(20), 
	poste VARCHAR(50), 
	diplome VARCHAR(50), 
	specialite VARCHAR(100), 
	ecole VARCHAR(100), 
	promotion INTEGER, 
	experience INTEGER, 
	score_ia FLOAT, 
	decision VARCHAR(20), 
	decision_manuelle BOOLEAN, 
	decideur_manuel VARCHAR(150), 
	date_decision_manuelle DATETIME, 
	langues VARCHAR(200), 
	competences TEXT, 
	cv_filename VARCHAR(200), 
	date_depot DATETIME, 
	offre_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(offre_id) REFERENCES offre (id)
);
INSERT INTO "candidat" VALUES(1,'YOUSSEF','Alami','youssef.alami@gmail.com','0661234567','(01) Chef de projets Architecte','MASTER','Gestion des entreprises','ENCG',2024,9,0.5382,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',1);
INSERT INTO "candidat" VALUES(2,'SARA','Benali','sara.benali@gmail.com','0677890123','(01) Chef de projets Architecte','MASTER','Informatique','USMBA',2024,8,0.6738,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',1);
INSERT INTO "candidat" VALUES(3,'KARIM','Idrissi','karim.idrissi@gmail.com','0654321987','(01) Chef de projets Architecte','TECHNICIEN SPECIALISE','Informatique','ISTA',2024,8,0.3919,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',1);
INSERT INTO "candidat" VALUES(4,'AMINE SAGHIRI','Mohammed','candidat.test@recrutia-demo.local','','(01) Chef de projets Architecte','LICENCE','Générale','NEXA Digital School',2024,0,0.1745,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',1);
INSERT INTO "candidat" VALUES(5,'BENALI','Leila','leila.benali@gmail.com','0672345678','CGM','MASTER','Gestion des entreprises','Autre',2024,4,0.85,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(6,'RACHIDI','Omar','omar.rachidi@gmail.com','0683456789','CGM','MASTER','Finance','ENCG',2024,6,0.85,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(7,'TAZI','Mehdi','tazi.mehdi@gmail.com','0661234567','CGM','MASTER','Finance','ENCG',2024,5,0.85,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(8,'BERRADA','Younes','younes.berrada.pro@gmail.com','0661112233','Assistant Architecte','MASTER','Génie Civil et Architecture','École Hassania des Travaux Publics',2020,6,0.3413,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',4);
INSERT INTO "candidat" VALUES(9,'IDRISSI','Salma','salma.idrissi.cv@gmail.com','0662223344','Assistant Architecte','TECHNICIEN SPECIALISE','Dessin de Bâtiment','ISTA Fès',2024,1,0.12,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',4);
INSERT INTO "candidat" VALUES(10,'OUAZZANI','Karim','karim.ouazzani.pro@gmail.com','0663334455','Assistant Architecte','MASTER','Architecture et Urbanisme','École Supérieure d''Architecture de Fès',2022,2,0.3359,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',4);
INSERT INTO "candidat" VALUES(11,'CHARKI','Nadia','nadia.charki.pro@gmail.com','0664445566','Assistant Architecte','LICENCE','Marketing et Commerce International','ESTICE Business School',2020,5,0.0975,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',4);
INSERT INTO "candidat" VALUES(12,'AMRANI','Yassine','yassine.amrani.cv@gmail.com','0665556677','Assistant Architecte','BAC','Informatique et Intelligence Artificielle','Lycée Al Khawarizmi',2023,0,0.1191,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',4);
INSERT INTO "candidat" VALUES(13,'ZIANI','Imane','imane.ziani.pro@gmail.com','0666667788','Assistant Architecte','LICENCE','Marketing, Communication et Événementiel','INSEEC',2025,1,0.1483,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',4);
INSERT INTO "candidat" VALUES(14,'BERRADA','Younes','younes.berrada2@gmail.com','0661112233','CGM','MASTER','Génie Civil et Architecture','École Hassania des Travaux Publics',2020,6,0.8051,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(15,'IDRISSI','Salma','salma.idrissi2@gmail.com','0662223344','CGM','TECHNICIEN SPECIALISE','Dessin de Bâtiment','ISTA Fès',2024,1,0.1924,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(16,'OUAZZANI','Karim','karim.ouazzani2@gmail.com','0663334455','CGM','MASTER','Architecture et Urbanisme','École Supérieure d''Architecture de Fès',2022,4,0.8259,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(17,'CHARKI','Nadia','nadia.charki2@gmail.com','0664445566','CGM','LICENCE','Marketing et Commerce International','ESTICE Business School',2020,5,0.3238,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(18,'AMRANI','Yassine','yassine.amrani2@gmail.com','0665556677','CGM','BAC','Informatique et Intelligence Artificielle','Lycée Al Khawarizmi',2023,1,0.1832,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(19,'ZIANI','Imane','imane.ziani2@gmail.com','0666667788','CGM','LICENCE','Marketing, Communication et Événementiel','INSEEC',2025,3,0.3251,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(20,'AMRANI','Hind','hind.amrani.pro@gmail.com','0667778899','CGM','LICENCE','Architecture et Bâtiment','ISTA',2020,4,0.4628,'Présélectionné',1,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.323944',3);
INSERT INTO "candidat" VALUES(21,'FILALI','Kenza','kenza.filali@gmail.com','0661001001','Responsable Comptabilité','MASTER','Finance et Comptabilité','ENCG Fès',2021,4,0.87,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',5);
INSERT INTO "candidat" VALUES(22,'BENKIRANE','Hamza','hamza.benkirane@gmail.com','0662002002','Responsable Comptabilité','MASTER','Comptabilité et Audit','ISCAE Casablanca',2020,5,0.91,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',5);
INSERT INTO "candidat" VALUES(23,'ALAOUI','Rim','rim.alaoui@gmail.com','0663003003','Responsable Comptabilité','LICENCE','Sciences de Gestion','FSJES Fès',2023,1,0.38,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',5);
INSERT INTO "candidat" VALUES(24,'TAHIRI','Youssef','youssef.tahiri@gmail.com','0664004004','Responsable Comptabilité','MASTER','Finance d''Entreprise','UIR Rabat',2022,2,0.61,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',5);
INSERT INTO "candidat" VALUES(25,'MANSOURI','Anas','anas.mansouri@gmail.com','0665005005','Technicien Réseaux','TECHNICIEN SPECIALISE','Réseaux et Télécommunications','ISTA Fès',2023,2,0.78,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',6);
INSERT INTO "candidat" VALUES(26,'SQALLI','Meryem','meryem.sqalli@gmail.com','0666006006','Technicien Réseaux','LICENCE','Informatique et Réseaux','Université Sidi Mohamed',2022,3,0.82,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',6);
INSERT INTO "candidat" VALUES(27,'GUESSOUS','Bilal','bilal.guessous@gmail.com','0667007007','Technicien Réseaux','BAC','Sciences Mathématiques','Lycée Ibn Khaldoun',2024,0,0.12,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',6);
INSERT INTO "candidat" VALUES(28,'LAHRICHI','Sara','sara.lahrichi@gmail.com','0668008008','Technicien Réseaux','TECHNICIEN SPECIALISE','Développement Informatique','OFPPT Fès',2023,1,0.55,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',6);
INSERT INTO "candidat" VALUES(29,'CHRAIBI','Dounia','dounia.chraibi@gmail.com','0669009009','Juriste','MASTER','Droit des Affaires','Université Mohammed V',2021,4,0.88,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',7);
INSERT INTO "candidat" VALUES(30,'KETTANI','Omar','omar.kettani@gmail.com','0660010010','Juriste','MASTER','Droit Public','Université Cadi Ayyad',2022,3,0.79,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',7);
INSERT INTO "candidat" VALUES(31,'BENJELLOUN','Nour','nour.benjelloun@gmail.com','0661011011','Juriste','LICENCE','Droit Privé','FSJES Meknès',2024,0,0.31,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',7);
INSERT INTO "candidat" VALUES(32,'FASSI','Tarik','tarik.fassi@gmail.com','0662012012','Juriste','MASTER','Droit des Marchés Publics','ENA Rabat',2020,5,0.93,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',7);
INSERT INTO "candidat" VALUES(33,'TAZI','Lina','lina.tazi@gmail.com','0663013013','Responsable RH','MASTER','Gestion des Ressources Humaines','ENCG Fès',2021,4,0.86,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',8);
INSERT INTO "candidat" VALUES(34,'CHERKAOUI','Mehdi','mehdi.cherkaoui@gmail.com','0664014014','Responsable RH','MASTER','Management et Leadership','HEM Fès',2020,5,0.89,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',8);
INSERT INTO "candidat" VALUES(35,'BENKIRAN','Fatima','fatima.benkiran@gmail.com','0665015015','Responsable RH','LICENCE','Psychologie du Travail','Université Sidi Mohamed',2023,1,0.42,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',8);
INSERT INTO "candidat" VALUES(36,'RHALI','Karim','karim.rhali@gmail.com','0666016016','Responsable RH','TECHNICIEN SPECIALISE','Secrétariat de Direction','ISTA Fès',2022,2,0.27,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',8);
INSERT INTO "candidat" VALUES(37,'BENSOUDA','Yassir','yassir.bensouda@gmail.com','0667017017','Ingénieur Génie Civil','MASTER','Génie Civil et Structures','École Mohammadia d''Ingénieurs',2021,4,0.92,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',9);
INSERT INTO "candidat" VALUES(38,'SEFRIOUI','Hajar','hajar.sefrioui@gmail.com','0668018018','Ingénieur Génie Civil','MASTER','BTP et Aménagement','EHTP Casablanca',2022,3,0.84,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',9);
INSERT INTO "candidat" VALUES(39,'LAZRAK','Soufiane','soufiane.lazrak@gmail.com','0669019019','Ingénieur Génie Civil','LICENCE','Génie Civil','FST Fès',2023,1,0.47,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',9);
INSERT INTO "candidat" VALUES(40,'OULHAJ','Zineb','zineb.oulhaj@gmail.com','0660020020','Ingénieur Génie Civil','MASTER','Géotechnique et Fondations','École Hassania des Travaux Publics',2020,5,0.95,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.381321',9);
INSERT INTO "candidat" VALUES(41,'BENALI','Hafsa','hafsa.benali@gmail.com','0661100001','Chargé de Développement Économique','MASTER','Économie et Gestion Territoriale','ENCG Fès',2021,4,0.84,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(42,'ERRACHIDI','Kamal','kamal.errachidi@gmail.com','0662200002','Chargé de Développement Économique','MASTER','Management des Organisations','USMBA Fès',2020,5,0.76,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(43,'ALAMI','Sanaa','sanaa.alami@gmail.com','0663300003','Chargé de Développement Économique','MASTER','Développement Local et Gouvernance','FSJES Fès',2022,3,0.68,'Présélectionné',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(44,'OUALI','Yassine','yassine.ouali@gmail.com','0664400004','Chargé de Développement Économique','LICENCE','Économie Appliquée','FSJES Meknès',2023,1,0.36,'À examiner',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(45,'TAHIRI','Nadia','nadia.tahiri@gmail.com','0665500005','Chargé de Développement Économique','MASTER','Finance et Commerce International','Autre',2019,3,0.31,'À examiner',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(46,'GUENOUN','Amine','amine.guenoun@gmail.com','0666600006','Chargé de Développement Économique','LICENCE','Géographie et Aménagement','FSJES Fès',2024,0,0.22,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(47,'LAHLOU','Zineb','zineb.lahlou@gmail.com','0667700007','Chargé de Développement Économique','BAC','Sciences Économiques','Lycée Moulay Idriss',2023,0,0.14,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(48,'BENSAID','Omar','omar.bensaid@gmail.com','0668800008','Chargé de Développement Économique','TECHNICIEN SPECIALISE','Commerce et Vente','ISTA Fès',2022,1,0.09,'Non retenu',0,NULL,NULL,NULL,NULL,NULL,'2026-09-23 08:15:22.424728',10);
INSERT INTO "candidat" VALUES(49,'ZOUGGARI','Karim','karim.zouggari@gmail.com','0683500400','Chargé de Développement Économique','BAC','Sciences Économiques','Lycee Ibn Khaldoun Fes',2024,2,0.05,'Non retenu',0,NULL,NULL,'Arabe, Français','Vente, Accueil clients, Sens du contact client, Motivation','CV_Karim_ZOUGGARI.pdf','2026-09-23 08:39:21.028287',10);
INSERT INTO "candidat" VALUES(50,'FENNANE','Mehdi','mehdi.fennane@gmail.com','0672400300','Chargé de Développement Économique','LICENCE','Economie Appliquee','FSJES Fes',2023,2,0.1956,'Non retenu',0,NULL,NULL,'Arabe, Français','Analyse économique, Word, Excel, Rédaction de rapports, Suivi administratif','CV_Mehdi_FENNANE.pdf','2026-09-23 08:39:23.063808',10);
INSERT INTO "candidat" VALUES(51,'CHAOUI','Nora','nora.chaoui@gmail.com','0661100200','Chargé de Développement Économique','MASTER','Économie et Gestion Territoriale','ENCG Fes',2020,6,0.4115,'Présélectionné',0,NULL,NULL,'Arabe, Français, Anglais','Analyse économique, rédaction administrative, Excel avancé, gestion de projets, suivi de projets territoriaux, rapports sectoriels, étude des investissements régionaux','CV_Nora_CHAOUI.pdf','2026-09-23 08:39:23.104766',10);
INSERT INTO "candidat" VALUES(52,'GUENOUN','Fatima','f.guenoun@email.ma','06 66 77 88 99','Responsable Communication','LICENCE','Economie','FSJES',2020,3,0.1875,'Non retenu',0,NULL,NULL,'','Gestion administrative, Communication, Informatique bureautique','CV_Fatima_GUENOUN.pdf','2026-09-23 13:30:47.357492',11);
INSERT INTO "candidat" VALUES(53,'EZZIANI','Hamza','h.ezziani@email.ma','06 55 66 77 88','Responsable Communication','LICENCE','Finance','ISTA',2020,3,0.1811,'Non retenu',0,NULL,NULL,'','Gestion administrative, Communication, Informatique bureautique','CV_Hamza_EZZIANI.pdf','2026-09-23 13:30:49.503348',11);
INSERT INTO "candidat" VALUES(54,'BENSOUDA','Karim','k.bensouda@email.ma','06 22 33 44 55','Responsable Communication','MASTER','Gestion des entreprises','FSJES',2021,3,0.5807,'Présélectionné',0,NULL,NULL,'','Gestion administrative, Communication, Informatique bureautique','CV_Karim_BENSOUDA.pdf','2026-09-23 13:30:51.631228',11);
INSERT INTO "candidat" VALUES(55,'TAHIRI','Meryem','m.tahiri@email.ma','06 11 22 33 44','Responsable Communication','MASTER','Gestion des entreprises','USMBA',2021,3,0.6053,'Présélectionné',0,NULL,NULL,'','Gestion administrative, Communication, Informatique bureautique','CV_Meryem_TAHIRI.pdf','2026-09-23 13:30:53.791948',11);
INSERT INTO "candidat" VALUES(56,'IBRAHIMI','Nora','n.ibrahimi@email.ma','06 88 99 00 11','Responsable Communication','LICENCE','Gestion des entreprises','ISTA',2019,4,0.2368,'Non retenu',0,NULL,NULL,'','Gestion administrative, Communication, Informatique bureautique','CV_Nora_IBRAHIMI.pdf','2026-09-23 13:30:55.952075',11);
INSERT INTO "candidat" VALUES(57,'HILALI','Rachid','r.hilali@email.ma','06 77 88 99 00','Responsable Communication','TECHNICIEN SPECIALISE','Commerce','ISTA',2022,2,0.08,'Non retenu',0,NULL,NULL,'','Gestion administrative, Communication, Informatique bureautique','CV_Rachid_HILALI.pdf','2026-09-23 13:30:58.403420',11);
INSERT INTO "candidat" VALUES(58,'DRISSI','Youssef','y.drissi@email.ma','06 44 55 66 77','Responsable Communication','LICENCE','Gestion des entreprises','ISTA',2020,3,0.2431,'Présélectionné',1,'ADER Administrateur','2026-09-23 13:34:50.736208','','Gestion administrative, Communication, Informatique bureautique','CV_Youssef_DRISSI.pdf','2026-09-23 13:31:00.700722',11);
INSERT INTO "candidat" VALUES(59,'CHAOUI','Zineb','z.chaoui@email.ma','06 33 44 55 66','Responsable Communication','MASTER','Finance','USMBA',2021,3,0.4646,'Présélectionné',0,NULL,NULL,'','Gestion administrative, Communication, Informatique bureautique','CV_Zineb_CHAOUI.pdf','2026-09-23 13:31:00.804319',11);
CREATE TABLE entretien (
	id INTEGER NOT NULL, 
	candidat_id INTEGER NOT NULL, 
	date_entretien DATETIME, 
	evaluateur VARCHAR(150), 
	poste_evaluateur VARCHAR(100), 
	note_presentation FLOAT, 
	note_motivation FLOAT, 
	note_competences FLOAT, 
	note_communication FLOAT, 
	note_culture FLOAT, 
	commentaire TEXT, 
	decision_entretien VARCHAR(30), 
	score_entretien FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidat_id) REFERENCES candidat (id)
);
CREATE TABLE evaluation_jury (
	id INTEGER NOT NULL, 
	candidat_id INTEGER NOT NULL, 
	numero_jury INTEGER NOT NULL, 
	nom_jury VARCHAR(150), 
	poste_jury VARCHAR(100), 
	note_presentation FLOAT, 
	note_motivation FLOAT, 
	note_competences FLOAT, 
	note_communication FLOAT, 
	note_culture FLOAT, 
	commentaire TEXT, 
	score_jury FLOAT, 
	date_evaluation DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidat_id) REFERENCES candidat (id)
);
INSERT INTO "evaluation_jury" VALUES(1,1,1,'M. Hassan Alaoui','Directeur RH',14.0,13.0,15.0,12.0,16.0,'',14.0,'2026-09-23 08:15:22.343418');
INSERT INTO "evaluation_jury" VALUES(2,1,2,'Mme. Fatima Bennani','Responsable Formation',13.0,15.0,12.0,14.0,13.0,'',13.4,'2026-09-23 08:15:22.343418');
INSERT INTO "evaluation_jury" VALUES(3,1,3,'M. Rachid Moussaoui','Chef de département',12.0,14.0,16.0,13.0,15.0,'',14.0,'2026-09-23 08:15:22.343418');
INSERT INTO "evaluation_jury" VALUES(4,1,4,'Mme. Amina Chaoui','DG Adjoint',15.0,16.0,14.0,15.0,14.0,'',14.8,'2026-09-23 08:15:22.343418');
INSERT INTO "evaluation_jury" VALUES(5,20,4,'Fati RBIKI','',10.0,10.0,18.5,10.0,10.0,'',11.7,'2026-09-23 08:15:22.343418');
CREATE TABLE offre (
	id INTEGER NOT NULL, 
	titre VARCHAR(200), 
	poste VARCHAR(100), 
	nombre_postes INTEGER, 
	diplome_requis TEXT, 
	experience_min INTEGER, 
	specialite VARCHAR(200), 
	langues VARCHAR(200), 
	missions TEXT, 
	attributions TEXT, 
	competences TEXT, 
	criteres_performance TEXT, 
	mots_cles VARCHAR(500), 
	date_limite VARCHAR(50), 
	actif BOOLEAN, 
	date_creation DATETIME, 
	PRIMARY KEY (id)
);
INSERT INTO "offre" VALUES(1,'(01) Chef de projets Architecte','(01) Chef de projets Architecte',1,'Architecte (Diplôme d''état Marocain ou diplôme privé reconnu par l''Etat ou diplôme étranger',1,'Architecture','Français, Arabe','Suivi et coordination des projets d''aménagement et de réhabilitation ; Préparation et lecture des plans ; Classement de dossiers ; Archivage des dossiers techniques.',NULL,'Maîtrise AutoCAD ; Connaissance normes construction ; Lecture plans architecturaux ; Suivi chantier.',NULL,'architecte,projet,chantier,autocad','30/09/2026',1,'2026-09-23 08:15:22.295015');
INSERT INTO "offre" VALUES(2,'(02) Charge de Communication et Marketing Digital','(02) Charge de Communication et Marketing Digital',2,'Master en Communication, Marketing ou équivalent',0,'Communication','Français, Arabe, Anglais','Gérer les réseaux sociaux ; Produire les contenus digitaux ; Assurer la couverture médiatique des événements.',NULL,'Canva, WordPress, Pack Office, gestion de projets événementiels.',NULL,'communication,marketing,digital,réseaux sociaux','30/09/2026',1,'2026-09-23 08:15:22.295015');
INSERT INTO "offre" VALUES(3,'CGM','CGM',1,'Master',2,'Gestion','Français, Arabe','Gestion marchés ; Suivi administratif ; Contact prestataires.',NULL,'Maîtrise des démarches administratives ; Maitrise de l''exécution des différents travaux.',NULL,'gestion,marchés,administratif','30/09/2026',1,'2026-09-23 08:15:22.295015');
INSERT INTO "offre" VALUES(4,'(04) Assistant(e) Architecte','Assistant Architecte',1,'Licence en Architecture ou Technicien Spécialisé en Bâtiment/Dessin',1,'Architecture','Français, Arabe','Assister l''architecte responsable dans le suivi des projets ; Préparer et mettre à jour les plans et documents techniques (AutoCAD) ; Participer aux visites de chantier.',NULL,'Maîtrise AutoCAD ; Connaissance normes construction ; Lecture plans architecturaux.',NULL,'architecte,assistant,autocad,dessin','30/09/2026',1,'2026-09-23 08:15:22.295015');
INSERT INTO "offre" VALUES(5,'Responsable Comptabilité et Finance','Responsable Comptabilité',1,'Master en Finance, Comptabilité ou ISCAE',3,'Finance/Comptabilité','Français, Arabe','Tenue de la comptabilité générale et analytique ; Élaboration des états financiers ; Suivi budgétaire ; Déclarations fiscales et sociales ; Relation avec les auditeurs et experts comptables.',NULL,'Maîtrise Sage ou ERP comptable ; Excel avancé ; Connaissance fiscalité marocaine ; Rigueur et organisation.',NULL,'comptabilité,finance,bilan,fiscalité,audit','31/10/2026',1,'2026-09-23 08:15:22.360376');
INSERT INTO "offre" VALUES(6,'Technicien Réseaux et Informatique','Technicien Réseaux',2,'Bac+2 ou Bac+3 en Informatique / Réseaux et Télécommunications',1,'Informatique/Réseaux','Français, Arabe','Maintenance du parc informatique ; Administration réseau LAN/WAN ; Support utilisateurs niveau 1 et 2 ; Gestion des sauvegardes et de la sécurité informatique.',NULL,'Cisco, Windows Server, Active Directory, ticketing ; Sens du service.',NULL,'informatique,réseau,maintenance,support,cisco','31/10/2026',1,'2026-09-23 08:15:22.360376');
INSERT INTO "offre" VALUES(7,'Juriste / Conseiller Juridique','Juriste',1,'Master en Droit des affaires ou Droit public',2,'Droit','Français, Arabe, Anglais apprécié','Rédaction et révision des contrats et marchés publics ; Veille juridique et réglementaire ; Conseil aux directions opérationnelles ; Gestion des contentieux.',NULL,'Maîtrise du droit marocain des marchés publics ; Rédaction juridique précise ; Gestion des délais.',NULL,'droit,juridique,contrat,marchés publics,contentieux','31/10/2026',1,'2026-09-23 08:15:22.360376');
INSERT INTO "offre" VALUES(8,'Responsable Ressources Humaines','Responsable RH',1,'Master en GRH, Management ou Sciences Sociales',3,'Ressources Humaines','Français, Arabe','Recrutement et intégration des nouveaux collaborateurs ; Gestion de la paie et des déclarations sociales ; Élaboration du plan de formation ; Suivi des indicateurs RH ; Gestion des relations sociales.',NULL,'Droit social marocain ; SIRH ; Capacités relationnelles et de médiation ; Excel RH.',NULL,'RH,recrutement,paie,formation,gestion sociale','31/10/2026',1,'2026-09-23 08:15:22.360376');
INSERT INTO "offre" VALUES(9,'Ingénieur Génie Civil','Ingénieur Génie Civil',1,'Ingénieur d''État ou Master en Génie Civil / BTP',2,'Génie Civil / BTP','Français, Arabe','Étude et suivi des projets de construction et réhabilitation ; Contrôle de la qualité des travaux ; Rédaction des rapports techniques ; Coordination avec les entreprises prestataires ; Réception des travaux.',NULL,'AutoCAD, Revit ou BIM ; Connaissance CCAG Travaux ; Gestion de chantier ; Métrés et devis.',NULL,'génie civil,construction,chantier,BTP,structure','31/10/2026',1,'2026-09-23 08:15:22.360376');
INSERT INTO "offre" VALUES(10,'Chargé de Développement Économique','Chargé de Développement Économique',2,'Master en Économie, Gestion ou Administration',2,'Économie / Développement territorial','Français, Arabe','Analyse des opportunités économiques régionales ; Accompagnement des porteurs de projets ; Rédaction de rapports et études sectorielles ; Coordination avec les partenaires institutionnels ; Suivi des indicateurs de développement.',NULL,'Maîtrise de l''analyse économique ; Rédaction administrative ; Connaissance du tissu économique régional ; Esprit de synthèse.',NULL,'développement,économie,territoire,projet,analyse','31/10/2026',1,'2026-09-23 08:15:22.402785');
INSERT INTO "offre" VALUES(11,'Responsable Communication Institutionnelle','Responsable Communication',1,'Master en Communication, Sciences de l''Information ou Marketing',3,'Communication / Marketing','Français, Arabe','Elaboration de la strategie de communication de l''agence ; Gestion des relations presse et medias ; Production de contenus institutionnels ; Organisation des evenements officiels ; Pilotage des reseaux sociaux et du site web.',NULL,'Maitrise des outils de communication digitale ; Redaction institutionnelle ; Gestion de projet ; Sens de l''esthetique et de la communication visuelle.',NULL,'communication,marketing,medias,institutionnel,evenement','31/10/2026',1,'2026-09-23 09:22:41.828521');
CREATE TABLE questions_entretien (
	id INTEGER NOT NULL, 
	candidat_id INTEGER NOT NULL, 
	questions_json TEXT, 
	posees_json TEXT, 
	coche_par_json TEXT, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (candidat_id), 
	FOREIGN KEY(candidat_id) REFERENCES candidat (id)
);
INSERT INTO "questions_entretien" VALUES(1,41,'["Quelles méthodes utilisez-vous concrètement pour réaliser un diagnostic économique territorial et quels indicateurs privilégiez-vous pour la région Fès-Meknès ?", "Comment construiriez-vous un argumentaire pour attirer un investisseur privé vers une zone d''activité économique peu développée de la région ?", "Quels outils ou cadres méthodologiques mobilisez-vous pour évaluer l''impact d''un projet de développement économique local sur l''emploi et la création de valeur ?", "Pouvez-vous décrire un projet concret que vous avez piloté ou auquel vous avez contribué durant vos 4 années d''expérience, en précisant votre rôle et les résultats obtenus ?", "Avez-vous déjà travaillé en coordination avec des acteurs publics, des collectivités territoriales ou des partenaires institutionnels ? Comment avez-vous géré les divergences d''intérêts ?", "En quoi votre formation en Économie et Gestion Territoriale à l''ENCG Fès vous a-t-elle préparé aux réalités du terrain en matière de développement régional ?", "Pourquoi souhaitez-vous rejoindre l''ADER Fès-Meknès aujourd''hui, et qu''est-ce que ce poste représente dans votre trajectoire professionnelle à moyen terme ?", "Dans cinq ans, quel type de responsabilités aimeriez-vous exercer au sein d''une agence de développement régional comme l''ADER ?", "Que savez-vous des missions et des axes stratégiques de l''ADER Fès-Meknès, et quel chantier vous semble prioritaire pour dynamiser l''attractivité économique de la région ?", "Selon vous, quelles sont les principales contraintes qui freinent le développement économique dans le secteur public territorial au Maroc, et comment un chargé de développement peut-il y répondre efficacement ?"]','[]','{}','2026-09-23 08:29:12.349558');
INSERT INTO "questions_entretien" VALUES(2,55,'["Comment construiriez-vous un plan de communication annuel pour une agence de développement régional disposant d''un budget limité et de publics cibles très variés (élus, investisseurs, citoyens, médias) ?", "Quels outils et indicateurs utilisez-vous concrètement pour mesurer l''impact d''une campagne de communication institutionnelle, et comment en rendez-vous compte à votre direction ?", "Comment gérez-vous une situation de communication de crise lorsqu''une information négative concernant votre organisation se répand sur les réseaux sociaux ou dans la presse régionale ?", "Votre diplôme est en gestion des entreprises et non en communication : quelles compétences spécifiques en communication avez-vous développées durant vos 3 années d''expérience professionnelle ?", "Citez une réalisation concrète dont vous êtes fier(e) dans votre parcours, en précisant votre rôle exact, les moyens mobilisés et les résultats obtenus.", "Avez-vous déjà travaillé avec des partenaires institutionnels, des collectivités territoriales ou des organismes publics, et comment avez-vous adapté votre communication à ces interlocuteurs ?", "Qu''est-ce qui vous a motivé à postuler pour un poste de responsable communication dans une agence publique de développement régional plutôt que dans le secteur privé ?", "Dans 3 ans, si vous occupez ce poste, quel impact concret souhaiteriez-vous avoir laissé sur la visibilité et l''image de l''ADER Fès-Meknès ?", "Que savez-vous des missions et des axes stratégiques de l''Agence de Développement Régional de Fès-Meknès, et quels sont selon vous ses enjeux de communication prioritaires aujourd''hui ?", "En quoi la communication dans un établissement public diffère-t-elle fondamentalement de celle d''une entreprise privée, et quelles contraintes spécifiques anticipez-vous dans ce contexte ?"]','[]','{}','2026-09-23 13:33:21.748104');
CREATE TABLE utilisateur_rh (
	id INTEGER NOT NULL, 
	nom VARCHAR(100) NOT NULL, 
	prenom VARCHAR(100) NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	email VARCHAR(150), 
	password_hash VARCHAR(256) NOT NULL, 
	role VARCHAR(20), 
	jury_numero INTEGER, 
	actif BOOLEAN, 
	date_creation DATETIME, 
	reset_token VARCHAR(100), 
	reset_token_expire DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
INSERT INTO "utilisateur_rh" VALUES(1,'Administrateur','ADER','admin',NULL,'scrypt:32768:8:1$G9WXLjrtKrXiOWXT$f4aa04f579c4d58f025ca209bd3cb18b1a5c06a3816b0795da7f5d0a90d1fbd7289ba2d913ca18e747dfa573d7f892cf926d5c00bc663152663df5d9fa623c9b','admin',NULL,1,'2026-09-23 08:15:20.606908',NULL,NULL);
INSERT INTO "utilisateur_rh" VALUES(2,'Ouchene','Bouchra','bouchra.ader',NULL,'scrypt:32768:8:1$4SThxzuDESy5p0r1$942758e1cb826ef193df33617b48748b6119344d48ced96cde8883a15c9e785a3140769bdc654656c0da1467751a8d89064518ac2a38057a90a1c7a9eafd57e0','jury',1,1,'2026-09-23 08:15:21.076353',NULL,NULL);
INSERT INTO "utilisateur_rh" VALUES(3,'Rhamni','Ali','ali.ader',NULL,'scrypt:32768:8:1$Ps8DgkMHbUR6RxsS$70824392bf802dfa4f4bfdb587bb410f7a9f398e3e6df42055da71741a84fe2feb556416ff8c9ca47902770047c4daf994e78814be334aa6036b5c3a2b087284','jury',2,1,'2026-09-23 08:15:21.483399',NULL,NULL);
INSERT INTO "utilisateur_rh" VALUES(4,'Benjalloun','Younnes','younnes.benjalloun',NULL,'scrypt:32768:8:1$Vt7bI10oVxVNNc0Q$0aa38d84a48367f2ef5774f0c3c5e8db8aeb33a61b6e9dc4d8f0e4969a461e874e87544831fa538bcd5bf9e65a1deced7d734e032792edfc6705bedfe9d04ac9','jury',3,1,'2026-09-23 08:15:21.837447',NULL,NULL);
INSERT INTO "utilisateur_rh" VALUES(5,'Rbiki','Fati','fati.ader',NULL,'scrypt:32768:8:1$seTzWj2QAOGeGjeG$0c5b0eb91b4490e58b30b0b061085caa7f87a93ddd55ecd546bfa284c04cffb53b3f38489c2562cb1ca4fe685a5c172f4e59ea6b805a3e60047c7a6112b9adb6','jury',4,1,'2026-09-23 08:15:22.275553',NULL,NULL);
CREATE TABLE verification_dossier (
	id INTEGER NOT NULL, 
	candidat_id INTEGER NOT NULL, 
	date_verification DATETIME, 
	verificateur VARCHAR(150), 
	conforme BOOLEAN, 
	diplome_conforme BOOLEAN, 
	experience_conforme BOOLEAN, 
	cin_conforme BOOLEAN, 
	autres_conformes BOOLEAN, 
	motif_interne TEXT, 
	email_envoye BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidat_id) REFERENCES candidat (id)
);
INSERT INTO "verification_dossier" VALUES(1,41,'2026-09-23 08:28:42.557643','ADER Administrateur',1,1,1,1,1,'',0);
INSERT INTO "verification_dossier" VALUES(2,55,'2026-09-23 13:32:50.980826','ADER Administrateur',1,1,1,1,1,'',0);
COMMIT;
