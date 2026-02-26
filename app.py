import streamlit as st
import geemap
from processing import SpatialProcessor

st.title("Mon Premier Portail GEE")

# 1. Connexion au moteur métier
@st.cache_resource
def load_engine():
    return SpatialProcessor()

engine = load_engine()

# 2. Formulaire de saisie
with st.sidebar:
    st.header("Coordonnées")
    lat = st.number_input("Latitude", value=48.85, format="%.4f")
    lon = st.number_input("Longitude", value=2.35, format="%.4f")
    submit = st.button("Afficher la zone")

# 3. Carte
m = geemap.Map(center=[lat, lon], zoom=12)

if submit:
    with st.spinner("Récupération de l'image depuis le Cloud..."):
        img = engine.get_satellite_image(lat, lon)

        vis_params = {
            'bands': ['B4', 'B3', 'B2'],
            'min': 0,
            'max': 3000
        }

        m.addLayer(img, vis_params, 'Sentinel-2 Image')
        st.success(f"Image chargée pour {lat}, {lon}")

m.to_streamlit(height=500)