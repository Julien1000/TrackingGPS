<template>
  <div ref="mapContainer" style="height: 80vh; width: 100%;"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import * as L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Définir une icône personnalisée pour le dernier point
const bluePersonIcon = new L.Icon({
  iconUrl: '/icons/my-logo.png',
  iconSize: [35, 35], // Taille visible
  iconAnchor: [17.5, 35], // Centre en bas
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
    let polylineLayers = {} // Un polyline par utilisateur
    let lastMarkerLayer = null // Pour afficher les derniers points

    // Création de la carte
    onMounted(() => {
      mapInstance = L.map(mapContainer.value).setView([48.8566, 2.3522], 6) // Vue initiale

      // Couche de tuiles OpenStreetMap
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
      }).addTo(mapInstance)

      // Couche pour les derniers points
      lastMarkerLayer = L.layerGroup().addTo(mapInstance)

      // Mise à jour initiale des points
      updateMap(props.points)
    })

    // Regarder les changements dans les points et mettre à jour la carte
    watch(
      () => props.points,
      (newPoints) => {
        updateMap(newPoints)
      }
    )

    // Mettre à jour la carte avec les nouveaux points
    function updateMap(points) {
      if (!mapInstance) return

      // Effacer les anciens marqueurs de dernier point
      lastMarkerLayer.clearLayers()

      // Regrouper les points par utilisateur
      const groupedPoints = groupPointsByUser(points)

      Object.keys(groupedPoints).forEach((user) => {
        const userPoints = groupedPoints[user]
        const latLngs = userPoints.map((p) => [p.latitude, p.longitude])

        // Mettre à jour ou créer la polyline pour cet utilisateur
        if (!polylineLayers[user]) {
          polylineLayers[user] = L.polyline(latLngs, { color: 'blue' }).addTo(mapInstance)
        } else {
          polylineLayers[user].setLatLngs(latLngs)
        }

        // Ajouter seulement le dernier point avec l'icône bonhomme bleu
        if (userPoints.length > 0) {
          const lastPoint = userPoints[userPoints.length - 1]
          if (lastPoint.latitude && lastPoint.longitude) {
            L.marker([lastPoint.latitude, lastPoint.longitude], { icon: bluePersonIcon })
              .bindPopup(
                `<b>${lastPoint.nom}</b><br>Lat: ${lastPoint.latitude}<br>Lon: ${lastPoint.longitude}`
              )
              .addTo(lastMarkerLayer)
          }
        }
      })
    }

    // Fonction pour regrouper les points par utilisateur
    function groupPointsByUser(points) {
      return points.reduce((acc, point) => {
        if (!acc[point.nom]) acc[point.nom] = []
        acc[point.nom].push(point)
        return acc
      }, {})
    }

    return {
      mapContainer,
    }
  },
}
</script>
