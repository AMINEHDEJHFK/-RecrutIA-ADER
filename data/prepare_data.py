"""
Script de préparation des données :
- Charge les vraies données des fichiers Excel ADER
- Génère des données synthétiques pour enrichir le dataset
- Sauvegarde le dataset final en CSV
"""

import pandas as pd
import numpy as np
import os

# ─── 1. DONNÉES RÉELLES ────────────────────────────────────────────────────────

real_data = [
    # Chargé Gestion des Marchés (CGM) — 7 candidats, 4 convoqués
    {"poste": "CGM", "diplome": "MASTER", "specialite": "Finances contrôle et audit",
     "ecole": "USMBA", "promotion": 2021, "experience_ans": 3, "selectionne": 1},
    {"poste": "CGM", "diplome": "MASTER", "specialite": "Gestion Financière et comptable",
     "ecole": "ENCG", "promotion": 2020, "experience_ans": 3, "selectionne": 1},
    {"poste": "CGM", "diplome": "MASTER", "specialite": "Gestion Financière et comptable",
     "ecole": "ENCG", "promotion": 2020, "experience_ans": 3, "selectionne": 1},
    {"poste": "CGM", "diplome": "MASTER", "specialite": "Management comptable et financier",
     "ecole": "USMBA", "promotion": 2019, "experience_ans": 3, "selectionne": 1},
    {"poste": "CGM", "diplome": "MASTER", "specialite": "Management financier et comptable",
     "ecole": "USMBA", "promotion": 2015, "experience_ans": 6, "selectionne": 0},
    {"poste": "CGM", "diplome": "LICENCE", "specialite": "Gestion des entreprises",
     "ecole": "FSJES", "promotion": 1990, "experience_ans": 7, "selectionne": 0},
    {"poste": "CGM", "diplome": "MASTER", "specialite": "Finances des marchés",
     "ecole": "UMR", "promotion": 2015, "experience_ans": 3, "selectionne": 0},

    # Aides Archiviste — 23 candidats, 5 convoqués
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Développement informatique",
     "ecole": "ISTA", "promotion": 2007, "experience_ans": 16, "selectionne": 1},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Audiovisuel",
     "ecole": "ISTA", "promotion": 2015, "experience_ans": 6, "selectionne": 1},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Développement informatique",
     "ecole": "ISTA", "promotion": 2014, "experience_ans": 7, "selectionne": 1},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN", "specialite": "Agent technique de vente",
     "ecole": "ISTA", "promotion": 2007, "experience_ans": 6, "selectionne": 1},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Commerce",
     "ecole": "ISTA", "promotion": 2019, "experience_ans": 0, "selectionne": 1},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Gestion des entreprises",
     "ecole": "ISTA", "promotion": 2014, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "LICENCE", "specialite": "Géographie",
     "ecole": "USM", "promotion": 2022, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Développement informatique",
     "ecole": "ISTA", "promotion": 2008, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Technique de développement Informatique",
     "ecole": "ISTA", "promotion": 2017, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Technique de développement Informatique",
     "ecole": "ISTA", "promotion": 2015, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Développement informatique",
     "ecole": "ISTA", "promotion": 2021, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Gestion des entreprises",
     "ecole": "MIAGE", "promotion": 2017, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Gestion des entreprises",
     "ecole": "ISTA", "promotion": 2010, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "LICENCE", "specialite": "Economie et Gestion",
     "ecole": "FSJES", "promotion": 2021, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Commerce",
     "ecole": "ISTA", "promotion": 2018, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN", "specialite": "Gestion informatisée",
     "ecole": "EKTEC", "promotion": 2008, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Réseaux Informatique",
     "ecole": "ISTA", "promotion": 2012, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Management touristique",
     "ecole": "ISTA", "promotion": 2024, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "LICENCE", "specialite": "Management et gestion de PME",
     "ecole": "FEDE", "promotion": 2020, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Commerce",
     "ecole": "ISTA", "promotion": 2019, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Gestion Financière et Comptable",
     "ecole": "ENCG", "promotion": 2023, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Gestion des entreprises",
     "ecole": "ISTA", "promotion": 2019, "experience_ans": 0, "selectionne": 0},
    {"poste": "ARCHIVISTE", "diplome": "TECHNICIEN", "specialite": "Comptable d'entreprises",
     "ecole": "ISTA", "promotion": 2020, "experience_ans": 0, "selectionne": 0},

    # Cadre Système d'Information (SI) — 2 convoqués sur ~10
    {"poste": "SI", "diplome": "MASTER", "specialite": "Informatique",
     "ecole": "USMBA", "promotion": 2020, "experience_ans": 3, "selectionne": 1},
    {"poste": "SI", "diplome": "MASTER", "specialite": "Système d'information",
     "ecole": "ENCG", "promotion": 2019, "experience_ans": 4, "selectionne": 1},
    {"poste": "SI", "diplome": "LICENCE", "specialite": "Informatique",
     "ecole": "FSJES", "promotion": 2021, "experience_ans": 1, "selectionne": 0},
    {"poste": "SI", "diplome": "TECHNICIEN SPECIALISE", "specialite": "Réseaux",
     "ecole": "ISTA", "promotion": 2018, "experience_ans": 2, "selectionne": 0},
    {"poste": "SI", "diplome": "LICENCE", "specialite": "Gestion",
     "ecole": "FSJES", "promotion": 2022, "experience_ans": 0, "selectionne": 0},
]

