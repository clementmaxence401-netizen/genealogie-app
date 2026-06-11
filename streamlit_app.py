import streamlit as st
import pandas as pd

# ==========================================
# 1. CONFIGURATION DE LA PAGE & STYLE "CLAUDE"
# ==========================================
st.set_page_config(
    page_title="Archives & Généalogie",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injection de CSS pour imiter l'interface de Claude (Anthropic)
# Couleurs douces, polices élégantes, angles arrondis et ombres subtiles.
st.markdown("""
    <style>
    /* Fond global et typographie */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FBF9F6 !important;
        font-family: 'Inter', sans-serif;
        color: #191919;
    }
    
    /* Sidebar style */
    [data-testid="stSidebar"] {
        background-color: #F3EFEA !important;
        border-right: 1px solid #E6DFD5;
    }
    
    /* Titres */
    h1, h2, h3 {
        color: #191919 !important;
        font-weight: 500 !important;
    }
    
    /* Cartes de liens style "Claude" */
    .link-card {
        background-color: #FFFFFF;
        border: 1px solid #E6DFD5;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .link-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25,25,25,0.05);
        border-color: #D4C9B9;
    }
    
    /* Badges de catégories */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .badge-archive { background-color: #E8F4F8; color: #1D657F; }
    .badge-genealogie { background-color: #EBF7ED; color: #2A6635; }
    .badge-militaire { background-color: #FDF3E7; color: #8F4E00; }
    
    /* Boutons de recherche et inputs */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF;
        border: 1px solid #D4C9B9 !important;
        border-radius: 8px !important;
        color: #191919;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #191919 !important;
        box-shadow: 0 0 0 1px #191919 !important;
    }
    
    /* Liens */
    .card-title-link {
        font-size: 1.1rem;
        font-weight: 600;
        color: #191919;
        text-decoration: none;
    }
    .card-title-link:hover {
        color: #D97706;
    }
    .card-desc {
        color: #6B6661;
        font-size: 0.9rem;
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DONNÉES (ARCHIVES, GÉNÉALOGIE, MILITAIRE)
# ==========================================

# Génération des données pour TOUTES les archives départementales principales (01 à 95 + DOM)
archives_data = [
    {"Nom": "01 - Ain", "Url": "https://archives.ain.fr/", "Type": "Archives Départementales", "Desc": "Registres paroissiaux, d'état civil, recensements et registres matricules de l'Ain."},
    {"Nom": "02 - Aisne", "Url": "https://archives.aisne.fr/", "Type": "Archives Départementales", "Desc": "Accès en ligne aux archives numérisées du département de l'Aisne."},
    {"Nom": "03 - Allier", "Url": "https://archives.allier.fr/", "Type": "Archives Départementales", "Desc": "Généalogie, cartes et plans, archives judiciaires de l'Allier."},
    {"Nom": "04 - Alpes-de-Haute-Provence", "Url": "https://www.archives04.fr/", "Type": "Archives Départementales", "Desc": "Consultation de l'état civil et des archives numérisées du 04."},
    {"Nom": "05 - Hautes-Alpes", "Url": "https://archives.hautes-alpes.fr/", "Type": "Archives Départementales", "Desc": "Fonds documentaires et historiques des Hautes-Alpes."},
    {"Nom": "06 - Alpes-Maritimes", "Url": "https://www.departement06.fr/les-archives-departementales-2850.html", "Type": "Archives Départementales", "Desc": "Registres d'état civil, plans cadastral et archives militaires des Alpes-Maritimes."},
    {"Nom": "07 - Ardèche", "Url": "https://archives.ardeche.fr/", "Type": "Archives Départementales", "Desc": "Histoire locale et généalogie en Ardèche."},
    {"Nom": "08 - Ardennes", "Url": "https://archives.cd08.fr/", "Type": "Archives Départementales", "Desc": "Accès aux fonds numérisés du département des Ardennes."},
    {"Nom": "09 - Ariège", "Url": "https://archives.ariege.fr/", "Type": "Archives Départementales", "Desc": "Recherches généalogiques et historiques en Ariège."},
    {"Nom": "10 - Aube", "Url": "https://archives-aube.fr/", "Type": "Archives Départementales", "Desc": "État civil, registres paroissiaux et cadastre de l'Aube."},
    {"Nom": "11 - Aude", "Url": "https://archivesdepartementales.aude.fr/", "Type": "Archives Départementales", "Desc": "Fonds numérisés et histoire du département de l'Aude."},
    {"Nom": "12 - Aveyron", "Url": "https://archives.aveyron.fr/", "Type": "Archives Départementales", "Desc": "Généalogie, recensements et documents administratifs de l'Aveyron."},
    {"Nom": "13 - Bouches-du-Rhône", "Url": "https://www.archives13.fr/", "Type": "Archives Départementales", "Desc": "Grandes collections de Marseille, Aix-en-Provence et des Bouches-du-Rhône."},
    {"Nom": "14 - Calvados", "Url": "https://archives.calvados.fr/", "Type": "Archives Départementales", "Desc": "Fonds normands, état civil et histoire locale du Calvados."},
    {"Nom": "15 - Cantal", "Url": "https://archives.cantal.fr/", "Type": "Archives Départementales", "Desc": "Archives numérisées et histoire des familles du Cantal."},
    {"Nom": "16 - Charente", "Url": "https://archives.lacharente.fr/", "Type": "Archives Départementales", "Desc": "Registres paroissiaux, état civil et archives notariales de la Charente."},
    {"Nom": "17 - Charente-Maritime", "Url": "https://archives.charente-maritime.fr/", "Type": "Archives Départementales", "Desc": "Histoire maritime, état civil et documents officiels de la Charente-Maritime."},
    {"Nom": "18 - Cher", "Url": "https://www.archives18.fr/", "Type": "Archives Départementales", "Desc": "Recherches généalogiques et cadastre du département du Cher."},
    {"Nom": "19 - Corrèze", "Url": "https://www.archives.correze.fr/", "Type": "Archives Départementales", "Desc": "Fonds d'état civil, militaires et cadastre de la Corrèze."},
    {"Nom": "2A - Corse-du-Sud", "Url": "https://archives.isula.corsica/", "Type": "Archives Départementales", "Desc": "Histoire et généalogie de la Corse-du-Sud."},
    {"Nom": "2B - Haute-Corse", "Url": "https://archives.isula.corsica/", "Type": "Archives Départementales", "Desc": "Fonds d'archives et documents d'état civil de la Haute-Corse."},
    {"Nom": "21 - Côte-d'Or", "Url": "https://archives.cotedor.fr/", "Type": "Archives Départementales", "Desc": "Fonds ducaux de Bourgogne et état civil de la Côte-d'Or."},
    {"Nom": "22 - Côtes-d'Armor", "Url": "https://archives.cotesdarmor.fr/", "Type": "Archives Départementales", "Desc": "Généalogie bretonne et histoire locale des Côtes-d'Armor."},
    {"Nom": "23 - Creuse", "Url": "https://archives.creuse.fr/", "Type": "Archives Départementales", "Desc": "Registres paroissiaux, d'état civil et registres de maçons de la Creuse."},
    {"Nom": "24 - Dordogne", "Url": "https://archives.dordogne.fr/", "Type": "Archives Départementales", "Desc": "Riches fonds du Périgord, état civil et archives notariales."},
    {"Nom": "25 - Doubs", "Url": "https://archives.doubs.fr/", "Type": "Archives Départementales", "Desc": "Recherches généalogiques en Franche-Comté (Doubs)."},
    {"Nom": "26 - Drôme", "Url": "https://archives.ladrome.fr/", "Type": "Archives Départementales", "Desc": "Fonds numérisés et histoire des communes de la Drôme."},
    {"Nom": "27 - Eure", "Url": "https://archives.eure.fr/", "Type": "Archives Départementales", "Desc": "État civil, registres de matricules militaires et plans de l'Eure."},
    {"Nom": "28 - Eure-et-Loir", "Url": "https://archives28.fr/", "Type": "Archives Départementales", "Desc": "Fonds d'histoire locale et de généalogie d'Eure-et-Loir."},
    {"Nom": "29 - Finistère", "Url": "https://archives.finistere.fr/", "Type": "Archives Départementales", "Desc": "Généalogie maritime, registres paroissiaux et d'état civil du Finistère."},
    {"Nom": "30 - Gard", "Url": "https://archives.gard.fr/", "Type": "Archives Départementales", "Desc": "Fonds protestants, état civil et histoire du Gard."},
    {"Nom": "31 - Haute-Garonne", "Url": "https://archives.hautegaronne.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil de Toulouse et de la Haute-Garonne."},
    {"Nom": "32 - Gers", "Url": "https://www.archives32.fr/", "Type": "Archives Départementales", "Desc": "Histoire de la Gascogne, registres paroissiaux et cadastre du Gers."},
    {"Nom": "33 - Gironde", "Url": "https://archives.gironde.fr/", "Type": "Archives Départementales", "Desc": "Fonds de Bordeaux et de la Gironde, commerce maritime et état civil."},
    {"Nom": "34 - Hérault", "Url": "https://archives-pierresvives.herault.fr/", "Type": "Archives Départementales", "Desc": "Espace Pierresvives, archives numérisées de l'Hérault."},
    {"Nom": "35 - Ille-et-Vilaine", "Url": "https://archives.ille-et-vilaine.fr/", "Type": "Archives Départementales", "Desc": "Fonds d'état civil de Rennes et du département d'Ille-et-Vilaine."},
    {"Nom": "36 - Indre", "Url": "https://www.archives36.fr/", "Type": "Archives Départementales", "Desc": "Registres paroissiaux et documents d'état civil de l'Indre."},
    {"Nom": "37 - Indre-et-Loire", "Url": "https://archives.touraine.fr/", "Type": "Archives Départementales", "Desc": "Histoire de la Touraine, châteaux de la Loire et état civil."},
    {"Nom": "38 - Isère", "Url": "https://archives.isere.fr/", "Type": "Archives Départementales", "Desc": "Fonds du Dauphiné, état civil et registres matricules de l'Isère."},
    {"Nom": "39 - Jura", "Url": "https://archives.jura.fr/", "Type": "Archives Départementales", "Desc": "Archives d'état civil et fonds historiques du département du Jura."},
    {"Nom": "40 - Landes", "Url": "https://archives.landes.fr/", "Type": "Archives Départementales", "Desc": "Histoire de la Chalosse et des Landes, état civil en ligne."},
    {"Nom": "41 - Loir-et-Cher", "Url": "https://archives.culture41.fr/", "Type": "Archives Départementales", "Desc": "Fonds historiques et généalogiques du Loir-et-Cher."},
    {"Nom": "42 - Loire", "Url": "https://www.archives42.fr/", "Type": "Archives Départementales", "Desc": "État civil, recensements et registres du Forez et de la Loire."},
    {"Nom": "43 - Haute-Loire", "Url": "https://www.archives43.fr/", "Type": "Archives Départementales", "Desc": "Recherches généalogiques et archives numérisées de la Haute-Loire."},
    {"Nom": "44 - Loire-Atlantique", "Url": "https://archives.loire-atlantique.fr/", "Type": "Archives Départementales", "Desc": "Fonds nantais, état civil et archives maritimes du 44."},
    {"Nom": "45 - Loiret", "Url": "https://archives-loiret.fr/", "Type": "Archives Départementales", "Desc": "Histoire de l'Orléanais et documents généalogiques du Loiret."},
    {"Nom": "46 - Lot", "Url": "https://archives.lot.fr/", "Type": "Archives Départementales", "Desc": "Cadastre, état civil et archives notariales du Lot."},
    {"Nom": "47 - Lot-et-Garonne", "Url": "https://www.archives47.fr/", "Type": "Archives Départementales", "Desc": "Fonds numérisés et documents d'histoire locale du Lot-et-Garonne."},
    {"Nom": "48 - Lozère", "Url": "https://archives.lozere.fr/", "Type": "Archives Départementales", "Desc": "Généalogie et histoire du Gévaudan (Lozère)."},
    {"Nom": "49 - Maine-et-Loire", "Url": "https://www.archives49.fr/", "Type": "Archives Départementales", "Desc": "Fonds d'Anjou, registres paroissiaux et d'état civil du 49."},
    {"Nom": "50 - Manche", "Url": "https://archives.manche.fr/", "Type": "Archives Départementales", "Desc": "Fonds normands, reconstruction et état civil de la Manche."},
    {"Nom": "51 - Marne", "Url": "https://archives.marne.fr/", "Type": "Archives Départementales", "Desc": "Histoire de la Champagne, état civil et registres de la Marne."},
    {"Nom": "52 - Haute-Marne", "Url": "https://archives.haute-marne.fr/", "Type": "Archives Départementales", "Desc": "Généalogie et documents numérisés de la Haute-Marne."},
    {"Nom": "53 - Mayenne", "Url": "https://archives.lamayenne.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil, cartes et plans de la Mayenne."},
    {"Nom": "54 - Meurthe-et-Moselle", "Url": "https://archives.meurthe-et-moselle.fr/", "Type": "Archives Départementales", "Desc": "Fonds lorrains, généalogie et registres militaires du 54."},
    {"Nom": "55 - Meuse", "Url": "https://archives.meuse.fr/", "Type": "Archives Départementales", "Desc": "Histoire de la Première Guerre mondiale et état civil de la Meuse."},
    {"Nom": "56 - Morbihan", "Url": "https://archives.morbihan.fr/", "Type": "Archives Départementales", "Desc": "Généalogie bretonne, état civil et amirauté du Morbihan."},
    {"Nom": "57 - Moselle", "Url": "https://archives57.com/", "Type": "Archives Départementales", "Desc": "Fonds spécifiques liés à l'histoire d'Alsace-Moselle."},
    {"Nom": "58 - Nièvre", "Url": "https://archives.nievre.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil et fonds d'histoire locale de la Nièvre."},
    {"Nom": "59 - Nord", "Url": "https://archivesdepartementales.lenord.fr/", "Type": "Archives Départementales", "Desc": "L'un des plus grands fonds de France (Flandres, Hainaut, Lille)."},
    {"Nom": "60 - Oise", "Url": "https://archives.oise.fr/", "Type": "Archives Départementales", "Desc": "État civil, plans d'intendance et archives de l'Oise."},
    {"Nom": "61 - Orne", "Url": "https://archives.orne.fr/", "Type": "Archives Départementales", "Desc": "Généalogie et documents historiques normands de l'Orne."},
    {"Nom": "62 - Pas-de-Calais", "Url": "https://archivespasdecalais.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil et archives de reconstruction du Pas-de-Calais."},
    {"Nom": "63 - Puy-de-Dôme", "Url": "https://www.archives-puy-dedome.fr/", "Type": "Archives Départementales", "Desc": "Fonds auvergnats, état civil et matricules militaires du 63."},
    {"Nom": "64 - Pyrénées-Atlantiques", "Url": "https://le64.fr/les-archives-departementales", "Type": "Archives Départementales", "Desc": "Histoire du Béarn et du Pays Basque, état civil en ligne."},
    {"Nom": "65 - Hautes-Pyrénées", "Url": "https://www.archives65.fr/", "Type": "Archives Départementales", "Desc": "Fonds pyrénéens et état civil des Hautes-Pyrénées."},
    {"Nom": "66 - Pyrénées-Orientales", "Url": "https://archives.ledepartement66.fr/", "Type": "Archives Départementales", "Desc": "Histoire du Roussillon, archives catalanes et état civil."},
    {"Nom": "67 - Bas-Rhin (Alsace)", "Url": "https://archives.alsace.eu/", "Type": "Archives Départementales", "Desc": "Fonds de la Collectivité européenne d'Alsace (Strasbourg)."},
    {"Nom": "68 - Haut-Rhin (Alsace)", "Url": "https://archives.alsace.eu/", "Type": "Archives Départementales", "Desc": "Fonds de la Collectivité européenne d'Alsace (Colmar)."},
    {"Nom": "69 - Rhône & Métropole de Lyon", "Url": "https://archives.rhone.fr/", "Type": "Archives Départementales", "Desc": "Fonds lyonnais et du département du Rhône, état civil et hospices."},
    {"Nom": "70 - Haute-Saône", "Url": "https://archives.haute-saone.fr/", "Type": "Archives Départementales", "Desc": "Recherches généalogiques et fonds comtois du 70."},
    {"Nom": "71 - Saône-et-Loire", "Url": "https://archives71.fr/", "Type": "Archives Départementales", "Desc": "État civil, registres paroissiaux et cadastre de Saône-et-Loire."},
    {"Nom": "72 - Sarthe", "Url": "https://archives.sarthe.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil, recensements et plans du Maine/Sarthe."},
    {"Nom": "73 - Savoie", "Url": "https://www.archives-savoie.fr/", "Type": "Archives Départementales", "Desc": "Fonds uniques de l'histoire du Duché de Savoie."},
    {"Nom": "74 - Haute-Savoie", "Url": "https://archives.hautesavoie.fr/", "Type": "Archives Départementales", "Desc": "Cadastre sarde, état civil et histoire de la Haute-Savoie."},
    {"Nom": "75 - Paris", "Url": "https://archives.paris.fr/", "Type": "Archives Départementales", "Desc": "État civil reconstitué, fiches de matricules et cadastre de Paris."},
    {"Nom": "76 - Seine-Maritime", "Url": "https://www.archivesdepartementales76.net/", "Type": "Archives Départementales", "Desc": "Fonds de Rouen, du Havre et de la Seine-Maritime."},
    {"Nom": "77 - Seine-et-Marne", "Url": "https://archives.seine-et-marne.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil et documents d'histoire locale du 77."},
    {"Nom": "78 - Yvelines", "Url": "https://archives.yvelines.fr/", "Type": "Archives Départementales", "Desc": "Histoire de Versailles et de l'ancien département de Seine-et-Oise."},
    {"Nom": "79 - Deux-Sèvres", "Url": "https://archives.deux-sevres.fr/", "Type": "Archives Départementales", "Desc": "État civil, plans de communes et documents des Deux-Sèvres."},
    {"Nom": "80 - Somme", "Url": "https://archives.somme.fr/", "Type": "Archives Départementales", "Desc": "Registres matricules, état civil et fonds de la Grande Guerre."},
    {"Nom": "81 - Tarn", "Url": "https://archives.tarn.fr/", "Type": "Archives Départementales", "Desc": "Histoire de l'Albigeois, état civil et compoix du Tarn."},
    {"Nom": "82 - Tarn-et-Garonne", "Url": "https://archives.tarnetgaronne.fr/", "Type": "Archives Départementales", "Desc": "Fonds numérisés et généalogie en Tarn-et-Garonne."},
    {"Nom": "83 - Var", "Url": "https://archives.var.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil, recensements et registres de l'amirauté du Var."},
    {"Nom": "84 - Vaucluse", "Url": "https://archives.vaucluse.fr/", "Type": "Archives Départementales", "Desc": "Fonds pontificaux d'Avignon et état civil du Vaucluse."},
    {"Nom": "85 - Vendée", "Url": "https://archives.vendee.fr/", "Type": "Archives Départementales", "Desc": "Fonds très riches sur les Guerres de Vendée et l'état civil du 85."},
    {"Nom": "86 - Vienne", "Url": "https://archives.vienne86.fr/", "Type": "Archives Départementales", "Desc": "Recherches généalogiques et historiques dans la Vienne."},
    {"Nom": "87 - Haute-Vienne", "Url": "https://archives.haute-vienne.fr/", "Type": "Archives Départementales", "Desc": "Registres d'état civil, de matricules et cadastre du Limousin (87)."},
    {"Nom": "88 - Vosges", "Url": "https://archives.vosges.fr/", "Type": "Archives Départementales", "Desc": "Fonds numérisés, état civil et documents militaires des Vosges."},
    {"Nom": "89 - Yonne", "Url": "https://archives89.fr/", "Type": "Archives Départementales", "Desc": "État civil, registres paroissiaux et cadastre napoléonien de l'Yonne."},
    {"Nom": "90 - Territoire de Belfort", "Url": "https://archives.territoiredebelfort.fr/", "Type": "Archives Départementales", "Desc": "Histoire locale et état civil du plus petit département hors IDF."},
    {"Nom": "91 - Essonne", "Url": "https://archives.essonne.fr/", "Type": "Archives Départementales", "Desc": "Fonds numérisés d'état civil de l'Essonne."},
    {"Nom": "92 - Hauts-de-Seine", "Url": "https://archives.hautsdeseine.fr/", "Type": "Archives Départementales", "Desc": "Histoire de la proche banlieue parisienne et état civil."},
    {"Nom": "93 - Seine-Saint-Denis", "Url": "https://archives.seinesaintdenis.fr/", "Type": "Archives Départementales", "Desc": "Fonds d'histoire contemporaine, industrielle et état civil."},
    {"Nom": "94 - Val-de-Marne", "Url": "https://archives.valdemarne.fr/", "Type": "Archives Départementales", "Desc": "Documents généalogiques et cadastre du Val-de-Marne."},
    {"Nom": "95 - Val-d'Oise", "Url": "https://archives.valdoise.fr/", "Type": "Archives Départementales", "Desc": "Registres paroissiaux, état civil et cartes anciennes du Val-d'Oise."}
]

genealogie_data = [
    {"Nom": "Filae", "Url": "https://www.filae.com", "Type": "Généalogie", "Desc": "Moteur de recherche majeur pour la généalogie française avec transcription d'actes."},
    {"Nom": "Geneanet", "Url": "https://www.geneanet.org", "Type": "Généalogie", "Desc": "Première communauté généalogique en Europe. Arbres en ligne, base collaborative et documents."},
    {"Nom": "FamilySearch", "Url": "https://www.familysearch.org", "Type": "Généalogie", "Desc": "Immense base de données mondiale et gratuite gérée par les Mormons."},
    {"Nom": "Géoportail", "Url": "https://www.geoportail.gouv.fr", "Type": "Généalogie", "Desc": "Cartes anciennes, plans de Cassini et évolution des territoires français."},
    {"Nom": "BNE (Bibliothèque Nationale Européenne)", "Url": "https://www.europeana.eu", "Type": "Généalogie", "Desc": "Accès aux collections culturelles et historiques numérisées d'Europe."},
    {"Nom": "Gallica (BnF)", "Url": "https://gallica.bnf.fr", "Type": "Généalogie", "Desc": "Bibliothèque numérique de la BnF : journaux locaux, armoriaux et biographies anciennes."}
]

militaire_data = [
    {"Nom": "Mémoire des Hommes", "Url": "https://www.memoiredeshommes.sga.defense.gouv.fr/", "Type": "Militaire", "Desc": "Base officielle des morts pour la France (WW1, WW2, Indochine, Algérie)."},
    {"Nom": "Grand Mémorial", "Url": "https://www.culture.fr/Grand-Memorial", "Type": "Militaire", "Desc": "Base nationale des registres matricules des soldats de la Grande Guerre."},
    {"Nom": "Base Léonore", "Url": "https://www.archives-nationales.culture.gouv.fr/leonore/", "Type": "Militaire", "Desc": "Dossiers des membres nominatifs de la Légion d'honneur depuis 1802."},
    {"Nom": "Service Historique de la Défense (SHD)", "Url": "https://www.servicehistorique.sga.defense.gouv.fr/", "Type": "Militaire", "Desc": "Centre d'archives officiel des armées françaises (Terre, Marine, Air)."},
    {"Nom": "Les Morts pour la France (Geneanet)", "Url": "https://www.geneanet.org/militaires/", "Type": "Militaire", "Desc": "Indexation collaborative de monuments aux morts et de registres militaires."}
]

# Fusion de toutes les listes
all_links = archives_data + genealogie_data + militaire_data
df = pd.DataFrame(all_links)

# ==========================================
# 3. INTERFACE DE L'APPLICATION (SIDEBAR & MAIN)
# ==========================================

# Barre latérale (Sidebar) - Filtres & À propos
with st.sidebar:
    st.markdown("<h2 style='margin-top:0;'>📜 Navigation</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Filtre par catégorie principale
    categories = ["Tous les liens", "Archives Départementales", "Généalogie", "Militaire"]
    selected_category = st.radio("Sélectionner un univers :", categories)
    
    st.markdown("---")
    st.markdown("### À propos")
    st.markdown(
        "Cette interface regroupe l'accès direct aux **83+ plateformes d'archives** départementales "
        "françaises ainsi qu'aux portails de recherche généalogique et militaire majeurs."
    )
    st.markdown("<p style='color:#8C8781; font-size:0.8rem;'>Inspiré du design minimaliste de Claude AI.</p>", unsafe_allow_html=True)

# Contenu principal
st.markdown("<h1 style='font-size: 2.2rem; margin-bottom: 5px;'>Portail d'Archives & Généalogie</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6B6661; font-size: 1.1rem; margin-bottom: 30px;'>Accédez instantanément aux sources historiques et registres numérisés.</p>", unsafe_allow_html=True)

# Barre de recherche globale style Claude
search_query = st.text_input("🔍 Rechercher un département, un pays, un outil (ex: 44, Filae, Marne...)", "")

# Application des filtres de recherche et de catégorie
filtered_df = df.copy()

if selected_category != "Tous les liens":
    filtered_df = filtered_df[filtered_df["Type"] == selected_category]

if search_query:
    filtered_df = filtered_df[
        filtered_df["Nom"].str.contains(search_query, case=False, na=False) |
        filtered_df["Desc"].str.contains(search_query, case=False, na=False)
    ]

# Affichage des résultats sous forme de grille de cartes
if not filtered_df.empty:
    st.markdown(f"<p style='color: #8C8781; font-size: 0.9rem; margin-bottom: 20px;'>{len(filtered_df)} résultat(s) trouvé(s)</p>", unsafe_allow_html=True)
    
    # Diviser l'affichage en 2 colonnes pour une grille fluide
    col1, col2 = st.columns(2)
    
    for idx, row in filtered_df.reset_index().iterrows():
        # Détermination de la classe CSS du badge selon le type
        badge_class = "badge-archive"
        if row["Type"] == "Généalogie":
            badge_class = "badge-genealogie"
        elif row["Type"] == "Militaire":
            badge_class = "badge-militaire"
            
        # Structure HTML de la carte
        card_html = f"""
        <div class="link-card">
            <span class="badge {badge_class}">{row['Type']}</span><br/>
            <a href="{row['Url']}" target="_blank" class="card-title-link">{row['Nom']} ↗</a>
            <div class="card-desc">{row['Desc']}</div>
        </div>
        """
        
        # Distribution alternée dans les colonnes
        if idx % 2 == 0:
            col1.markdown(card_html, unsafe_allow_html=True)
        else:
            col2.markdown(card_html, unsafe_allow_html=True)
else:
    st.info("Aucun lien ne correspond à votre recherche actuelle. Essayez d'autres mots-clés.")
