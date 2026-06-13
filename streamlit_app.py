import streamlit as st
import pandas as pd

# ==========================================
# 1. CONFIGURATION DE LA PAGE & STYLE "CLAUDE"
# ==========================================
st.set_page_config(
    page_title="Portail Archives & Généalogie",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS pour l'identité visuelle de Claude AI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FBF9F6 !important;
        font-family: 'Inter', sans-serif;
        color: #191919;
    }
    
    [data-testid="stSidebar"] {
        background-color: #F3EFEA !important;
        border-right: 1px solid #E6DFD5;
    }
    
    h1, h2, h3 {
        color: #191919 !important;
        font-weight: 500 !important;
    }
    
    /* Cartes de liens */
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
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 10px;
        margin-right: 5px;
    }
    .badge-archive { background-color: #E8F4F8; color: #1D657F; }
    .badge-genealogie { background-color: #EBF7ED; color: #2A6635; }
    .badge-militaire { background-color: #FDF3E7; color: #8F4E00; }
    .badge-international { background-color: #F3E8FF; color: #6B21A8; }
    
    /* Badge de Pays */
    .badge-country {
        background-color: #EAE5DC;
        color: #4A4641;
    }
    
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF;
        border: 1px solid #D4C9B9 !important;
        border-radius: 8px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #191919 !important;
        box-shadow: 0 0 0 1px #191919 !important;
    }
    
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
# 2. BASE DE DONNÉES ENRICHIE
# ==========================================

france_data = [
    # --- Archives Départementales (01 à 95) ---
    {"Nom": "01 - Ain", "Url": "https://archives.ain.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres paroissiaux, d'état civil, recensements et registres matricules de l'Ain."},
    {"Nom": "02 - Aisne", "Url": "https://archives.aisne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Accès en ligne aux archives numérisées du département de l'Aisne."},
    {"Nom": "03 - Allier", "Url": "https://archives.allier.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie, cartes et plans, archives judiciaires de l'Allier."},
    {"Nom": "04 - Alpes-de-Haute-Provence", "Url": "https://www.archives04.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Consultation de l'état civil et des archives numérisées du 04."},
    {"Nom": "05 - Hautes-Alpes", "Url": "https://archives.hautes-alpes.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds documentaires et historiques des Hautes-Alpes."},
    {"Nom": "06 - Alpes-Maritimes", "Url": "https://www.departement06.fr/les-archives-departementales-2850.html", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil, plans cadastral et archives militaires."},
    {"Nom": "07 - Ardèche", "Url": "https://archives.ardeche.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire locale et généalogie en Ardèche."},
    {"Nom": "08 - Ardennes", "Url": "https://archives.cd08.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Accès aux fonds numérisés du département des Ardennes."},
    {"Nom": "09 - Ariège", "Url": "https://archives.ariege.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Recherches généalogiques et historiques en Ariège."},
    {"Nom": "10 - Aube", "Url": "https://archives-aube.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil, registres paroissiaux et cadastre de l'Aube."},
    {"Nom": "11 - Aude", "Url": "https://archivesdepartementales.aude.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds numérisés et histoire du département de l'Aude."},
    {"Nom": "12 - Aveyron", "Url": "https://archives.aveyron.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie, recensements et documents de l'Aveyron."},
    {"Nom": "13 - Bouches-du-Rhône", "Url": "https://www.archives13.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Grandes collections de Marseille, Aix-en-Provence et des Bouches-du-Rhône."},
    {"Nom": "14 - Calvados", "Url": "https://archives.calvados.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds normands, état civil et histoire locale du Calvados."},
    {"Nom": "15 - Cantal", "Url": "https://archives.cantal.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Archives numérisées et histoire des familles du Cantal."},
    {"Nom": "16 - Charente", "Url": "https://archives.lacharente.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres paroissiaux, état civil et archives notariales."},
    {"Nom": "17 - Charente-Maritime", "Url": "https://archives.charente-maritime.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire maritime, état civil et documents officiels de la Charente-Maritime."},
    {"Nom": "18 - Cher", "Url": "https://www.archives18.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Recherches généalogiques et cadastre du département du Cher."},
    {"Nom": "19 - Corrèze", "Url": "https://www.archives.correze.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds d'état civil, militaires et cadastre de la Corrèze."},
    {"Nom": "2A - Corse-du-Sud", "Url": "https://archives.isula.corsica/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire et généalogie de la Corse-du-Sud."},
    {"Nom": "2B - Haute-Corse", "Url": "https://archives.isula.corsica/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds d'archives et documents d'état civil de la Haute-Corse."},
    {"Nom": "21 - Côte-d'Or", "Url": "https://archives.cotedor.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds ducaux de Bourgogne et état civil de la Côte-d'Or."},
    {"Nom": "22 - Côtes-d'Armor", "Url": "https://archives.cotesdarmor.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie bretonne et histoire locale des Côtes-d'Armor."},
    {"Nom": "23 - Creuse", "Url": "https://archives.creuse.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres paroissiaux, d'état civil et registres de maçons de la Creuse."},
    {"Nom": "24 - Dordogne", "Url": "https://archives.dordogne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Riches fonds du Périgord, état civil et archives notariales."},
    {"Nom": "25 - Doubs", "Url": "https://archives.doubs.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Recherches généalogiques en Franche-Comté (Doubs)."},
    {"Nom": "26 - Drôme", "Url": "https://archives.ladrome.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds numérisés et histoire des communes de la Drôme."},
    {"Nom": "27 - Eure", "Url": "https://archives.eure.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil, registres de matricules militaires et plans de l'Eure."},
    {"Nom": "28 - Eure-et-Loir", "Url": "https://archives28.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds d'histoire locale et de généalogie d'Eure-et-Loir."},
    {"Nom": "29 - Finistère", "Url": "https://archives.finistere.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie maritime, registres paroissiaux et d'état civil du Finistère."},
    {"Nom": "30 - Gard", "Url": "https://archives.gard.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds protestants, état civil et histoire du Gard."},
    {"Nom": "31 - Haute-Garonne", "Url": "https://archives.hautegaronne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil de Toulouse et de la Haute-Garonne."},
    {"Nom": "32 - Gers", "Url": "https://www.archives32.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de la Gascogne, registres paroissiaux et cadastre du Gers."},
    {"Nom": "33 - Gironde", "Url": "https://archives.gironde.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds de Bordeaux et de la Gironde, commerce maritime et état civil."},
    {"Nom": "34 - Hérault", "Url": "https://archives-pierresvives.herault.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Espace Pierresvives, archives numérisées de l'Hérault."},
    {"Nom": "35 - Ille-et-Vilaine", "Url": "https://archives.ille-et-vilaine.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds d'état civil de Rennes et du département d'Ille-et-Vilaine."},
    {"Nom": "36 - Indre", "Url": "https://www.archives36.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres paroissiaux et documents d'état civil de l'Indre."},
    {"Nom": "37 - Indre-et-Loire", "Url": "https://archives.touraine.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de la Touraine, châteaux de la Loire et état civil."},
    {"Nom": "38 - Isère", "Url": "https://archives.isere.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds du Dauphiné, état civil et registres matricules de l'Isère."},
    {"Nom": "39 - Jura", "Url": "https://archives.jura.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Archives d'état civil et fonds historiques du département du Jura."},
    {"Nom": "40 - Landes", "Url": "https://archives.landes.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de la Chalosse et des Landes, état civil en ligne."},
    {"Nom": "41 - Loir-et-Cher", "Url": "https://archives.culture41.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds historiques et généalogiques du Loir-et-Cher."},
    {"Nom": "42 - Loire", "Url": "https://www.archives42.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil, recensements et registres du Forez et de la Loire."},
    {"Nom": "43 - Haute-Loire", "Url": "https://www.archives43.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Recherches généalogiques et archives numérisées de la Haute-Loire."},
    {"Nom": "44 - Loire-Atlantique", "Url": "https://archives.loire-atlantique.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds nantais, état civil et archives maritimes du 44."},
    {"Nom": "45 - Loiret", "Url": "https://archives-loiret.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de l'Orléanais et documents généalogiques du Loiret."},
    {"Nom": "46 - Lot", "Url": "https://archives.lot.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Cadastre, état civil et archives notariales du Lot."},
    {"Nom": "47 - Lot-et-Garonne", "Url": "https://www.archives47.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds numérisés et documents d'histoire locale du Lot-et-Garonne."},
    {"Nom": "48 - Lozère", "Url": "https://archives.lozere.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie et histoire du Gévaudan (Lozère)."},
    {"Nom": "49 - Maine-et-Loire", "Url": "https://www.archives49.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds d'Anjou, registres paroissiaux et d'état civil du 49."},
    {"Nom": "50 - Manche", "Url": "https://archives.manche.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds normands, reconstruction et état civil de la Manche."},
    {"Nom": "51 - Marne", "Url": "https://archives.marne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de la Champagne, état civil et registres de la Marne."},
    {"Nom": "52 - Haute-Marne", "Url": "https://archives.haute-marne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie et documents numérisés de la Haute-Marne."},
    {"Nom": "53 - Mayenne", "Url": "https://archives.lamayenne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil, cartes et plans de la Mayenne."},
    {"Nom": "54 - Meurthe-et-Moselle", "Url": "https://archives.meurthe-et-moselle.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds lorrains, généalogie et registres militaires du 54."},
    {"Nom": "55 - Meuse", "Url": "https://archives.meuse.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de la Première Guerre mondiale et état civil de la Meuse."},
    {"Nom": "56 - Morbihan", "Url": "https://archives.morbihan.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie bretonne, état civil et amirauté du Morbihan."},
    {"Nom": "57 - Moselle", "Url": "https://archives57.com/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds spécifiques liés à l'histoire d'Alsace-Moselle."},
    {"Nom": "58 - Nièvre", "Url": "https://archives.nievre.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil et fonds d'histoire locale de la Nièvre."},
    {"Nom": "59 - Nord", "Url": "https://archivesdepartementales.lenord.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "L'un des plus grands fonds de France (Flandres, Hainaut, Lille)."},
    {"Nom": "60 - Oise", "Url": "https://archives.oise.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil, plans d'intendance et archives de l'Oise."},
    {"Nom": "61 - Orne", "Url": "https://archives.orne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Généalogie et documents historiques normands de l'Orne."},
    {"Nom": "62 - Pas-de-Calais", "Url": "https://archivespasdecalais.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil et archives de reconstruction du Pas-de-Calais."},
    {"Nom": "63 - Puy-de-Dôme", "Url": "https://www.archives-puy-dedome.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds auvergnats, état civil et matricules militaires du 63."},
    {"Nom": "64 - Pyrénées-Atlantiques", "Url": "https://le64.fr/les-archives-departementales", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire du Béarn et du Pays Basque, état civil en ligne."},
    {"Nom": "65 - Hautes-Pyrénées", "Url": "https://www.archives65.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds pyrénéens et état civil des Hautes-Pyrénées."},
    {"Nom": "66 - Pyrénées-Orientales", "Url": "https://archives.ledepartement66.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire du Roussillon, archives catalanes et état civil."},
    {"Nom": "67 - Bas-Rhin (Alsace)", "Url": "https://archives.alsace.eu/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds de la Collectivité européenne d'Alsace (Strasbourg)."},
    {"Nom": "68 - Haut-Rhin (Alsace)", "Url": "https://archives.alsace.eu/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds de la Collectivité européenne d'Alsace (Colmar)."},
    {"Nom": "69 - Rhône & Métropole de Lyon", "Url": "https://archives.rhone.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds lyonnais et du département du Rhône, état civil."},
    {"Nom": "70 - Haute-Saône", "Url": "https://archives.haute-saone.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Recherches généalogiques et fonds comtois du 70."},
    {"Nom": "71 - Saône-et-Loire", "Url": "https://archives71.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil, registres paroissiaux et cadastre de Saône-et-Loire."},
    {"Nom": "72 - Sarthe", "Url": "https://archives.sarthe.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil, recensements et plans du Maine/Sarthe."},
    {"Nom": "73 - Savoie", "Url": "https://www.archives-savoie.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds uniques de l'histoire du Duché de Savoie."},
    {"Nom": "74 - Haute-Savoie", "Url": "https://archives.hautesavoie.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Cadastre sarde, état civil et histoire de la Haute-Savoie."},
    {"Nom": "75 - Paris", "Url": "https://archives.paris.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil reconstitué, fiches de matricules et cadastre de Paris."},
    {"Nom": "76 - Seine-Maritime", "Url": "https://www.archivesdepartementales76.net/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds de Rouen, du Havre et de la Seine-Maritime."},
    {"Nom": "77 - Seine-et-Marne", "Url": "https://archives.seine-et-marne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil et documents d'histoire locale du 77."},
    {"Nom": "78 - Yvelines", "Url": "https://archives.yvelines.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de Versailles et de l'ancien département de Seine-et-Oise."},
    {"Nom": "79 - Deux-Sèvres", "Url": "https://archives.deux-sevres.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil, plans de communes et documents des Deux-Sèvres."},
    {"Nom": "80 - Somme", "Url": "https://archives.somme.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres matricules, état civil et fonds de la Grande Guerre."},
    {"Nom": "81 - Tarn", "Url": "https://archives.tarn.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de l'Albigeois, état civil et compoix du Tarn."},
    {"Nom": "82 - Tarn-et-Garonne", "Url": "https://archives.tarnetgaronne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds numérisés et généalogie en Tarn-et-Garonne."},
    {"Nom": "83 - Var", "Url": "https://archives.var.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil, recensements et registres de l'amirauté du Var."},
    {"Nom": "84 - Vaucluse", "Url": "https://archives.vaucluse.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds pontificaux d'Avignon et état civil du Vaucluse."},
    {"Nom": "85 - Vendée", "Url": "https://archives.vendee.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds très riches sur les Guerres de Vendée et l'état civil."},
    {"Nom": "86 - Vienne", "Url": "https://archives.vienne86.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Recherches généalogiques et historiques dans la Vienne."},
    {"Nom": "87 - Haute-Vienne", "Url": "https://archives.haute-vienne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres d'état civil, de matricules et cadastre du Limousin."},
    {"Nom": "88 - Vosges", "Url": "https://archives.vosges.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds numérisés, état civil et documents militaires des Vosges."},
    {"Nom": "89 - Yonne", "Url": "https://archives89.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "État civil, registres paroissiaux et cadastre napoléonien de l'Yonne."},
    {"Nom": "90 - Territoire de Belfort", "Url": "https://archives.territoiredebelfort.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire locale et état civil du plus petit département hors IDF."},
    {"Nom": "91 - Essonne", "Url": "https://archives.essonne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds numérisés d'état civil de l'Essonne."},
    {"Nom": "92 - Hauts-de-Seine", "Url": "https://archives.hautsdeseine.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Histoire de la proche banlieue parisienne et état civil."},
    {"Nom": "93 - Seine-Saint-Denis", "Url": "https://archives.seinesaintdenis.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Fonds d'histoire contemporaine, industrielle et état civil."},
    {"Nom": "94 - Val-de-Marne", "Url": "https://archives.valdemarne.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Documents généalogiques et cadastre du Val-de-Marne."},
    {"Nom": "95 - Val-d'Oise", "Url": "https://archives.valdoise.fr/", "Type": "Archives Départementales", "Pays": "France", "Desc": "Registres paroissiaux, état civil et cartes anciennes du Val-d'Oise."},
    
    # --- Portails Nationaux (Généalogie / Militaire) ---
    {"Nom": "Filae", "Url": "https://www.filae.com", "Type": "Généalogie", "Pays": "France", "Desc": "Moteur de recherche majeur pour la généalogie française avec transcription d'actes."},
    {"Nom": "Geneanet", "Url": "https://www.geneanet.org", "Type": "Généalogie", "Pays": "France", "Desc": "Première communauté généalogique en Europe. Arbres en ligne et base collaborative."},
    {"Nom": "Mémoire des Hommes", "Url": "https://www.memoiredeshommes.sga.defense.gouv.fr/", "Type": "Militaire", "Pays": "France", "Desc": "Base officielle des morts pour la France (Guerres mondiales, théâtres extérieurs)."},
    {"Nom": "Grand Mémorial", "Url": "https://www.culture.fr/Grand-Memorial", "Type": "Militaire", "Pays": "France", "Desc": "Registre matricule national des soldats de la Première Guerre mondiale."}
]

international_data = [
    # --- ALLEMAGNE ---
    {"Nom": "CompGen (Allemagne)", "Url": "https://www.compgen.de", "Type": "Généalogie", "Pays": "Allemagne", "Desc": "La plus grande association de généalogie en Allemagne. Bases de données massives et gratuites (Loss Lists WW1)."},
    {"Nom": "Archion (Allemagne)", "Url": "https://www.archion.de", "Type": "Généalogie", "Pays": "Allemagne", "Desc": "Portail majeur payant d'accès aux registres paroissiaux protestants (Evangelisch) d'Allemagne."},
    {"Nom": "Matricula Online", "Url": "https://data.matricula-online.eu", "Type": "Généalogie", "Pays": "Allemagne", "Desc": "Accès gratuit aux registres paroissiaux catholiques numérisés d'Allemagne, Autriche et pays limitrophes."},
    {"Nom": "Bundesarchiv (Archives Fédérales)", "Url": "https://www.bundesarchiv.de", "Type": "Militaire", "Pays": "Allemagne", "Desc": "Archives d'État allemandes, incluant les documents de l'histoire militaire centrale (anciennes archives de la Wehrmacht)."},

    # --- ITALIE ---
    {"Nom": "Antenati (Italie)", "Url": "https://www.antenati.san.beniculturali.it", "Type": "Généalogie", "Pays": "Italie", "Desc": "Portail officiel gratuit de l'État italien donnant accès aux registres d'état civil numérisés des archives d'État (Stato Civile)."},
    {"Nom": "Anagrafe Nazionale (ANPR)", "Url": "https://www.anagrafenazionale.interno.it", "Type": "Généalogie", "Pays": "Italie", "Desc": "Registre national de la population italienne actuelle et historique (accès restreint/démarches officielles)."},
    {"Nom": "CIAN (Archives Nationales Italiennes)", "Url": "https://www.archiviacentrali.it", "Type": "Archives Départementales", "Pays": "Italie", "Desc": "Portail d'accès aux documents historiques et aux conscriptions militaires régionales (Liste di Leva)."},

    # --- USA ---
    {"Nom": "NARA (National Archives USA)", "Url": "https://www.archives.gov", "Type": "Archives Départementales", "Pays": "USA", "Desc": "Archives nationales des États-Unis. Contient les recensements historiques, les dossiers d'immigration et militaires."},
    {"Nom": "Ancestry (USA / Mondial)", "Url": "https://www.ancestry.com", "Type": "Généalogie", "Pays": "USA", "Desc": "Le géant mondial de la généalogie. Incontournable pour l'immigration américaine, les recensements (Census) et les bases de données militaires."},
    {"Nom": "FamilySearch (Mondial)", "Url": "https://www.familysearch.org", "Type": "Généalogie", "Pays": "USA", "Desc": "Plateforme mondiale gratuite gérée par les USA avec d'immenses collections numérisées d'Amérique et d'Europe."},
    {"Nom": "Fold3 (Militaire USA)", "Url": "https://www.fold3.com", "Type": "Militaire", "Pays": "USA", "Desc": "Base de données spécialisée dans les archives militaires américaines (Guerre de Sécession, WW1, WW2). Publié par Ancestry."}
]

# Fusion complète de la base de données
all_links = france_data + international_data
df = pd.DataFrame(all_links)

# ==========================================
# 3. INTERFACE UTILISATEUR (SIDEBAR & FILTRES)
# ==========================================

with st.sidebar:
    st.markdown("<h2 style='margin-top:0;'>📜 Filtres de Recherche</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. Filtre par Pays
    list_pays = ["Tous les pays", "France", "Allemagne", "Italie", "USA"]
    selected_pays = st.selectbox("Sélectionner un pays :", list_pays)
    
    st.markdown("---")
    
    # 2. Filtre par Catégorie de document
    categories = ["Toutes les catégories", "Archives Départementales", "Généalogie", "Militaire"]
    selected_category = st.radio("Type de recherche :", categories)
    
    st.markdown("---")
    st.markdown("### À propos")
    st.markdown(
        "Ce portail hybride unifie les ressources locales françaises (01 à 95) "
        "et les grandes plateformes d'archives d'Europe et d'Amérique."
    )

# Zones de titres principales
st.markdown("<h1 style='font-size: 2.2rem; margin-bottom: 5px;'>Portail d'Archives Internationales</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #6B6661; font-size: 1.1rem; margin-bottom: 30px;'>Accès centralisé aux registres paroissiaux, militaires, civils et de l'immigration.</p>", unsafe_allow_html=True)

# Barre de recherche globale
search_query = st.text_input("🔍 Rechercher un outil, un numéro de département, un mot-clé (ex: Antenati, 75, Wehrmacht...)", "")

# ==========================================
# 4. LOGIQUE DE FILTRAGE DES DONNÉES
# ==========================================
filtered_df = df.copy()

# Filtrage par pays
if selected_pays != "Tous les pays":
    filtered_df = filtered_df[filtered_df["Pays"] == selected_pays]

# Filtrage par type
if selected_category != "Toutes les catégories":
    filtered_df = filtered_df[filtered_df["Type"] == selected_category]

# Filtrage par chaîne de caractères (moteur de recherche)
if search_query:
    filtered_df = filtered_df[
        filtered_df["Nom"].str.contains(search_query, case=False, na=False) |
        filtered_df["Desc"].str.contains(search_query, case=False, na=False) |
        filtered_df["Pays"].str.contains(search_query, case=False, na=False)
    ]

# ==========================================
# 5. AFFICHAGE DES RÉSULTATS (GRILLE CLAUDE)
# ==========================================
if not filtered_df.empty:
    st.markdown(f"<p style='color: #8C8781; font-size: 0.9rem; margin-bottom: 20px;'>{len(filtered_df)} résultat(s) trouvé(s)</p>", unsafe_allow_html=True)
    
    # Organisation en deux colonnes
    col1, col2 = st.columns(2)
    
    for idx, row in filtered_df.reset_index().iterrows():
        # Configuration dynamique des badges de type
        badge_class = "badge-archive"
        if row["Type"] == "Généalogie":
            badge_class = "badge-genealogie"
        elif row["Type"] == "Militaire":
            badge_class = "badge-militaire"
            
        # Code HTML de la carte
        card_html = f"""
        <div class="link-card">
            <span class="badge {badge_class}">{row['Type']}</span>
            <span class="badge badge-country">{row['Pays']}</span><br/>
            <a href="{row['Url']}" target="_blank" class="card-title-link">{row['Nom']} ↗</a>
            <div class="card-desc">{row['Desc']}</div>
        </div>
        """
        
        # Dispatching alterné
        if idx % 2 == 0:
            col1.markdown(card_html, unsafe_allow_html=True)
        else:
            col2.markdown(card_html, unsafe_allow_html=True)
else:
    st.info("Aucun résultat ne correspond à vos filtres ou à votre recherche.")
