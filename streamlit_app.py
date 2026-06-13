import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Portail Archives & Généalogie",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #1C1612 !important;
        font-family: 'Inter', sans-serif;
        color: #F2EBE0;
    }
    [data-testid="stSidebar"] {
        background-color: #141009 !important;
        border-right: 1px solid #3A2E22;
    }
    [data-testid="stSidebar"] * { color: #C9B89A !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #F2EBE0 !important;
        font-family: 'IM Fell English', serif !important;
    }
    .stRadio label, .stMultiSelect label, .stCheckbox label {
        color: #C9B89A !important;
        font-size: 0.88rem !important;
    }
    h1, h2, h3 { color: #F2EBE0 !important; }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #2A1F14 0%, #1C1612 60%, #0F0B08 100%);
        border: 1px solid #3A2E22;
        border-radius: 16px;
        padding: 40px 48px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: "❧";
        position: absolute;
        right: 40px;
        top: 20px;
        font-size: 6rem;
        color: #3A2E22;
        line-height: 1;
    }
    .hero-title {
        font-family: 'IM Fell English', serif;
        font-size: 2.6rem;
        color: #F2EBE0;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }
    .hero-sub {
        color: #8B6B4A;
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.03em;
    }
    .hero-stats {
        display: flex;
        gap: 32px;
        margin-top: 24px;
    }
    .hero-stat {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .hero-stat-num {
        font-family: 'IM Fell English', serif;
        font-size: 2rem;
        color: #D4820A;
        line-height: 1;
    }
    .hero-stat-label {
        font-size: 0.75rem;
        color: #8B6B4A;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Barre de recherche */
    div[data-testid="stTextInput"] input {
        background-color: #141009 !important;
        border: 1px solid #3A2E22 !important;
        border-radius: 10px !important;
        color: #F2EBE0 !important;
        font-size: 0.95rem !important;
        padding: 12px 16px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #8B6B4A !important;
        box-shadow: 0 0 0 2px rgba(139,107,74,0.25) !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: #5A4A38 !important; }

    /* Chips filtres rapides */
    .filter-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 20px;
    }
    .chip {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.15s ease;
        color: #C9B89A;
        background: #2A1F14;
        border-color: #3A2E22;
    }

    /* Compteur résultats */
    .result-count {
        color: #8B6B4A;
        font-size: 0.85rem;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* Cartes */
    .link-card {
        background-color: #231A12;
        border: 1px solid #3A2E22;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 14px;
        transition: border-color 0.2s ease, background-color 0.2s ease;
        position: relative;
    }
    .link-card:hover {
        border-color: #8B6B4A;
        background-color: #2A1F14;
    }

    /* Ligne de badges */
    .card-badges {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
        margin-bottom: 10px;
        align-items: center;
    }

    /* Badge type */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .badge-archive { background-color: #1E3040; color: #7AB3CC; border: 1px solid #2A4A5E; }
    .badge-genealogie { background-color: #1A2E20; color: #7ABF8E; border: 1px solid #2A4A34; }
    .badge-militaire { background-color: #2E1A2E; color: #BF7ABF; border: 1px solid #4A2A4A; }

    /* Badge gratuit / payant — effet tampon */
    .badge-free {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: transparent;
        border: 2px solid #4A7C59;
        color: #4A7C59;
        transform: rotate(-1deg);
        box-shadow: 1px 1px 0 #4A7C5940;
    }
    .badge-paid {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: transparent;
        border: 2px solid #D4820A;
        color: #D4820A;
        transform: rotate(-1deg);
        box-shadow: 1px 1px 0 #D4820A40;
    }
    .badge-freemium {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: transparent;
        border: 2px solid #8B6B4A;
        color: #8B6B4A;
        transform: rotate(-1deg);
        box-shadow: 1px 1px 0 #8B6B4A40;
    }

    /* Badge type document */
    .doc-tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 3px;
        font-size: 0.68rem;
        background: #2A1F14;
        border: 1px solid #3A2E22;
        color: #8B6B4A;
        margin-right: 3px;
        margin-bottom: 3px;
    }

    .card-title-link {
        font-family: 'IM Fell English', serif;
        font-size: 1.15rem;
        font-weight: 400;
        color: #F2EBE0;
        text-decoration: none;
        display: block;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .card-title-link:hover { color: #D4820A; }

    .card-desc {
        color: #8B7055;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-top: 4px;
    }

    .card-docs {
        margin-top: 10px;
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
    }

    /* Séparateur section */
    .section-title {
        font-family: 'IM Fell English', serif;
        font-size: 1.4rem;
        color: #F2EBE0;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #3A2E22;
    }

    /* Sidebar radio styling */
    [data-testid="stRadio"] div[role="radiogroup"] { gap: 4px !important; }

    /* Override Streamlit defaults */
    .stMarkdown p { color: #C9B89A; }
    div[data-testid="stSelectbox"] select { background-color: #141009 !important; color: #F2EBE0 !important; }

    /* Multiselect */
    [data-testid="stMultiSelect"] > div > div {
        background-color: #141009 !important;
        border-color: #3A2E22 !important;
        color: #F2EBE0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DONNÉES
# ==========================================

DOC_TYPES = {
    "État civil": "📋",
    "Registres paroissiaux": "⛪",
    "Registres militaires": "⚔️",
    "Cadastre": "🗺️",
    "Recensements": "👥",
    "Notaires": "📝",
    "Presse ancienne": "📰",
    "Photos/Cartes": "🖼️",
    "Arbres généalogiques": "🌳",
    "Légion d'honneur": "🏅",
}

archives_data = [
    {"Nom": "01 - Ain", "Url": "https://archives.ain.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux", "Registres militaires", "Recensements"], "Desc": "Registres paroissiaux, d'état civil, recensements et registres matricules de l'Ain."},
    {"Nom": "02 - Aisne", "Url": "https://archives.aisne.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Accès en ligne aux archives numérisées du département de l'Aisne."},
    {"Nom": "03 - Allier", "Url": "https://archives.allier.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Cadastre"], "Desc": "Généalogie, cartes et plans, archives judiciaires de l'Allier."},
    {"Nom": "04 - Alpes-de-Haute-Provence", "Url": "https://www.archives04.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Consultation de l'état civil et des archives numérisées du 04."},
    {"Nom": "05 - Hautes-Alpes", "Url": "https://archives.hautes-alpes.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil"], "Desc": "Fonds documentaires et historiques des Hautes-Alpes."},
    {"Nom": "06 - Alpes-Maritimes", "Url": "https://www.departement06.fr/les-archives-departementales-2850.html", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Cadastre", "Registres militaires"], "Desc": "Registres d'état civil, plans cadastral et archives militaires des Alpes-Maritimes."},
    {"Nom": "07 - Ardèche", "Url": "https://archives.ardeche.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Histoire locale et généalogie en Ardèche."},
    {"Nom": "08 - Ardennes", "Url": "https://archives.cd08.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil"], "Desc": "Accès aux fonds numérisés du département des Ardennes."},
    {"Nom": "09 - Ariège", "Url": "https://archives.ariege.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Recherches généalogiques et historiques en Ariège."},
    {"Nom": "10 - Aube", "Url": "https://archives-aube.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Cadastre"], "Desc": "État civil, registres paroissiaux et cadastre de l'Aube."},
    {"Nom": "13 - Bouches-du-Rhône", "Url": "https://www.archives13.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux", "Cadastre", "Recensements"], "Desc": "Grandes collections de Marseille, Aix-en-Provence et des Bouches-du-Rhône."},
    {"Nom": "14 - Calvados", "Url": "https://archives.calvados.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds normands, état civil et histoire locale du Calvados."},
    {"Nom": "21 - Côte-d'Or", "Url": "https://archives.cotedor.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds ducaux de Bourgogne et état civil de la Côte-d'Or."},
    {"Nom": "29 - Finistère", "Url": "https://archives.finistere.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Généalogie maritime, registres paroissiaux et d'état civil du Finistère."},
    {"Nom": "31 - Haute-Garonne", "Url": "https://archives.hautegaronne.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux", "Registres militaires"], "Desc": "Registres d'état civil de Toulouse et de la Haute-Garonne."},
    {"Nom": "33 - Gironde", "Url": "https://archives.gironde.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Notaires"], "Desc": "Fonds de Bordeaux et de la Gironde, commerce maritime et état civil."},
    {"Nom": "34 - Hérault", "Url": "https://archives-pierresvives.herault.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Cadastre"], "Desc": "Espace Pierresvives, archives numérisées de l'Hérault."},
    {"Nom": "35 - Ille-et-Vilaine", "Url": "https://archives.ille-et-vilaine.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds d'état civil de Rennes et du département d'Ille-et-Vilaine."},
    {"Nom": "38 - Isère", "Url": "https://archives.isere.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres militaires", "Cadastre"], "Desc": "Fonds du Dauphiné, état civil et registres matricules de l'Isère."},
    {"Nom": "44 - Loire-Atlantique", "Url": "https://archives.loire-atlantique.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux", "Notaires"], "Desc": "Fonds nantais, état civil et archives maritimes du 44."},
    {"Nom": "49 - Maine-et-Loire", "Url": "https://www.archives49.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds d'Anjou, registres paroissiaux et d'état civil du 49."},
    {"Nom": "57 - Moselle", "Url": "https://archives57.com/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds spécifiques liés à l'histoire d'Alsace-Moselle."},
    {"Nom": "59 - Nord", "Url": "https://archivesdepartementales.lenord.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux", "Cadastre", "Recensements"], "Desc": "L'un des plus grands fonds de France (Flandres, Hainaut, Lille)."},
    {"Nom": "67/68 - Alsace", "Url": "https://archives.alsace.eu/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds de la Collectivité européenne d'Alsace (Strasbourg & Colmar)."},
    {"Nom": "69 - Rhône", "Url": "https://archives.rhone.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Recensements"], "Desc": "Fonds lyonnais et du département du Rhône, état civil et hospices."},
    {"Nom": "75 - Paris", "Url": "https://archives.paris.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres militaires", "Cadastre"], "Desc": "État civil reconstitué, fiches de matricules et cadastre de Paris."},
    {"Nom": "76 - Seine-Maritime", "Url": "https://www.archivesdepartementales76.net/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds de Rouen, du Havre et de la Seine-Maritime."},
    {"Nom": "80 - Somme", "Url": "https://archives.somme.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres militaires"], "Desc": "Registres matricules, état civil et fonds de la Grande Guerre."},
    {"Nom": "85 - Vendée", "Url": "https://archives.vendee.fr/", "Type": "Archives Départementales", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fonds très riches sur les Guerres de Vendée et l'état civil du 85."},
]

