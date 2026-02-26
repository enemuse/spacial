import ee
import streamlit as st

class SpatialProcessor:
    def __init__(self):
        """Initialise la connexion à Earth Engine via les secrets Streamlit"""
        try:
            # Vérifier si on est en local ou sur Streamlit Cloud
            if "earth_engine" in st.secrets:
                # Récupération des infos du fichier .streamlit/secrets.toml
                creds_dict = dict(st.secrets["earth_engine"])
                
                # Authentification par compte de service
                credentials = ee.ServiceAccountCredentials(
                    creds_dict['client_email'], 
                    key_data=creds_dict['private_key']
                )
                ee.Initialize(credentials=credentials)
            else:
                # Fallback pour le développement local classique
                ee.Initialize(project='app-teledetection')
        except Exception as e:
            st.error(f"Erreur d'initialisation Earth Engine : {e}")

    def get_satellite_image(self, lat, lon):
        """Récupère la dernière image Sentinel-2 pour un point donné"""
        point = ee.Geometry.Point([lon, lat])

        # On cherche l'image la plus récente et la moins nuageuse
        image = (ee.ImageCollection('COPERNICUS/S2_SR')
                .filterBounds(point)
                .sort('CLOUDY_PIXEL_PERCENTAGE')
                .first())

        return image