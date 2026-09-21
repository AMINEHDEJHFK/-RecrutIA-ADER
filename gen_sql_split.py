"""
Génère 4 fichiers SQL séparés (petits) pour Railway Console.
"""
import os, sys
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(BASE_DIR, 'recrut.db')}"
sys.path.insert(0, BASE_DIR)
from app import app, db, Candidat, UtilisateurRH, Offre, EvaluationJury, QuestionsEntretien

def esc(v):
    if v is None: return "NULL"
    if isinstance(v, bool): return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"

with app.app_context():
    # 1 — Utilisateurs
    lines = []
    for u in UtilisateurRH.query.all():
        lines.append(
            f"INSERT INTO utilisateur_rh (id,nom,prenom,username,password_hash,role,actif,date_creation,email,jury_numero) VALUES ("
            f"{u.id},{esc(u.nom)},{esc(u.prenom)},{esc(u.username)},{esc(u.password_hash)},{esc(u.role)},"
            f"{'TRUE' if u.actif else 'FALSE'},{esc(str(u.date_creation))},{esc(u.email)},{esc(u.jury_numero)}"
            f") ON CONFLICT (id) DO UPDATE SET jury_numero=EXCLUDED.jury_numero,role=EXCLUDED.role;"
        )
    open(os.path.join(BASE_DIR,"sql_1_users.sql"),"w",encoding="utf-8").write("\n".join(lines))
    print(f"sql_1_users.sql — {len(lines)} lignes")

    # 2 — Offres + Candidats 1-10
    lines = []
    for o in Offre.query.all():
        lines.append(
            f"INSERT INTO offre (id,titre,poste,nombre_postes,diplome_requis,experience_min,specialite,langues,missions,competences,mots_cles,date_limite,actif,date_creation) VALUES ("
            f"{o.id},{esc(o.titre)},{esc(o.poste)},{esc(o.nombre_postes)},{esc(o.diplome_requis)},{esc(o.experience_min)},"
            f"{esc(o.specialite)},{esc(o.langues)},{esc(o.missions)},{esc(o.competences)},{esc(o.mots_cles)},"
            f"{esc(o.date_limite)},{'TRUE' if o.actif else 'FALSE'},{esc(str(o.date_creation))}"
            f") ON CONFLICT (id) DO NOTHING;"
        )
    candidats = Candidat.query.all()
    for c in candidats[:10]:
        dm = 'TRUE' if c.decision_manuelle else 'FALSE'
        lines.append(
            f"INSERT INTO candidat (id,nom,prenom,email,telephone,poste,diplome,specialite,ecole,promotion,experience,score_ia,decision,decision_manuelle,decideur_manuel,langues,competences,cv_filename,date_depot,offre_id) VALUES ("
            f"{c.id},{esc(c.nom)},{esc(c.prenom)},{esc(c.email)},{esc(c.telephone)},{esc(c.poste)},{esc(c.diplome)},"
            f"{esc(c.specialite)},{esc(c.ecole)},{esc(c.promotion)},{c.experience},{esc(c.score_ia)},"
            f"{esc(c.decision)},{dm},{esc(c.decideur_manuel)},{esc(c.langues)},{esc(c.competences)},{esc(c.cv_filename)},{esc(str(c.date_depot))},{esc(c.offre_id)}"
            f") ON CONFLICT (id) DO UPDATE SET score_ia=EXCLUDED.score_ia,decision=EXCLUDED.decision;"
        )
    open(os.path.join(BASE_DIR,"sql_2_offres_cand1.sql"),"w",encoding="utf-8").write("\n".join(lines))
    print(f"sql_2_offres_cand1.sql — {len(lines)} lignes")

    # 3 — Candidats 11-20
    lines = []
    for c in candidats[10:]:
        dm = 'TRUE' if c.decision_manuelle else 'FALSE'
        lines.append(
            f"INSERT INTO candidat (id,nom,prenom,email,telephone,poste,diplome,specialite,ecole,promotion,experience,score_ia,decision,decision_manuelle,decideur_manuel,langues,competences,cv_filename,date_depot,offre_id) VALUES ("
            f"{c.id},{esc(c.nom)},{esc(c.prenom)},{esc(c.email)},{esc(c.telephone)},{esc(c.poste)},{esc(c.diplome)},"
            f"{esc(c.specialite)},{esc(c.ecole)},{esc(c.promotion)},{c.experience},{esc(c.score_ia)},"
            f"{esc(c.decision)},{dm},{esc(c.decideur_manuel)},{esc(c.langues)},{esc(c.competences)},{esc(c.cv_filename)},{esc(str(c.date_depot))},{esc(c.offre_id)}"
            f") ON CONFLICT (id) DO UPDATE SET score_ia=EXCLUDED.score_ia,decision=EXCLUDED.decision;"
        )
    open(os.path.join(BASE_DIR,"sql_3_cand2.sql"),"w",encoding="utf-8").write("\n".join(lines))
    print(f"sql_3_cand2.sql — {len(lines)} lignes")

    # 4 — Evaluations + Questions
    lines = []
    for e in EvaluationJury.query.all():
        cols = [c.key for c in EvaluationJury.__table__.columns]
        vals = [esc(getattr(e, col)) for col in cols]
        lines.append(f"INSERT INTO evaluation_jury ({','.join(cols)}) VALUES ({','.join(vals)}) ON CONFLICT (id) DO NOTHING;")
    for q in QuestionsEntretien.query.all():
        lines.append(
            f"INSERT INTO questions_entretien (id,candidat_id,questions_json,posees_json,coche_par_json,updated_at) VALUES ("
            f"{q.id},{q.candidat_id},{esc(q.questions_json)},{esc(q.posees_json)},{esc(q.coche_par_json)},{esc(str(q.updated_at))}"
            f") ON CONFLICT (id) DO NOTHING;"
        )
    open(os.path.join(BASE_DIR,"sql_4_evals.sql"),"w",encoding="utf-8").write("\n".join(lines))
    print(f"sql_4_evals.sql — {len(lines)} lignes")

print("\nOK — 4 fichiers créés. Colle-les dans Railway un par un.")
