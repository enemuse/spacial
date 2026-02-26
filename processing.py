import ee
class SpatialProcessor:
    def init(self):
        """Initialise la connexion à Earth Engine"""
        ee.Initialize(project="nodal-pixel-429306-b3")
    def get_satellite_image(self, lat, lon):
        """Récupère la dernière image Sentinel-2 pour un point donné"""
        point = ee.Geometry.Point([lon, lat])

        # On cherche l'image la plus récente et la moins nuageuse
        image = (ee.ImageCollection('COPERNICUS/S2_SR')
                .filterBounds(point)
                .sort('CLOUDY_PIXEL_PERCENTAGE')
                .first())

        return image