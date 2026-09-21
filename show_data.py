import os, sys
os.environ['DATABASE_URL'] = 'sqlite:///recrut.db'
sys.path.insert(0, '.')
from app import app, Candidat, Offre, EvaluationJury
with app.app_context():
    offres = Offre.query.all()
    candidats = Candidat.query.all()
    evals = EvaluationJury.query.all()
    print(f'{len(offres)} offres, {len(candidats)} candidats, {len(evals)} evals')
    for o in offres:
        print(f'O|{o.id}|{o.titre}|{o.poste}|{o.nombre_postes}|{o.diplome_requis}|{o.experience_min}|{o.specialite or ""}|{o.diplome_requis or ""}')
    for c in candidats:
        sc = round(c.score_ia, 4) if c.score_ia else 0
        print(f'C|{c.id}|{c.nom}|{c.prenom}|{c.email or ""}|{c.telephone or ""}|{c.poste}|{c.diplome}|{c.specialite or ""}|{c.ecole or ""}|{c.promotion or 2020}|{c.experience}|{sc}|{c.decision or "Non retenu"}|{c.offre_id or 1}|{1 if c.decision_manuelle else 0}')
    for e in evals:
        cols = [col.key for col in EvaluationJury.__table__.columns]
        vals = [str(getattr(e, col) or '') for col in cols]
        print('E|' + '|'.join(vals))
