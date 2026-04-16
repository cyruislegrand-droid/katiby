import streamlit as st
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm
import io
import datetime
import os

# --------------------------------------------------
# Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Katiby — Vos Documents Juridiques",
    page_icon="📄",
    layout="centered"
)

# CSS Fintech
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f0f4f8;
}

section[data-testid="stSidebar"] {
    display: none;
}

.header-katiby {
    background: linear-gradient(135deg, #0a1628 0%, #0f2347 100%);
    border-radius: 16px;
    padding: 36px 32px;
    margin-bottom: 24px;
    text-align: center;
}

.header-badge {
    display: inline-block;
    background: rgba(37,99,235,0.2);
    border: 1px solid rgba(37,99,235,0.4);
    border-radius: 20px;
    padding: 4px 14px;
    color: #93c5fd;
    font-size: 12px;
    margin-bottom: 16px;
}

.header-title {
    font-size: 32px;
    font-weight: 500;
    color: white;
    margin-bottom: 8px;
    line-height: 1.2;
}

.header-title span {
    color: #60a5fa;
}

.header-subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-bottom: 20px;
}

.header-stats {
    display: flex;
    justify-content: center;
    gap: 40px;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding-top: 20px;
    margin-top: 20px;
}

.stat-item {
    text-align: center;
}

.stat-number {
    color: white;
    font-size: 20px;
    font-weight: 500;
}

.stat-label {
    color: #64748b;
    font-size: 11px;
    margin-top: 2px;
}

.stSelectbox label, .stTextInput label, .stTextArea label, .stCheckbox label {
    color: #1e293b !important;
  .stApp, .main, .block-container {
    background: #f0f4f8 !important;
    color: #1e293b !important;
}

p, label, span, div {
    color: #1e293b !important;
}  
    font-weight: 500 !important;
    font-size: 14px !important;
}

.stSelectbox > div > div {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
}

.stTextInput > div > div > input {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
}

.stTextArea > div > div > textarea {
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
}

.stForm {
    background: white;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #e2e8f0;
}

div[data-testid="stFormSubmitButton"] > button {
    background: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 32px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    width: 100% !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background: #1d4ed8 !important;
}

.stDownloadButton > button {
    background: #0f172a !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stSuccess {
    background: #f0fdf4 !important;
    border: 1px solid #bbf7d0 !important;
    border-radius: 8px !important;
    color: #166534 !important;
}

.stWarning {
    background: #fffbeb !important;
    border: 1px solid #fde68a !important;
    border-radius: 8px !important;
}

.stInfo {
    background: #eff6ff !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 8px !important;
    color: #1e40af !important;
}

h1, h2, h3 {
    color: #0f172a !important;
}

.footer-katiby {
    text-align: center;
    padding: 20px;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 32px;
}
.stApp {
    background: #f0f4f8 !important;
}
.stApp p, .stApp label, .stApp div:not(.header-katiby):not(.header-title):not(.header-subtitle):not(.header-badge):not(.header-stats):not(.stat-item):not(.stat-number):not(.stat-label), .stApp span:not(.header-title span) {
    color: #1e293b !important;
}
}
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
<div class="header-katiby">
    <div class="header-badge">✦ Conforme à la législation marocaine</div>
    <div class="header-title">Kati<span>by</span> — Vos Documents Juridiques</div>
    <div class="header-subtitle">67 modèles pour PME, auto-entrepreneurs, associations et coopératives</div>
    <div class="header-stats">
        <div class="stat-item">
            <div class="stat-number">67</div>
            <div class="stat-label">Modèles</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">11</div>
            <div class="stat-label">Catégories</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">399 DH</div>
            <div class="stat-label">Abonnement annuel</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">2 min</div>
            <div class="stat-label">Par document</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

CLE_GROQ = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=CLE_GROQ)

