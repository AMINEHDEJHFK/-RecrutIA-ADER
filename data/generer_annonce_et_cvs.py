"""
Génération d'une annonce ADER Fès + 8 CVs de test variés
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os

OUT_CV  = os.path.join(os.path.dirname(__file__), "..", "static", "cv_tests")
OUT_ANN = os.path.join(os.path.dirname(__file__), "..", "static", "annonces")
os.makedirs(OUT_CV,  exist_ok=True)
os.makedirs(OUT_ANN, exist_ok=True)

W, H = A4
BLEU = (0.10, 0.23, 0.36)
OR   = (0.78, 0.66, 0.29)

# ═══════════════════════════════════════════════════════════════
# HELPERS COMMUNS
# ═══════════════════════════════════════════════════════════════

def draw_text(c, x, y, text, font="Helvetica", size=10, color=(0.1,0.1,0.1)):
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, text)
    return y - size - 4

def draw_wrapped(c, x, y, text, font="Helvetica", size=10, max_width=500):
    c.setFont(font, size)
    c.setFillColorRGB(0.15, 0.15, 0.15)
    words = text.split()
    line = ""
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, font, size) < max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= size + 4
            line = word
    if line:
        c.drawString(x, y, line)
        y -= size + 4
    return y

def section_title(c, x, y, title):
    c.setFillColorRGB(*BLEU)
    c.rect(x, y - 2, W - 2*x, 18, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x + 5, y + 2, title)
    return y - 24

def bullet(c, x, y, text, size=10):
    c.setFillColorRGB(0.78, 0.66, 0.29)
    c.setFont("Helvetica-Bold", size)
    c.drawString(x, y, "o")
    c.setFillColorRGB(0.15, 0.15, 0.15)
    c.setFont("Helvetica", size)
    c.drawString(x + 14, y, text)
    return y - size - 5

# ═══════════════════════════════════════════════════════════════
# ANNONCE : Chargé de Communication et Marketing Digital
# ═══════════════════════════════════════════════════════════════

path_ann = os.path.join(OUT_ANN, "Annonce_ADER_Communication_Marketing.pdf")
c = canvas.Canvas(path_ann, pagesize=A4)

# En-tête logo ADER
c.setFillColorRGB(*BLEU)
c.rect(0, H - 90, W, 90, fill=1, stroke=0)
c.setFillColorRGB(*OR)
c.setFont("Helvetica-Bold", 20)
c.drawString(40, H - 45, "ADER - FES")
c.setFillColorRGB(1, 1, 1)
c.setFont("Helvetica", 11)
c.drawString(40, H - 65, "Agence de Developpement Regional de Fes")
c.setFont("Helvetica-Oblique", 9)
c.drawString(40, H - 80, "Immeuble 21, Rue Mohammed Diouri, 30000 (VN) - Fes")

# Titre poste
c.setFillColorRGB(*BLEU)
c.setFont("Helvetica-Bold", 13)
c.drawString(40, H - 115, "Poste pourvu : (02) Charge de Communication et Marketing Digital")
c.setFont("Helvetica", 10)
c.setFillColorRGB(0.3, 0.3, 0.3)
c.drawString(40, H - 132, "Au sein de l'ADER - Fes  |  Sis a : Immeuble 21, Rue Mohammed Diouri, 30000 (VN) - Fes")

y = H - 160

# Missions
y = section_title(c, 40, y, "Missions :")
missions = [
    "Elaborer et mettre en oeuvre la strategie de communication de l'ADER-FES ;",
    "Gerer les reseaux sociaux et le site web institutionnel de l'agence ;",
    "Produire des contenus digitaux (articles, videos, infographies) ;",
    "Assurer la couverture mediatique des evenements organises par l'agence ;",
    "Concevoir les supports de communication (plaquettes, affiches, newsletters) ;",
    "Suivre et analyser les indicateurs de performance des campagnes digitales.",
]
for m in missions:
    y = bullet(c, 45, y, m)

y -= 5
y = section_title(c, 40, y, "Principales Attributions :")
attributions = [
    "Rediger et diffuser les communiques de presse et actualites de l'agence ;",
    "Coordonner avec les partenaires medias et institutionnels ;",
    "Organiser les conferences de presse et evenements de l'agence ;",
    "Assurer la veille concurrentielle et mediatique ;",
    "Gerer le budget communication en coordination avec la direction financiere.",
]
for a in attributions:
    y = bullet(c, 45, y, a)

y -= 5
y = section_title(c, 40, y, "Conditions d'acces au Poste :")
c.setFillColorRGB(0.15, 0.15, 0.15)
c.setFont("Helvetica-Bold", 10)
c.drawString(45, y, "- Diplome :")
c.setFont("Helvetica", 10)
c.drawString(110, y, "Master en Communication, Marketing, Journalisme ou equivalent.")
y -= 16
c.setFont("Helvetica-Bold", 10)
c.drawString(45, y, "- Experience :")
c.setFont("Helvetica", 10)
c.drawString(120, y, "Minimum 2 ans d'experience dans un poste similaire.")
y -= 16
c.setFont("Helvetica-Bold", 10)
c.drawString(45, y, "- Langues :")
c.setFont("Helvetica", 10)
c.drawString(110, y, "Maitrise du francais et de l'arabe. Anglais souhaitable.")
y -= 20

y = section_title(c, 40, y, "Competences requises :")
competences = [
    "Maitrise des outils de creation graphique (Photoshop, Canva, Premiere) ;",
    "Bonne maitrise des reseaux sociaux et du SEO/SEA ;",
    "Excellentes capacites redactionnelles en arabe et en francais ;",
    "Sens de la creativite et de l'innovation ;",
    "Capacite a travailler sous pression et a respecter les delais.",
]
for comp in competences:
    y = bullet(c, 45, y, comp)

y -= 5
y = section_title(c, 40, y, "Dossier de candidature :")
dossier = [
    "Curriculum vitae actualise (CV) ;",
    "Lettre de motivation ;",
    "Copie de la carte nationale d'identite (CINE) ;",
    "Copies legalisees des diplomes ;",
    "Attestations justifiant les experiences professionnelles.",
]
for d in dossier:
    y = bullet(c, 45, y, d)

y -= 10
c.setFillColorRGB(*BLEU)
c.setFont("Helvetica-Bold", 10)
c.drawString(40, y, "Le dernier delai de candidature est fixe au : 28 Fevrier 2025")

# Pied de page
c.setFillColorRGB(*BLEU)
c.rect(0, 0, W, 35, fill=1, stroke=0)
c.setFillColorRGB(1, 1, 1)
c.setFont("Helvetica", 8)
c.drawCentredString(W/2, 15, "ADER Fes - Immeuble 21, Rue Mohammed Diouri, 30000 Fes | www.ader-fes.ma")

c.save()
print("Annonce creee :", path_ann)

# ═══════════════════════════════════════════════════════════════
# HELPERS CVs
# ═══════════════════════════════════════════════════════════════

def cv_entete(c, nom, titre, email, tel, ville):
    c.setFillColorRGB(*BLEU)
    c.rect(0, H - 110, W, 110, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, H - 50, nom)
    c.setFillColorRGB(*OR)
    c.setFont("Helvetica", 12)
    c.drawString(40, H - 70, titre)
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.setFont("Helvetica", 9)
    c.drawString(40, H - 88, f"{ville}  |  {tel}  |  {email}")

def cv_section(c, x, y, titre):
    c.setFillColorRGB(*BLEU)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x, y, titre)
    c.setStrokeColorRGB(*OR)
    c.setLineWidth(1.5)
    c.line(x, y - 3, W - x, y - 3)
    return y - 20

def cv_exp(c, x, y, poste, lieu, dates):
    c.setFillColorRGB(*BLEU)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, poste)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(x, y - 13, f"{lieu}  |  {dates}")
    return y - 28

def cv_item(c, x, y, text):
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica", 9)
    c.drawString(x, y, f"- {text}")
    return y - 14

# ═══════════════════════════════════════════════════════════════
# 8 CVs variés
# ═══════════════════════════════════════════════════════════════

cvs = [
    # (fichier, nom, prenom, email, tel, ville, titre_cv, diplome, ecole, promo_debut, promo_fin, exps, langues)
    {
        "fichier": "CV_CHERKAOUI_Fatima_Communication.pdf",
        "nom": "CHERKAOUI Fatima", "prenom": "Fatima",
        "email": "fatima.cherkaoui@gmail.com", "tel": "0661112233", "ville": "Fes, Maroc",
        "titre": "Candidate - Chargee de Communication",
        "formation": [
            ("Master Communication et Medias Numeriques", "2019 - 2021", "FSJES Fes"),
            ("Licence Sciences de la Communication", "2016 - 2019", "USMBA Fes"),
        ],
        "exps": [
            ("Chargee de Communication", "2021 - 2024 (3 ans)", "Mairie de Fes",
             ["Gestion des reseaux sociaux de la ville", "Redaction de communiques de presse", "Organisation d'evenements institutionnels"]),
        ],
        "competences": ["Photoshop, Canva, Premiere Pro", "Facebook, Instagram, LinkedIn, Twitter", "Redaction web et SEO"],
        "langues": ["Arabe : Langue maternelle", "Francais : Courant (C1)", "Anglais : Intermediaire (B1)"],
    },
    {
        "fichier": "CV_MANSOURI_Yassine_Marketing.pdf",
        "nom": "MANSOURI Yassine", "prenom": "Yassine",
        "email": "yassine.mansouri@gmail.com", "tel": "0677223344", "ville": "Fes, Maroc",
        "titre": "Candidat - Marketing Digital",
        "formation": [
            ("Master Marketing et Commerce International", "2020 - 2022", "ENCG Fes"),
            ("Licence Gestion des Entreprises", "2017 - 2020", "FSJES Fes"),
        ],
        "exps": [
            ("Responsable Marketing Digital", "2022 - 2024 (2 ans)", "StartupMaroc, Fes",
             ["Gestion des campagnes Google Ads et Facebook Ads", "Analyse des KPIs et reporting mensuel", "Creation de contenu pour les reseaux sociaux"]),
            ("Stagiaire Marketing", "2022 (6 mois)", "OCP Khouribga",
             ["Etude de marche et analyse concurrentielle"]),
        ],
        "competences": ["Google Analytics, SEO/SEA", "Canva, Adobe Illustrator", "Email marketing, CRM HubSpot"],
        "langues": ["Arabe : Langue maternelle", "Francais : Courant (C1)", "Anglais : Avance (B2)"],
    },
    {
        "fichier": "CV_BENSOUDA_Meryem_Journalisme.pdf",
        "nom": "BENSOUDA Meryem", "prenom": "Meryem",
        "email": "meryem.bensouda@gmail.com", "tel": "0654334455", "ville": "Meknes, Maroc",
        "titre": "Candidate - Journaliste et Communicante",
        "formation": [
            ("Master Journalisme et Communication", "2018 - 2020", "FSJES Fes"),
            ("Licence Lettres et Sciences Humaines", "2015 - 2018", "USMBA Fes"),
        ],
        "exps": [
            ("Journaliste Web", "2020 - 2024 (4 ans)", "Medias24 Casablanca",
             ["Redaction d'articles et reportages", "Production de contenus video pour YouTube", "Gestion du compte Twitter (@medias24)"]),
        ],
        "competences": ["WordPress, Joomla", "Final Cut Pro, Premiere", "Redaction web SEO"],
        "langues": ["Arabe : Langue maternelle", "Francais : Courant (C1)", "Anglais : Notions (A2)"],
    },
    {
        "fichier": "CV_TAZI_Omar_Informatique.pdf",
        "nom": "TAZI Omar", "prenom": "Omar",
        "email": "omar.tazi@gmail.com", "tel": "0612445566", "ville": "Fes, Maroc",
        "titre": "Candidat - Developpeur Web",
        "formation": [
            ("Master Informatique et Systemes d'Information", "2019 - 2021", "ENSA Fes"),
            ("Licence Genie Informatique", "2016 - 2019", "ENSA Fes"),
        ],
        "exps": [
            ("Developpeur Full Stack", "2021 - 2024 (3 ans)", "AgriTech Maroc",
             ["Developpement Python/Django", "Administration base de donnees", "Integration API REST"]),
        ],
        "competences": ["Python, JavaScript, SQL", "Django, React, Docker", "Git, Linux"],
        "langues": ["Arabe : Langue maternelle", "Francais : Courant (C1)", "Anglais : Avance (B2)"],
    },
    {
        "fichier": "CV_FILALI_Nadia_Communication.pdf",
        "nom": "FILALI Nadia", "prenom": "Nadia",
        "email": "nadia.filali@gmail.com", "tel": "0698556677", "ville": "Fes, Maroc",
        "titre": "Candidate - Communication Institutionnelle",
        "formation": [
            ("Master Communication Institutionnelle et Relations Publiques", "2017 - 2019", "USMBA Fes"),
            ("Licence Sciences de la Communication", "2014 - 2017", "FSJES Fes"),
        ],
        "exps": [
            ("Responsable Communication", "2019 - 2024 (5 ans)", "ADER Fes",
             ["Elaboration de la strategie de communication", "Gestion du site web et des reseaux sociaux", "Organisation des evenements institutionnels"]),
        ],
        "competences": ["Adobe Creative Suite", "Gestion de projet, Trello", "Relations presse et medias"],
        "langues": ["Arabe : Langue maternelle", "Francais : Courant (C1)", "Anglais : Intermediaire (B1)"],
    },
    {
        "fichier": "CV_RHAZALI_Karim_Technicien.pdf",
        "nom": "RHAZALI Karim", "prenom": "Karim",
        "email": "karim.rhazali@gmail.com", "tel": "0623667788", "ville": "Fes, Maroc",
        "titre": "Candidat - Technicien Audiovisuel",
        "formation": [
            ("Technicien Specialise en Audiovisuel", "2016 - 2018", "ISTA Fes"),
            ("Baccalaureat Sciences Physiques", "2016", "Lycee Ibn Khaldoun - Fes"),
        ],
        "exps": [
            ("Technicien Audiovisuel", "2018 - 2024 (6 ans)", "Studio Media Fes",
             ["Production et montage video", "Photographie institutionnelle", "Diffusion en direct sur les reseaux sociaux"]),
        ],
        "competences": ["Premiere Pro, After Effects", "Photographie et eclairage", "Streaming et podcast"],
        "langues": ["Arabe : Langue maternelle", "Francais : Intermediaire (B1)"],
    },
    {
        "fichier": "CV_ALAOUI_Samira_Marketing.pdf",
        "nom": "ALAOUI Samira", "prenom": "Samira",
        "email": "samira.alaoui@gmail.com", "tel": "0645778899", "ville": "Rabat, Maroc",
        "titre": "Candidate - Chef de Projet Communication",
        "formation": [
            ("Master Marketing Strategique et Communication", "2016 - 2018", "ENCG Fes"),
            ("Licence Sciences Economiques et Gestion", "2013 - 2016", "FSJES Fes"),
        ],
        "exps": [
            ("Chef de Projet Communication", "2018 - 2022 (4 ans)", "Agence Com+ Rabat",
             ["Gestion de projets communication pour clients publics", "Elaboration des plans de communication annuels", "Coordination avec les agences de publicite"]),
            ("Chargee de Communication", "2022 - 2024 (2 ans)", "Wilaya de Rabat",
             ["Communication institutionnelle et relations presse", "Gestion des reseaux sociaux officiels"]),
        ],
        "competences": ["Management de projet (PMP)", "Canva, PowerPoint avance", "Relations publiques et lobbying"],
        "langues": ["Arabe : Langue maternelle", "Francais : Courant (C1)", "Anglais : Avance (B2)", "Espagnol : Notions"],
    },
    {
        "fichier": "CV_BERRADA_Said_Licence.pdf",
        "nom": "BERRADA Said", "prenom": "Said",
        "email": "said.berrada@gmail.com", "tel": "0611889900", "ville": "Fes, Maroc",
        "titre": "Candidat - Communication et Relations Publiques",
        "formation": [
            ("Licence Sciences de la Communication", "2017 - 2020", "FSJES Fes"),
            ("Baccalaureat Lettres", "2017", "Lycee Moulay Idriss - Fes"),
        ],
        "exps": [
            ("Agent de Communication", "2020 - 2024 (4 ans)", "Association Culturelle Fes",
             ["Gestion de la page Facebook (15k abonnes)", "Organisation d'evenements culturels", "Redaction de newsletters mensuelles"]),
        ],
        "competences": ["Canva, CapCut", "Facebook, Instagram, TikTok", "Redaction et prise de parole"],
        "langues": ["Arabe : Langue maternelle", "Francais : Courant (B2)"],
    },
]

for cv in cvs:
    path = os.path.join(OUT_CV, cv["fichier"])
    c = canvas.Canvas(path, pagesize=A4)

    cv_entete(c, cv["nom"], cv["titre"], cv["email"], cv["tel"], cv["ville"])

    y = H - 135
    y = cv_section(c, 40, y, "FORMATION")
    for (diplome, dates, ecole) in cv["formation"]:
        c.setFillColorRGB(*BLEU)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y, diplome)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(40, y - 13, f"{ecole}  |  {dates}")
        y -= 30

    y -= 5
    y = cv_section(c, 40, y, "EXPERIENCE PROFESSIONNELLE")
    for exp in cv["exps"]:
        y = cv_exp(c, 40, y, exp[0], exp[1], exp[2])
        for item in exp[3]:
            y = cv_item(c, 55, y, item)
        y -= 5

    y -= 5
    y = cv_section(c, 40, y, "COMPETENCES")
    for comp in cv["competences"]:
        y = cv_item(c, 50, y, comp)

    y -= 5
    y = cv_section(c, 40, y, "LANGUES")
    for lang in cv["langues"]:
        y = cv_item(c, 50, y, lang)

    c.save()
    print(f"CV cree : {cv['fichier']}")

print(f"\nAnnonce dans : {OUT_ANN}")
print(f"CVs dans     : {OUT_CV}")
