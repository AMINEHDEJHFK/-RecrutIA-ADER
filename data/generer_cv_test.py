"""
Génération de 3 CV PDF de test pour RecrutIA ADER Fès
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "static", "cv_tests")
os.makedirs(OUT, exist_ok=True)

W, H = A4  # 595 x 842

BLEU = (0.10, 0.23, 0.36)
OR   = (0.78, 0.66, 0.29)

def ligne(c, x, y, largeur):
    c.setStrokeColorRGB(*OR)
    c.setLineWidth(1.5)
    c.line(x, y, x + largeur, y)

def titre_section(c, x, y, texte):
    c.setFillColorRGB(*BLEU)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, texte)
    ligne(c, x, y - 4, W - 2 * x)
    return y - 20

def entete(c, nom, titre, email, tel, ville):
    # Fond bleu
    c.setFillColorRGB(*BLEU)
    c.rect(0, H - 120, W, 120, fill=1, stroke=0)
    # Nom
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, H - 55, nom)
    # Titre
    c.setFillColorRGB(*OR)
    c.setFont("Helvetica", 13)
    c.drawString(40, H - 78, titre)
    # Infos contact
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.setFont("Helvetica", 10)
    c.drawString(40, H - 100, f"{ville}  |  {tel}  |  {email}")

def bullet_item(c, x, y, texte, taille=10):
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica", taille)
    c.drawString(x, y, f"- {texte}")
    return y - 16

def sous_titre(c, x, y, poste, dates, lieu):
    c.setFillColorRGB(*BLEU)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, poste)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(x, y - 14, f"{lieu}  |  {dates}")
    return y - 30

# ═══════════════════════════════════════════════════════
# CV 1 — Bon profil CGM (devrait être PRÉSÉLECTIONNÉ)
# ═══════════════════════════════════════════════════════
c = canvas.Canvas(os.path.join(OUT, "CV_ALAMI_Youssef_CGM.pdf"), pagesize=A4)

entete(c, "ALAMI Youssef", "Candidat - Chargé de Gestion des Marchés",
       "youssef.alami@gmail.com", "0661234567", "Fès, Maroc")

y = H - 145
y = titre_section(c, 40, y, "FORMATION")
y = sous_titre(c, 40, y, "Master en Gestion Financière et Comptable", "2018 - 2020", "ENCG Fès")
y = sous_titre(c, 40, y, "Licence en Sciences Economiques", "2015 - 2018", "FSJES Fès")

y -= 10
y = titre_section(c, 40, y, "EXPERIENCE PROFESSIONNELLE")
y = sous_titre(c, 40, y, "Responsable Marchés Publics", "2020 - 2024 (4 ans)", "Commune de Fès")
y = bullet_item(c, 55, y, "Gestion et suivi des appels d'offres")
y = bullet_item(c, 55, y, "Rédaction des cahiers des charges")
y = bullet_item(c, 55, y, "Contrôle de la conformité réglementaire")

y -= 10
y = titre_section(c, 40, y, "COMPETENCES")
y = bullet_item(c, 55, y, "Maîtrise des marchés publics et réglementation")
y = bullet_item(c, 55, y, "Comptabilité analytique et contrôle de gestion")
y = bullet_item(c, 55, y, "Maîtrise de Excel, SAP")

y -= 10
y = titre_section(c, 40, y, "LANGUES")
y = bullet_item(c, 55, y, "Arabe : Langue maternelle")
y = bullet_item(c, 55, y, "Français : Courant (C1)")
y = bullet_item(c, 55, y, "Anglais : Intermédiaire (B1)")

c.save()
print("CV 1 cree : ALAMI Youssef (CGM - bon profil)")

# ═══════════════════════════════════════════════════════
# CV 2 — Bon profil SI (devrait être PRÉSÉLECTIONNÉ)
# ═══════════════════════════════════════════════════════
c = canvas.Canvas(os.path.join(OUT, "CV_BENALI_Sara_SI.pdf"), pagesize=A4)

entete(c, "BENALI Sara", "Candidat - Cadre Système d'Information",
       "sara.benali@gmail.com", "0677890123", "Fès, Maroc")

y = H - 145
y = titre_section(c, 40, y, "FORMATION")
y = sous_titre(c, 40, y, "Master en Informatique et Systemes d'Information", "2019 - 2021", "USMBA Fès")
y = sous_titre(c, 40, y, "Licence en Génie Informatique", "2016 - 2019", "ENSA Fès")

y -= 10
y = titre_section(c, 40, y, "EXPERIENCE PROFESSIONNELLE")
y = sous_titre(c, 40, y, "Développeuse Web Full Stack", "2021 - 2024 (3 ans)", "AgriTech Maroc, Fès")
y = bullet_item(c, 55, y, "Développement d'applications web en Python / Django")
y = bullet_item(c, 55, y, "Administration bases de données PostgreSQL")
y = bullet_item(c, 55, y, "Mise en place d'APIs REST et intégration mobile")

y = sous_titre(c, 40, y, "Stagiaire Développement", "2021 (6 mois)", "OCP Khouribga")
y = bullet_item(c, 55, y, "Développement d'un tableau de bord de suivi de production")

y -= 10
y = titre_section(c, 40, y, "COMPETENCES TECHNIQUES")
y = bullet_item(c, 55, y, "Python, Java, JavaScript, SQL")
y = bullet_item(c, 55, y, "Django, Flask, React")
y = bullet_item(c, 55, y, "Docker, Git, Linux")
y = bullet_item(c, 55, y, "Machine Learning (scikit-learn, TensorFlow)")

y -= 10
y = titre_section(c, 40, y, "LANGUES")
y = bullet_item(c, 55, y, "Arabe : Langue maternelle")
y = bullet_item(c, 55, y, "Français : Courant (C1)")
y = bullet_item(c, 55, y, "Anglais : Avancé (B2)")

c.save()
print("CV 2 cree : BENALI Sara (SI - bon profil)")

# ═══════════════════════════════════════════════════════
# CV 3 — Profil Archiviste (profil moyen)
# ═══════════════════════════════════════════════════════
c = canvas.Canvas(os.path.join(OUT, "CV_IDRISSI_Karim_Archiviste.pdf"), pagesize=A4)

entete(c, "IDRISSI Karim", "Candidat - Aide Archiviste",
       "karim.idrissi@gmail.com", "0654321987", "Fès, Maroc")

y = H - 145
y = titre_section(c, 40, y, "FORMATION")
y = sous_titre(c, 40, y, "Technicien Spécialisé en Développement Informatique", "2015 - 2017", "ISTA Fès")
y = sous_titre(c, 40, y, "Baccalauréat Sciences Physiques", "2015", "Lycée Ibn Khaldoun - Fès")

y -= 10
y = titre_section(c, 40, y, "EXPERIENCE PROFESSIONNELLE")
y = sous_titre(c, 40, y, "Agent Administratif", "2018 - 2024 (6 ans)", "Wilaya de Fès-Meknès")
y = bullet_item(c, 55, y, "Classement et archivage des documents administratifs")
y = bullet_item(c, 55, y, "Numérisation et gestion électronique des documents")
y = bullet_item(c, 55, y, "Saisie et mise à jour des bases de données")
y = bullet_item(c, 55, y, "Accueil et orientation du public")

y -= 10
y = titre_section(c, 40, y, "COMPETENCES")
y = bullet_item(c, 55, y, "Gestion documentaire et archivage physique/numérique")
y = bullet_item(c, 55, y, "Maîtrise de Word, Excel, Outlook")
y = bullet_item(c, 55, y, "Rigueur et sens de l'organisation")

y -= 10
y = titre_section(c, 40, y, "LANGUES")
y = bullet_item(c, 55, y, "Arabe : Langue maternelle")
y = bullet_item(c, 55, y, "Français : Intermédiaire (B1)")

c.save()
print("CV 3 cree : IDRISSI Karim (Archiviste)")
print(f"\nTous les CV sont dans : {OUT}")
