"""
RecrutIA - Application Flask de recrutement intelligent pour ADER Fes
"""

import os, pickle, re, io
from functools import wraps
import pandas as pd
import pdfplumber
from flask import (Flask, render_template, request, redirect,
                   url_for, flash, jsonify, session)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ─── CONFIGURATION ─────────────────────────────────────────────────────────────

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = "ader_recrut_ia_2024"

# Compte RH (identifiants fixes)
RH_USERNAME = "rh_ader"
RH_PASSWORD = generate_password_hash("ader2024")

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("rh_logged_in"):
            flash("Accès réservé au personnel RH. Veuillez vous connecter.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'recrut.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {"pdf"}

# ─── MODÈLE ML ─────────────────────────────────────────────────────────────────

def charger_ou_entrainer_modele():
    model_path   = os.path.join(BASE_DIR, "models", "rf_model.pkl")
    encoder_path = os.path.join(BASE_DIR, "models", "encoders.pkl")

    if os.path.exists(model_path) and os.path.exists(encoder_path):
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        with open(encoder_path, "rb") as f:
            encoders = pickle.load(f)
        return model, encoders

    # Entraînement automatique si les .pkl n'existent pas (ex: Railway)
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder

    data_path = os.path.join(BASE_DIR, "data", "candidats.csv")
    df = pd.read_csv(data_path, encoding="utf-8-sig")

    niveau_map = {"DOCTORAT":5,"MASTER":4,"LICENCE":3,"TECHNICIEN SPECIALISE":2,"TECHNICIEN":1,"BAC":0}
    df["niveau_diplome"] = df["diplome"].map(niveau_map).fillna(1)
    df["annee_diplome_anciennete"] = 2024 - df["promotion"]

    le_poste      = LabelEncoder()
    le_ecole      = LabelEncoder()
    le_specialite = LabelEncoder()
    df["poste_enc"]      = le_poste.fit_transform(df["poste"].str.upper().str.strip())
    df["ecole_enc"]      = le_ecole.fit_transform(df["ecole"].str.upper().str.strip())
    df["specialite_enc"] = le_specialite.fit_transform(df["specialite"].str.upper().str.strip())

    FEATURES = ["poste_enc","niveau_diplome","ecole_enc","specialite_enc",
                "experience_ans","annee_diplome_anciennete"]
    X, y = df[FEATURES], df["selectionne"]

    model = RandomForestClassifier(n_estimators=200, max_depth=10,
                                   min_samples_split=5, random_state=42,
                                   class_weight="balanced")
    model.fit(X, y)

    encoders = {"le_poste": le_poste, "le_ecole": le_ecole,
                "le_specialite": le_specialite, "features": FEATURES}

    os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(encoder_path, "wb") as f:
        pickle.dump(encoders, f)

    return model, encoders

RF_MODEL, ENCODERS = charger_ou_entrainer_modele()

DIPLOME_NIVEAU = {
    "DOCTORAT": 5, "MASTER": 4, "LICENCE": 3,
    "TECHNICIEN SPECIALISE": 2, "TECHNICIEN": 1, "BAC": 0,
}

POSTES = ["CGM", "ARCHIVISTE", "SI"]
DIPLOMES = ["MASTER", "LICENCE", "TECHNICIEN SPECIALISE", "TECHNICIEN", "DOCTORAT", "BAC"]

# ─── BASE DE DONNÉES ───────────────────────────────────────────────────────────

class Candidat(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    nom          = db.Column(db.String(100))
    prenom       = db.Column(db.String(100))
    email        = db.Column(db.String(120))
    telephone    = db.Column(db.String(20))
    poste        = db.Column(db.String(50))
    diplome      = db.Column(db.String(50))
    specialite   = db.Column(db.String(100))
    ecole        = db.Column(db.String(100))
    promotion    = db.Column(db.Integer)
    experience   = db.Column(db.Integer)
    score_ia     = db.Column(db.Float)
    decision     = db.Column(db.String(20))   # "Présélectionné" / "Non retenu"
    cv_filename  = db.Column(db.String(200))
    date_depot   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "prenom": self.prenom,
            "poste": self.poste,
            "diplome": self.diplome,
            "specialite": self.specialite,
            "experience": self.experience,
            "score_ia": round(self.score_ia * 100, 1) if self.score_ia else 0,
            "decision": self.decision,
            "date_depot": self.date_depot.strftime("%d/%m/%Y") if self.date_depot else "",
        }

with app.app_context():
    db.create_all()

# ─── FONCTIONS UTILITAIRES ─────────────────────────────────────────────────────

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def encoder_safe(le, valeur):
    """Encode une valeur inconnue en 0 si pas dans les classes du LabelEncoder."""
    valeur = str(valeur).upper().strip()
    if valeur in le.classes_:
        return le.transform([valeur])[0]
    return 0


def predire(poste, diplome, specialite, ecole, experience, promotion):
    """Lance la prédiction ML et retourne (probabilité, décision)."""
    niveau = DIPLOME_NIVEAU.get(diplome.upper().strip(), 1)
    anciennete = 2024 - int(promotion)

    features = [[
        encoder_safe(ENCODERS["le_poste"], poste),
        niveau,
        encoder_safe(ENCODERS["le_ecole"], ecole),
        encoder_safe(ENCODERS["le_specialite"], specialite),
        int(experience),
        anciennete,
    ]]

    proba = RF_MODEL.predict_proba(features)[0][1]
    decision = "Présélectionné" if proba >= 0.5 else "Non retenu"
    return round(proba, 4), decision


def extraire_cv(filepath):
    """Extrait les informations clés d'un CV PDF."""
    infos = {
        "nom": "", "prenom": "", "email": "", "telephone": "",
        "diplome": "", "specialite": "", "ecole": "",
        "promotion": 2020, "experience": 0,
    }
    try:
        with pdfplumber.open(filepath) as pdf:
            texte = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )

        lignes = [l.strip() for l in texte.split("\n") if l.strip()]

        # ── Nom / Prénom : première ligne non vide ──────────────────────────
        if lignes:
            mots = lignes[0].split()
            if len(mots) >= 2:
                infos["prenom"] = mots[0].capitalize()
                infos["nom"] = " ".join(mots[1:]).upper()

        # ── Email ────────────────────────────────────────────────────────────
        m = re.search(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", texte)
        if m:
            infos["email"] = m.group()

        # ── Téléphone (France +33 ou Maroc +212 ou 06/07) ───────────────────
        m = re.search(
            r"(?:\+33|0033|0)[1-9](?:[\s.\-]?\d{2}){4}"
            r"|(?:\+212|0212|0)[5-7]\d{8}",
            texte
        )
        if m:
            infos["telephone"] = re.sub(r"[\s.\-]", "", m.group())

        # ── Diplôme ──────────────────────────────────────────────────────────
        diplome_map = {
            "doctorat": "DOCTORAT",
            "master 2": "MASTER", "master2": "MASTER", "mater 2": "MASTER",
            "master 1": "MASTER", "master": "MASTER", "msc": "MASTER",
            "licence": "LICENCE", "bachelor": "LICENCE",
            "technicien specialise": "TECHNICIEN SPECIALISE",
            "technicien spécialisé": "TECHNICIEN SPECIALISE",
            "technicien": "TECHNICIEN",
            "dut": "TECHNICIEN SPECIALISE",
            "bts": "TECHNICIEN SPECIALISE",
            "bac": "BAC",
        }
        texte_lower = texte.lower()
        for mot, valeur in diplome_map.items():
            if mot in texte_lower:
                infos["diplome"] = valeur
                break

        # ── Spécialité : mots-clés domaines ─────────────────────────────────
        specialites_map = {
            "intelligence artificielle": "Intelligence Artificielle",
            "data science": "Data Science",
            "informatique": "Informatique",
            "système d'information": "Système d'information",
            "réseaux": "Réseaux et télécommunications",
            "génie logiciel": "Génie logiciel",
            "finance": "Finance",
            "gestion": "Gestion des entreprises",
            "comptabilit": "Comptabilité",
            "marketing": "Marketing",
            "commerce": "Commerce",
            "génie des procédés": "Génie des procédés",
            "génie civil": "Génie civil",
        }
        for mot, valeur in specialites_map.items():
            if mot in texte_lower:
                infos["specialite"] = valeur
                break

        # ── École ────────────────────────────────────────────────────────────
        ecoles_map = {
            "nexa": "NEXA Digital School",
            "encg": "ENCG", "usmba": "USMBA", "ensa": "ENSA",
            "est ": "EST", "ista": "ISTA", "fsjes": "FSJES",
            "claude bernard": "Université Claude Bernard Lyon 1",
            "lyon 1": "Université Claude Bernard Lyon 1",
            "fede": "FEDE", "umr": "UMR", "ektec": "EKTEC",
        }
        for mot, valeur in ecoles_map.items():
            if mot in texte_lower:
                infos["ecole"] = valeur
                break

        # ── Promotion (dernière année mentionnée) ────────────────────────────
        annees = re.findall(r"\b(20[0-2]\d)\b", texte)
        if annees:
            infos["promotion"] = int(sorted(annees)[-1])

        # ── Expérience totale : calcul depuis les dates d'emploi ─────────────
        # Cherche patterns "Mois AAAA - Mois AAAA" ou "AAAA - AAAA"
        periodes = re.findall(
            r"(\d{4})\s*[-–à]\s*(?:(?:janvier|février|mars|avril|mai|juin|"
            r"juillet|août|septembre|octobre|novembre|décembre)\s+)?(\d{4}|aujourd'hui|présent|actuel)",
            texte, re.IGNORECASE
        )
        total_mois = 0
        for debut, fin in periodes:
            try:
                d = int(debut)
                f = 2024 if fin.lower() in ["aujourd'hui", "présent", "actuel"] else int(fin)
                if 1990 <= d <= 2024 and d <= f:
                    total_mois += (f - d) * 12
            except:
                pass
        if total_mois > 0:
            infos["experience"] = min(round(total_mois / 12), 30)
        else:
            # Fallback : cherche "X an(s) d'expérience"
            m = re.search(r"(\d+)\s*an[s]?\s*d.exp", texte, re.IGNORECASE)
            if m:
                infos["experience"] = int(m.group(1))

    except Exception as e:
        print(f"Erreur extraction CV : {e}")

    return infos

# ─── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ── Candidat : dépôt de candidature ──────────────────────────────────────────

@app.route("/candidature", methods=["GET", "POST"])
def candidature():
    if request.method == "POST":
        # Récupérer les données du formulaire
        nom        = request.form.get("nom", "").strip()
        prenom     = request.form.get("prenom", "").strip()
        email      = request.form.get("email", "").strip()
        telephone  = request.form.get("telephone", "").strip()
        poste      = request.form.get("poste", "")
        diplome    = request.form.get("diplome", "")
        specialite = request.form.get("specialite", "").strip()
        ecole      = request.form.get("ecole", "").strip()
        promotion  = request.form.get("promotion", 2020)
        experience = request.form.get("experience", 0)

        # Fichier CV
        cv_filename = None
        if "cv" in request.files:
            fichier = request.files["cv"]
            if fichier and allowed_file(fichier.filename):
                cv_filename = secure_filename(fichier.filename)
                fichier.save(os.path.join(app.config["UPLOAD_FOLDER"], cv_filename))

        # Prédiction IA
        proba, decision = predire(poste, diplome, specialite,
                                  ecole, experience, promotion)

        # Sauvegarde en base
        candidat = Candidat(
            nom=nom, prenom=prenom, email=email, telephone=telephone,
            poste=poste, diplome=diplome, specialite=specialite,
            ecole=ecole, promotion=int(promotion), experience=int(experience),
            score_ia=proba, decision=decision, cv_filename=cv_filename,
        )
        db.session.add(candidat)
        db.session.commit()

        return render_template("resultat.html",
                               candidat=candidat,
                               score=round(proba * 100, 1))

    return render_template("candidature.html", postes=POSTES, diplomes=DIPLOMES)


# ── Upload CV → extraction automatique ────────────────────────────────────────

@app.route("/extraire_cv", methods=["POST"])
def extraire_cv_route():
    if "cv" not in request.files:
        return jsonify({"error": "Pas de fichier"}), 400

    fichier = request.files["cv"]
    if not allowed_file(fichier.filename):
        return jsonify({"error": "Format non supporté (PDF uniquement)"}), 400

    cv_filename = secure_filename(fichier.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], cv_filename)
    fichier.save(filepath)

    infos = extraire_cv(filepath)
    infos["cv_filename"] = cv_filename
    return jsonify(infos)


