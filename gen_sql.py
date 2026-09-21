"""
Génère un dump SQL propre pour PostgreSQL depuis SQLite local.
"""
import os, sys
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(BASE_DIR, 'recrut.db')}"

sys.path.insert(0, BASE_DIR)
from app import app, db, Candidat, UtilisateurRH, Offre, EvaluationJury, QuestionsEntretien

def esc(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, int) or isinstance(v, float):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"

lines = ["-- RecrutIA ADER — dump PostgreSQL\n"]

with app.app_context():
    # Utilisateurs
    lines.append("-- utilisateur_rh")
    for u in UtilisateurRH.query.all():
        lines.append(
            f"INSERT INTO utilisateur_rh (id,nom,prenom,username,password_hash,role,actif,date_creation,email,jury_numero) VALUES ("
            f"{u.id},{esc(u.nom)},{esc(u.prenom)},{esc(u.username)},{esc(u.password_hash)},{esc(u.role)},"
            f"{'TRUE' if u.actif else 'FALSE'},{esc(str(u.date_creation))},{esc(u.email)},{esc(u.jury_numero)}"
            f") ON CONFLICT (id) DO UPDATE SET jury_numero=EXCLUDED.jury_numero, role=EXCLUDED.role;"
        )

    # Offres
    lines.append("\n-- offre")
    for o in Offre.query.all():
        lines.append(
            f"INSERT INTO offre (id,titre,poste,nombre_postes,diplome_requis,experience_min,specialite,langues,missions,competences,mots_cles,date_limite,actif,date_creation) VALUES ("
            f"{o.id},{esc(o.titre)},{esc(o.poste)},{esc(o.nombre_postes)},{esc(o.diplome_requis)},{esc(o.experience_min)},"
            f"{esc(o.specialite)},{esc(o.langues)},{esc(o.missions)},{esc(o.competences)},{esc(o.mots_cles)},"
            f"{esc(o.date_limite)},{'TRUE' if o.actif else 'FALSE'},{esc(str(o.date_creation))}"
            f") ON CONFLICT (id) DO NOTHING;"
        )

    # Candidats
    lines.append("\n-- candidat")
    for c in Candidat.query.all():
        dm = 'TRUE' if c.decision_manuelle else 'FALSE'
        lines.append(
            f"INSERT INTO candidat (id,nom,prenom,email,telephone,poste,diplome,specialite,ecole,promotion,experience,score_ia,decision,decision_manuelle,decideur_manuel,date_decision_manuelle,langues,competences,cv_filename,date_depot,offre_id) VALUES ("
            f"{c.id},{esc(c.nom)},{esc(c.prenom)},{esc(c.email)},{esc(c.telephone)},{esc(c.poste)},{esc(c.diplome)},"
            f"{esc(c.specialite)},{esc(c.ecole)},{esc(c.promotion)},{c.experience},{esc(c.score_ia)},"
            f"{esc(c.decision)},{dm},{esc(c.decideur_manuel)},{esc(str(c.date_decision_manuelle) if c.date_decision_manuelle else None)},"
            f"{esc(c.langues)},{esc(c.competences)},{esc(c.cv_filename)},{esc(str(c.date_depot))},{esc(c.offre_id)}"
            f") ON CONFLICT (id) DO UPDATE SET score_ia=EXCLUDED.score_ia, decision=EXCLUDED.decision, decision_manuelle=EXCLUDED.decision_manuelle;"
        )

    # Evaluations jury
    lines.append("\n-- evaluation_jury")
    for e in EvaluationJury.query.all():
        cols = [c.key for c in EvaluationJury.__table__.columns]
        vals = []
        for col in cols:
            v = getattr(e, col)
            vals.append(esc(v) if not isinstance(v, bool) else ('TRUE' if v else 'FALSE'))
        lines.append(
            f"INSERT INTO evaluation_jury ({','.join(cols)}) VALUES ({','.join(vals)}) ON CONFLICT (id) DO NOTHING;"
        )

    # Questions entretien
    lines.append("\n-- questions_entretien")
    for q in QuestionsEntretien.query.all():
        lines.append(
            f"INSERT INTO questions_entretien (id,candidat_id,questions_json,posees_json,coche_par_json,updated_at) VALUES ("
            f"{q.id},{q.candidat_id},{esc(q.questions_json)},{esc(q.posees_json)},{esc(q.coche_par_json)},{esc(str(q.updated_at))}"
            f") ON CONFLICT (id) DO NOTHING;"
        )

    out = "\n".join(lines)
    path = os.path.join(BASE_DIR, "dump_recrutia.sql")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK — fichier généré : {path}")
    print(f"Utilisateurs: {UtilisateurRH.query.count()}, Candidats: {Candidat.query.count()}, Offres: {Offre.query.count()}, Evals: {EvaluationJury.query.count()}")
