"""
Scoring NLP de compatibilité candidat ↔ offre.
Modèle : TF-IDF + Logistic Regression (entraîné sur 635 candidats ADER).
Aucune API externe — fonctionne entièrement en local.
"""

import os
import pickle
import unicodedata
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── Chargement du modèle NLP entraîné ───────────────────────────────────────

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_NLP_MODEL_PATH = os.path.join(_BASE_DIR, "nlp_model.pkl")

_NLP_MODEL = None

def _charger_nlp_model():
    """Charge le modèle NLP depuis le .pkl, ou l'entraîne automatiquement s'il n'existe pas."""
    global _NLP_MODEL
    if _NLP_MODEL is not None:
        return _NLP_MODEL

    if os.path.exists(_NLP_MODEL_PATH):
        with open(_NLP_MODEL_PATH, "rb") as f:
            _NLP_MODEL = pickle.load(f)
        return _NLP_MODEL

    # ── Entraînement automatique (ex: premier démarrage sur Railway) ──────────
    try:
        import pandas as pd
        from sklearn.pipeline import Pipeline
        from sklearn.linear_model import LogisticRegression

        data_path = os.path.join(_BASE_DIR, "..", "data", "candidats.csv")
        df = pd.read_csv(data_path, encoding="utf-8-sig")

        def _construire_texte(row):
            parties = [
                str(row.get("poste", "")),
                str(row.get("diplome", "")),
                str(row.get("specialite", "")),
                str(row.get("ecole", "")),
                f"{row.get('experience_ans', 0)} ans experience",
            ]
            return " ".join(p for p in parties if p and p != "nan").lower()

        df["texte"] = df.apply(_construire_texte, axis=1)

        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=2,
                max_features=5000,
                sublinear_tf=True,
            )),
            ("clf", LogisticRegression(
                class_weight="balanced",
                max_iter=1000,
                random_state=42,
            )),
        ])
        pipeline.fit(df["texte"], df["selectionne"])

        with open(_NLP_MODEL_PATH, "wb") as f:
            pickle.dump(pipeline, f)

        _NLP_MODEL = pipeline
    except Exception:
        _NLP_MODEL = None

    return _NLP_MODEL


# ─── Utilitaires texte ────────────────────────────────────────────────────────

def _nettoyer(texte: str) -> str:
    """Minuscules, sans accents, sans ponctuation inutile."""
    if not texte:
        return ""
    texte = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode("ascii")
    texte = texte.lower()
    texte = re.sub(r"[^\w\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


def _texte_candidat(candidat_dict: dict) -> str:
    """Construit le texte représentatif du candidat (même format que l'entraînement)."""
    parties = [
        candidat_dict.get("poste", ""),
        candidat_dict.get("diplome", ""),
        candidat_dict.get("specialite", ""),
        candidat_dict.get("ecole", ""),
        f"{candidat_dict.get('experience', 0)} ans experience",
        candidat_dict.get("competences", ""),
        candidat_dict.get("langues", ""),
    ]
    return _nettoyer(" ".join(str(p) for p in parties if p and str(p) != "nan"))


def _texte_offre(offre) -> str:
    """Construit le texte représentatif de l'offre."""
    parties = [
        offre.titre or "",
        offre.poste or "",
        offre.specialite or "",
        offre.missions or "",
        offre.attributions or "",
        offre.competences or "",
        offre.mots_cles or "",
    ]
    return _nettoyer(" ".join(p for p in parties if p))


# ─── Scoring principal ────────────────────────────────────────────────────────

def scorer_compatibilite(offre, candidat_dict: dict) -> float:
    """
    Retourne un score de compatibilité entre 0.0 et 1.0.

    Étape 1 : utilise le modèle NLP entraîné (TF-IDF + Logistic Regression)
              pour scorer le profil textuel du candidat.
    Étape 2 : ajuste le score selon la similarité cosinus avec le texte de l'offre.

    offre         : objet SQLAlchemy Offre
    candidat_dict : dict avec poste, diplome, specialite, ecole, experience, competences, langues
    """
    texte_c = _texte_candidat(candidat_dict)
    texte_o = _texte_offre(offre)

    if not texte_c:
        return 0.5

    model = _charger_nlp_model()

    # ── Score NLP (modèle entraîné sur 635 candidats) ──────────────────────────
    if model is not None:
        try:
            score_nlp = float(model.predict_proba([texte_c])[0][1])
        except Exception:
            score_nlp = 0.5
    else:
        score_nlp = 0.5

    # ── Ajustement par similarité cosinus offre ↔ candidat ────────────────────
    if texte_o:
        try:
            vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
            matrice = vectorizer.fit_transform([texte_o, texte_c])
            sim = float(cosine_similarity(matrice[0], matrice[1])[0][0])
            # Normalise la similarité entre 0.1 et 1.0
            sim_norm = 0.1 + 0.9 * min(sim * 3.0, 1.0)
            # Score final NLP = 70% modèle entraîné + 30% similarité avec l'offre
            score_final = 0.70 * score_nlp + 0.30 * sim_norm
        except Exception:
            score_final = score_nlp
    else:
        score_final = score_nlp

    return round(score_final, 4)


def score_final_fusionne(score_rf: float, score_tfidf: float,
                          poids_rf: float = 0.65) -> float:
    """
    Fusionne le score Random Forest (critères structurés) et
    le score NLP (compatibilité textuelle avec l'offre).

    poids_rf = 0.65 → RF pèse 65%, NLP 35%
    """
    poids_tfidf = 1.0 - poids_rf
    return round(poids_rf * score_rf + poids_tfidf * score_tfidf, 4)
