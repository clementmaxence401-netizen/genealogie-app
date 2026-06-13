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
        background-color: #F7F2EB !important;
        font-family: 'Inter', sans-serif;
        color: #2C1F0E;
    }
    [data-testid="stSidebar"] {
        background-color: #EDE5D8 !important;
        border-right: 1px solid #D4C4AC;
    }
    [data-testid="stSidebar"] * { color: #4A3520 !important; }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #1A0F05 !important;
        font-family: 'IM Fell English', serif !important;
    }
    .stRadio label, .stMultiSelect label, .stCheckbox label {
        color: #5A4030 !important;
        font-size: 0.88rem !important;
    }
    h1, h2, h3 { color: #1A0F05 !important; }
    .stMarkdown p { color: #4A3520; }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #FFF8EE 0%, #F0E6D2 60%, #E8D8BC 100%);
        border: 1px solid #C8AD8A;
        border-radius: 18px;
        padding: 44px 52px;
        margin-bottom: 32px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(139,90,40,0.10);
    }
    .hero::before {
        content: "❧";
        position: absolute;
        right: 44px;
        top: 16px;
        font-size: 7rem;
        color: rgba(180,130,70,0.18);
        line-height: 1;
    }
    .hero-title {
        font-family: 'IM Fell English', serif;
        font-size: 2.8rem;
        color: #1A0F05;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }
    .hero-sub {
        color: #7A5A38;
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.03em;
    }
    .hero-stats {
        display: flex;
        gap: 36px;
        margin-top: 28px;
        flex-wrap: wrap;
    }
    .hero-stat {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    .hero-stat-num {
        font-family: 'IM Fell English', serif;
        font-size: 2.2rem;
        color: #B86A0A;
        line-height: 1;
    }
    .hero-stat-label {
        font-size: 0.72rem;
        color: #9A7A55;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Barre de recherche */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        border: 1.5px solid #C8AD8A !important;
        border-radius: 10px !important;
        color: #2C1F0E !important;
        font-size: 0.95rem !important;
        padding: 12px 16px !important;
        box-shadow: 0 1px 4px rgba(139,90,40,0.06) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #B86A0A !important;
        box-shadow: 0 0 0 2px rgba(184,106,10,0.15) !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: #B89A70 !important; }

    /* Compteur résultats */
    .result-count {
        color: #9A7A55;
        font-size: 0.85rem;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* Cartes */
    .link-card {
        background-color: #FFFFFF;
        border: 1px solid #DDD0BA;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 14px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.15s ease;
        position: relative;
        box-shadow: 0 1px 4px rgba(139,90,40,0.05);
    }
    .link-card:hover {
        border-color: #B86A0A;
        box-shadow: 0 6px 20px rgba(139,90,40,0.12);
        transform: translateY(-2px);
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
        border-radius: 5px;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
    }
    .badge-archive { background-color: #DDEEFF; color: #1A5F8A; border: 1px solid #AACCE8; }
    .badge-genealogie { background-color: #DDFAEB; color: #1A6B40; border: 1px solid #AADFC4; }
    .badge-militaire { background-color: #F5E6FF; color: #6B1A8A; border: 1px solid #D4AAEE; }
    .badge-domtom { background-color: #FFF3D6; color: #8A5800; border: 1px solid #EED888; }

    /* Badges tarif — effet tampon */
    .badge-free {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 5px;
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: transparent;
        border: 2px solid #2A8A4A;
        color: #2A8A4A;
        transform: rotate(-1.2deg);
        box-shadow: 1px 1px 0 rgba(42,138,74,0.2);
    }
    .badge-paid {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 5px;
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: transparent;
        border: 2px solid #C05000;
        color: #C05000;
        transform: rotate(-1.2deg);
        box-shadow: 1px 1px 0 rgba(192,80,0,0.2);
    }
    .badge-freemium {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 5px;
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        background: transparent;
        border: 2px solid #8A6A1A;
        color: #8A6A1A;
        transform: rotate(-1.2deg);
        box-shadow: 1px 1px 0 rgba(138,106,26,0.2);
    }

    /* Tags documents */
    .doc-tag {
        display: inline-block;
        padding: 2px 9px;
        border-radius: 4px;
        font-size: 0.68rem;
        background: #F4EEE4;
        border: 1px solid #DDD0BA;
        color: #7A5A38;
        margin-right: 3px;
        margin-bottom: 3px;
    }

    .card-title-link {
        font-family: 'IM Fell English', serif;
        font-size: 1.15rem;
        font-weight: 400;
        color: #1A0F05;
        text-decoration: none;
        display: block;
        margin-bottom: 6px;
        line-height: 1.3;
    }
    .card-title-link:hover { color: #B86A0A; }

    .card-desc {
        color: #7A6050;
        font-size: 0.84rem;
        line-height: 1.55;
        margin-top: 4px;
    }
    .card-docs {
        margin-top: 10px;
        display: flex;
        flex-wrap: wrap;
        gap: 3px;
    }

    /* Multiselect tags */
    [data-testid="stMultiSelect"] > div > div {
        background-color: #FFFFFF !important;
        border-color: #C8AD8A !important;
        color: #2C1F0E !important;
    }
    span[data-baseweb="tag"] {
        background-color: #F0E6D2 !important;
        color: #4A3520 !important;
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

def ad(num, nom, url, docs, desc, domtom=False):
    return {
        "Nom": f"{num} - {nom}",
        "Url": url,
        "Type": "Archives Départementales",
        "Sous-type": "DOM-TOM" if domtom else "Métropole",
        "Tarif": "Gratuit",
        "Docs": docs,
        "Desc": desc,
    }

EC = "État civil"
RP = "Registres paroissiaux"
RM = "Registres militaires"
CA = "Cadastre"
RE = "Recensements"
NO = "Notaires"
PA = "Presse ancienne"
PC = "Photos/Cartes"
AG = "Arbres généalogiques"
LH = "Légion d'honneur"

archives_data = [
    ad("01","Ain","https://archives.ain.fr/",[EC,RP,RM,RE],"Registres paroissiaux, état civil, recensements et matricules de l'Ain."),
    ad("02","Aisne","https://archives.aisne.fr/",[EC,RP,CA],"Archives numérisées du département de l'Aisne."),
    ad("03","Allier","https://archives.allier.fr/",[EC,CA,RM],"Généalogie, cartes et plans, archives judiciaires de l'Allier."),
    ad("04","Alpes-de-Haute-Provence","https://www.archives04.fr/",[EC,RP],"État civil et archives numérisées du 04."),
    ad("05","Hautes-Alpes","https://archives.hautes-alpes.fr/",[EC,RP],"Fonds documentaires des Hautes-Alpes."),
    ad("06","Alpes-Maritimes","https://www.departement06.fr/les-archives-departementales-2850.html",[EC,CA,RM],"État civil, cadastre et archives militaires des Alpes-Maritimes."),
    ad("07","Ardèche","https://archives.ardeche.fr/",[EC,RP,CA],"Histoire locale et généalogie en Ardèche."),
    ad("08","Ardennes","https://archives.cd08.fr/",[EC,RP],"Fonds numérisés des Ardennes."),
    ad("09","Ariège","https://archives.ariege.fr/",[EC,RP],"Recherches généalogiques en Ariège."),
    ad("10","Aube","https://archives-aube.fr/",[EC,RP,CA],"État civil, registres paroissiaux et cadastre de l'Aube."),
    ad("11","Aude","https://archivesdepartementales.aude.fr/",[EC,RP,CA],"Fonds numérisés et histoire de l'Aude."),
    ad("12","Aveyron","https://archives.aveyron.fr/",[EC,RP,RE],"Généalogie, recensements et documents de l'Aveyron."),
    ad("13","Bouches-du-Rhône","https://www.archives13.fr/",[EC,RP,CA,RE,NO],"Grandes collections de Marseille, Aix-en-Provence et des Bouches-du-Rhône."),
    ad("14","Calvados","https://archives.calvados.fr/",[EC,RP,RM],"Fonds normands, état civil et histoire du Calvados."),
    ad("15","Cantal","https://archives.cantal.fr/",[EC,RP],"Archives numérisées du Cantal."),
    ad("16","Charente","https://archives.lacharente.fr/",[EC,RP,NO],"Registres paroissiaux et archives notariales de la Charente."),
    ad("17","Charente-Maritime","https://archives.charente-maritime.fr/",[EC,RP,RM],"Histoire maritime et état civil de la Charente-Maritime."),
    ad("18","Cher","https://www.archives18.fr/",[EC,RP,CA],"Généalogie et cadastre du Cher."),
    ad("19","Corrèze","https://www.archives.correze.fr/",[EC,RM,CA],"État civil, militaires et cadastre de la Corrèze."),
    ad("2A","Corse-du-Sud","https://archives.isula.corsica/",[EC,RP],"Histoire et généalogie de la Corse-du-Sud."),
    ad("2B","Haute-Corse","https://archives.isula.corsica/",[EC,RP],"Fonds d'archives de la Haute-Corse."),
    ad("21","Côte-d'Or","https://archives.cotedor.fr/",[EC,RP,CA],"Fonds ducaux de Bourgogne et état civil de la Côte-d'Or."),
    ad("22","Côtes-d'Armor","https://archives.cotesdarmor.fr/",[EC,RP],"Généalogie bretonne et histoire des Côtes-d'Armor."),
    ad("23","Creuse","https://archives.creuse.fr/",[EC,RP],"Registres de la Creuse, dont les archives des maçons migrants."),
    ad("24","Dordogne","https://archives.dordogne.fr/",[EC,RP,NO,CA],"Riches fonds du Périgord, état civil et archives notariales."),
    ad("25","Doubs","https://archives.doubs.fr/",[EC,RP,RM],"Généalogie en Franche-Comté (Doubs)."),
    ad("26","Drôme","https://archives.ladrome.fr/",[EC,RP,CA],"Fonds numérisés de la Drôme."),
    ad("27","Eure","https://archives.eure.fr/",[EC,RP,RM,CA],"État civil, matricules militaires et plans de l'Eure."),
    ad("28","Eure-et-Loir","https://archives28.fr/",[EC,RP],"Généalogie et histoire locale d'Eure-et-Loir."),
    ad("29","Finistère","https://archives.finistere.fr/",[EC,RP,RM],"Généalogie maritime et registres du Finistère."),
    ad("30","Gard","https://archives.gard.fr/",[EC,RP,CA],"Fonds protestants, état civil et histoire du Gard."),
    ad("31","Haute-Garonne","https://archives.hautegaronne.fr/",[EC,RP,RM],"État civil de Toulouse et de la Haute-Garonne."),
    ad("32","Gers","https://www.archives32.fr/",[EC,RP,CA],"Histoire de la Gascogne et cadastre du Gers."),
    ad("33","Gironde","https://archives.gironde.fr/",[EC,NO,RM],"Fonds de Bordeaux, commerce maritime et état civil."),
    ad("34","Hérault","https://archives-pierresvives.herault.fr/",[EC,CA,RE],"Espace Pierresvives, archives numérisées de l'Hérault."),
    ad("35","Ille-et-Vilaine","https://archives.ille-et-vilaine.fr/",[EC,RP],"Fonds d'état civil de Rennes et d'Ille-et-Vilaine."),
    ad("36","Indre","https://www.archives36.fr/",[EC,RP],"Registres paroissiaux et état civil de l'Indre."),
    ad("37","Indre-et-Loire","https://archives.touraine.fr/",[EC,RP,CA],"Histoire de la Touraine et des châteaux de la Loire."),
    ad("38","Isère","https://archives.isere.fr/",[EC,RM,CA],"Fonds du Dauphiné, état civil et matricules de l'Isère."),
    ad("39","Jura","https://archives.jura.fr/",[EC,RP],"Archives d'état civil du Jura."),
    ad("40","Landes","https://archives.landes.fr/",[EC,RP,CA],"Histoire de la Chalosse et état civil des Landes."),
    ad("41","Loir-et-Cher","https://archives.culture41.fr/",[EC,RP],"Fonds généalogiques du Loir-et-Cher."),
    ad("42","Loire","https://www.archives42.fr/",[EC,RP,RE],"État civil, recensements du Forez et de la Loire."),
    ad("43","Haute-Loire","https://www.archives43.fr/",[EC,RP],"Archives numérisées de la Haute-Loire."),
    ad("44","Loire-Atlantique","https://archives.loire-atlantique.fr/",[EC,RP,NO,RM],"Fonds nantais, état civil et archives maritimes."),
    ad("45","Loiret","https://archives-loiret.fr/",[EC,RP,CA],"Histoire de l'Orléanais et généalogie du Loiret."),
    ad("46","Lot","https://archives.lot.fr/",[EC,RP,CA,NO],"Cadastre, état civil et archives notariales du Lot."),
    ad("47","Lot-et-Garonne","https://www.archives47.fr/",[EC,RP],"Fonds numérisés du Lot-et-Garonne."),
    ad("48","Lozère","https://archives.lozere.fr/",[EC,RP],"Généalogie du Gévaudan (Lozère)."),
    ad("49","Maine-et-Loire","https://www.archives49.fr/",[EC,RP,CA],"Fonds d'Anjou et état civil du Maine-et-Loire."),
    ad("50","Manche","https://archives.manche.fr/",[EC,RP,RM],"Fonds normands et état civil de la Manche."),
    ad("51","Marne","https://archives.marne.fr/",[EC,RP,CA],"Histoire de la Champagne et état civil de la Marne."),
    ad("52","Haute-Marne","https://archives.haute-marne.fr/",[EC,RP],"Généalogie et fonds de la Haute-Marne."),
    ad("53","Mayenne","https://archives.lamayenne.fr/",[EC,RP,CA,PC],"État civil, cartes et plans de la Mayenne."),
    ad("54","Meurthe-et-Moselle","https://archives.meurthe-et-moselle.fr/",[EC,RP,RM],"Fonds lorrains et registres militaires du 54."),
    ad("55","Meuse","https://archives.meuse.fr/",[EC,RP,RM],"Histoire de la Grande Guerre et état civil de la Meuse."),
    ad("56","Morbihan","https://archives.morbihan.fr/",[EC,RP,RM],"Généalogie bretonne et amirauté du Morbihan."),
    ad("57","Moselle","https://archives57.com/",[EC,RP],"Fonds spécifiques d'Alsace-Moselle."),
    ad("58","Nièvre","https://archives.nievre.fr/",[EC,RP,CA],"Histoire locale et état civil de la Nièvre."),
    ad("59","Nord","https://archivesdepartementales.lenord.fr/",[EC,RP,CA,RE,RM],"L'un des plus grands fonds de France (Flandres, Hainaut, Lille)."),
    ad("60","Oise","https://archives.oise.fr/",[EC,RP,CA],"État civil et plans d'intendance de l'Oise."),
    ad("61","Orne","https://archives.orne.fr/",[EC,RP,RM],"Généalogie normande de l'Orne."),
    ad("62","Pas-de-Calais","https://archivespasdecalais.fr/",[EC,RP,RM,CA],"État civil et archives de reconstruction du Pas-de-Calais."),
    ad("63","Puy-de-Dôme","https://www.archives-puy-dedome.fr/",[EC,RP,RM],"Fonds auvergnats et matricules militaires du 63."),
    ad("64","Pyrénées-Atlantiques","https://le64.fr/les-archives-departementales",[EC,RP,CA],"Histoire du Béarn et du Pays Basque."),
    ad("65","Hautes-Pyrénées","https://www.archives65.fr/",[EC,RP],"Fonds pyrénéens et état civil des Hautes-Pyrénées."),
    ad("66","Pyrénées-Orientales","https://archives.ledepartement66.fr/",[EC,RP,CA],"Histoire du Roussillon et archives catalanes."),
    ad("67","Bas-Rhin (Alsace)","https://archives.alsace.eu/",[EC,RP,CA],"Fonds de la Collectivité européenne d'Alsace (Strasbourg)."),
    ad("68","Haut-Rhin (Alsace)","https://archives.alsace.eu/",[EC,RP],"Fonds de la Collectivité européenne d'Alsace (Colmar)."),
    ad("69","Rhône & Métropole de Lyon","https://archives.rhone.fr/",[EC,RP,RE],"Fonds lyonnais, état civil et hospices."),
    ad("70","Haute-Saône","https://archives.haute-saone.fr/",[EC,RP],"Fonds comtois de la Haute-Saône."),
    ad("71","Saône-et-Loire","https://archives71.fr/",[EC,RP,CA],"État civil et cadastre de Saône-et-Loire."),
    ad("72","Sarthe","https://archives.sarthe.fr/",[EC,RP,CA,RE],"Registres du Maine et de la Sarthe."),
    ad("73","Savoie","https://www.archives-savoie.fr/",[EC,RP,CA],"Fonds uniques du Duché de Savoie."),
    ad("74","Haute-Savoie","https://archives.hautesavoie.fr/",[EC,RP,CA],"Cadastre sarde et état civil de la Haute-Savoie."),
    ad("75","Paris","https://archives.paris.fr/",[EC,RM,CA,RE],"État civil reconstitué, matricules et cadastre de Paris."),
    ad("76","Seine-Maritime","https://www.archivesdepartementales76.net/",[EC,RP,NO],"Fonds de Rouen, du Havre et de la Seine-Maritime."),
    ad("77","Seine-et-Marne","https://archives.seine-et-marne.fr/",[EC,RP,CA],"État civil et documents de Seine-et-Marne."),
    ad("78","Yvelines","https://archives.yvelines.fr/",[EC,RP,CA],"Histoire de Versailles et de l'ancien Seine-et-Oise."),
    ad("79","Deux-Sèvres","https://archives.deux-sevres.fr/",[EC,RP,CA],"État civil et plans des Deux-Sèvres."),
    ad("80","Somme","https://archives.somme.fr/",[EC,RM,RE],"Registres matricules, état civil et fonds de la Grande Guerre."),
    ad("81","Tarn","https://archives.tarn.fr/",[EC,RP,CA],"Histoire de l'Albigeois et compoix du Tarn."),
    ad("82","Tarn-et-Garonne","https://archives.tarnetgaronne.fr/",[EC,RP],"Fonds numérisés du Tarn-et-Garonne."),
    ad("83","Var","https://archives.var.fr/",[EC,RP,RM,RE],"État civil, recensements et amirauté du Var."),
    ad("84","Vaucluse","https://archives.vaucluse.fr/",[EC,RP,NO],"Fonds pontificaux d'Avignon et état civil du Vaucluse."),
    ad("85","Vendée","https://archives.vendee.fr/",[EC,RP,RM],"Fonds sur les Guerres de Vendée et état civil."),
    ad("86","Vienne","https://archives.vienne86.fr/",[EC,RP,CA],"Généalogie et histoire dans la Vienne."),
    ad("87","Haute-Vienne","https://archives.haute-vienne.fr/",[EC,RM,CA],"État civil, matricules et cadastre du Limousin."),
    ad("88","Vosges","https://archives.vosges.fr/",[EC,RP,RM],"Fonds numérisés et militaires des Vosges."),
    ad("89","Yonne","https://archives89.fr/",[EC,RP,CA],"État civil et cadastre napoléonien de l'Yonne."),
    ad("90","Territoire de Belfort","https://archives.territoiredebelfort.fr/",[EC,RP],"Histoire du plus petit département hors IDF."),
    ad("91","Essonne","https://archives.essonne.fr/",[EC,RP,CA],"Fonds numérisés d'état civil de l'Essonne."),
    ad("92","Hauts-de-Seine","https://archives.hautsdeseine.fr/",[EC,RP,RE],"Histoire de la proche banlieue parisienne."),
    ad("93","Seine-Saint-Denis","https://archives.seinesaintdenis.fr/",[EC,RP],"Fonds industriels et état civil de Seine-Saint-Denis."),
    ad("94","Val-de-Marne","https://archives.valdemarne.fr/",[EC,RP,CA],"Documents généalogiques et cadastre du Val-de-Marne."),
    ad("95","Val-d'Oise","https://archives.valdoise.fr/",[EC,RP,PC],"Registres paroissiaux et cartes anciennes du Val-d'Oise."),
    # DOM-TOM
    ad("971","Guadeloupe","https://archives.guadeloupe.fr/",[EC,RP,RM],"État civil, registres paroissiaux et archives de l'habitation en Guadeloupe.", domtom=True),
    ad("972","Martinique","https://archives.martinique.fr/",[EC,RP,NO],"Fonds coloniaux, notaires et état civil de la Martinique.", domtom=True),
    ad("973","Guyane","https://archives.guyane.fr/",[EC,RP],"Archives numérisées et état civil de la Guyane française.", domtom=True),
    ad("974","La Réunion","https://archives.reunion.fr/",[EC,RP,CA],"État civil, registres paroissiaux et cadastre de La Réunion.", domtom=True),
    ad("976","Mayotte","https://archives.mayotte.fr/",[EC],"Archives d'état civil et fonds historiques de Mayotte.", domtom=True),
    ad("975","Saint-Pierre-et-Miquelon","https://www.collectivite-saint-pierre-et-miquelon.fr/",[EC,RP],"Archives et état civil de Saint-Pierre-et-Miquelon.", domtom=True),
    ad("977","Saint-Barthélemy","https://www.comite-saint-barths.com/",[EC],"Ressources généalogiques de Saint-Barthélemy.", domtom=True),
    ad("978","Saint-Martin","https://www.com-saint-martin.fr/",[EC],"Archives et état civil de Saint-Martin.", domtom=True),
    ad("987","Polynésie française","https://www.archives.gov.pf/",[EC,RP,CA],"Archives territoriales et état civil de la Polynésie française.", domtom=True),
    ad("988","Nouvelle-Calédonie","https://archives.gouv.nc/",[EC,RP,CA],"Archives de la Nouvelle-Calédonie, cadastre et état civil.", domtom=True),
    ad("986","Wallis-et-Futuna","https://www.wallis-et-futuna.fr/",[EC],"État civil et fonds historiques de Wallis-et-Futuna.", domtom=True),
]

genealogie_data = [
    {"Nom": "Geneanet", "Url": "https://www.geneanet.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Freemium", "Docs": [AG,EC,PA], "Desc": "Première communauté généalogique en Europe. Arbres en ligne et base collaborative."},
    {"Nom": "FamilySearch", "Url": "https://www.familysearch.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG,EC,RP], "Desc": "Immense base de données mondiale et gratuite gérée par les Mormons."},
    {"Nom": "Gallica (BnF)", "Url": "https://gallica.bnf.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [PA,PC], "Desc": "Bibliothèque numérique de la BnF : journaux locaux, armoriaux et biographies anciennes."},
    {"Nom": "Géoportail", "Url": "https://www.geoportail.gouv.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [CA,PC], "Desc": "Cartes anciennes, plans de Cassini et évolution des territoires français."},
    {"Nom": "Europeana", "Url": "https://www.europeana.eu", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [PC,PA], "Desc": "Collections culturelles et historiques numérisées d'Europe."},
    {"Nom": "MyHeritage", "Url": "https://www.myheritage.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Freemium", "Docs": [AG,EC], "Desc": "Plateforme internationale avec colorisation photo et recherche ADN."},
    {"Nom": "Filae", "Url": "https://www.filae.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Freemium", "Docs": [EC,RP], "Desc": "Moteur de recherche majeur pour la généalogie française, transcription d'actes."},
    {"Nom": "Ancestry", "Url": "https://www.ancestry.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Payant", "Docs": [AG,EC,RP,RM], "Desc": "La plus grande base de données généalogique mondiale avec milliards d'entrées."},
    {"Nom": "Racines & Histoire", "Url": "http://racineshistoire.free.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG], "Desc": "Encyclopédie des noms de famille et des origines des familles françaises."},
    {"Nom": "Cercle Généalogique de Bretagne", "Url": "https://www.cgb-bretagne.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Relevés et base de données pour la Bretagne historique."},
    {"Nom": "Généalogie Alsace", "Url": "https://www.genealogie-alsace.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Index et relevés spécialisés pour les familles alsaciennes."},
    {"Nom": "GeneaFrance", "Url": "https://geneafrance.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG,EC], "Desc": "Annuaire des ressources généalogiques françaises en ligne."},
    {"Nom": "Généanet Relevés", "Url": "https://gw.geneanet.org/releves", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Index bénévoles de registres paroissiaux et d'état civil."},
    {"Nom": "1789-1815.com", "Url": "https://www.1789-1815.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM], "Desc": "Base des soldats des guerres révolutionnaires et napoléoniennes."},
    {"Nom": "Find A Grave", "Url": "https://www.findagrave.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,PC], "Desc": "Base mondiale de sépultures avec photos de tombes et liens familiaux."},
    {"Nom": "BillionGraves", "Url": "https://billiongraves.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC], "Desc": "Indexation communautaire de cimetières du monde entier."},
    {"Nom": "WikiTree", "Url": "https://www.wikitree.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG], "Desc": "Arbre généalogique mondial collaboratif et entièrement gratuit."},
    {"Nom": "Geni", "Url": "https://www.geni.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Freemium", "Docs": [AG], "Desc": "Projet d'arbre mondial unique : relier vos ancêtres à tous les autres."},
    {"Nom": "Rodovid", "Url": "https://fr.rodovid.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG], "Desc": "Wiki généalogique multilingue et participatif."},
    {"Nom": "WeRelate", "Url": "https://www.werelate.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG,EC], "Desc": "Wiki généalogique gratuit hébergé par la Bibliothèque publique de l'Utah."},
    {"Nom": "The Peerage", "Url": "https://www.thepeerage.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG], "Desc": "Base de données des familles nobles et pairs d'Europe."},
    {"Nom": "Arolsen Archives", "Url": "https://arolsen-archives.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC], "Desc": "Archives mondiales sur les victimes du nazisme."},
    {"Nom": "Find My Past", "Url": "https://www.findmypast.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Payant", "Docs": [EC,RP,RM], "Desc": "Spécialisé Grande-Bretagne, Irlande et archives coloniales françaises."},
    {"Nom": "Find A Grave (France)", "Url": "https://fr.findagrave.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,PC], "Desc": "Version francophone de Find A Grave, cimetières de France."},
    {"Nom": "RetroNews (BnF)", "Url": "https://www.retronews.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Freemium", "Docs": [PA], "Desc": "Presse ancienne numérisée par la BnF : 600+ titres de 1631 à 1952."},
    {"Nom": "Persée", "Url": "https://www.persee.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [PA], "Desc": "Bibliothèque numérique de revues scientifiques françaises en sciences humaines."},
    {"Nom": "Google Books", "Url": "https://books.google.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [PA], "Desc": "Millions d'ouvrages anciens numérisés : almanachs, annuaires, biographies."},
    {"Nom": "Openarchives.eu", "Url": "https://www.openarchives.eu", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Portail européen agrégeant de nombreux fonds d'archives numérisées."},
    {"Nom": "Généalogie & Histoire de la Caraïbe", "Url": "https://www.ghcaraibe.org", "Type": "Généalogie", "Sous-type": "DOM-TOM", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Relevés et ressources pour les DOM-TOM et les Antilles françaises."},
    {"Nom": "Ressources du Québec", "Url": "https://www.genealogie.qc.ca", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Fédération québécoise des sociétés de généalogie."},
    {"Nom": "PRDH-IGD (Québec)", "Url": "https://www.prdh-igd.com", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Freemium", "Docs": [EC,RP], "Desc": "Démographie historique, familles du Québec ancien."},
    {"Nom": "Généanet Cartes Postales", "Url": "https://cp.geneanet.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [PC], "Desc": "Plus d'un million de cartes postales anciennes de communes françaises."},
    {"Nom": "Ancestris (logiciel)", "Url": "https://ancestris.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG], "Desc": "Logiciel généalogique open-source français, compatible GEDCOM."},
    {"Nom": "Gramps (logiciel)", "Url": "https://gramps-project.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [AG], "Desc": "Logiciel généalogique libre, puissant et multiplateforme."},
    {"Nom": "MemorialGenWeb", "Url": "https://www.memorialgenweb.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM,PC], "Desc": "Photos et relevés de tous les monuments aux morts de France."},
    {"Nom": "CGO - Cercle Généalogique de l'Ouest", "Url": "https://www.cgo.asso.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Relevés et recherches pour l'Anjou, le Maine et la Touraine."},
    {"Nom": "Cercle Généalogique du Languedoc", "Url": "https://www.cgl-montpellier.org", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Relevés et index pour le Languedoc et l'Hérault."},
    {"Nom": "Association Généalogique du Pas-de-Calais", "Url": "https://www.agpc.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Relevés bénévoles pour le Pas-de-Calais et le Nord."},
    {"Nom": "Corel (Normandie)", "Url": "https://www.corel-genealogie.fr", "Type": "Généalogie", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [EC,RP], "Desc": "Cercles de recherche généalogique normands."},
]

militaire_data = [
    {"Nom": "Mémoire des Hommes", "Url": "https://www.memoiredeshommes.sga.defense.gouv.fr/", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM,EC], "Desc": "Base officielle des morts pour la France (WW1, WW2, Indochine, Algérie)."},
    {"Nom": "Grand Mémorial", "Url": "https://www.culture.fr/Grand-Memorial", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM], "Desc": "Base nationale des registres matricules des soldats de la Grande Guerre."},
    {"Nom": "Base Léonore", "Url": "https://www.archives-nationales.culture.gouv.fr/leonore/", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [LH], "Desc": "Dossiers des membres de la Légion d'honneur depuis 1802."},
    {"Nom": "Service Historique de la Défense (SHD)", "Url": "https://www.servicehistorique.sga.defense.gouv.fr/", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM], "Desc": "Centre d'archives officiel des armées françaises (Terre, Marine, Air)."},
    {"Nom": "Les Morts pour la France (Geneanet)", "Url": "https://www.geneanet.org/militaires/", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM,EC], "Desc": "Indexation collaborative de monuments aux morts et registres militaires."},
    {"Nom": "Commonwealth War Graves (CWGC)", "Url": "https://www.cwgc.org", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM], "Desc": "1,7 million de soldats du Commonwealth dont soldats enterrés en France."},
    {"Nom": "Fold3 (archives militaires US)", "Url": "https://www.fold3.com", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Payant", "Docs": [RM], "Desc": "Archives militaires américaines numérisées, pension rolls et dossiers."},
    {"Nom": "1789-1815.com", "Url": "https://www.1789-1815.com", "Type": "Militaire", "Sous-type": "Métropole", "Tarif": "Gratuit", "Docs": [RM], "Desc": "Base des soldats des guerres révolutionnaires et napoléoniennes."},
]

all_links = archives_data + genealogie_data + militaire_data
df = pd.DataFrame(all_links)

# ==========================================
# INTERFACE
# ==========================================

with st.sidebar:
    st.markdown("<h2 style='margin-top:0; font-family: IM Fell English, serif; color:#1A0F05;'>📜 Filtres</h2>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 🗂️ Univers")
    categories = ["Tous", "Archives Départementales", "Généalogie", "Militaire"]
    selected_category = st.radio("", categories, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🌍 Territoire")
    sous_types = ["Tous", "Métropole", "DOM-TOM"]
    selected_sous_type = st.radio("", sous_types, label_visibility="collapsed", key="sous_type")

    st.markdown("---")
    st.markdown("### 💰 Accès")
    tarif_options = st.multiselect(
        "",
        ["Gratuit", "Freemium", "Payant"],
        default=["Gratuit", "Freemium", "Payant"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📄 Types de documents")
    all_doc_types = list(DOC_TYPES.keys())
    selected_docs = st.multiselect(
        "",
        all_doc_types,
        default=[],
        placeholder="Tous les types",
        label_visibility="collapsed"
    )

    st.markdown("---")
    total_all = len(df)
    free_all = len(df[df["Tarif"] == "Gratuit"])
    st.markdown(
        f"<p style='font-size:0.8rem; color:#7A6050;'>{total_all} sources indexées dont {free_all} gratuites.</p>",
        unsafe_allow_html=True
    )

# Hero
total = len(df)
free_count = len(df[df["Tarif"] == "Gratuit"])
depart_count = len([x for x in all_links if x["Type"] == "Archives Départementales"])
domtom_count = len([x for x in all_links if x.get("Sous-type") == "DOM-TOM"])

st.markdown(f"""
<div class="hero">
    <p class="hero-title">Portail Archives & Généalogie</p>
    <p class="hero-sub">Sources primaires, registres numérisés et outils de recherche familiale · France métropolitaine & outre-mer</p>
    <div class="hero-stats">
        <div class="hero-stat">
            <span class="hero-stat-num">{total}</span>
            <span class="hero-stat-label">Sources indexées</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">{free_count}</span>
            <span class="hero-stat-label">Gratuites</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">{depart_count}</span>
            <span class="hero-stat-label">Archives dép.</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-num">{domtom_count}</span>
            <span class="hero-stat-label">Depts DOM-TOM</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Recherche
search_query = st.text_input("", placeholder="🔍  Rechercher… département, outil, type de document (ex : 971, Guadeloupe, matricule, notaires)", label_visibility="collapsed")

# Filtrage
filtered_df = df.copy()

if selected_category != "Tous":
    filtered_df = filtered_df[filtered_df["Type"] == selected_category]

if selected_sous_type != "Tous":
    filtered_df = filtered_df[filtered_df["Sous-type"] == selected_sous_type]

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

st.markdown(f"<p class='result-count'>{len(filtered_df)} source(s) trouvée(s)</p>", unsafe_allow_html=True)

if not filtered_df.empty:
    col1, col2 = st.columns(2, gap="medium")

    for idx, row in filtered_df.reset_index(drop=True).iterrows():
        badge_class = "badge-archive"
        if row["Type"] == "Généalogie":
            badge_class = "badge-genealogie"
        elif row["Type"] == "Militaire":
            badge_class = "badge-militaire"

        is_domtom = row.get("Sous-type") == "DOM-TOM"

        tarif_class = "badge-free"
        tarif_label = "✓ Gratuit"
        if row["Tarif"] == "Payant":
            tarif_class = "badge-paid"
            tarif_label = "Payant"
        elif row["Tarif"] == "Freemium":
            tarif_class = "badge-freemium"
            tarif_label = "Freemium"

        domtom_badge = '<span class="badge badge-domtom">DOM-TOM</span>' if is_domtom else ""

        docs_html = "".join([
            f'<span class="doc-tag">{DOC_TYPES.get(d, "📄")} {d}</span>'
            for d in row["Docs"]
        ])

        card_html = f"""
        <div class="link-card">
            <div class="card-badges">
                <span class="badge {badge_class}">{row['Type']}</span>
                {domtom_badge}
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
    <div style='text-align:center; padding: 60px 20px; color: #9A7A55; background:#FFF8EE; border-radius:14px; border:1px solid #DDD0BA;'>
        <div style='font-size: 2.5rem; margin-bottom: 12px;'>☍</div>
        <p style='font-family: IM Fell English, serif; font-size: 1.2rem; color: #7A5A38;'>Aucune source ne correspond à vos critères.</p>
        <p style='font-size: 0.85rem;'>Essayez d'élargir les filtres ou de modifier votre recherche.</p>
    </div>
    """, unsafe_allow_html=True)
