import os, sys
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(BASE_DIR, 'recrut.db')}"
sys.path.insert(0, BASE_DIR)
from app import app, EvaluationJury, QuestionsEntretien

def esc(v):
    if v is None: return "NULL"
    if isinstance(v, bool): return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)): return str(v)
    return "'" + str(v).replace("'", "''") + "'"

with app.app_context():
    # Evaluations seulement
    lines = []
    for e in EvaluationJury.query.all():
        cols = [c.key for c in EvaluationJury.__table__.columns]
        vals = [esc(getattr(e, col)) for col in cols]
        lines.append(f"INSERT INTO evaluation_jury ({','.join(cols)}) VALUES ({','.join(vals)}) ON CONFLICT (id) DO NOTHING;")
    open(os.path.join(BASE_DIR,"sql_4a_evals.sql"),"w",encoding="utf-8").write("\n".join(lines))
    print(f"sql_4a_evals.sql — {len(lines)} lignes")

    # Questions seulement (une par une)
    questions = QuestionsEntretien.query.all()
    for i, q in enumerate(questions):
        line = (f"INSERT INTO questions_entretien (id,candidat_id,questions_json,posees_json,coche_par_json,updated_at) VALUES ("
                f"{q.id},{q.candidat_id},{esc(q.questions_json)},{esc(q.posees_json)},{esc(q.coche_par_json)},{esc(str(q.updated_at))}"
                f") ON CONFLICT (id) DO NOTHING;")
        fname = os.path.join(BASE_DIR, f"sql_5_q{i+1}.sql")
        open(fname,"w",encoding="utf-8").write(line)
    print(f"sql_5_q*.sql — {len(questions)} fichiers (un par question)")

print("OK")
