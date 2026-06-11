st.caption("Tous les sites essentiels classés par zone géographique, type de document et accessibilité.")
st.write("---")

# ── Barre latérale de filtres ──────────────────────────────────────────────────
st.sidebar.header("🔍 Filtrer les ressources")

# Recherche par mot-clé
search_query = st.sidebar.text_input("Rechercher un site ou un pays", "").strip().lower()

# Filtre par catégorie (Zone / Thématique)
selected_cat = st.sidebar.selectbox("Zone ou Thématique", CATEGORIES)

# Filtre par type d'archives
selected_type = st.sidebar.selectbox("Type d'archives", TYPES_ARCHIVES)

# Filtre par coût
cost_filter = st.sidebar.radio("Accessibilité", ["Tous", "Gratuits uniquement", "Payants / Premium"])

# ── Filtrage des données ──────────────────────────────────────────────────────
filtered_sites = []
for s in SITES:
    # Filtre de recherche textuelle
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
    # Création d'une grille à 2 colonnes pour optimiser l'espace visuel
    col1, col2 = st.columns(2)
    
    for idx, s in enumerate(filtered_sites):
        # Récupération du style du badge de catégorie
        bg_class, emoji = BADGE_STYLES.get(s["cat"], ("outils", "🔧"))
        
        # Badge de gratuité
        gratuit_badge = '<span class="badge badge-gratuit">Gratuit</span>' if s["gratuit"] else '<span class="badge badge-payant">Payant / Premium</span>'
        
        # Construction du code HTML pour la carte
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
        
        # Répartition équitable dans les deux colonnes
        if idx % 2 == 0:
            col1.markdown(card_html, unsafe_allow_html=True)
        else:
            col2.markdown(card_html, unsafe_allow_html=True)