# --------------------------------------------------
# Catalogue des documents
# --------------------------------------------------
CATALOGUE = {
    "⚖ Commercial & Contrats": [
        "Mise en demeure",
        "Contrat de prestation de service",
        "Contrat de vente",
        "Bon de commande",
        "Facture proforma",
        "Lettre de relance amiable niveau 1",
        "Lettre de relance amiable niveau 2",
        "Lettre de relance amiable niveau 3",
        "Accord de confidentialité NDA",
        "Promesse de vente",
        "Contrat d'agent commercial",
        "Lettre de résiliation de contrat",
    ],
    "💰 Recouvrement": [
        "Reconnaissance de dette",
        "Échéancier de remboursement",
        "Quittance de paiement",
        "Mainlevée de dette",
    ],
    "👥 Ressources Humaines": [
        "Contrat CDD",
        "Contrat CDI",
        "Lettre d'embauche",
        "Renouvellement période d'essai",
        "Lettre d'avertissement",
        "Lettre de mise à pied",
        "Lettre de licenciement pour faute",
        "Licenciement économique",
        "Démission",
        "Attestation de travail",
        "Certificat de travail",
        "Reçu pour solde de tout compte",
    ],
    "🧾 Auto-Entrepreneur": [
        "Contrat de mission freelance",
        "Facture auto-entrepreneur",
        "Lettre de démarrage d'activité",
        "Résiliation de mission",
    ],
    "🏢 Bail Commercial": [
        "Contrat de bail commercial",
        "Résiliation de bail",
        "Demande de renouvellement de bail",
        "Mise en demeure propriétaire",
    ],
    "🏛 Administratif": [
        "Réclamation DGI",
        "Demande de délai de paiement CNSS",
        "Opposition à contrainte",
        "Lettre de contestation d'amende",
        "Demande d'autorisation d'exploitation",
        "Pouvoir simple",
    ],
    "🏗 Sociétés SARL": [
        "PV d'assemblée générale",
        "Décision de gérance",
        "Cession de parts sociales",
        "Convocation AGO",
        "Convocation AGE",
    ],
    "🔒 Protection des Données": [
        "Politique de confidentialité",
        "Consentement traitement données",
        "Clause protection données contrat",
    ],
    "🤝 Coopératives": [
        "Statuts de coopérative",
        "PV assemblée générale coopérative",
        "Règlement intérieur coopérative",
        "Demande d'adhésion coopérative",
        "Lettre de retrait d'un membre",
        "Convocation conseil d'administration",
        "Rapport moral annuel",
        "Contrat de fourniture coopérative",
    ],
    "🌱 Associations": [
        "Statuts d'association",
        "PV de création association",
        "Règlement intérieur association",
        "Convocation assemblée générale",
        "Rapport d'activité annuel",
        "Demande de subvention",
        "Lettre de partenariat",
        "Reçu de don",
        "Déclaration de modification des statuts",
    ],
    "🔗 GIE": [
        "Contrat constitutif du GIE",
        "PV de réunion du GIE",
        "Convention de gestion entre membres",
        "Lettre d'adhésion au GIE",
        "Résolution de dissolution du GIE",
    ],
}

