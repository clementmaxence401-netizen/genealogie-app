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

# ── Données Initiales ─────────────────────────────────────────────────────────
SITES = [
    # ── Mondial ───────────────────────────────────────────────────────────────
    {"name": "Ancestry",           "url": "https://www.ancestry.com",           "desc": "La plus grande base de données généalogiques au monde. Milliards d'actes et d'arbres familiaux.",         "cat": "Mondial",   "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": False},
    {"name": "MyHeritage",         "url": "https://www.myheritage.com",         "desc": "Plateforme internationale pour créer son arbre, faire correspondre les ADN et accéder aux archives.",                    "cat": "Mondial",   "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": False},
    {"name": "Find A Grave",       "url": "https://www.findagrave.com",         "desc": "Base de données de cimetières du monde entier avec photos de pierres tombales.",                                         "cat": "Mondial",   "pays": "Multi", "type": "Cimetières / Tombes", "gratuit": True},
    {"name": "Geni",               "url": "https://www.geni.com",               "desc": "Arbre mondial partagé en ligne, collaboration avec d'autres chercheurs.",                                                "cat": "Mondial",   "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Africa Ancestry",    "url": "https://www.africanancestry.com",    "desc": "Tests ADN spécialisés dans les origines africaines et la diaspora.",                                                     "cat": "Mondial",   "pays": "Multi", "type": "ADN", "gratuit": False},
    {"name": "Geneanet Mondial",   "url": "https://www.geneanet.org",           "desc": "Extension mondiale du réseau collaboratif avec des arbres couvrant tous les continents.",                                "cat": "Mondial",   "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Filae International","url": "https://www.filae.com",              "desc": "Accès aux indexations de recensements et registres d'Europe et du monde.",                                               "cat": "Mondial",   "pays": "Multi", "type": "État Civil / Registres", "gratuit": False},
    {"name": "WorldGenWeb Project","url": "https://www.worldgenweb.org",        "desc": "Projet bénévole mondial visant à héberger des sites de recherche généalogique par pays.",                                "cat": "Mondial",   "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Internat. Civic Coat","url": "https://www.heraldry-wiki.com",     "desc": "La plus grande base de données publique d'héraldique et d'armoiries familiales mondiales.",                              "cat": "Mondial",   "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Forebears",          "url": "https://forebears.io",               "desc": "Dictionnaire géographique des noms de famille, cartographie de la répartition et statistiques mondiales.",               "cat": "Mondial",   "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "WeRelate",           "url": "https://www.werelate.org",           "desc": "Le plus grand wiki de généalogie au monde, proposing des arbres et outils collaboratifs.",                                "cat": "Mondial",   "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Genealogia.org",     "url": "http://www.genealogia.org",           "desc": "Portail d'orientation global pour les archives et l'immigration internationale.",                                       "cat": "Mondial",   "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Immigrant Ships",    "url": "https://www.immigrantships.net",     "desc": "Transcriptions de listes de passagers de navires du monde entier à travers l'histoire.",                                 "cat": "Mondial",   "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "GeneaSub",           "url": "https://www.geneasub.com",           "desc": "Moteur de recherche global spécialisé dans les bases de données généalogiques libres.",                                  "cat": "Mondial",   "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Cemeteries Route",   "url": "https://www.significantcemeteries.org", "desc": "Réseau et index des cimetières historiques d'importance patrimoniale globale.",                                        "cat": "Mondial",   "pays": "Multi", "type": "Cimetières / Tombes", "gratuit": True},

    # ── France ────────────────────────────────────────────────────────────────
    {"name": "Geneanet",           "url": "https://www.geneanet.org",           "desc": "Réseau généalogique français et international, arbres collaboratifs et actes paroissiaux.",                              "cat": "France",    "pays": "France", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Filae",              "url": "https://www.filae.com",              "desc": "Archives numérisées françaises, état civil et recensements. Leader en France.",                                         "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": False},
    {"name": "France Archives",    "url": "https://francearchives.gouv.fr",     "desc": "Portail d'accès à toutes les archives départementales françaises numérisées.",                                           "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Mémoire des Hommes", "url": "https://www.memoiredeshommes.sga.defense.gouv.fr", "desc": "Portail officiel du Ministère des Armées. Registres matricules, fiches de Morts pour la France (14-18, 39-45, Indochine), résistants et fusillés.", "cat": "France", "pays": "France", "type": "Militaires", "gratuit": True},
    {"name": "Grand Mémorial",     "url": "http://www.culture.fr/Genealogie/Grand-Memorial", "desc": "Moteur de recherche national des registres matricules des soldats de la Grande Guerre (classes 1887-1921).", "cat": "France", "pays": "France", "type": "Militaires", "gratuit": True},
    {"name": "Service Historique de la Défense (SHD)", "url": "https://www.servicehistorique.sga.defense.gouv.fr", "desc": "Accès aux inventaires et archives des forces armées françaises (Vincennes, Caen, Rochefort, Lorient).", "cat": "France", "pays": "France", "type": "Militaires", "gratuit": True},
    {"name": "SGA / Sépultures de Guerre", "url": "https://www.sga.defense.gouv.fr/meponweb/", "desc": "Permet de trouver le lieu d'inhumation des soldats morts pour la France dans les nécropoles nationales et carrés militaires.", "cat": "France", "pays": "France", "type": "Militaires", "gratuit": True},
    {"name": "Généalogie.com",     "url": "https://www.genealogie.com",         "desc": "Portail généalogique français avec millions de fiches et entraide communautaire.",                                      "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "SOSA Conseil",       "url": "https://www.sosa.fr",                "desc": "Service professionnel de recherches généalogiques en France.",                                                           "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": False},
    {"name": "CGF Association",    "url": "https://www.cgf.asso.fr",            "desc": "Cercle Généalogique de France, aide et ressources pour chercheurs amateurs.",                                           "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "GeneaBank",          "url": "http://www.geneabank.org",           "desc": "Banque de données mutualisée des associations généalogiques françaises.",                                                "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Bagneux Archives",   "url": "https://www.archives-recherche.fr",  "desc": "Exemple d'annuaire regroupant les archives communales et municipales de France.",                                         "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Cercle du Hainaut",  "url": "https://www.ghdk.fr",                "desc": "Groupement généalogique de la région Nord et Flandres françaises.",                                                      "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Généalogie Algérie", "url": "https://www.anom.culture.gouv.fr",   "desc": "Archives Nationales d'Outre-Mer (ANOM). Registres paroissiaux et d'état civil coloniaux.",                               "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "RFGénéalogie",       "url": "https://www.rfgenealogie.com",       "desc": "Revue Française de Généalogie. Actualités, guides pratiques et méthodes de recherche.",                                  "cat": "France",    "pays": "France", "type": "Presse / Journaux", "gratuit": False},
    {"name": "Guide Généalogie",   "url": "https://www.guide-genealogie.com",   "desc": "Fiches pratiques complètes pour apprendre à chercher ses ancêtres en France.",                                           "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Familles Parisiennes","url": "http://www.famillesparisiennes.org", "desc": "Bases de données et archives notariales sur les familles de Paris et de l'Île-de-France.",                                   "cat": "France",    "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "GeneaWiki",          "url": "https://fr.geneawiki.com",           "desc": "L'encyclopédie de la généalogie gratuite, écrite de manière collaborative.",                                             "cat": "France",    "pays": "France", "type": "Logiciels / Arbres", "gratuit": True},

    # ── Europe ────────────────────────────────────────────────────────────────
    {"name": "Findmypast",         "url": "https://www.findmypast.com",         "desc": "Spécialisé dans les archives britanniques, irlandaises, américaines et du Commonwealth.",                               "cat": "Europe",    "pays": "Royaume-Uni", "type": "État Civil / Registres", "gratuit": False},
    {"name": "The National Archives UK - Military", "url": "https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/?research-guide-category=military-and-maritime", "desc": "Guides, registres officiels et livrets militaires de l'armée britannique, de la Royal Navy et de la RAF.", "cat": "Europe", "pays": "Royaume-Uni", "type": "Militaires", "gratuit": True},
    {"name": "Commonwealth War Graves", "url": "https://www.cwgc.org",          "desc": "Base de données officielle commémorant les 1,7 million d'hommes et femmes des forces du Commonwealth morts durant les guerres mondiales.", "cat": "Europe", "pays": "Royaume-Uni", "type": "Militaires", "gratuit": True},
    {"name": "Volksbund (Allemagne - Militaire)", "url": "https://www.volksbund.de/graebersuche", "desc": "Base de données officielle allemande recensant près de 5 millions de soldats allemands tombés ou disparus pendant les guerres mondiales.", "cat": "Europe", "pays": "Allemagne", "type": "Militaires", "gratuit": True},
    {"name": "War Heritage Institute (Belgique)", "url": "https://www.wardeadregister.be", "desc": "Le 'Morts pour la Belgique' officiel. Base de données des soldats et victimes de guerre belges.", "cat": "Europe", "pays": "Belgique", "type": "Militaires", "gratuit": True},
    {"name": "Caduti Grande Guerra (Italie)", "url": "http://www.cadutigrandeguerra.it", "desc": "Registre national et numérisé des militaires italiens morts pour la patrie lors de la Première Guerre mondiale.", "cat": "Europe", "pays": "Italie", "type": "Militaires", "gratuit": True},
    {"name": "PARES Archives Militaires (Espagne)", "url": "https://pares.mcu.es", "desc": "Section militaire des archives espagnoles. Idéal pour retracer les soldats de la guerre civile et de l'Empire.", "cat": "Europe", "pays": "Espagne", "type": "Militaires", "gratuit": True},
    {"name": "Kriegsarchiv Wien (Autriche)", "url": "https://www.oesta.gv.at",   "desc": "Archives de guerre autrichiennes. Fiches militaires indispensables pour l'ancien Empire Austro-Hongrois.", "cat": "Europe", "pays": "Autriche", "type": "Militaires", "gratuit": True},
    {"name": "The Genealogist UK", "url": "https://www.thegenealogist.co.uk",   "desc": "Archives britanniques, recensements UK, BMD et arbres familiaux.",                                                      "cat": "Europe",    "pays": "Royaume-Uni", "type": "État Civil / Registres", "gratuit": False},
    {"name": "FamilyRelatives UK", "url": "https://www.familyrelatives.com",    "desc": "Registres d'état civil anglais et gallois, naissances, mariages, décès.",                                              "cat": "Europe",    "pays": "Royaume-Uni", "type": "État Civil / Registres", "gratuit": True},
    {"name": "MyAncestry.dk",      "url": "https://www.myancestry.dk",          "desc": "Registres danois, recensements et listes de paroisse.",                                                                 "cat": "Europe",    "pays": "Danemark", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Íslendingabók",      "url": "https://www.islendingabok.is",       "desc": "Base de données islandaise, quasi toute la population depuis le 9e siècle.",                                           "cat": "Europe",    "pays": "Islande", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "ScotlandsPeople",    "url": "https://www.scotlandspeople.gov.uk", "desc": "Le site officiel d'archives généalogiques pour l'Écosse (actes, recensements).",                                             "cat": "Europe",    "pays": "Royaume-Uni", "type": "État Civil / Registres", "gratuit": False},
    {"name": "IrishGenealogy",     "url": "https://www.irishgenealogy.ie",      "desc": "Portail d'État irlandais gratuit offrant l'accès aux registres d'état civil et d'église.",                                "cat": "Europe",    "pays": "Irlande", "type": "État Civil / Registres", "gratuit": True},
    {"name": "WieWasWie (Pays-Bas)","url": "https://www.wiewaswie.nl",          "desc": "La plus grande base de données d'archives néerlandaise pour l'état civil.",                                              "cat": "Europe",    "pays": "Pays-Bas", "type": "État Civil / Registres", "gratuit": True},
    {"name": "GeniWal (Belgique)", "url": "http://www.geniwal.bi",              "desc": "Association de généalogie informatique pour la région Wallonie et Bruxelles.",                                           "cat": "Europe",    "pays": "Belgique", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Genealogie Online NL","url": "https://www.genealogieonline.nl",   "desc": "Publication d'arbres généalogiques et recherche de correspondances aux Pays-Bas.",                                      "cat": "Europe",    "pays": "Pays-Bas", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "GenTeam Autriche",   "url": "https://www.genteam.at",              "desc": "Base de données monumentale pour l'Autriche, la Bohême et une partie de l'Europe centrale.",                              "cat": "Europe",    "pays": "Autriche", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Portalgadi Portugal","url": "https://tombo.pt",                    "desc": "Index complet d'accès direct aux registres paroissiaux numérisés du Portugal.",                                          "cat": "Europe",    "pays": "Portugal", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Kranich (Suisse)",   "url": "https://www.sgff-ssgh.ch",           "desc": "Société Suisse d'Études Généalogiques. Ressources et conseils pour la Confédération.",                                  "cat": "Europe",    "pays": "Suisse", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Czech Archives",     "url": "https://www.mza.cz",                 "desc": "Portail des archives régionales de Moravie et République Tchèque.",                                                     "cat": "Europe",    "pays": "République Tchèque", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Hungaricana",        "url": "https://archives.hungaricana.hu",    "desc": "Portail d'archives de la Hongrie contenant cartes, actes et documents d'état civil.",                                    "cat": "Europe",    "pays": "Hongrie", "type": "État Civil / Registres", "gratuit": True},

    # ── Amériques ─────────────────────────────────────────────────────────────
    {"name": "BAnQ Québec",        "url": "https://www.banq.qc.ca",              "desc": "Archives québécoises, registres d'état civil, notariaux et judiciaires.",                                              "cat": "Amériques", "pays": "Canada", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Collection Drouin",  "url": "https://www.genealogiequebec.com",   "desc": "Collection Drouin, actes paroissiaux historiques du Québec et de l'Ontario.",                                           "cat": "Amériques", "pays": "Canada", "type": "État Civil / Registres", "gratuit": False},
    {"name": "USGenWeb",           "url": "https://usgenweb.org",               "desc": "Projet collaboratif de généalogie américaine par comté et état.",                                                      "cat": "Amériques", "pays": "États-Unis", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Fold3",              "url": "https://www.fold3.com",              "desc": "Archives militaires américaines, registres de guerre, dossiers de service.",                                            "cat": "Amériques", "pays": "États-Unis", "type": "Militaires", "gratuit": False},
    {"name": "Ellis Island",       "url": "https://www.statueofliberty.org",    "desc": "Base de données des immigrants arrivés à Ellis Island entre 1892 et 1957.",                                            "cat": "Amériques", "pays": "États-Unis", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Ancestry Latino",    "url": "https://www.ancestry.com/cs/la-latin-american-records", "desc": "Archives d'Amérique latine (Mexique, Brésil, Argentine, Chili…).",                                  "cat": "Amériques", "pays": "Multi", "type": "État Civil / Registres", "gratuit": False},
    {"name": "Library and Archives","url": "https://library-archives.canada.ca", "desc": "Archives nationales du Canada. Recensements historiques, dossiers militaires et d'immigration.",                        "cat": "Amériques", "pays": "Canada", "type": "État Civil / Registres", "gratuit": True},
    {"name": "National Archives US","url": "https://www.archives.gov",           "desc": "Archives nationales des États-Unis. Contient l'ensemble des recensements fédéraux historiques.",                        "cat": "Amériques", "pays": "États-Unis", "type": "État Civil / Registres", "gratuit": True},
    {"name": "PRDH Québec",        "url": "https://www.prdh-igd.com",           "desc": "Répertoire des actes de baptême, mariage et sépulture du Québec ancien (1621-1849).",                                    "cat": "Amériques", "pays": "Canada", "type": "État Civil / Registres", "gratuit": False},
    {"name": "Castle Garden",      "url": "http://www.castlegarden.org",        "desc": "Accès gratuit aux informations de 11 millions d'immigrants arrivés à New York avant Ellis Island (1830-1892).",         "cat": "Amériques", "pays": "États-Unis", "type": "État Civil / Registres", "gratuit": True},
    {"name": "FamilySearch Latino","url": "https://www.familysearch.org/es/",   "desc": "Portail dédié et indexations massives pour l'Espagne et l'Amérique du Sud.",                                             "cat": "Amériques", "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},

    # ── Archives ──────────────────────────────────────────────────────────────
    {"name": "Archives nationales","url": "https://www.archives-nationales.culture.gouv.fr", "desc": "Archives nationales françaises, documents historiques accessibles en ligne.",                              "cat": "Archives",  "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Gallica – BnF",      "url": "https://gallica.bnf.fr",              "desc": "Bibliothèque numérique de la BnF. Presses, registres, journaux anciens.",                                              "cat": "Archives",  "pays": "France", "type": "Presse / Journaux", "gratuit": True},
    {"name": "Riksarkivet (Suède)","url": "https://riksarkivet.se",              "desc": "Archives nationales suédoises avec registres paroissiaux et recensements.",                                            "cat": "Archives",  "pays": "Suède", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Arkivverket (Norvège)","url": "https://www.arkivverket.no",       "desc": "Archives nationales norvégiennes, registres démographiques et paroissiaux.",                                           "cat": "Archives",  "pays": "Norvège", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Antenati (Italie)",  "url": "https://www.antenati.san.beniculturali.it", "desc": "Archives d'état civil italien, actes numérisés du 19e siècle.",                                                 "cat": "Archives",  "pays": "Italie", "type": "État Civil / Registres", "gratuit": True},
    {"name": "DigitArq (Portugal)","url": "https://digitarq.arquivos.pt",       "desc": "Archives nationales du Portugal, registres notariaux et paroissiaux.",                                                 "cat": "Archives",  "pays": "Portugal", "type": "État Civil / Registres", "gratuit": True},
    {"name": "PARES (Espagne)",    "url": "https://pares.mcu.es",               "desc": "Portail des archives espagnoles, documents historiques et généalogiques.",                                              "cat": "Archives",  "pays": "Espagne", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Szukaj (Pologne)",   "url": "https://szukajwarchiwach.gov.pl",    "desc": "Portail des archives polonaises avec registres paroissiaux et documents d'état.",                                       "cat": "Archives",  "pays": "Pologne", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Openarch (Pays-Bas)","url": "https://www.openarch.nl",             "desc": "Archives ouvertes des Pays-Bas et Belgique, état civil et registres divers.",                                           "cat": "Archives",  "pays": "Pays-Bas", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Nationaal Archief",  "url": "https://www.nationaalarchief.nl",    "desc": "Archives nationales néerlandaises, registres d'état civil numérisés.",                                                 "cat": "Archives",  "pays": "Pays-Bas", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Europeana Archives", "url": "https://www.europeana.eu",           "desc": "Bibliothèque et archives numériques de l'Union Européenne, des millions d'images historiques.",                           "cat": "Archives",  "pays": "Multi", "type": "Presse / Journaux", "gratuit": True},

    # ── Religions ─────────────────────────────────────────────────────────────
    {"name": "FamilySearch",       "url": "https://www.familysearch.org",       "desc": "Bibliothèque généalogique gratuite de l'Église LDS. Milliards de documents numérisés.",                                 "cat": "Religions", "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Archion (Allemagne)","url": "https://www.archion.de",              "desc": "Archives kirchenbuch (registres d'église) pour l'Allemagne et l'Autriche.",                                            "cat": "Religions", "pays": "Allemagne", "type": "État Civil / Registres", "gratuit": False},
    {"name": "Matricula Online",   "url": "https://data.matricula-online.eu",   "desc": "Registres paroissiaux catholiques pour l'Europe centrale (Autriche, Allemagne, Pologne).",                             "cat": "Religions", "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "JRI-Poland",         "url": "https://jri-poland.org",              "desc": "Index des registres juifs de Pologne et d'Europe de l'Est.",                                                            "cat": "Religions", "pays": "Pologne", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Sephardic Genealogy","url": "https://www.sephardicgen.com",       "desc": "Généalogie séfarade, registres des communautés juives du bassin méditerranéen.",                                       "cat": "Religions", "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Catholic Hierarchy", "url": "https://www.catholic-hierarchy.org", "desc": "Base de données du clergé catholique, utile pour retracer les oncles et tantes ecclésiastiques.",                           "cat": "Religions", "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "JewishGen",          "url": "https://www.jewishgen.org",          "desc": "La ressource centrale gratuite pour la généalogie juive mondiale, des millions de fiches.",                             "cat": "Religions", "pays": "Multi", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Huguenots de France","url": "https://www.huguenots.fr",            "desc": "Cercle de généalogie protestante. Histoire et dispersion des familles huguenotes exilées.",                              "cat": "Religions", "pays": "France", "type": "État Civil / Registres", "gratuit": True},
    {"name": "Paroisses de Suisse", "url": "https://www.bistum-basel.ch",        "desc": "Accès aux archives diocésaines et paroissiales numérisées des différents cantons suisses.",                             "cat": "Religions", "pays": "Suisse", "type": "État Civil / Registres", "gratuit": True},

    # ── Outils & Logiciels ────────────────────────────────────────────────────
    {"name": "BillionGraves",      "url": "https://billiongraves.com",          "desc": "Registre numérique de cimetières, photos et transcriptions de tombes mondiales.",                                        "cat": "Outils",    "pays": "Multi", "type": "Cimetières / Tombes", "gratuit": True},
    {"name": "WikiTree",           "url": "https://www.wikitree.com",           "desc": "Arbre généalogique universel collaboratif et gratuit. Millions de profils liés.",                                        "cat": "Outils",    "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Cyndi's List",       "url": "https://www.cyndislist.com",          "desc": "Annuaire de 300 000 liens généalogiques classés par pays et sujet.",                                                     "cat": "Outils",    "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "RootsWeb",           "url": "https://www.rootsweb.com",           "desc": "Un des plus anciens réseaux généalogiques en ligne. Millions d'arbres partagés.",                                       "cat": "Outils",    "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Eureka Généalogie",  "url": "https://www.eureka.re",               "desc": "Moteur de recherche généalogique multibase pour la France.",                                                            "cat": "Outils",    "pays": "France", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "GEDmatch",           "url": "https://www.gedmatch.com",           "desc": "Outil de comparaison ADN multi-plateformes pour généalogistes.",                                                      "cat": "Outils",    "pays": "Multi", "type": "ADN", "gratuit": True},
    {"name": "23andMe",            "url": "https://www.23andme.com",            "desc": "Tests ADN pour l'ascendance et la santé, correspondances génétiques.",                                                  "cat": "Outils",    "pays": "Multi", "type": "ADN", "gratuit": False},
    {"name": "ADN Geneanet",       "url": "https://adn.geneanet.org",           "desc": "Tests ADN généalogiques en partenariat avec Family Tree DNA.",                                                         "cat": "Outils",    "pays": "Multi", "type": "ADN", "gratuit": False},
    {"name": "GRAMPS",             "url": "https://gramps-project.org",          "desc": "Logiciel libre de généalogie multiplateforme (Windows, Mac, Linux).",                                                 "cat": "Outils",    "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": True},
    {"name": "Heredis",            "url": "https://www.heredis.com",            "desc": "Logiciel français de généalogie avec synchronisation cloud et sources.",                                               "cat": "Outils",    "pays": "France", "type": "Logiciels / Arbres", "gratuit": False},
    {"name": "MacFamilyTree",      "url": "https://www.synium.de/products/macfamilytree/", "desc": "Logiciel de généalogie pour Mac avec visualisations modernes.",                                             "cat": "Outils",    "pays": "Multi", "type": "Logiciels / Arbres", "gratuit": False},
]

# ── Générateur automatique des 101 Archives Départementales Françaises ──────
DEPARTEMENTS = [
    ("01", "Ain"), ("02", "Aisne"), ("03", "Allier"), ("04", "Alpes-de-Haute-Provence"), ("05", "Hautes-Alpes"),
    ("06", "Alpes-Maritimes"), ("07", "Ardèche"), ("08", "Ardennes"), ("09", "Ariège"), ("10", "Aube"),
    ("11", "Aude"), ("12", "Aveyron"), ("13", "Bouches-du-Rhône"), ("14", "Calvados"), ("15", "Cantal"),
    ("16", "Charente"), ("17", "Charente-Maritime"), ("18", "Cher"), ("19", "Corrèze"), ("2A", "Corse-du-Sud"),
    ("2B", "Haute-Corse"), ("21", "Côte-d'Or"), ("22", "Côtes-d'Armor"), ("23", "Creuse"), ("24", "Dordogne"),
    ("25", "Doubs"), ("26", "Drôme"), ("27", "Eure"), ("28", "Eure-et-Loir"), ("29", "Finistère"),
    ("30", "Gard"), ("31", "Haute-Garonne"), ("32", "Gers"), ("33", "Gironde"), ("34", "Hérault"),
    ("35", "Ille-et-Vilaine"), ("36", "Indre"), ("37", "Indre-et-Loire"), ("38", "Isère"), ("39", "Jura"),
    ("40", "Landes"), ("41", "Loir-et-Cher"), ("42", "Loire"), ("43", "Haute-Loire"), ("44", "Loire-Atlantique"),
    ("45", "Loiret"), ("46", "Lot"), ("47", "Lot-et-Garonne"), ("48", "Lozère"), ("49", "Maine-et-Loire"),
    ("50", "Manche"), ("51", "Marne"), ("52", "Haute-Marne"), ("53", "Mayenne"), ("54", "Meurthe-et-Moselle"),
    ("55", "Meuse"), ("56", "Morbihan"), ("57", "Moselle"), ("58", "Nièvre"), ("59", "Nord"),
    ("60", "Oise"), ("61", "Orne"), ("62", "Pas-de-Calais"), ("63", "Puy-de-Dôme"), ("64", "Pyrénées-Atlantiques"),
    ("65", "Hautes-Pyrénées"), ("66", "Pyrénées-Orientales"), ("67", "Bas-Rhin"), ("68", "Haut-Rhin"), ("69", "Rhône"),
    ("70", "Haute-Saône"), ("71", "Saône-et-Loire"), ("72", "Sarthe"), ("73", "Savoie"), ("74", "Haute-Savoie"),
    ("75", "Paris"), ("76", "Seine-Maritime"), ("77", "Seine-et-Marne"), ("78", "Yvelines"), ("79", "Deux-Sèvres"),
    ("80", "Somme"), ("81", "Tarn"), ("82", "Tarn-et-Garonne"), ("83", "Var"), ("84", "Vaucluse"),
    ("85", "Vendée"), ("86", "Vienne"), ("87", "Haute-Vienne"), ("88", "Vosges"), ("89", "Yonne"),
    ("90", "Territoire de Belfort"), ("91", "Essonne"), ("92", "Hauts-de-Seine"), ("93", "Seine-Saint-Denis"), ("94", "Val-de-Marne"),
    ("95", "Val-d'Oise"), ("971", "Guadeloupe"), ("972", "Martinique"), ("973", "Guyane"), ("974", "La Réunion"), ("976", "Mayotte")
]

# Cas particuliers d'URLs qui ne respectent pas le schéma standard "archives.numero.fr"
EXCEPTIONS_URL = {
    "2A": "https://archives.isula.corsica",
    "2B": "https://archives.isula.corsica",
    "54": "https://archives.meurthe-et-moselle.fr",
    "67": "https://archives.alsace.eu",
    "68": "https://archives.alsace.eu",
    "69": "https://archives.rhone.fr",
    "75": "https://archives.paris.fr",
    "93": "https://archives.seinesaintdenis.fr",
}

for num, nom in DEPARTEMENTS:
    # Détermination de l'URL optimale
    url = EXCEPTIONS_URL.get(num, f"https://archives.{num}.fr")
    
    # Création de l'élément dictionnaire
    site_dep = {
        "name": f"Archives Départementales - {nom} ({num})",
        "url": url,
        "desc": f"Accès officiel aux registres paroissiaux, état civil, recensements et plans cadastraux numérisés du département : {nom}.",
        "cat": "Archives",
        "pays": f"France ({num})",
        "type": "État Civil / Registres",
        "gratuit": True
    }
    SITES.append(site_dep)

# ── Listes pour Filtres ───────────────────────────────────────────────────────
CATEGORIES = ["Toutes", "Mondial", "France", "Europe", "Amériques", "Archives", "Outils", "Religions"]
TYPES_ARCHIVES = ["Tous", "État Civil / Registres", "Militaires", "Cimetières / Tombes", "Presse / Journaux", "ADN", "Logiciels / Arbres"]

BADGE_STYLES = {
    "Mondial":   ("monde",    "🌍"),
    "France":    ("france",   "🇫🇷"),
    "Europe":    ("europe",   "🇪🇺"),
    "Amériques": ("amerique", "🌎"),
    "Archives":  ("archives", "🗄️"),
    "Outils":    ("outils",   "🔧"),
    "Religions": ("religions","⛪"),
}

# ── Interface Graphique ───────────────────────────────────────────────────────
st.title("🌍 Ressources généalogiques mondiales")
st.caption("Tous les sites essentiels classés par zone géographique, type de document et accessibilité.")
st.write("---")

# ── Barre latérale de filtres ──────────────────────────────────────────────────
st.sidebar.header("🔍 Filtrer les ressources")

# Recherche par mot-clé (Recherche aussi sur le nom du département ou son numéro)
search_query = st.sidebar.text_input("Rechercher un site, un pays ou un département (ex: 44)", "").strip().lower()

# Filtre par catégorie (Zone / Thématique)
selected_cat = st.sidebar.selectbox("Zone ou Thématique", CATEGORIES)

# Filtre par type d'archives
selected_type = st.sidebar.selectbox("Type d'archives", TYPES_ARCHIVES)

# Filtre par coût
cost_filter = st.sidebar.radio("Accessibilité", ["Tous", "Gratuits uniquement", "Payants / Premium"])

# ── Filtrage dynamique des données ────────────────────────────────────────────
filtered_sites = []
for s in SITES:
    # Filtre de recherche textuelle globale
    if search_query and (search_query not in s["name"].lower() and search_query not in s["desc"].lower() and search_query not in s["pays"].lower()):
        continue
    
    # Filtre de catégorie
    if selected_cat != "Toutes" and s["cat"] != selected_cat:
        continue
        
    # Filtre de type
    if selected_type != "Tous" and s["type"] != selected_type:
        continue
        
    # Filtre de coût
    if cost_filter == "Gratuits uniquement" and not s["gratuit"]:
        continue
    elif cost_filter == "Payants / Premium" and s["gratuit"]:
        continue
        
    filtered_sites.append(s)

# ── Affichage des résultats ───────────────────────────────────────────────────
st.subheader(f"🗂️ Ressources disponibles ({len(filtered_sites)})")

if not filtered_sites:
    st.info("Aucun site ne correspond à vos critères de recherche. Essayez d'élargir vos filtres.")
else:
    # Création d'une grille à 2 colonnes réactive
    col1, col2 = st.columns(2)
    
    for idx, s in enumerate(filtered_sites):
        # Récupération du style du badge de catégorie
        bg_class, emoji = BADGE_STYLES.get(s["cat"], ("outils", "🔧"))
        
        # Badge de gratuité
        gratuit_badge = '<span class="badge badge-gratuit">Gratuit</span>' if s["gratuit"] else '<span class="badge badge-payant">Payant / Premium</span>'
        
        # Construction du HTML de la carte
        card_html = f"""
        <div class="card">
            <div class="card-title">{s['name']} <span style="font-weight: normal; font-size: 13px; color: #888;">({s['pays']})</span></div>
            <div class="card-desc">{s['desc']}</div>
            <div class="card-footer">
                <span class="badge badge-{bg_class}">{emoji} {s['cat']}</span>
                <span class="badge badge-outils">📂 {s['type']}</span>
                {gratuit_badge}
                <a class="link-btn" href="{s['url']}" target="_blank">Visiter le site ↗</a>
            </div>
        </div>
        """
        
        # Distribution alternée gauche/droite dans la grille
        if idx % 2 == 0:
            col1.markdown(card_html, unsafe_allow_html=True)
        else:
            col2.markdown(card_html, unsafe_allow_html=True)
