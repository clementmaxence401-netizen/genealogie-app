import streamlit as st

# ── Configuration de la page ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Ressources Généalogiques Mondiales",
    page_icon="🌍",
    layout="wide",
)

# ── CSS personnalisé ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    .card {
        background: #f9f9f9;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 14px 16px;
        margin-bottom: 10px;
        transition: box-shadow 0.2s;
    }
    .card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .card-title { font-size: 16px; font-weight: 600; margin: 0 0 4px; }
    .card-desc  { font-size: 13px; color: #555; margin: 0 0 8px; }
    .card-footer { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
    .badge {
        font-size: 11px; font-weight: 600;
        padding: 3px 9px; border-radius: 20px;
    }
    .badge-monde    { background:#EDE9FE; color:#4C1D95; }
    .badge-france   { background:#DBEAFE; color:#1E3A5F; }
    .badge-europe   { background:#DCFCE7; color:#14532D; }
    .badge-amerique { background:#FEE2E2; color:#7F1D1D; }
    .badge-archives { background:#FEF3C7; color:#78350F; }
    .badge-outils   { background:#CCFBF1; color:#134E4A; }
    .badge-religions{ background:#FCE7F3; color:#831843; }
    .badge-gratuit  { background:#D1FAE5; color:#065F46; }
    .badge-payant   { background:#FEE2E2; color:#991B1B; }
    .link-btn {
        font-size: 12px; color: #6D28D9; text-decoration: none;
        margin-left: auto; font-weight: 500;
    }
    h1 { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Données ───────────────────────────────────────────────────────────────────
SITES = [
    # ── Mondial (15 sites) ────────────────────────────────────────────────────
    {"name": "Ancestry",           "url": "https://www.ancestry.com",           "desc": "La plus grande base de données généalogiques au monde. Milliards d'actes et d'arbres familiaux.",         "cat": "Mondial",   "gratuit": False},
    {"name": "MyHeritage",         "url": "https://www.myheritage.com",         "desc": "Plateforme internationale pour créer son arbre, faire correspondre les ADN et accéder aux archives.",                    "cat": "Mondial",   "gratuit": False},
    {"name": "Find A Grave",       "url": "https://www.findagrave.com",         "desc": "Base de données de cimetières du monde entier avec photos de pierres tombales.",                                         "cat": "Mondial",   "gratuit": True},
    {"name": "Geni",               "url": "https://www.geni.com",               "desc": "Arbre mondial partagé en ligne, collaboration avec d'autres chercheurs.",                                                "cat": "Mondial",   "gratuit": True},
    {"name": "Africa Ancestry",    "url": "https://www.africanancestry.com",    "desc": "Tests ADN spécialisés dans les origines africaines et la diaspora.",                                                     "cat": "Mondial",   "gratuit": False},
    {"name": "Geneanet Mondial",   "url": "https://www.geneanet.org",           "desc": "Extension mondiale du réseau collaboratif avec des arbres couvrant tous les continents.",                                "cat": "Mondial",   "gratuit": True},
    {"name": "Filae International","url": "https://www.filae.com",              "desc": "Accès aux indexations de recensements et registres d'Europe et du monde.",                                               "cat": "Mondial",   "gratuit": False},
    {"name": "WorldGenWeb Project","url": "https://www.worldgenweb.org",        "desc": "Projet bénévole mondial visant à héberger des sites de recherche généalogique par pays.",                                "cat": "Mondial",   "gratuit": True},
    {"name": "Internat. Civic Coat","url": "https://www.heraldry-wiki.com",     "desc": "La plus grande base de données publique d'héraldique et d'armoiries familiales mondiales.",                              "cat": "Mondial",   "gratuit": True},
    {"name": "Forebears",          "url": "https://forebears.io",               "desc": "Dictionnaire géographique des noms de famille, cartographie de la répartition et statistiques mondiales.",               "cat": "Mondial",   "gratuit": True},
    {"name": "WeRelate",           "url": "https://www.werelate.org",           "desc": "Le plus grand wiki de généalogie au monde, proposant des arbres et outils collaboratifs.",                                "cat": "Mondial",   "gratuit": True},
    {"name": "Genealogia.org",     "url": "http://www.genealogia.org",           "desc": "Portail d'orientation global pour les archives et l'immigration internationale.",                                       "cat": "Mondial",   "gratuit": True},
    {"name": "Immigrant Ships",    "url": "https://www.immigrantships.net",     "desc": "Transcriptions de listes de passagers de navires du monde entier à travers l'histoire.",                                 "cat": "Mondial",   "gratuit": True},
    {"name": "GeneaSub",           "url": "https://www.geneasub.com",           "desc": "Moteur de recherche global spécialisé dans les bases de données généalogiques libres.",                                  "cat": "Mondial",   "gratuit": True},
    {"name": "Cemeteries Route",   "url": "https://www.significantcemeteries.org", "desc": "Réseau et index des cimetières historiques d'importance patrimoniale globale.",                                        "cat": "Mondial",   "gratuit": True},

    # ── France (15 sites) ────────────────────────────────────────────────────
    {"name": "Geneanet",           "url": "https://www.geneanet.org",           "desc": "Réseau généalogique français et international, arbres collaboratifs et actes paroissiaux.",                             "cat": "France",    "gratuit": True},
    {"name": "Filae",              "url": "https://www.filae.com",              "desc": "Archives numérisées françaises, état civil et recensements. Leader en France.",                                         "cat": "France",    "gratuit": False},
    {"name": "France Archives",    "url": "https://francearchives.gouv.fr",     "desc": "Portail d'accès à toutes les archives départementales françaises numérisées.",                                          "cat": "France",    "gratuit": True},
    {"name": "Généalogie.com",     "url": "https://www.genealogie.com",         "desc": "Portail généalogique français avec millions de fiches et entraide communautaire.",                                      "cat": "France",    "gratuit": True},
    {"name": "SOSA Conseil",       "url": "https://www.sosa.fr",                "desc": "Service professionnel de recherches généalogiques en France.",                                                          "cat": "France",    "gratuit": False},
    {"name": "CGF Association",    "url": "https://www.cgf.asso.fr",            "desc": "Cercle Généalogique de France, aide et ressources pour chercheurs amateurs.",                                           "cat": "France",    "gratuit": True},
                        "cat": "France",    "gratuit": True