df_real = pd.DataFrame(real_data)

# ─── 2. DONNÉES SYNTHÉTIQUES ──────────────────────────────────────────────────

np.random.seed(42)

postes = ["CGM", "ARCHIVISTE", "SI"]
diplomes_niveau = {
    "DOCTORAT": 5, "MASTER": 4, "LICENCE": 3,
    "TECHNICIEN SPECIALISE": 2, "TECHNICIEN": 1, "BAC": 0
}

specialites_par_poste = {
    "CGM": ["Finances contrôle et audit", "Gestion Financière et comptable",
            "Management financier", "Comptabilité", "Audit", "Droit des affaires",
            "Gestion des entreprises", "Marketing"],
    "ARCHIVISTE": ["Développement informatique", "Gestion des entreprises",
                   "Commerce", "Audiovisuel", "Réseaux Informatique",
                   "Secrétariat", "Documentation", "Bibliothéconomie",
                   "Management touristique", "Comptabilité"],
    "SI": ["Informatique", "Système d'information", "Réseaux et télécommunications",
           "Génie logiciel", "Cybersécurité", "Base de données",
           "Développement web", "Intelligence artificielle"],
}

ecoles_reconnues = ["ENCG", "USMBA", "ENSA", "EST", "ISTA", "FSJES", "FEDE", "UMR"]
ecoles_autres = ["EKTEC", "MIAGE", "USM", "ESISA", "ISGA"]

synthetic_rows = []
for _ in range(600):
    poste = np.random.choice(postes)

    # Diplôme selon poste
    if poste == "CGM":
        diplome = np.random.choice(
            ["MASTER", "MASTER", "MASTER", "LICENCE", "DOCTORAT"],
            p=[0.5, 0.2, 0.1, 0.15, 0.05]
        )
        diplome = np.random.choice(["MASTER", "LICENCE", "DOCTORAT"], p=[0.65, 0.25, 0.10])
    elif poste == "ARCHIVISTE":
        diplome = np.random.choice(
            ["TECHNICIEN SPECIALISE", "TECHNICIEN", "LICENCE", "MASTER"],
            p=[0.50, 0.20, 0.20, 0.10]
        )
    else:  # SI
        diplome = np.random.choice(
            ["MASTER", "LICENCE", "TECHNICIEN SPECIALISE", "DOCTORAT"],
            p=[0.50, 0.30, 0.15, 0.05]
        )

    specialite = np.random.choice(specialites_par_poste[poste])
    toutes_ecoles = ecoles_reconnues + ecoles_autres  # 13 écoles
    ecole = np.random.choice(toutes_ecoles,
                             p=[0.12, 0.12, 0.08, 0.10, 0.14, 0.09, 0.06, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04])
    promotion = np.random.randint(2005, 2025)
    experience_ans = np.random.randint(0, 15)

    # Logique de sélection basée sur des règles métier ADER
    score = 0
    niveau = diplomes_niveau.get(diplome, 0)

    if poste == "CGM":
        if niveau >= 4:
            score += 3  # Master requis
        if "financ" in specialite.lower() or "audit" in specialite.lower() or "comptab" in specialite.lower():
            score += 2
        if ecole in ["ENCG", "USMBA", "FSJES"]:
            score += 1
        if 2 <= experience_ans <= 8:
            score += 2
        if experience_ans > 10:
            score -= 1

    elif poste == "ARCHIVISTE":
        if niveau >= 2:
            score += 2
        if "informatique" in specialite.lower() or "document" in specialite.lower() or "archive" in specialite.lower():
            score += 2
        if ecole in ["ISTA", "EST"]:
            score += 1
        if experience_ans >= 5:
            score += 2
        elif experience_ans >= 2:
            score += 1

    else:  # SI
        if niveau >= 4:
            score += 3
        if "informatique" in specialite.lower() or "système" in specialite.lower() or "logiciel" in specialite.lower():
            score += 2
        if ecole in ["ENSA", "USMBA", "ENCG"]:
            score += 1
        if 2 <= experience_ans <= 10:
            score += 2

    # Ajouter du bruit
    score += np.random.normal(0, 0.8)
    selectionne = 1 if score >= 4.5 else 0

    synthetic_rows.append({
        "poste": poste,
        "diplome": diplome,
        "specialite": specialite,
        "ecole": ecole,
        "promotion": promotion,
        "experience_ans": experience_ans,
        "selectionne": selectionne,
    })

df_synthetic = pd.DataFrame(synthetic_rows)

# ─── 3. FUSION ET SAUVEGARDE ──────────────────────────────────────────────────

df_final = pd.concat([df_real, df_synthetic], ignore_index=True)
df_final["source"] = ["reel"] * len(df_real) + ["synthetique"] * len(df_synthetic)

output_path = os.path.join(os.path.dirname(__file__), "candidats.csv")
df_final.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Dataset cree : {len(df_final)} lignes")
print(f"  Reelles      : {len(df_real)}")
print(f"  Synthetiques : {len(df_synthetic)}")
print(f"\nDistribution selectionnes :")
print(df_final["selectionne"].value_counts())
print(f"\nFichier : {output_path}")
