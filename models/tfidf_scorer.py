"""
Scoring de compatibilité candidat ↔ offre par TF-IDF + similarité cosinus.
Aucune API externe requise — fonctionne entièrement en local.
"""

import unicodedata
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _nettoyer(texte: str) -> str:
    """Minuscules, sans accents, sans ponctuation inutile."""
    if not texte:
        return ""
    texte = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode("ascii")
    texte = texte.lower()
    texte = re.sub(r"[^\w\s]", " ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte


def _texte_offre(offre) -> str:
    """Construit un texte représentatif de l'offre à partir de ses champs."""
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


def _texte_candidat(candidat_dict: dict) -> str:
    """Construit un texte représentatif du candidat à partir de ses champs."""
    parties = [
        candidat_dict.get("poste", ""),
        candidat_dict.get("diplome", ""),
        candidat_dict.get("specialite", ""),
        candidat_dict.get("ecole", ""),
        candidat_dict.get("competences", ""),
        candidat_dict.get("langues", ""),
    ]
    # Ajoute l'expérience sous forme lisible
    exp = candidat_dict.get("experience", 0)
    if exp:
        parties.append(f"{exp} ans experience")
    return _nettoyer(" ".join(str(p) for p in parties if p))


def scorer_compatibilite(offre, candidat_dict: dict) -> float:
    """
    Retourne un score de compatibilité entre 0.0 et 1.0.
    0.0 = aucun rapport | 1.0 = parfaitement compatible.

    offre         : objet SQLAlchemy Offre (avec titre, missions, competences...)
    candidat_dict : dict avec clés poste, diplome, specialite, ecole, competences, langues, experience
    """
    texte_o = _texte_offre(offre)
    texte_c = _texte_candidat(candidat_dict)

    if not texte_o or not texte_c:
        return 0.5  # pas assez de texte → score neutre

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),   # unigrammes + bigrammes
        min_df=1,
        sublinear_tf=True,    # atténue l'effet des mots très fréquents
    )

    try:
        matrice = vectorizer.fit_transform([texte_o, texte_c])
        score = float(cosine_similarity(matrice[0], matrice[1])[0][0])
    except Exception:
        return 0.5

    # Normalise entre 0.1 et 1.0 pour éviter les scores nuls
    # (même un candidat peu compatible mérite un plancher)
    score = 0.1 + 0.9 * min(score * 3.0, 1.0)
    return round(score, 4)


def score_final_fusionne(score_rf: float, score_tfidf: float,
                          poids_rf: float = 0.65) -> float:
    """
    Fusionne le score Random Forest (critères structurés) et
    le score TF-IDF (compatibilité textuelle avec l'offre).

    poids_rf = 0.65 → RF pèse 65%, TF-IDF 35%
    """
    poids_tfidf = 1.0 - poids_rf
    return round(poids_rf * score_rf + poids_tfidf * score_tfidf, 4)
