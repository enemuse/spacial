import streamlit as st
import ee
import geemap.foliumap as geemap   # ← LE CHANGEMENT CLÉ
from processing import SpatialProcessor

st.set_page_config(page_title="Mon Premier Portail GEE", layout="wide", page_icon="🛰️")
st.title("🛰️ Mon Premier Portail GEE")

# 1. Chargement du moteur (une seule fois grâce au cache)
@st.cache_resource
def load_engine():
    engine = SpatialProcessor()
    # Si ton SpatialProcessor ne fait PAS déjà ee.Initialize(), ajoute ici :
    # ee.Initialize(credentials=..., project='ton-project-id')
    return engine

engine = load_engine()

# 2. Sidebar
with st.sidebar:
    st.header("📍 Coordonnées")
    lat = st.number_input("Latitude", value=33.9716, format="%.4f")   # Rabat par défaut
    lon = st.number_input("Longitude", value=-6.8498, format="%.4f")
    submit = st.button("Afficher la zone", type="primary", use_container_width=True)

# 3. Carte (créée à chaque rerun → normal et rapide avec folium)
m = geemap.Map(
    center=[lat, lon],
    zoom=12,
    height=650,
    ee_initialize=False,
    add_google_map=False  # optionnel, évite conflit de tuiles
)

if submit:
    with st.spinner("Récupération de l'image Sentinel-2 depuis Google Earth Engine..."):
        try:
            img = engine.get_satellite_image(lat, lon)

            if img is None:
                st.error("❌ Aucune image retournée par SpatialProcessor")
            else:
                vis_params = {
                    'bands': ['B4', 'B3', 'B2'],
                    'min': 0,
                    'max': 3000,
                    'gamma': 1.4
                }

                m.addLayer(img, vis_params, 'Sentinel-2 True Color')
                st.success(f"✅ Image chargée avec succès pour {lat:.4f}, {lon:.4f}")

        except Exception as e:
            st.error(f"❌ Erreur Earth Engine : {str(e)}")
            st.info("Vérifie que `ee.Initialize()` est bien appelé dans ta classe `SpatialProcessor`.")

# Affichage final de la carte
m.to_streamlit(height=650)

# Bouton bonus
if st.button("🔄 Réinitialiser la carte"):
    st.rerun()