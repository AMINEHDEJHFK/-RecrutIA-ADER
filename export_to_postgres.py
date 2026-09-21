"""
Script pour exporter les données SQLite locales vers PostgreSQL Railway
Usage: python export_to_postgres.py
"""
import os, sys
from dotenv import load_dotenv
load_dotenv()

POSTGRES_URL = input("Colle l'URL PostgreSQL Railway (DATABASE_URL) : ").strip()
if POSTGRES_URL.startswith("postgres://"):
    POSTGRES_URL = POSTGRES_URL.replace("postgres://", "postgresql://", 1)

# Connexion SQLite locale
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sqlite_engine = create_engine(f"sqlite:///{os.path.join(BASE_DIR, 'recrut.db')}")
pg_engine = create_engine(POSTGRES_URL)

# Import du modèle
sys.path.insert(0, BASE_DIR)
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(BASE_DIR, 'recrut.db')}"
from app import db, app, Candidat, UtilisateurRH, Offre, EvaluationJury

with app.app_context():
    # Créer les tables dans PostgreSQL
    app.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URL
    db.engine.dispose()
    with pg_engine.connect() as conn:
        pass

    # Recréer avec PG
    from flask import Flask
    app2 = Flask(__name__)
    app2.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_URL
    app2.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app2.secret_key = "export"

    from flask_sqlalchemy import SQLAlchemy
    db2 = SQLAlchemy(app2)

    with app2.app_context():
        # Lire depuis SQLite
        candidats = Candidat.query.all()
        utilisateurs = UtilisateurRH.query.all()
        offres = Offre.query.all()
        evaluations = EvaluationJury.query.all()

        print(f"SQLite: {len(candidats)} candidats, {len(utilisateurs)} utilisateurs, {len(offres)} offres, {len(evaluations)} évaluations")

        # Écrire dans PostgreSQL via SQL brut
        with pg_engine.begin() as conn:
            # Tables dans l'ordre
            conn.execute(text("DROP TABLE IF EXISTS evaluation_jury CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS candidat CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS utilisateur_rh CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS offre CASCADE"))

        print("Tables supprimées. Recréation...")

        # Créer les tables via SQLAlchemy avec PG
        from app import db as db_orig
        db_orig.engine.dispose()

        # On va juste générer le SQL d'insertion
        print("\nGénération du fichier SQL d'export...")

        lines = []
        lines.append("-- Export RecrutIA ADER -- SQLite vers PostgreSQL")
        lines.append("-- Généré automatiquement\n")

        # Utilisateurs RH
        lines.append("-- Utilisateurs RH")
        for u in utilisateurs:
            lines.append(f"INSERT INTO utilisateur_rh (id, nom, prenom, username, password_hash, role, actif, date_creation) VALUES "
                        f"({u.id}, '{u.nom}', '{u.prenom}', '{u.username}', '{u.password_hash}', '{u.role}', {u.actif}, '{u.date_creation}') "
                        f"ON CONFLICT (id) DO NOTHING;")

        # Candidats
        lines.append("\n-- Candidats")
        for c in candidats:
            nom = (c.nom or '').replace("'", "''")
            prenom = (c.prenom or '').replace("'", "''")
            ecole = (c.ecole or '').replace("'", "''")
            specialite = (c.specialite or '').replace("'", "''")
            poste = (c.poste or '').replace("'", "''")
            diplome = (c.diplome or '').replace("'", "''")
            cv = (c.cv_filename or '').replace("'", "''")
            statut = (c.statut or '').replace("'", "''")
            conformite = (c.conformite_dossier or '').replace("'", "''")

            lines.append(f"INSERT INTO candidat (id, nom, prenom, ecole, specialite, poste, diplome, promotion, experience, score_ia, statut, cv_filename, conformite_dossier, date_candidature) VALUES "
                        f"({c.id}, '{nom}', '{prenom}', '{ecole}', '{specialite}', '{poste}', '{diplome}', '{c.promotion}', {c.experience}, {c.score_ia or 'NULL'}, '{statut}', '{cv}', '{conformite}', '{c.date_candidature}') "
                        f"ON CONFLICT (id) DO NOTHING;")

        # Offres
        lines.append("\n-- Offres")
        for o in offres:
            titre = (o.titre or '').replace("'", "''")
            desc = (o.description or '').replace("'", "''")
            lines.append(f"INSERT INTO offre (id, titre, description, actif) VALUES "
                        f"({o.id}, '{titre}', '{desc}', {o.actif}) "
                        f"ON CONFLICT (id) DO NOTHING;")

        # Evaluations
        lines.append("\n-- Evaluations jury")
        for e in evaluations:
            lines.append(f"INSERT INTO evaluation_jury (id, candidat_id, jury_numero, critere_technique, critere_experience, critere_motivation, critere_communication, note_finale, date_evaluation) VALUES "
                        f"({e.id}, {e.candidat_id}, {e.jury_numero}, {e.critere_technique}, {e.critere_experience}, {e.critere_motivation}, {e.critere_communication}, {e.note_finale}, '{e.date_evaluation}') "
                        f"ON CONFLICT (id) DO NOTHING;")

        sql_content = "\n".join(lines)
        output_file = os.path.join(BASE_DIR, "dump_recrutia.sql")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(sql_content)

        print(f"\nFichier SQL généré : {output_file}")
        print(f"Total : {len(utilisateurs)} utilisateurs, {len(candidats)} candidats, {len(offres)} offres, {len(evaluations)} évaluations")
        print("\nMaintenant va dans Railway > Postgres > Console et colle le contenu du fichier SQL.")
