"""
Génération de la vraie annonce ADER Fès avec logo et design officiel
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

W, H = A4
BLEU = (0.10, 0.23, 0.36)
OR   = (0.78, 0.66, 0.29)
GRIS = (0.95, 0.95, 0.95)

BASE = os.path.join(os.path.dirname(__file__), "..")
LOGO = os.path.join(BASE, "static", "annonces", "logo_ader_0.png")
OUT  = os.path.join(BASE, "static", "annonces", "Annonce_ADER_Communication_Marketing_Officielle.pdf")

c = canvas.Canvas(OUT, pagesize=A4)

# ── En-tête avec logo ────────────────────────────────────────────
# Fond blanc en-tête
c.setFillColorRGB(1, 1, 1)
c.rect(0, H - 100, W, 100, fill=1, stroke=0)

# Ligne dorée en bas de l'en-tête
c.setFillColorRGB(*OR)
c.rect(0, H - 103, W, 3, fill=1, stroke=0)

# Logo ADER
if os.path.exists(LOGO):
    try:
        logo = ImageReader(LOGO)
        c.drawImage(logo, 30, H - 90, width=180, height=70, preserveAspectRatio=True, mask='auto')
    except:
        pass

# Infos agence à droite
c.setFillColorRGB(*BLEU)
c.setFont("Helvetica-Bold", 9)
c.drawRightString(W - 30, H - 35, "Agence de Developpement Regional de Fes")
c.setFont("Helvetica", 8)
c.setFillColorRGB(0.4, 0.4, 0.4)
c.drawRightString(W - 30, H - 48, "Immeuble 21, Rue Mohammed Diouri")
c.drawRightString(W - 30, H - 59, "30000 (VN) - Fes")
c.drawRightString(W - 30, H - 70, "www.ader-fes.ma")

# ── Bandeau titre poste ──────────────────────────────────────────
c.setFillColorRGB(*BLEU)
c.rect(0, H - 140, W, 34, fill=1, stroke=0)
c.setFillColorRGB(1, 1, 1)
c.setFont("Helvetica-Bold", 12)
c.drawCentredString(W/2, H - 122, "Poste pourvu : (02) Charge de Communication et Marketing Digital")

c.setFillColorRGB(*GRIS)
c.rect(0, H - 160, W, 20, fill=1, stroke=0)
c.setFillColorRGB(*BLEU)
c.setFont("Helvetica-Oblique", 9)
c.drawCentredString(W/2, H - 153, "Au sein de l'ADER - Fes  |  Sis a : Immeuble 21, Rue Mohammed Diouri, 30000 (VN) - Fes")

# ── Contenu ──────────────────────────────────────────────────────
y = H - 185

def section(c, y, titre):
    c.setFillColorRGB(*BLEU)
    c.rect(30, y - 3, W - 60, 17, fill=1, stroke=0)
    # Ligne dorée gauche
    c.setFillColorRGB(*OR)
    c.rect(30, y - 3, 5, 17, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(42, y + 1, titre)
    return y - 22

def bullet_item(c, x, y, text, size=9.5):
    c.setFillColorRGB(*OR)
    c.circle(x + 4, y + 3, 2, fill=1, stroke=0)
    c.setFillColorRGB(0.15, 0.15, 0.15)
    c.setFont("Helvetica", size)
    # Wrap text
    max_w = W - x - 50
    words = text.split()
    line = ""
    first = True
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, "Helvetica", size) < max_w:
            line = test
        else:
            draw_x = x + 12 if first else x + 12
            c.drawString(draw_x, y, line)
            y -= size + 3
            line = word
            first = False
    if line:
        c.drawString(x + 12, y, line)
        y -= size + 3
    return y - 2

def label_value(c, y, label, value, size=9.5):
    c.setFillColorRGB(*BLEU)
    c.setFont("Helvetica-Bold", size)
    c.drawString(42, y, label)
    lw = c.stringWidth(label, "Helvetica-Bold", size)
    c.setFillColorRGB(0.15, 0.15, 0.15)
    c.setFont("Helvetica", size)
    c.drawString(42 + lw + 5, y, value)
    return y - size - 6

# MISSIONS
y = section(c, y, "Missions :")
missions = [
    "Elaborer et mettre en oeuvre la strategie de communication de l'ADER-FES ;",
    "Gerer les reseaux sociaux et le site web institutionnel de l'agence ;",
    "Produire des contenus digitaux (articles, videos, infographies) ;",
    "Assurer la couverture mediatique des evenements organises par l'agence ;",
    "Concevoir les supports de communication (plaquettes, affiches, newsletters) ;",
    "Suivre et analyser les indicateurs de performance des campagnes digitales.",
]
for m in missions:
    y = bullet_item(c, 38, y, m)

y -= 6
y = section(c, y, "Principales Attributions :")
attributions = [
    "Rediger et diffuser les communiques de presse et actualites de l'agence ;",
    "Coordonner avec les partenaires medias et institutionnels ;",
    "Organiser les conferences de presse et evenements de l'agence ;",
    "Assurer la veille concurrentielle et mediatique ;",
    "Gerer le budget communication en coordination avec la direction financiere.",
]
for a in attributions:
    y = bullet_item(c, 38, y, a)

y -= 6
y = section(c, y, "Conditions d'acces au Poste :")
y = label_value(c, y, "Diplome :", "Master en Communication, Marketing, Journalisme ou equivalent.")
y = label_value(c, y, "Experience :", "Minimum 2 ans d'experience dans un poste similaire.")
y = label_value(c, y, "Langues :", "Maitrise du francais et de l'arabe. Anglais souhaitable.")
y = label_value(c, y, "Mobilite geographique :", "Requise.")

y -= 6
y = section(c, y, "Competences requises :")
competences = [
    "Maitrise des outils de creation graphique (Photoshop, Canva, Premiere) ;",
    "Bonne maitrise des reseaux sociaux et du SEO/SEA ;",
    "Excellentes capacites redactionnelles en arabe et en francais ;",
    "Sens de la creativite et de l'innovation ;",
    "Capacite a travailler sous pression et respecter les delais.",
]
for comp in competences:
    y = bullet_item(c, 38, y, comp)

y -= 6
y = section(c, y, "Dossier de candidature :")
dossier = [
    "Curriculum vitae actualise (CV) ;",
    "Lettre de motivation ;",
    "Copie legalisee de carte nationale d'identite (CINE) ;",
    "Copies legalisees des diplomes ;",
    "Attestations justifiant les experiences professionnelles exigees.",
]
for d in dossier:
    y = bullet_item(c, 38, y, d)

# Date limite
y -= 8
c.setFillColorRGB(*GRIS)
c.rect(30, y - 8, W - 60, 22, fill=1, stroke=0)
c.setFillColorRGB(*OR)
c.rect(30, y - 8, 5, 22, fill=1, stroke=0)
c.setFillColorRGB(*BLEU)
c.setFont("Helvetica-Bold", 10)
c.drawString(42, y + 1, "Le dernier delai de candidature est fixe au :  28 Fevrier 2025")

# ── Pied de page ─────────────────────────────────────────────────
c.setFillColorRGB(*BLEU)
c.rect(0, 0, W, 40, fill=1, stroke=0)
c.setFillColorRGB(*OR)
c.rect(0, 38, W, 2, fill=1, stroke=0)
c.setFillColorRGB(1, 1, 1)
c.setFont("Helvetica-Bold", 8)
c.drawCentredString(W/2, 22, "ADER Fes - Agence de Developpement Regional")
c.setFont("Helvetica", 7)
c.setFillColorRGB(0.8, 0.8, 0.8)
c.drawCentredString(W/2, 10, "Immeuble 21, Rue Mohammed Diouri, 30000 (VN) - Fes  |  www.ader-fes.ma")

c.save()
print("Annonce officielle creee :", OUT)
