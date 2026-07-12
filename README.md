# RecrutIA - ADER Fès

Système intelligent de présélection des candidats pour l'Agence de Développement de la Région de Fès-Meknès.

## Prérequis

- Python 3.11+
- pip

## Installation

```bash
pip install flask flask-sqlalchemy scikit-learn pandas numpy pdfplumber openpyxl werkzeug
```

## Lancement

```bash
# 1. Générer les données
python data/prepare_data.py

# 2. Entraîner le modèle
python models/train_model.py

# 3. Lancer l'application
python app.py
```

Accès : http://localhost:5000

## Identifiants de test

- Dashboard RH : http://localhost:5000/dashboard
- Dépôt candidature : http://localhost:5000/candidature

## Stack technique

- Backend : Flask (Python)
- Base de données : SQLite
- ML : Random Forest (scikit-learn) — Accuracy : 77%
- CV Parsing : pdfplumber + regex
- Frontend : Bootstrap 5 + Font Awesome
