"""
Entraînement du modèle NLP de compatibilité candidat ↔ offre.
Algorithme : TF-IDF + Logistic Regression (classification supervisée)
Variable cible : selectionne (0 = non retenu, 1 = présélectionné)

Ce modèle complète le Random Forest (critères structurés) en ajoutant
une dimension textuelle : il apprend quels profils textuels sont sélectionnés.
"""

import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline

# ─── 1. CHARGEMENT DES DONNÉES ────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "data", "candidats.csv")
df = pd.read_csv(data_path, encoding="utf-8-sig")

print(f"Dataset : {df.shape[0]} candidats")
print(f"Sélectionnés : {df['selectionne'].sum()} | Non retenus : {(df['selectionne']==0).sum()}")

# ─── 2. CONSTRUCTION DU TEXTE REPRÉSENTATIF DE CHAQUE CANDIDAT ───────────────
# On concatène les champs textuels pour créer un "document" par candidat
# Ex: "CGM MASTER Finances controle audit USMBA 3 ans"

def construire_texte_candidat(row):
    parties = [
        str(row.get("poste", "")),
        str(row.get("diplome", "")),
        str(row.get("specialite", "")),
        str(row.get("ecole", "")),
        f"{row.get('experience_ans', 0)} ans experience",
    ]
    return " ".join(p for p in parties if p and p != "nan").lower()

df["texte"] = df.apply(construire_texte_candidat, axis=1)

print("\nExemple de texte généré :")
print(f"  → {df['texte'].iloc[0]}")

X = df["texte"]
y = df["selectionne"]

# ─── 3. SPLIT TRAIN / TEST (80% / 20%) ────────────────────────────────────────

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain : {len(X_train)} | Test : {len(X_test)}")

# ─── 4. PIPELINE TF-IDF + LOGISTIC REGRESSION ────────────────────────────────
# Pipeline = TF-IDF vectorise le texte, puis Logistic Regression classifie

nlp_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),    # unigrammes + bigrammes
        min_df=2,              # ignore les mots qui apparaissent moins de 2 fois
        max_features=5000,     # garde les 5000 features les plus utiles
        sublinear_tf=True,     # log(tf) pour atténuer les répétitions
    )),
    ("clf", LogisticRegression(
        class_weight="balanced",   # compense le déséquilibre 0/1
        max_iter=1000,
        random_state=42,
        C=1.0,                     # régularisation standard
    )),
])

nlp_pipeline.fit(X_train, y_train)

# ─── 5. ÉVALUATION ────────────────────────────────────────────────────────────

y_pred = nlp_pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\nAccuracy NLP : {acc:.2%}")
print("\nClassification Report :")
print(classification_report(y_test, y_pred,
                            target_names=["Non sélectionné", "Sélectionné"]))

# ─── 6. SAUVEGARDE ────────────────────────────────────────────────────────────

models_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(models_dir, "nlp_model.pkl")

with open(model_path, "wb") as f:
    pickle.dump(nlp_pipeline, f)

print(f"\nModèle NLP sauvegardé : {model_path}")
print("Utilisation : nlp_pipeline.predict_proba([texte_candidat])[0][1]")