# --------------------------------------------------
# Champs par type de document
# --------------------------------------------------
def get_champs(document):
    champs_communs = {
        "expediteur_nom": "Votre nom / Raison sociale *",
        "expediteur_adresse": "Votre adresse *",
        "expediteur_ville": "Votre ville *",
        "expediteur_tel": "Votre téléphone",
    }
    champs_destinataire = {
        "destinataire_nom": "Nom du destinataire *",
        "destinataire_adresse": "Adresse du destinataire",
        "destinataire_ville": "Ville du destinataire",
    }
    champs_montant = {"montant": "Montant (DH)"}
    champs_delai = {"delai": "Délai accordé"}
    champs_description = {"description": "Détails / Contexte *"}
    champs_date = {"date_contrat": "Date du contrat"}
    champs_objet = {"objet": "Objet / Titre du document"}

    if document in ["Mise en demeure", "Lettre de relance amiable niveau 1",
                    "Lettre de relance amiable niveau 2", "Lettre de relance amiable niveau 3",
                    "Reconnaissance de dette", "Mainlevée de dette"]:
        return {**champs_communs, **champs_destinataire,
                **champs_montant, **champs_delai, **champs_description}
    elif document in ["Contrat CDD", "Contrat CDI", "Lettre d'embauche",
                      "Contrat de mission freelance"]:
        return {**champs_communs,
                "salarie_nom": "Nom du salarié / Prestataire *",
                "poste": "Poste / Mission *",
                "salaire": "Salaire / Rémunération (DH) *",
                "date_debut": "Date de début *",
                "duree": "Durée (pour CDD)",
                **champs_description}
    elif document in ["Lettre d'avertissement", "Lettre de mise à pied",
                      "Lettre de licenciement pour faute", "Licenciement économique",
                      "Attestation de travail", "Certificat de travail",
                      "Reçu pour solde de tout compte", "Démission"]:
        return {**champs_communs,
                "salarie_nom": "Nom du salarié *",
                "poste": "Poste occupé *",
                "date_embauche": "Date d'embauche",
                **champs_description}
    elif document in ["Contrat de prestation de service", "Contrat de vente",
                      "Bon de commande", "Accord de confidentialité NDA",
                      "Promesse de vente", "Contrat d'agent commercial"]:
        return {**champs_communs, **champs_destinataire,
                **champs_objet, **champs_montant,
                **champs_date, **champs_description}
    elif document in ["Contrat de bail commercial", "Résiliation de bail",
                      "Demande de renouvellement de bail", "Mise en demeure propriétaire"]:
        return {**champs_communs, **champs_destinataire,
                "adresse_local": "Adresse du local commercial *",
                "loyer": "Montant du loyer (DH)",
                **champs_description}
    elif document in ["PV d'assemblée générale", "PV assemblée générale coopérative",
                      "PV de création association", "PV de réunion du GIE",
                      "Convocation AGO", "Convocation AGE"]:
        return {**champs_communs,
                "date_reunion": "Date de la réunion *",
                "lieu_reunion": "Lieu de la réunion *",
                "ordre_du_jour": "Ordre du jour *",
                **champs_description}
    elif document in ["Statuts de coopérative", "Statuts d'association",
                      "Contrat constitutif du GIE"]:
        return {**champs_communs,
                "objet_social": "Objet social / But *",
                "siege_social": "Siège social *",
                "capital": "Capital / Dotation initiale (DH)",
                "fondateurs": "Noms des fondateurs *",
                **champs_description}
    elif document in ["Demande de subvention", "Réclamation DGI",
                      "Demande de délai de paiement CNSS",
                      "Opposition à contrainte",
                      "Lettre de contestation d'amende",
                      "Demande d'autorisation d'exploitation"]:
        return {**champs_communs,
                "administration": "Administration concernée *",
                "reference": "Référence / Numéro de dossier",
                **champs_montant, **champs_description}
    else:
        return {**champs_communs, **champs_destinataire,
                **champs_objet, **champs_description}


# --------------------------------------------------
# Sélection document
# --------------------------------------------------
col_cat, col_doc = st.columns(2)
with col_cat:
    categorie = st.selectbox("Catégorie", list(CATALOGUE.keys()))
with col_doc:
    document = st.selectbox("Document", CATALOGUE[categorie])

st.info(f"📄 **{document}** — Formulaire adapté ci-dessous")
st.divider()

# --------------------------------------------------
# Formulaire dynamique
# --------------------------------------------------
champs = get_champs(document)

with st.form("katiby_form"):
    st.subheader(f"{document}")

    valeurs = {}
    champs_liste = list(champs.items())
    i = 0
    while i < len(champs_liste):
        if i + 1 < len(champs_liste):
            col1, col2 = st.columns(2)
            with col1:
                k1, label1 = champs_liste[i]
                if k1 in ["description", "ordre_du_jour", "objet_social", "fondateurs"]:
                    valeurs[k1] = st.text_area(label1, height=120)
                else:
                    valeurs[k1] = st.text_input(label1)
            with col2:
                k2, label2 = champs_liste[i+1]
                if k2 in ["description", "ordre_du_jour", "objet_social", "fondateurs"]:
                    valeurs[k2] = st.text_area(label2, height=120)
                else:
                    valeurs[k2] = st.text_input(label2)
            i += 2
        else:
            k, label = champs_liste[i]
            if k in ["description", "ordre_du_jour", "objet_social", "fondateurs"]:
                valeurs[k] = st.text_area(label, height=150)
            else:
                valeurs[k] = st.text_input(label)
            i += 1

    st.divider()
    st.warning(
        "**Abonnement annuel : 399 DH | Document à l'unité : 29 DH**\n\n"
        "Virement bancaire : CIH Bank — RIB : XX XXX XXXX XXXXXXXXXXXX XX\n"
        "Intitulé : KATIBY + votre nom"
    )
    paiement = st.checkbox("Je confirme avoir effectué le paiement")
    generer = st.form_submit_button("Générer le document →", type="primary")