genealogie_data = [
    # Sites gratuits
    {"Nom": "Geneanet", "Url": "https://www.geneanet.org", "Type": "Généalogie", "Tarif": "Freemium", "Docs": ["Arbres généalogiques", "État civil", "Presse ancienne"], "Desc": "Première communauté généalogique en Europe. Arbres en ligne, base collaborative et documents."},
    {"Nom": "FamilySearch", "Url": "https://www.familysearch.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques", "État civil", "Registres paroissiaux"], "Desc": "Immense base de données mondiale et gratuite gérée par les Mormons."},
    {"Nom": "Géoportail", "Url": "https://www.geoportail.gouv.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Cadastre", "Photos/Cartes"], "Desc": "Cartes anciennes, plans de Cassini et évolution des territoires français."},
    {"Nom": "Gallica (BnF)", "Url": "https://gallica.bnf.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Presse ancienne", "Photos/Cartes"], "Desc": "Bibliothèque numérique de la BnF : journaux locaux, armoriaux et biographies anciennes."},
    {"Nom": "Europeana", "Url": "https://www.europeana.eu", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Photos/Cartes", "Presse ancienne"], "Desc": "Accès aux collections culturelles et historiques numérisées d'Europe."},
    {"Nom": "MyHeritage", "Url": "https://www.myheritage.fr", "Type": "Généalogie", "Tarif": "Freemium", "Docs": ["Arbres généalogiques", "État civil"], "Desc": "Plateforme internationale avec outils de colorisation photo et recherche ADN."},
    {"Nom": "Filae", "Url": "https://www.filae.com", "Type": "Généalogie", "Tarif": "Freemium", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Moteur de recherche majeur pour la généalogie française avec transcription d'actes."},
    {"Nom": "Généanet Relevés", "Url": "https://gw.geneanet.org/releves", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Index bénévoles des registres paroissiaux et d'état civil, communauté collaborative."},
    {"Nom": "Racines & Histoire", "Url": "http://racineshistoire.free.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Encyclopédie des noms de famille et des origines des familles françaises."},
    {"Nom": "Géné@PACA", "Url": "https://www.genea-paca.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fédération des cercles de généalogie de la région Provence-Alpes-Côte d'Azur."},
    {"Nom": "Cercle Généalogique du Languedoc", "Url": "https://www.cgl-montpellier.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil"], "Desc": "Relevés et index généalogiques pour le Languedoc et l'Hérault."},
    {"Nom": "Association Généalogique du Pas-de-Calais", "Url": "https://www.agpc.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Relevés bénévoles pour le Pas-de-Calais et région Nord."},
    {"Nom": "GeneaFrance", "Url": "https://geneafrance.com", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques", "État civil"], "Desc": "Annuaire des ressources généalogiques françaises en ligne."},
    {"Nom": "Cercle Généalogique de Bretagne", "Url": "https://www.cgb-bretagne.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Relevés et base de données pour la Bretagne historique."},
    {"Nom": "Généalogie Alsace", "Url": "https://www.genealogie-alsace.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Index et relevés spécialisés pour les familles alsaciennes."},
    {"Nom": "Corel (Normandie)", "Url": "https://www.corel-genealogie.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Cercles de recherche généalogique pour la Normandie."},
    {"Nom": "Généaologie.com", "Url": "https://www.genealogie.com", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Portail généalogique francophone : arbres, entraide et forums."},
    {"Nom": "1789-1815.com", "Url": "https://www.1789-1815.com", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Registres militaires"], "Desc": "Base de données des soldats des guerres révolutionnaires et napoléoniennes."},
    {"Nom": "Arolsen Archives", "Url": "https://arolsen-archives.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil"], "Desc": "Archives mondiales sur les victimes du nazisme, recherches familiales."},
    {"Nom": "Immigrant Ships Transcribers Guild", "Url": "https://www.immigrantships.net", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil"], "Desc": "Listes de passagers de bateaux transatlantiques, utile pour l'émigration."},
    {"Nom": "Find A Grave", "Url": "https://www.findagrave.com", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Photos/Cartes"], "Desc": "Base mondiale de sépultures avec photos de tombes et liens familiaux."},
    {"Nom": "BillionGraves", "Url": "https://billiongraves.com", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil"], "Desc": "Indexation communautaire de cimetières du monde entier via smartphones."},
    {"Nom": "WikiTree", "Url": "https://www.wikitree.com", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Arbre généalogique mondial collaboratif et entièrement gratuit."},
    {"Nom": "Geni", "Url": "https://www.geni.com", "Type": "Généalogie", "Tarif": "Freemium", "Docs": ["Arbres généalogiques"], "Desc": "Projet d'arbre mondial unique : reliez vos ancêtres à tous les autres."},
    {"Nom": "OpenTree of Life", "Url": "https://tree.opentreeoflife.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Arbre phylogénétique open-source de toutes les espèces vivantes."},
    {"Nom": "Rodovid", "Url": "https://fr.rodovid.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Wiki généalogique multilingue et participatif."},
    {"Nom": "WeRelate", "Url": "https://www.werelate.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques", "État civil"], "Desc": "Wiki généalogique gratuit hébergé par la Bibliothèque publique de l'Utah."},
    {"Nom": "The Peerage", "Url": "https://www.thepeerage.com", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Base de données des familles nobles et pairs d'Europe."},
    {"Nom": "Généaologies des Familles Bretonnes", "Url": "https://www.infobretagne.com/genealogie.htm", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques", "Registres paroissiaux"], "Desc": "Ressources et liens généalogiques spécialisés pour la Bretagne."},
    {"Nom": "Ressources du Québec", "Url": "https://www.genealogie.qc.ca", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Fédération québécoise des sociétés de généalogie, ressources francophones."},
    {"Nom": "PRDH-IGD (Québec)", "Url": "https://www.prdh-igd.com", "Type": "Généalogie", "Tarif": "Freemium", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Programme de recherche en démographie historique, familles du Québec ancien."},
    {"Nom": "Système Loiselle", "Url": "https://www.loiselle.ca", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Registres paroissiaux"], "Desc": "Index des mariages catholiques du Québec par régions et paroisses."},
    {"Nom": "GRHS (German-Russian Heritage)", "Url": "https://www.grhs.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil"], "Desc": "Ressources pour les familles d'origine germano-russe immigrées en Amérique."},
    {"Nom": "Généanet Cartes Postales", "Url": "https://cp.geneanet.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Photos/Cartes"], "Desc": "Plus d'un million de cartes postales anciennes pour identifier lieux et coutumes."},
    {"Nom": "RetroNews (BnF)", "Url": "https://www.retronews.fr", "Type": "Généalogie", "Tarif": "Freemium", "Docs": ["Presse ancienne"], "Desc": "Presse ancienne numérisée par la BnF : plus de 600 titres de 1631 à 1952."},
    {"Nom": "Persée", "Url": "https://www.persee.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Presse ancienne"], "Desc": "Bibliothèque numérique de revues scientifiques françaises en sciences humaines."},
    {"Nom": "Google Books", "Url": "https://books.google.fr", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Presse ancienne"], "Desc": "Des millions d'ouvrages anciens numérisés, dont de nombreux almanachs et annuaires."},
    {"Nom": "Openarchives.eu", "Url": "https://www.openarchives.eu", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Portail européen agrégeant de nombreux fonds d'archives numérisées."},
    {"Nom": "Généalogie & Histoire de la Caraïbe", "Url": "https://www.ghcaraibe.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["État civil", "Registres paroissiaux"], "Desc": "Relevés et ressources pour les DOM-TOM et les Antilles françaises."},
    {"Nom": "Ancestris (logiciel gratuit)", "Url": "https://ancestris.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Logiciel généalogique open-source français, compatible GEDCOM."},
    {"Nom": "Gramps (logiciel gratuit)", "Url": "https://gramps-project.org", "Type": "Généalogie", "Tarif": "Gratuit", "Docs": ["Arbres généalogiques"], "Desc": "Logiciel généalogique libre, puissant et multiplateforme."},
]

militaire_data = [
    {"Nom": "Mémoire des Hommes", "Url": "https://www.memoiredeshommes.sga.defense.gouv.fr/", "Type": "Militaire", "Tarif": "Gratuit", "Docs": ["Registres militaires", "État civil"], "Desc": "Base officielle des morts pour la France (WW1, WW2, Indochine, Algérie)."},
    {"Nom": "Grand Mémorial", "Url": "https://www.culture.fr/Grand-Memorial", "Type": "Militaire", "Tarif": "Gratuit", "Docs": ["Registres militaires"], "Desc": "Base nationale des registres matricules des soldats de la Grande Guerre."},
    {"Nom": "Base Léonore", "Url": "https://www.archives-nationales.culture.gouv.fr/leonore/", "Type": "Militaire", "Tarif": "Gratuit", "Docs": ["Légion d'honneur"], "Desc": "Dossiers des membres nominatifs de la Légion d'honneur depuis 1802."},
    {"Nom": "Service Historique de la Défense (SHD)", "Url": "https://www.servicehistorique.sga.defense.gouv.fr/", "Type": "Militaire", "Tarif": "Gratuit", "Docs": ["Registres militaires"], "Desc": "Centre d'archives officiel des armées françaises (Terre, Marine, Air)."},
    {"Nom": "Les Morts pour la France (Geneanet)", "Url": "https://www.geneanet.org/militaires/", "Type": "Militaire", "Tarif": "Gratuit", "Docs": ["Registres militaires", "État civil"], "Desc": "Indexation collaborative de monuments aux morts et de registres militaires."},
    {"Nom": "Casualties WW2 (Commonwealth)", "Url": "https://www.cwgc.org", "Type": "Militaire", "Tarif": "Gratuit", "Docs": ["Registres militaires"], "Desc": "Commonwealth War Graves Commission : 1,7 million de soldats du Commonwealth."},
    {"Nom": "Fold3 (archives militaires US)", "Url": "https://www.fold3.com", "Type": "Militaire", "Tarif": "Payant", "Docs": ["Registres militaires"], "Desc": "Archives militaires américaines numérisées, pension rolls et dossiers de service."},
    {"Nom": "Bases Nationales des Monuments aux Morts", "Url": "https://www.memorialgenweb.org", "Type": "Militaire", "Tarif": "Gratuit", "Docs": ["Registres militaires", "Photos/Cartes"], "Desc": "MemorialGenWeb : photos et relevés de tous les monuments aux morts de France."},
]

all_links = archives_data + genealogie_data + militaire_data
df = pd.DataFrame(all_links)

# ==========================================
# INTERFACE
# ==========================================

with st.sidebar:
    st.markdown("<h2 style='margin-top:0; font-family: IM Fell English, serif;'>📜 Filtres</h2>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### Univers")
    categories = ["Tous", "Archives Départementales", "Généalogie", "Militaire"]
    selected_category = st.radio("", categories, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### Accès")
    tarif_options = st.multiselect(
        "",
        ["Gratuit", "Freemium", "Payant"],
        default=["Gratuit", "Freemium", "Payant"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### Types de documents")
    all_doc_types = list(DOC_TYPES.keys())
    selected_docs = st.multiselect(
        "",
        all_doc_types,
        default=[],
        placeholder="Tous les types",
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.8rem; color:#5A4A38;'>Portail regroupant 100+ sources d'archives françaises et de généalogie.</p>",
        unsafe_allow_html=True
    )

# Hero
total = len(df)
free_count = len(df[df["Tarif"] == "Gratuit"])
depart_count = len([x for x in all_links if x["Type"] == "Archives Départementales"])
genea_count = len([x for x in all_links if x["Type"] == "Généalogie"])

st.markdown(f"""
<div class="hero">
    <p class="hero-title">Portail Archives & Généalogie</p>
    <p class="hero-sub">Sources primaires, registres numérisés et outils de recherche familiale</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <span class="hero-stat-num">{total}</span>
            <span class="hero-stat-label">Sources indexées</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">{free_count}</span>
            <span class="hero-stat-label">Entièrement gratuites</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">{depart_count}</span>
            <span class="hero-stat-label">Archives dép.</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">{genea_count}</span>
            <span class="hero-stat-label">Sites généalogie</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Recherche
search_query = st.text_input("", placeholder="🔍  Rechercher un département, un outil, un document… (ex: 44, Filae, matricule)", label_visibility="collapsed")

# Filtrage
filtered_df = df.copy()

if selected_category != "Tous":
    filtered_df = filtered_df[filtered_df["Type"] == selected_category]

if tarif_options:
    filtered_df = filtered_df[filtered_df["Tarif"].isin(tarif_options)]

if selected_docs:
    filtered_df = filtered_df[
        filtered_df["Docs"].apply(lambda d: any(doc in d for doc in selected_docs))
    ]

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["Nom"].str.lower().str.contains(q, na=False) |
        filtered_df["Desc"].str.lower().str.contains(q, na=False) |
        filtered_df["Docs"].apply(lambda d: any(q in doc.lower() for doc in d))
    ]

# Résultats
st.markdown(f"<p class='result-count'>{len(filtered_df)} source(s) trouvée(s)</p>", unsafe_allow_html=True)

if not filtered_df.empty:
    col1, col2 = st.columns(2, gap="medium")

    for idx, row in filtered_df.reset_index(drop=True).iterrows():
        badge_class = "badge-archive"
        if row["Type"] == "Généalogie":
            badge_class = "badge-genealogie"
        elif row["Type"] == "Militaire":
            badge_class = "badge-militaire"

        tarif_class = "badge-free"
        tarif_label = "Gratuit"
        if row["Tarif"] == "Payant":
            tarif_class = "badge-paid"
            tarif_label = "Payant"
        elif row["Tarif"] == "Freemium":
            tarif_class = "badge-freemium"
            tarif_label = "Freemium"

        docs_html = "".join([
            f'<span class="doc-tag">{DOC_TYPES.get(d, "📄")} {d}</span>'
            for d in row["Docs"]
        ])

        card_html = f"""
        <div class="link-card">
            <div class="card-badges">
                <span class="badge {badge_class}">{row['Type']}</span>
                <span class="{tarif_class}">{tarif_label}</span>
            </div>
            <a href="{row['Url']}" target="_blank" class="card-title-link">{row['Nom']} ↗</a>
            <div class="card-desc">{row['Desc']}</div>
            <div class="card-docs">{docs_html}</div>
        </div>
        """

        if idx % 2 == 0:
            col1.markdown(card_html, unsafe_allow_html=True)
        else:
            col2.markdown(card_html, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align:center; padding: 60px 20px; color: #5A4A38;'>
        <div style='font-size: 2.5rem; margin-bottom: 12px;'>☍</div>
        <p style='font-family: IM Fell English, serif; font-size: 1.2rem; color: #8B6B4A;'>Aucune source ne correspond à vos critères.</p>
        <p style='font-size: 0.85rem;'>Essayez d'élargir les filtres ou de modifier votre recherche.</p>
    </div>
    """, unsafe_allow_html=True)
