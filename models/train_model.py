"""
Entraînement du modèle ML de présélection des candidats ADER Fes.
Algorithme : Random Forest (classification)
Variable cible : selectionne (0 = non retenu, 1 = présélectionné)
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)

# ─── 1. CHARGEMENT DES DONNÉES ────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "candidats.csv")
df = pd.read_csv(data_path, encoding="utf-8-sig")

print(f"Dataset : {df.shape[0]} lignes, {df.shape[1]} colonnes")

# ─── 2. FEATURE ENGINEERING ───────────────────────────────────────────────────

# Niveau de diplôme en valeur numérique
diplome_niveau = {
    "DOCTORAT": 5,
    "MASTER": 4,
    "LICENCE": 3,
    "TECHNICIEN SPECIALISE": 2,
    "TECHNICIEN": 1,
    "BAC": 0,
}
df["niveau_diplome"] = df["diplome"].map(diplome_niveau).fillna(1)

# Ancienneté du diplôme
df["annee_diplome_anciennete"] = 2024 - df["promotion"]

# Encodage des variables catégorielles
le_poste = LabelEncoder()
le_ecole = LabelEncoder()
le_specialite = LabelEncoder()

df["poste_enc"] = le_poste.fit_transform(df["poste"].str.upper().str.strip())
df["ecole_enc"] = le_ecole.fit_transform(df["ecole"].str.upper().str.strip())
df["specialite_enc"] = le_specialite.fit_transform(
    df["specialite"].str.upper().str.strip()
)

# Features finales
FEATURES = [
    "poste_enc",
    "niveau_diplome",
    "ecole_enc",
    "specialite_enc",
    "experience_ans",
    "annee_diplome_anciennete",
]

X = df[FEATURES]
y = df["selectionne"]

# ─── 3. SPLIT TRAIN / TEST (80% / 20%) ────────────────────────────────────────

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train : {len(X_train)} | Test : {len(X_test)}")

# ─── 4. ENTRAÎNEMENT RANDOM FOREST ────────────────────────────────────────────

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced",
)
rf_model.fit(X_train, y_train)

# ─── 5. ÉVALUATION ────────────────────────────────────────────────────────────

y_pred = rf_model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\nAccuracy : {acc:.2%}")
print("\nClassification Report :")
print(classification_report(y_test, y_pred,
                            target_names=["Non selectionne", "Selectionne"]))
print("Confusion Matrix :")
print(confusion_matrix(y_test, y_pred))

# Importance des features
print("\nImportance des variables :")
for feat, imp in sorted(zip(FEATURES, rf_model.feature_importances_),
                         key=lambda x: -x[1]):
    print(f"  {feat:<30} {imp:.3f}")

# ─── 6. SAUVEGARDE DU MODÈLE ET ENCODEURS ─────────────────────────────────────

models_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(models_dir, "rf_model.pkl"), "wb") as f:
    pickle.dump(rf_model, f)

with open(os.path.join(models_dir, "encoders.pkl"), "wb") as f:
    pickle.dump({
        "le_poste": le_poste,
        "le_ecole": le_ecole,
        "le_specialite": le_specialite,
        "features": FEATURES,
    }, f)

print("\nModele et encodeurs sauvegardes.")