# --------------------------------------------------
# Génération
# --------------------------------------------------
if generer:
    if not paiement:
        st.error("Veuillez confirmer le paiement.")
    elif not valeurs.get("expediteur_nom"):
        st.error("Veuillez remplir tous les champs obligatoires (*).")
    else:
        with st.spinner("Génération de votre document en cours..."):

            date_today = datetime.date.today().strftime("%d/%m/%Y")
            infos = "\n".join([f"{k}: {v}" for k, v in valeurs.items() if v])
            infos += f"\nDate: {date_today}"

            prompt = (
                "Tu es un juriste marocain expert spécialisé en droit des affaires. "
                "Rédige le document suivant de manière professionnelle et formelle, "
                "conforme à la législation marocaine en vigueur. "
                "Cite les articles de loi pertinents quand c'est approprié.\n\n"
                "TYPE DE DOCUMENT: " + document + "\n\n"
                "INFORMATIONS:\n" + infos + "\n\n"
                "Instructions: Document complet, professionnel, prêt à utiliser. "
                "Format structuré avec titre, en-tête, corps et signature. "
                "Maximum 500 mots."
            )

            reponse = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1500
            )

            texte = reponse.choices[0].message.content

        # PDF
        buffer = io.BytesIO()
        doc_pdf = SimpleDocTemplate(
            buffer, pagesize=A4,
            rightMargin=2.5*cm, leftMargin=2.5*cm,
            topMargin=2*cm, bottomMargin=2*cm
        )
        styles = getSampleStyleSheet()
        s_titre = ParagraphStyle('T', parent=styles['Heading1'],
            fontSize=14, spaceAfter=20, alignment=1)
        s_normal = ParagraphStyle('N', parent=styles['Normal'],
            fontSize=11, spaceAfter=10, leading=16)
        s_entete = ParagraphStyle('E', parent=styles['Normal'],
            fontSize=10, spaceAfter=5)

        contenu = []
        nom = valeurs.get("expediteur_nom", "")
        adresse = valeurs.get("expediteur_adresse", "")
        ville = valeurs.get("expediteur_ville", "")
        tel = valeurs.get("expediteur_tel", "")

        contenu.append(Paragraph("<b>" + nom + "</b>", s_entete))
        if adresse:
            contenu.append(Paragraph(adresse + (", " + ville if ville else ""), s_entete))
        if tel:
            contenu.append(Paragraph("Tél : " + tel, s_entete))

        dest_nom = valeurs.get("destinataire_nom", "")
        dest_adresse = valeurs.get("destinataire_adresse", "")
        dest_ville = valeurs.get("destinataire_ville", "")

        if dest_nom:
            contenu.append(Spacer(1, 0.4*cm))
            contenu.append(Paragraph("À : <b>" + dest_nom + "</b>", s_entete))
            if dest_adresse:
                contenu.append(Paragraph(dest_adresse + (", " + dest_ville if dest_ville else ""), s_entete))

        contenu.append(Spacer(1, 0.3*cm))
        contenu.append(Paragraph((ville if ville else "") + ", le " + date_today, s_entete))
        contenu.append(Spacer(1, 0.5*cm))

        for ligne in texte.split('\n'):
            if ligne.strip():
                ligne_propre = ligne.strip().replace('#', '').strip()
                if ligne_propre.isupper() or '**' in ligne_propre:
                    ligne_propre = ligne_propre.replace('**', '')
                    contenu.append(Paragraph(ligne_propre, s_titre))
                else:
                    contenu.append(Paragraph(ligne_propre, s_normal))
                contenu.append(Spacer(1, 0.15*cm))

        doc_pdf.build(contenu)
        buffer.seek(0)

        st.success("Document généré avec succès !")
        st.subheader("Aperçu")
        st.text_area("", texte, height=400, label_visibility="collapsed")

        nom_fichier = document.lower().replace(' ', '_').replace("'", "") + ".pdf"
        st.download_button(
            label="📥 Télécharger le PDF",
            data=buffer,
            file_name=nom_fichier,
            mime="application/pdf"
        )

        st.info("Conservez ce document et envoyez-le par courrier recommandé si nécessaire.")

st.markdown('<div class="footer-katiby">© 2025 Katiby — Documents juridiques pour PME marocaines • 399 DH/an</div>', unsafe_allow_html=True)