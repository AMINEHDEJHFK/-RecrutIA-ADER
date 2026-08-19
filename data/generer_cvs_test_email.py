"""
Génère 3 CVs de test avec de vrais emails pour tester les notifications.
Profils CGM forts => tous présélectionnés.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

OUT = os.path.join(os.path.dirname(__file__), "cvs_test_email")
os.makedirs(OUT, exist_ok=True)

VERT  = colors.HexColor("#0D5724")
ORANGE = colors.HexColor("#E66210")
GRIS  = colors.HexColor("#3D4240")
CLAIR = colors.HexColor("#E8F2EB")

candidats = [
    {
        "nom": "TAZI", "prenom": "Mehdi",
        "email": "mohammedamine.saghiri@usmba.ac.ma",
        "telephone": "06 61 23 45 67",
        "poste": "Chargé de la Gestion des Marchés",
        "diplome": "Master",
        "specialite": "Finance et Audit",
        "ecole": "ENCG Fès",
        "promotion": "2019",
        "experience": "5 ans",
        "missions": [
            "Gestion et suivi des marchés publics conformément au CMP marocain",
            "Rédaction des cahiers des charges et des appels d'offres",
            "Analyse et évaluation des offres techniques et financières",
            "Coordination avec les services comptables et juridiques",
            "Reporting mensuel à la direction générale",
        ],
        "competences": ["Marchés publics", "Finance publique", "Excel avancé", "SAP", "Arabe / Français / Anglais"],
        "formations": [
            ("2017–2019", "Master Finance et Audit", "ENCG Fès"),
            ("2014–2017", "Licence Sciences Économiques", "FSJES Fès"),
        ],
        "experiences": [
            ("2019–2024", "Chargé des marchés", "Région Fès-Meknès", "Gestion des appels d'offres et suivi budgétaire"),
            ("2017–2019", "Assistant administratif", "Mairie de Fès", "Traitement des dossiers marchés"),
        ],
    },
    {
        "nom": "BENALI", "prenom": "Leila",
        "email": "mohammed-amine.saghiri.edu@groupe-gema.com",
        "telephone": "06 72 34 56 78",
        "poste": "Chargé de la Gestion des Marchés",
        "diplome": "Master",
        "specialite": "Audit et Contrôle de Gestion",
        "ecole": "ISCAE Casablanca",
        "promotion": "2020",
        "experience": "4 ans",
        "missions": [
            "Contrôle et audit des dépenses publiques",
            "Élaboration des rapports financiers trimestriels",
            "Gestion des procédures d'appels d'offres",
            "Veille réglementaire sur les marchés publics",
            "Formation des équipes sur les procédures CMP",
        ],
        "competences": ["Audit interne", "Contrôle de gestion", "Power BI", "Marchés publics", "Français / Anglais"],
        "formations": [
            ("2018–2020", "Master Audit et Contrôle de Gestion", "ISCAE Casablanca"),
            ("2015–2018", "Licence Économie et Gestion", "Faculté de Casablanca"),
        ],
        "experiences": [
            ("2020–2024", "Auditrice marchés publics", "Agence Urbaine Casablanca", "Audit et contrôle des marchés"),
            ("2018–2020", "Stagiaire contrôle de gestion", "OCP Groupe", "Reporting et analyse budgétaire"),
        ],
    },
    {
        "nom": "RACHIDI", "prenom": "Omar",
        "email": "aminesaghiri21@gmail.com",
        "telephone": "06 83 45 67 89",
        "poste": "Chargé de la Gestion des Marchés",
        "diplome": "Master",
        "specialite": "Comptabilité et Finance d'Entreprise",
        "ecole": "ENCG Marrakech",
        "promotion": "2018",
        "experience": "6 ans",
        "missions": [
            "Pilotage complet des procédures de passation des marchés",
            "Analyse financière des offres soumissionnaires",
            "Rédaction des avenants et des actes d'engagement",
            "Gestion du tableau de bord marchés",
            "Relations avec les fournisseurs et prestataires",
        ],
        "competences": ["Passation marchés", "Comptabilité générale", "Sage Comptabilité", "Gestion budgétaire", "Arabe / Français"],
        "formations": [
            ("2016–2018", "Master Comptabilité et Finance", "ENCG Marrakech"),
            ("2013–2016", "Licence Gestion", "FSJES Marrakech"),
        ],
        "experiences": [
            ("2018–2024", "Responsable marchés", "Commune Marrakech", "Gestion intégrale des marchés publics"),
            ("2016–2018", "Comptable", "Cabinet d'expertise", "Tenue comptable et déclarations fiscales"),
        ],
    },
]


def faire_cv(c):
    nom_fichier = os.path.join(OUT, f"CV_{c['nom']}_{c['prenom']}.pdf")
    doc = SimpleDocTemplate(nom_fichier, pagesize=A4,
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)

    styles = getSampleStyleSheet()
    s_nom   = ParagraphStyle("nom",   fontName="Helvetica-Bold", fontSize=22, textColor=VERT,   spaceAfter=2)
    s_poste = ParagraphStyle("poste", fontName="Helvetica",      fontSize=11, textColor=ORANGE, spaceAfter=6)
    s_h2    = ParagraphStyle("h2",    fontName="Helvetica-Bold", fontSize=10, textColor=VERT,   spaceBefore=10, spaceAfter=4)
    s_body  = ParagraphStyle("body",  fontName="Helvetica",      fontSize=9,  textColor=GRIS,   spaceAfter=3, leading=13)
    s_bold  = ParagraphStyle("bold",  fontName="Helvetica-Bold", fontSize=9,  textColor=GRIS,   spaceAfter=2)
    s_info  = ParagraphStyle("info",  fontName="Helvetica",      fontSize=9,  textColor=GRIS)

    story = []

    # ── EN-TÊTE ─────────────────────────────────────────────────
    entete = Table([
        [
            Paragraph(f"{c['prenom']} {c['nom']}", s_nom),
            Paragraph(f"<b>{c['email']}</b><br/>{c['telephone']}", s_info),
        ]
    ], colWidths=[10*cm, 7*cm])
    entete.setStyle(TableStyle([
        ("VALIGN",  (0,0), (-1,-1), "TOP"),
        ("ALIGN",   (1,0), (1,0),   "RIGHT"),
        ("BACKGROUND", (0,0), (-1,-1), CLAIR),
        ("ROWPADDING", (0,0), (-1,-1), 8),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(entete)
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(c["poste"], s_poste))
    story.append(HRFlowable(width="100%", thickness=2, color=VERT, spaceAfter=8))

    # ── INFOS CLÉS ───────────────────────────────────────────────
    story.append(Paragraph("INFORMATIONS CLÉS", s_h2))
    infos_table = Table([
        ["Diplôme :",    c["diplome"],    "Expérience :", c["experience"]],
        ["Spécialité :", c["specialite"], "École :",      c["ecole"]],
        ["Promotion :",  c["promotion"],  "Email :",      c["email"]],
    ], colWidths=[2.5*cm, 6*cm, 2.5*cm, 6*cm])
    infos_table.setStyle(TableStyle([
        ("FONTNAME",  (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME",  (0,0), (0,-1),  "Helvetica-Bold"),
        ("FONTNAME",  (2,0), (2,-1),  "Helvetica-Bold"),
        ("FONTSIZE",  (0,0), (-1,-1), 9),
        ("TEXTCOLOR", (0,0), (0,-1),  VERT),
        ("TEXTCOLOR", (2,0), (2,-1),  VERT),
        ("ROWPADDING",(0,0), (-1,-1), 4),
        ("GRID",      (0,0), (-1,-1), 0.3, colors.HexColor("#E8EDEA")),
    ]))
    story.append(infos_table)

    # ── EXPÉRIENCES ──────────────────────────────────────────────
    story.append(Paragraph("EXPÉRIENCES PROFESSIONNELLES", s_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=VERT, spaceAfter=6))
    for (periode, titre, lieu, desc) in c["experiences"]:
        exp_tbl = Table([[
            Paragraph(periode, ParagraphStyle("p", fontName="Helvetica", fontSize=8, textColor=ORANGE)),
            [Paragraph(f"<b>{titre}</b> — {lieu}", s_bold),
             Paragraph(desc, s_body)],
        ]], colWidths=[2.5*cm, 14.5*cm])
        exp_tbl.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (1,0), (1,0), 8),
        ]))
        story.append(exp_tbl)
        story.append(Spacer(1, 0.2*cm))

    # ── MISSIONS ─────────────────────────────────────────────────
    story.append(Paragraph("MISSIONS CLÉS", s_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=VERT, spaceAfter=6))
    for m in c["missions"]:
        story.append(Paragraph(f"• {m}", s_body))

    # ── FORMATION ────────────────────────────────────────────────
    story.append(Paragraph("FORMATION", s_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=VERT, spaceAfter=6))
    for (periode, diplome, ecole) in c["formations"]:
        story.append(Paragraph(f"<b>{periode}</b> — {diplome} | <i>{ecole}</i>", s_body))

    # ── COMPÉTENCES ──────────────────────────────────────────────
    story.append(Paragraph("COMPÉTENCES", s_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=VERT, spaceAfter=6))
    comp_data = [[Paragraph(f"✓ {comp}", s_body) for comp in c["competences"]]]
    comp_tbl = Table(comp_data, colWidths=[3.4*cm]*5)
    comp_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), CLAIR),
        ("ROWPADDING", (0,0), (-1,-1), 5),
        ("GRID",       (0,0), (-1,-1), 0.3, colors.white),
    ]))
    story.append(comp_tbl)

    doc.build(story)
    print(f"OK CV genere : {nom_fichier}")


for c in candidats:
    faire_cv(c)

print("\n3 CVs generes dans :", OUT)
