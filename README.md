# RecrutIA ADER

Application web de présélection des candidats par intelligence artificielle explicable, développée pour l'ADER-Fès (Agence pour le Développement et la Réhabilitation de la ville de Fès) dans le cadre de ma thèse professionnelle (Mastère Data & IA).

- **URL publique :** https://web-production-ae396c.up.railway.app
- **Dépôt Git :** https://github.com/AMINEHDEJHFK/-RecrutIA-ADER

## Fonctionnalités

- Import des CV (PDF) par le service RH et extraction automatique des informations
- Score de présélection : 65 % Random Forest + 35 % NLP (TF-IDF), avec explication SHAP de chaque score
- Décision automatique : Présélectionné (≥ 0,34), À examiner (0,24 – 0,34), Non retenu (< 0,24)
- Évaluation des candidats par les 4 membres du jury, moyenne calculée automatiquement
- Génération de 10 questions d'entretien personnalisées
- Vérification des pièces du dossier et classement final

> L'API Claude (extraction des CV et questions d'entretien) est utilisée uniquement pour les tests, car l'ADER-Fès ne dispose pas encore d'un modèle de langage local. Sans clé API, l'application fonctionne avec une extraction par règles.

## Prérequis

- Python 3.11 ou plus
- pip
- (facultatif) Poppler, uniquement pour lire les annonces PDF scannées
- (facultatif) une clé API Anthropic

## Installation

```bash
git clone https://github.com/AMINEHDEJHFK/-RecrutIA-ADER.git
cd -RecrutIA-ADER
python -m venv venv
venv\Scripts\activate          # Windows  (Linux / macOS : source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # Linux / macOS : cp .env.example .env
```

Remplir ensuite le fichier `.env` (clé API facultative).

## Base de données

Par défaut, l'application utilise une base **SQLite** (`recrut.db`), créée automatiquement au premier lancement. SQLite ne demande ni utilisateur ni mot de passe.

Pour charger les données de test fournies :

```bash
sqlite3 recrut.db < recrutia_dump.sql
```

En production, l'application utilise **PostgreSQL** : il suffit de renseigner `DATABASE_URL` dans le `.env`, par exemple `postgresql://utilisateur:motdepasse@localhost:5432/recrutia`. Les identifiants de la base de production ne sont pas publiés dans ce dépôt.

## Lancement

```bash
python app.py
```

Puis ouvrir http://localhost:5000

Pour réentraîner les modèles (facultatif, les fichiers `.pkl` sont déjà fournis) :

```bash
python models/train_model.py
python models/train_nlp_model.py
```

## Identifiants de test

| Rôle | Identifiant | Mot de passe | Accès |
|---|---|---|---|
| Administrateur (back office) | `admin` | `ader2024` | Gestion des comptes + toutes les fonctions RH |
| Jury 1 | `bouchra.ader` | `bouchraader` | Grille d'évaluation du jury 1 |
| Jury 2 | `ali.ader` | `aliader` | Grille d'évaluation du jury 2 |
| Jury 3 | `younnes.benjalloun` | `younnesader` | Grille d'évaluation du jury 3 |
| Jury 4 | `fati.ader` | `fatiader` | Grille d'évaluation du jury 4 |

Accès administrateur au back office : se connecter avec `admin`, puis menu **Utilisateurs** (`/admin/utilisateurs`).

Ces comptes sont créés automatiquement au premier démarrage. Leurs mots de passe doivent être changés avant toute utilisation réelle.

## Compatibilité navigateurs

Interface construite avec Bootstrap 5, compatible avec les navigateurs récents : Google Chrome, Mozilla Firefox, Microsoft Edge et Safari.

## Stack technique

- Back-end : Python, Flask, SQLAlchemy
- Base de données : SQLite (local), PostgreSQL (production)
- Machine learning : scikit-learn (Random Forest, TF-IDF + régression logistique), SHAP
- Extraction des CV : pdfplumber + API Claude (tests) avec repli par règles
- Front-end : Jinja2, Bootstrap 5, Font Awesome
- Déploiement : Gunicorn (Procfile)

## Structure

```
app.py                 application Flask (routes, modèles de données)
models/                modèles ML (.pkl) et scripts d'entraînement
data/                  jeu de données d'entraînement (candidats.csv)
templates/             pages HTML (Jinja2)
static/                CSS, images
recrutia_dump.sql      export SQL (structure + données de test)
requirements.txt       dépendances Python
.env.example           modèle du fichier de configuration
Procfile, nixpacks.toml  configuration du déploiement
```
