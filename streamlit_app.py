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
        background-color: #FDFAF5 !important;
        font-family: 'Inter', sans-serif;
        color: #1E1208;
    }
    [data-testid="stSidebar"] {
        background-color: #F5EFE4 !important;
        border-right: 1.5px solid #D8C8AE;
    }
    [data-testid="stSidebar"] * { color: #3A2810 !important; }
    [data-testid="stSidebar"] h2 {
        color: #1E1208 !important;
        font-family: 'IM Fell English', serif !important;
        font-size: 1.4rem !important;
    }
    [data-testid="stSidebar"] h3 {
        color: #2E1A08 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .stRadio label { color: #4A3420 !important; font-size: 0.88rem !important; }
    .stMarkdown p { color: #4A3420; }

    /* Hero */
    .hero {
        background: linear-gradient(140deg, #FFFDF8 0%, #FFF3DC 45%, #FFE8BE 100%);
        border: 1.5px solid #E8C87A;
        border-radius: 20px;
        padding: 48px 56px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 6px 32px rgba(180,120,20,0.10), 0 1px 0 rgba(255,255,255,0.8) inset;
    }
    .hero::before {
        content: "❧";
        position: absolute;
        right: 48px; top: 10px;
        font-size: 8rem;
        color: rgba(200,150,40,0.12);
        line-height: 1;
    }
    .hero::after {
        content: "";
        position: absolute;
        left: 0; top: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #D4820A, #E8B840, #D4820A);
        border-radius: 20px 20px 0 0;
    }
    .hero-title {
        font-family: 'IM Fell English', serif;
        font-size: 3rem;
        color: #1E1208;
        margin: 0 0 10px 0;
        line-height: 1.15;
    }
    .hero-sub {
        color: #7A5520;
        font-size: 1rem;
        margin: 0;
        letter-spacing: 0.02em;
    }
    .hero-stats {
        display: flex; gap: 40px; margin-top: 32px; flex-wrap: wrap;
    }
    .hero-stat { display: flex; flex-direction: column; gap: 4px; }
    .hero-stat-num {
        font-family: 'IM Fell English', serif;
        font-size: 2.4rem;
        color: #B86A0A;
        line-height: 1;
    }
    .hero-stat-label {
        font-size: 0.7rem; color: #9A7040;
        text-transform: uppercase; letter-spacing: 0.1em;
    }

    /* Recherche */
    div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        border: 1.5px solid #D8C090 !important;
        border-radius: 12px !important;
        color: #1E1208 !important;
        font-size: 0.95rem !important;
        padding: 14px 18px !important;
        box-shadow: 0 2px 8px rgba(180,120,20,0.07) !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #B86A0A !important;
        box-shadow: 0 0 0 3px rgba(184,106,10,0.12) !important;
    }
    div[data-testid="stTextInput"] input::placeholder { color: #C0A060 !important; }

    /* Compteur */
    .result-count {
        color: #9A7040; font-size: 0.85rem;
        margin-bottom: 18px; font-style: italic;
    }

    /* Cartes */
    .link-card {
        background-color: #FFFFFF;
        border: 1.5px solid #E8DEC8;
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 14px;
        transition: border-color 0.18s, box-shadow 0.18s, transform 0.15s;
        box-shadow: 0 2px 8px rgba(180,120,20,0.06), 0 1px 0 rgba(255,255,255,0.9) inset;
    }
    .link-card:hover {
        border-color: #C8880A;
        box-shadow: 0 8px 28px rgba(180,120,20,0.14);
        transform: translateY(-2px);
    }
    .card-badges {
        display: flex; gap: 6px; flex-wrap: wrap;
        margin-bottom: 10px; align-items: center;
    }
    .badge {
        display: inline-block; padding: 3px 10px;
        border-radius: 5px; font-size: 0.67rem;
        font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em;
    }
    .badge-archive  { background:#E0F0FF; color:#1558A0; border:1px solid #B8D8F5; }
    .badge-genealogie { background:#E0FAF0; color:#126840; border:1px solid #A8E8CC; }
    .badge-militaire  { background:#F5E8FF; color:#6A1A90; border:1px solid #D8B8F0; }
    .badge-domtom   { background:#FFF6D0; color:#8A5800; border:1px solid #EECC60; }

    .badge-free {
        display:inline-block; padding:3px 10px; border-radius:5px;
        font-size:0.67rem; font-weight:800; text-transform:uppercase; letter-spacing:0.1em;
        background:transparent; border:2px solid #208A40; color:#208A40;
        transform:rotate(-1.2deg); box-shadow:1px 1px 0 rgba(32,138,64,0.18);
    }
    .badge-paid {
        display:inline-block; padding:3px 10px; border-radius:5px;
        font-size:0.67rem; font-weight:800; text-transform:uppercase; letter-spacing:0.1em;
        background:transparent; border:2px solid #B84000; color:#B84000;
        transform:rotate(-1.2deg); box-shadow:1px 1px 0 rgba(184,64,0,0.18);
    }
    .badge-freemium {
        display:inline-block; padding:3px 10px; border-radius:5px;
        font-size:0.67rem; font-weight:800; text-transform:uppercase; letter-spacing:0.1em;
        background:transparent; border:2px solid #9A6800; color:#9A6800;
        transform:rotate(-1.2deg); box-shadow:1px 1px 0 rgba(154,104,0,0.18);
    }
    .card-title-link {
        font-family: 'IM Fell English', serif;
        font-size: 1.12rem; font-weight:400;
        color: #1E1208; text-decoration:none;
        display:block; margin-bottom:6px; line-height:1.3;
    }
    .card-title-link:hover { color: #B86A0A; }
    .card-desc { color: #6A5030; font-size:0.84rem; line-height:1.55; }
    .card-docs { margin-top:10px; display:flex; flex-wrap:wrap; gap:4px; }
    .doc-tag {
        display:inline-block; padding:2px 9px; border-radius:4px;
        font-size:0.68rem; background:#FFF8EE; border:1px solid #E8D0A0; color:#8A6020;
    }

    /* Vide */
    .empty-state {
        text-align:center; padding:60px 20px;
        background:#FFFDF5; border-radius:16px; border:1.5px dashed #E8D0A0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# DONNÉES
# ==========================================
EC  = "État civil"
RP  = "Registres paroissiaux"
RM  = "Registres militaires"
CAD = "Cadastre"
REC = "Recensements"
NOT = "Notaires"
PA  = "Presse ancienne"
PC  = "Photos/Cartes"
AG  = "Arbres généalogiques"
LH  = "Légion d'honneur"

DOC_TYPES = {
    EC:"📋", RP:"⛪", RM:"⚔️", CAD:"🗺️", REC:"👥",
    NOT:"📝", PA:"📰", PC:"🖼️", AG:"🌳", LH:"🏅",
}

G  = "Gratuit"
FM = "Freemium"
PAY= "Payant"
MET= "Métropole"
DOM= "DOM-TOM"
AD = "Archives Départementales"

archives_data = [
    # ——— MÉTROPOLE 01-19 ———
    {"Nom":"01 - Ain","Url":"https://archives.ain.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,RM,REC],"Desc":"Registres paroissiaux, état civil, recensements et matricules de l'Ain."},
    {"Nom":"02 - Aisne","Url":"https://archives.aisne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,RM],"Desc":"Archives numérisées du département de l'Aisne."},
    {"Nom":"03 - Allier","Url":"https://archives.allier.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"Généalogie, cartes et plans, archives judiciaires de l'Allier."},
    {"Nom":"04 - Alpes-de-Haute-Provence","Url":"https://www.archives04.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Consultation de l'état civil et des archives numérisées du 04."},
    {"Nom":"05 - Hautes-Alpes","Url":"https://archives.hautes-alpes.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC],"Desc":"Fonds documentaires et historiques des Hautes-Alpes."},
    {"Nom":"06 - Alpes-Maritimes","Url":"https://www.departement06.fr/les-archives-departementales-2850.html","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD,RM],"Desc":"Registres d'état civil, plans cadastraux et archives militaires du 06."},
    {"Nom":"07 - Ardèche","Url":"https://archives.ardeche.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire locale et généalogie en Ardèche."},
    {"Nom":"08 - Ardennes","Url":"https://archives.cd08.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds numérisés du département des Ardennes."},
    {"Nom":"09 - Ariège","Url":"https://archives.ariege.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Recherches généalogiques et historiques en Ariège."},
    {"Nom":"10 - Aube","Url":"https://archives-aube.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,CAD],"Desc":"État civil, registres paroissiaux et cadastre de l'Aube."},
    {"Nom":"11 - Aude","Url":"https://archivesdepartementales.aude.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds numérisés et histoire du département de l'Aude."},
    {"Nom":"12 - Aveyron","Url":"https://archives.aveyron.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,REC],"Desc":"Généalogie, recensements et documents administratifs de l'Aveyron."},
    {"Nom":"13 - Bouches-du-Rhône","Url":"https://www.archives13.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,CAD,REC],"Desc":"Grandes collections de Marseille, Aix-en-Provence et des Bouches-du-Rhône."},
    {"Nom":"14 - Calvados","Url":"https://archives.calvados.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds normands, état civil et histoire locale du Calvados."},
    {"Nom":"15 - Cantal","Url":"https://archives.cantal.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Archives numérisées et histoire des familles du Cantal."},
    {"Nom":"16 - Charente","Url":"https://archives.lacharente.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,NOT],"Desc":"Registres paroissiaux, état civil et archives notariales de la Charente."},
    {"Nom":"17 - Charente-Maritime","Url":"https://archives.charente-maritime.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire maritime, état civil et documents de la Charente-Maritime."},
    {"Nom":"18 - Cher","Url":"https://www.archives18.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"Recherches généalogiques et cadastre du département du Cher."},
    {"Nom":"19 - Corrèze","Url":"https://www.archives.correze.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM,CAD],"Desc":"Fonds d'état civil, militaires et cadastre de la Corrèze."},
    # ——— CORSE ———
    {"Nom":"2A - Corse-du-Sud","Url":"https://archives.isula.corsica/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire et généalogie de la Corse-du-Sud (portail Isula)."},
    {"Nom":"2B - Haute-Corse","Url":"https://archives.isula.corsica/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds d'archives et d'état civil de la Haute-Corse (portail Isula)."},
    # ——— 21-49 ———
    {"Nom":"21 - Côte-d'Or","Url":"https://archives.cotedor.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds ducaux de Bourgogne et état civil de la Côte-d'Or."},
    {"Nom":"22 - Côtes-d'Armor","Url":"https://archives.cotesdarmor.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Généalogie bretonne et histoire locale des Côtes-d'Armor."},
    {"Nom":"23 - Creuse","Url":"https://archives.creuse.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Registres paroissiaux, état civil et registres des maçons de la Creuse."},
    {"Nom":"24 - Dordogne","Url":"https://archives.dordogne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,NOT],"Desc":"Riches fonds du Périgord, état civil et archives notariales."},
    {"Nom":"25 - Doubs","Url":"https://archives.doubs.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Recherches généalogiques en Franche-Comté (Doubs)."},
    {"Nom":"26 - Drôme","Url":"https://archives.ladrome.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds numérisés et histoire des communes de la Drôme."},
    {"Nom":"27 - Eure","Url":"https://archives.eure.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM],"Desc":"État civil, registres de matricules militaires et plans de l'Eure."},
    {"Nom":"28 - Eure-et-Loir","Url":"https://archives28.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds d'histoire locale et de généalogie d'Eure-et-Loir."},
    {"Nom":"29 - Finistère","Url":"https://archives.finistere.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Généalogie maritime, registres paroissiaux et d'état civil du Finistère."},
    {"Nom":"30 - Gard","Url":"https://archives.gard.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds protestants, état civil et histoire du Gard."},
    {"Nom":"31 - Haute-Garonne","Url":"https://archives.hautegaronne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,RM],"Desc":"Registres d'état civil de Toulouse et de la Haute-Garonne."},
    {"Nom":"32 - Gers","Url":"https://www.archives32.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,CAD],"Desc":"Histoire de la Gascogne, registres paroissiaux et cadastre du Gers."},
    {"Nom":"33 - Gironde","Url":"https://archives.gironde.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,NOT],"Desc":"Fonds de Bordeaux et de la Gironde, commerce maritime et état civil."},
    {"Nom":"34 - Hérault","Url":"https://archives-pierresvives.herault.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"Espace Pierresvives, archives numérisées de l'Hérault."},
    {"Nom":"35 - Ille-et-Vilaine","Url":"https://archives.ille-et-vilaine.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds d'état civil de Rennes et du département d'Ille-et-Vilaine."},
    {"Nom":"36 - Indre","Url":"https://www.archives36.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Registres paroissiaux et documents d'état civil de l'Indre."},
    {"Nom":"37 - Indre-et-Loire","Url":"https://archives.touraine.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire de la Touraine, châteaux de la Loire et état civil."},
    {"Nom":"38 - Isère","Url":"https://archives.isere.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM,CAD],"Desc":"Fonds du Dauphiné, état civil et registres matricules de l'Isère."},
    {"Nom":"39 - Jura","Url":"https://archives.jura.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Archives d'état civil et fonds historiques du département du Jura."},
    {"Nom":"40 - Landes","Url":"https://archives.landes.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire de la Chalosse et des Landes, état civil en ligne."},
    {"Nom":"41 - Loir-et-Cher","Url":"https://archives.culture41.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds historiques et généalogiques du Loir-et-Cher."},
    {"Nom":"42 - Loire","Url":"https://www.archives42.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,REC],"Desc":"État civil, recensements et registres du Forez et de la Loire."},
    {"Nom":"43 - Haute-Loire","Url":"https://www.archives43.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Recherches généalogiques et archives numérisées de la Haute-Loire."},
    {"Nom":"44 - Loire-Atlantique","Url":"https://archives.loire-atlantique.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,NOT],"Desc":"Fonds nantais, état civil et archives maritimes du 44."},
    {"Nom":"45 - Loiret","Url":"https://archives-loiret.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire de l'Orléanais et documents généalogiques du Loiret."},
    {"Nom":"46 - Lot","Url":"https://archives.lot.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD,NOT],"Desc":"Cadastre, état civil et archives notariales du Lot."},
    {"Nom":"47 - Lot-et-Garonne","Url":"https://www.archives47.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds numérisés et documents d'histoire locale du Lot-et-Garonne."},
    {"Nom":"48 - Lozère","Url":"https://archives.lozere.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Généalogie et histoire du Gévaudan (Lozère)."},
    {"Nom":"49 - Maine-et-Loire","Url":"https://www.archives49.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds d'Anjou, registres paroissiaux et d'état civil du 49."},
    # ——— 50-76 ———
    {"Nom":"50 - Manche","Url":"https://archives.manche.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds normands, reconstruction et état civil de la Manche."},
    {"Nom":"51 - Marne","Url":"https://archives.marne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire de la Champagne, état civil et registres de la Marne."},
    {"Nom":"52 - Haute-Marne","Url":"https://archives.haute-marne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Généalogie et documents numérisés de la Haute-Marne."},
    {"Nom":"53 - Mayenne","Url":"https://archives.lamayenne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"Registres d'état civil, cartes et plans de la Mayenne."},
    {"Nom":"54 - Meurthe-et-Moselle","Url":"https://archives.meurthe-et-moselle.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,RM],"Desc":"Fonds lorrains, généalogie et registres militaires du 54."},
    {"Nom":"55 - Meuse","Url":"https://archives.meuse.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM],"Desc":"Histoire de la Première Guerre mondiale et état civil de la Meuse."},
    {"Nom":"56 - Morbihan","Url":"https://archives.morbihan.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Généalogie bretonne, état civil et amirauté du Morbihan."},
    {"Nom":"57 - Moselle","Url":"https://archives57.com/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds spécifiques liés à l'histoire d'Alsace-Moselle."},
    {"Nom":"58 - Nièvre","Url":"https://archives.nievre.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Registres d'état civil et fonds d'histoire locale de la Nièvre."},
    {"Nom":"59 - Nord","Url":"https://archivesdepartementales.lenord.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,CAD,REC],"Desc":"L'un des plus grands fonds de France (Flandres, Hainaut, Lille)."},
    {"Nom":"60 - Oise","Url":"https://archives.oise.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"État civil, plans d'intendance et archives de l'Oise."},
    {"Nom":"61 - Orne","Url":"https://archives.orne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Généalogie et documents historiques normands de l'Orne."},
    {"Nom":"62 - Pas-de-Calais","Url":"https://archivespasdecalais.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM],"Desc":"Registres d'état civil et archives de reconstruction du Pas-de-Calais."},
    {"Nom":"63 - Puy-de-Dôme","Url":"https://www.archives-puy-dedome.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM],"Desc":"Fonds auvergnats, état civil et matricules militaires du 63."},
    {"Nom":"64 - Pyrénées-Atlantiques","Url":"https://le64.fr/les-archives-departementales","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire du Béarn et du Pays Basque, état civil en ligne."},
    {"Nom":"65 - Hautes-Pyrénées","Url":"https://www.archives65.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds pyrénéens et état civil des Hautes-Pyrénées."},
    {"Nom":"66 - Pyrénées-Orientales","Url":"https://archives.ledepartement66.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire du Roussillon, archives catalanes et état civil."},
    {"Nom":"67 - Bas-Rhin (Alsace)","Url":"https://archives.alsace.eu/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds de la Collectivité européenne d'Alsace (Strasbourg)."},
    {"Nom":"68 - Haut-Rhin (Alsace)","Url":"https://archives.alsace.eu/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds de la Collectivité européenne d'Alsace (Colmar)."},
    {"Nom":"69 - Rhône","Url":"https://archives.rhone.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,REC],"Desc":"Fonds lyonnais et du département du Rhône, état civil et hospices civils."},
    {"Nom":"70 - Haute-Saône","Url":"https://archives.haute-saone.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Recherches généalogiques et fonds comtois du 70."},
    {"Nom":"71 - Saône-et-Loire","Url":"https://archives71.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,CAD],"Desc":"État civil, registres paroissiaux et cadastre de Saône-et-Loire."},
    {"Nom":"72 - Sarthe","Url":"https://archives.sarthe.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,REC],"Desc":"Registres d'état civil, recensements et plans du Maine/Sarthe."},
    {"Nom":"73 - Savoie","Url":"https://www.archives-savoie.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds uniques de l'histoire du Duché de Savoie."},
    {"Nom":"74 - Haute-Savoie","Url":"https://archives.hautesavoie.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"Cadastre sarde, état civil et histoire de la Haute-Savoie."},
    {"Nom":"75 - Paris","Url":"https://archives.paris.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM,CAD],"Desc":"État civil reconstitué, fiches de matricules et cadastre de Paris."},
    {"Nom":"76 - Seine-Maritime","Url":"https://www.archivesdepartementales76.net/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds de Rouen, du Havre et de la Seine-Maritime."},
    # ——— 77-95 ———
    {"Nom":"77 - Seine-et-Marne","Url":"https://archives.seine-et-marne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Registres d'état civil et documents d'histoire locale du 77."},
    {"Nom":"78 - Yvelines","Url":"https://archives.yvelines.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"Histoire de Versailles et de l'ancien département de Seine-et-Oise."},
    {"Nom":"79 - Deux-Sèvres","Url":"https://archives.deux-sevres.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"État civil, plans de communes et documents des Deux-Sèvres."},
    {"Nom":"80 - Somme","Url":"https://archives.somme.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM],"Desc":"Registres matricules, état civil et fonds de la Grande Guerre."},
    {"Nom":"81 - Tarn","Url":"https://archives.tarn.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire de l'Albigeois, état civil et compoix du Tarn."},
    {"Nom":"82 - Tarn-et-Garonne","Url":"https://archives.tarnetgaronne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds numérisés et généalogie en Tarn-et-Garonne."},
    {"Nom":"83 - Var","Url":"https://archives.var.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,REC],"Desc":"Registres d'état civil, recensements et amirauté du Var."},
    {"Nom":"84 - Vaucluse","Url":"https://archives.vaucluse.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds pontificaux d'Avignon et état civil du Vaucluse."},
    {"Nom":"85 - Vendée","Url":"https://archives.vendee.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds très riches sur les Guerres de Vendée et l'état civil du 85."},
    {"Nom":"86 - Vienne","Url":"https://archives.vienne86.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Recherches généalogiques et historiques dans la Vienne."},
    {"Nom":"87 - Haute-Vienne","Url":"https://archives.haute-vienne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM,CAD],"Desc":"Registres d'état civil, de matricules et cadastre du Limousin (87)."},
    {"Nom":"88 - Vosges","Url":"https://archives.vosges.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RM],"Desc":"Fonds numérisés, état civil et documents militaires des Vosges."},
    {"Nom":"89 - Yonne","Url":"https://archives89.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,CAD],"Desc":"État civil, registres paroissiaux et cadastre napoléonien de l'Yonne."},
    {"Nom":"90 - Territoire de Belfort","Url":"https://archives.territoiredebelfort.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire locale et état civil du plus petit département français."},
    {"Nom":"91 - Essonne","Url":"https://archives.essonne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds numérisés d'état civil de l'Essonne."},
    {"Nom":"92 - Hauts-de-Seine","Url":"https://archives.hautsdeseine.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Histoire de la proche banlieue parisienne et état civil."},
    {"Nom":"93 - Seine-Saint-Denis","Url":"https://archives.seinesaintdenis.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fonds d'histoire contemporaine, industrielle et état civil."},
    {"Nom":"94 - Val-de-Marne","Url":"https://archives.valdemarne.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,CAD],"Desc":"Documents généalogiques et cadastre du Val-de-Marne."},
    {"Nom":"95 - Val-d'Oise","Url":"https://archives.valdoise.fr/","Type":AD,"Sous-type":MET,"Tarif":G,"Docs":[EC,RP,CAD],"Desc":"Registres paroissiaux, état civil et cartes anciennes du Val-d'Oise."},
    # ——— DOM-TOM ———
    {"Nom":"971 - Guadeloupe","Url":"https://archives.guadeloupe.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP,REC],"Desc":"Archives de la Guadeloupe : état civil, registres paroissiaux et recensements d'esclaves."},
    {"Nom":"972 - Martinique","Url":"https://archives.martinique.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP,REC],"Desc":"Archives de la Martinique : registres coloniaux, état civil et documents d'esclavage."},
    {"Nom":"973 - Guyane","Url":"https://archives.guyane.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP],"Desc":"Archives de la Guyane : état civil, bagne et documents coloniaux."},
    {"Nom":"974 - La Réunion","Url":"https://archives.regionreunion.com/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP,REC],"Desc":"Archives de La Réunion : état civil, registres de l'engagisme et recensements."},
    {"Nom":"976 - Mayotte","Url":"https://archives.mayotte.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP],"Desc":"Archives départementales de Mayotte : état civil et fonds coloniaux."},
    {"Nom":"Saint-Pierre-et-Miquelon","Url":"https://archives.saint-pierre-et-miquelon.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP],"Desc":"Archives de Saint-Pierre-et-Miquelon : registres paroissiaux et état civil."},
    {"Nom":"Nouvelle-Calédonie (ANOM)","Url":"https://anom.archivesnationales.culture.gouv.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP,REC],"Desc":"Archives Nationales d'Outre-Mer (ANOM) : fonds de Nouvelle-Calédonie, Polynésie et îles."},
    {"Nom":"Polynésie française","Url":"https://archives.gov.pf/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP],"Desc":"Archives de la Polynésie française : état civil, registres de Papeete et îles."},
    {"Nom":"Saint-Martin / Saint-Barthélemy","Url":"https://anom.archivesnationales.culture.gouv.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP],"Desc":"Documents de Saint-Martin et Saint-Barthélemy via l'ANOM."},
    {"Nom":"Wallis-et-Futuna","Url":"https://anom.archivesnationales.culture.gouv.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP],"Desc":"Archives de Wallis-et-Futuna via le portail ANOM."},
    {"Nom":"ANOM - Archives Nationales d'Outre-Mer","Url":"https://anom.archivesnationales.culture.gouv.fr/","Type":AD,"Sous-type":DOM,"Tarif":G,"Docs":[EC,RP,REC,NOT],"Desc":"Portail central de tous les fonds coloniaux français : Antilles, Afrique, Indochine, Océanie."},
]

genealogie_data = [
    {"Nom":"Geneanet","Url":"https://www.geneanet.org","Type":"Généalogie","Sous-type":MET,"Tarif":FM,"Docs":[AG,EC,PA],"Desc":"Première communauté généalogique en Europe. Arbres en ligne, base collaborative et documents."},
    {"Nom":"FamilySearch","Url":"https://www.familysearch.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG,EC,RP],"Desc":"Immense base mondiale 100 % gratuite, gérée par l'Église des SdJ."},
    {"Nom":"MyHeritage","Url":"https://www.myheritage.fr","Type":"Généalogie","Sous-type":MET,"Tarif":FM,"Docs":[AG,EC],"Desc":"Plateforme internationale avec colorisation photo et recherche ADN."},
    {"Nom":"Filae","Url":"https://www.filae.com","Type":"Généalogie","Sous-type":MET,"Tarif":FM,"Docs":[EC,RP],"Desc":"Moteur de recherche majeur pour la généalogie française avec transcription d'actes."},
    {"Nom":"Gallica (BnF)","Url":"https://gallica.bnf.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[PA,PC],"Desc":"Bibliothèque numérique de la BnF : journaux locaux, armoriaux et biographies anciennes."},
    {"Nom":"RetroNews (BnF)","Url":"https://www.retronews.fr","Type":"Généalogie","Sous-type":MET,"Tarif":FM,"Docs":[PA],"Desc":"Presse ancienne numérisée par la BnF : plus de 600 titres de 1631 à 1952."},
    {"Nom":"Géoportail","Url":"https://www.geoportail.gouv.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[CAD,PC],"Desc":"Cartes anciennes, plans de Cassini et évolution des territoires français."},
    {"Nom":"Europeana","Url":"https://www.europeana.eu","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[PA,PC],"Desc":"Collections culturelles et historiques numérisées d'Europe."},
    {"Nom":"Généanet Relevés bénévoles","Url":"https://gw.geneanet.org/releves","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Index bénévoles des registres paroissiaux et d'état civil, communauté collaborative."},
    {"Nom":"WikiTree","Url":"https://www.wikitree.com","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG],"Desc":"Arbre généalogique mondial collaboratif et entièrement gratuit."},
    {"Nom":"Find A Grave","Url":"https://www.findagrave.com","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,PC],"Desc":"Base mondiale de sépultures avec photos de tombes et liens familiaux."},
    {"Nom":"BillionGraves","Url":"https://billiongraves.com","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC],"Desc":"Indexation communautaire de cimetières du monde entier via smartphones."},
    {"Nom":"Geni","Url":"https://www.geni.com","Type":"Généalogie","Sous-type":MET,"Tarif":FM,"Docs":[AG],"Desc":"Projet d'arbre mondial unique : reliez vos ancêtres à tous les autres."},
    {"Nom":"Rodovid","Url":"https://fr.rodovid.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG],"Desc":"Wiki généalogique multilingue et participatif."},
    {"Nom":"WeRelate","Url":"https://www.werelate.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG,EC],"Desc":"Wiki généalogique gratuit hébergé par la Bibliothèque publique de l'Utah."},
    {"Nom":"Généaologie.com","Url":"https://www.genealogie.com","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG],"Desc":"Portail généalogique francophone : arbres, entraide et forums."},
    {"Nom":"Persée","Url":"https://www.persee.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[PA],"Desc":"Bibliothèque numérique de revues scientifiques françaises en sciences humaines."},
    {"Nom":"Google Books","Url":"https://books.google.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[PA],"Desc":"Des millions d'ouvrages anciens numérisés, dont de nombreux almanachs et annuaires."},
    {"Nom":"1789-1815.com","Url":"https://www.1789-1815.com","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[RM],"Desc":"Base des soldats des guerres révolutionnaires et napoléoniennes."},
    {"Nom":"Arolsen Archives","Url":"https://arolsen-archives.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC],"Desc":"Archives mondiales sur les victimes du nazisme, recherches familiales."},
    {"Nom":"Immigrant Ships Transcribers Guild","Url":"https://www.immigrantships.net","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC],"Desc":"Listes de passagers de bateaux transatlantiques, utile pour l'émigration."},
    {"Nom":"The Peerage","Url":"https://www.thepeerage.com","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG],"Desc":"Base de données des familles nobles et pairs d'Europe."},
    {"Nom":"Racines & Histoire","Url":"http://racineshistoire.free.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG],"Desc":"Encyclopédie des noms de famille et des origines des familles françaises."},
    {"Nom":"MemorialGenWeb","Url":"https://www.memorialgenweb.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[RM,PC],"Desc":"Photos et relevés de tous les monuments aux morts de France."},
    {"Nom":"Généanet Cartes Postales","Url":"https://cp.geneanet.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[PC],"Desc":"Plus d'un million de cartes postales anciennes de communes françaises."},
    {"Nom":"Ancestris","Url":"https://ancestris.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG],"Desc":"Logiciel généalogique open-source français, compatible GEDCOM."},
    {"Nom":"Gramps","Url":"https://gramps-project.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[AG],"Desc":"Logiciel généalogique libre, puissant et multiplateforme."},
    {"Nom":"Openarchives.eu","Url":"https://www.openarchives.eu","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Portail européen agrégeant de nombreux fonds d'archives numérisées."},
    {"Nom":"PRDH-IGD (Québec)","Url":"https://www.prdh-igd.com","Type":"Généalogie","Sous-type":MET,"Tarif":FM,"Docs":[EC,RP],"Desc":"Programme de recherche en démographie historique, familles du Québec ancien."},
    {"Nom":"Ressources généalogiques Québec","Url":"https://www.genealogie.qc.ca","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fédération québécoise des sociétés de généalogie, ressources francophones."},
    {"Nom":"Système Loiselle","Url":"https://www.loiselle.ca","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[RP],"Desc":"Index des mariages catholiques du Québec par régions et paroisses."},
    {"Nom":"Généalogie & Histoire de la Caraïbe","Url":"https://www.ghcaraibe.org","Type":"Généalogie","Sous-type":DOM,"Tarif":G,"Docs":[EC,RP],"Desc":"Relevés et ressources pour les DOM-TOM et les Antilles françaises."},
    {"Nom":"Cercle Généalogique de Bretagne","Url":"https://www.cgb-bretagne.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Relevés et base de données pour la Bretagne historique."},
    {"Nom":"Géné@PACA","Url":"https://www.genea-paca.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Fédération des cercles de généalogie de la région PACA."},
    {"Nom":"Généalogie Alsace","Url":"https://www.genealogie-alsace.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Index et relevés spécialisés pour les familles alsaciennes."},
    {"Nom":"Cercle Généalogique du Languedoc","Url":"https://www.cgl-montpellier.org","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Relevés et index généalogiques pour le Languedoc et l'Hérault."},
    {"Nom":"Association Généalogique du Pas-de-Calais","Url":"https://www.agpc.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Relevés bénévoles pour le Pas-de-Calais et le Nord."},
    {"Nom":"CGO - Cercle Généalogique de l'Ouest","Url":"https://www.cgo.asso.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Relevés et recherches pour l'Anjou, le Maine et la Touraine."},
    {"Nom":"Corel (Normandie)","Url":"https://www.corel-genealogie.fr","Type":"Généalogie","Sous-type":MET,"Tarif":G,"Docs":[EC,RP],"Desc":"Cercles de recherche généalogique normands."},
]

militaire_data = [
    {"Nom":"Mémoire des Hommes","Url":"https://www.memoiredeshommes.sga.defense.gouv.fr/","Type":"Militaire","Sous-type":MET,"Tarif":G,"Docs":[RM,EC],"Desc":"Base officielle des morts pour la France (WW1, WW2, Indochine, Algérie)."},
    {"Nom":"Grand Mémorial","Url":"https://www.culture.fr/Grand-Memorial","Type":"Militaire","Sous-type":MET,"Tarif":G,"Docs":[RM],"Desc":"Base nationale des registres matricules des soldats de la Grande Guerre."},
    {"Nom":"Base Léonore","Url":"https://www.archives-nationales.culture.gouv.fr/leonore/","Type":"Militaire","Sous-type":MET,"Tarif":G,"Docs":[LH],"Desc":"Dossiers des membres de la Légion d'honneur depuis 1802."},
    {"Nom":"Service Historique de la Défense (SHD)","Url":"https://www.servicehistorique.sga.defense.gouv.fr/","Type":"Militaire","Sous-type":MET,"Tarif":G,"Docs":[RM],"Desc":"Centre d'archives officiel des armées françaises (Terre, Marine, Air)."},
    {"Nom":"Les Morts pour la France (Geneanet)","Url":"https://www.geneanet.org/militaires/","Type":"Militaire","Sous-type":MET,"Tarif":G,"Docs":[RM,EC],"Desc":"Indexation collaborative de monuments aux morts et registres militaires."},
    {"Nom":"Commonwealth War Graves (CWGC)","Url":"https://www.cwgc.org","Type":"Militaire","Sous-type":MET,"Tarif":G,"Docs":[RM],"Desc":"1,7 million de soldats du Commonwealth dont soldats enterrés en France."},
    {"Nom":"Fold3 (archives militaires US)","Url":"https://www.fold3.com","Type":"Militaire","Sous-type":MET,"Tarif":PAY,"Docs":[RM],"Desc":"Archives militaires américaines numérisées, pension rolls et dossiers."},
    {"Nom":"1789-1815.com","Url":"https://www.1789-1815.com","Type":"Militaire","Sous-type":MET,"Tarif":G,"Docs":[RM],"Desc":"Base des soldats des guerres révolutionnaires et napoléoniennes."},
]

all_links = archives_data + genealogie_data + militaire_data
df = pd.DataFrame(all_links)

# ==========================================
# INTERFACE
# ==========================================

with st.sidebar:
    st.markdown("<h2 style='margin-top:0;'>📜 Filtres</h2>", unsafe_allow_html=True)
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
        "", ["Gratuit", "Freemium", "Payant"],
        default=["Gratuit", "Freemium", "Payant"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📄 Types de documents")
    all_doc_types = list(DOC_TYPES.keys())
    selected_docs = st.multiselect(
        "", all_doc_types, default=[],
        placeholder="Tous les types",
        label_visibility="collapsed"
    )

    st.markdown("---")
    total_all = len(df)
    free_all = len(df[df["Tarif"] == G])
    st.markdown(
        f"<p style='font-size:0.8rem; color:#7A6050;'>{total_all} sources · {free_all} entièrement gratuites</p>",
        unsafe_allow_html=True
    )

# Hero
total     = len(df)
free_count= len(df[df["Tarif"] == G])
ad_count  = len([x for x in all_links if x["Type"] == AD])
dom_count = len([x for x in all_links if x.get("Sous-type") == DOM])

st.markdown(f"""
<div class="hero">
    <p class="hero-title">Portail Archives & Généalogie</p>
    <p class="hero-sub">Sources primaires, registres numérisés et outils de recherche familiale · France métropolitaine &amp; Outre-mer</p>
    <div class="hero-stats">
        <div class="hero-stat"><span class="hero-stat-num">{total}</span><span class="hero-stat-label">Sources indexées</span></div>
        <div class="hero-stat"><span class="hero-stat-num">{free_count}</span><span class="hero-stat-label">Entièrement gratuites</span></div>
        <div class="hero-stat"><span class="hero-stat-num">{ad_count}</span><span class="hero-stat-label">Archives dép.</span></div>
        <div class="hero-stat"><span class="hero-stat-num">{dom_count}</span><span class="hero-stat-label">Sources DOM-TOM</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

search_query = st.text_input(
    "", placeholder="🔍  Rechercher… département, outil, type de document (ex : 971, Guadeloupe, cadastre, notaires)",
    label_visibility="collapsed"
)

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
        if row["Type"] == "Généalogie":   badge_class = "badge-genealogie"
        elif row["Type"] == "Militaire":  badge_class = "badge-militaire"

        is_dom = row.get("Sous-type") == DOM
        domtom_badge = '<span class="badge badge-domtom">DOM-TOM</span>' if is_dom else ""

        tarif_class, tarif_label = "badge-free", "✓ Gratuit"
        if row["Tarif"] == PAY:  tarif_class, tarif_label = "badge-paid", "Payant"
        elif row["Tarif"] == FM: tarif_class, tarif_label = "badge-freemium", "Freemium"

        docs_html = "".join(
            f'<span class="doc-tag">{DOC_TYPES.get(d,"📄")} {d}</span>'
            for d in row["Docs"]
        )

        card = f"""
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
        if idx % 2 == 0: col1.markdown(card, unsafe_allow_html=True)
        else:             col2.markdown(card, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div style='font-size:2.5rem;margin-bottom:12px;'>☍</div>
        <p style='font-family:IM Fell English,serif;font-size:1.2rem;color:#7A5520;'>Aucune source ne correspond à vos critères.</p>
        <p style='font-size:0.85rem;color:#9A7040;'>Essayez d'élargir les filtres ou de modifier votre recherche.</p>
    </div>
    """, unsafe_allow_html=True)