# ── Login / Logout RH ─────────────────────────────────────────────────────────

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("rh_logged_in"):
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == RH_USERNAME and check_password_hash(RH_PASSWORD, password):
            session["rh_logged_in"] = True
            flash("Connexion réussie. Bienvenue dans l'espace RH.", "success")
            return redirect(url_for("dashboard"))
        flash("Identifiants incorrects.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Vous êtes déconnecté.", "info")
    return redirect(url_for("index"))


# ── Dashboard RH ──────────────────────────────────────────────────────────────

@app.route("/dashboard")
@login_required
def dashboard():
    candidats = Candidat.query.order_by(Candidat.score_ia.desc()).all()

    stats = {
        "total": len(candidats),
        "preselectionnes": sum(1 for c in candidats if c.decision == "Présélectionné"),
        "non_retenus": sum(1 for c in candidats if c.decision == "Non retenu"),
    }
    stats["taux"] = (
        round(stats["preselectionnes"] / stats["total"] * 100, 1)
        if stats["total"] > 0 else 0
    )

    return render_template("dashboard.html",
                           candidats=candidats, stats=stats)


@app.route("/candidat/<int:candidat_id>")
@login_required
def detail_candidat(candidat_id):
    candidat = Candidat.query.get_or_404(candidat_id)
    return render_template("detail.html",
                           candidat=candidat,
                           score=round(candidat.score_ia * 100, 1))


@app.route("/api/candidats")
@login_required
def api_candidats():
    candidats = Candidat.query.order_by(Candidat.score_ia.desc()).all()
    return jsonify([c.to_dict() for c in candidats])


if __name__ == "__main__":
    app.run(debug=True, port=5000)
