<template>
  <div ref="mapContainer" style="height: 80vh; width: 100%;"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import * as L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Importer les icônes Leaflet en mode ESM
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'

delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

export default {
  name: 'MapView',
  props: {
    points: {
      type: Array,
      default: () => [],
    },
  },
  setup(props) {
    const mapContainer = ref(null)
    let mapInstance = null
    let markersLayer = null

    // Au montage, créer la carte
    onMounted(() => {
      mapInstance = L.map(mapContainer.value).setView([48.8566, 2.3522], 6)

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
      }).addTo(mapInstance)

      markersLayer = L.layerGroup().addTo(mapInstance)

      // Première maj avec les points existants
      updateMarkers(props.points)
    })

    // Si la props "points" évolue => on remplace tout sur la carte
    watch(
      () => props.points,
      (newPoints) => {
        updateMarkers(newPoints)
      }
    )

    // Fonction qui reconstruit tous les marqueurs
    function updateMarkers(points) {
      if (!markersLayer) return

      markersLayer.clearLayers()

      points.forEach((p) => {
        // Assure-toi que p.latitude / p.longitude soient définis
        if (p.latitude && p.longitude) {
          L.marker([p.latitude, p.longitude])
            .bindPopup(
              `<b>${p.nom}</b><br>Lat: ${p.latitude}<br>Lon: ${p.longitude}`
            )
            .addTo(markersLayer)
        }
      })
    }

    return {
      mapContainer,
    }
  },
}
</script>
