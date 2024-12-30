<template>
  <div>
    <h1>GPS Tracker - Dynamic Points</h1>
    <!-- On passe coords à MapView pour affichage Leaflet -->
    <MapView :points="coords" />
  </div>
</template>

<script>
import axios from 'axios'
import MapView from './components/MapView.vue'

export default {
  name: 'App',
  components: { MapView },
  data() {
    return {
      coords: [], // tableau vide au départ
      buffer: [], // Buffer pour regrouper les updates
    }
  },
  mounted() {
    // 1) Récupérer la liste complète des coordonnées déjà présentes
    axios
      .get('http://localhost:8000/coords') // <-- URL backend, adapt si besoin
      .then((res) => {
        this.coords = res.data
      })
      .catch((err) => {
        console.error('Erreur lors de la récupération des coords:', err)
      })

    // 2) Ouvrir la WebSocket
    this.ws = new WebSocket('ws://localhost:8000/ws')
    this.ws.onmessage = (event) => {
      // 3) À chaque message, on parse et on ajoute au buffer
      try {
        const newCoord = JSON.parse(event.data)
        this.buffer.push(newCoord)
      } catch (err) {
        console.error('Erreur de parsing message WebSocket:', err)
      }
    }

    // 4) Regrouper les mises à jour toutes les 500ms
    this.updateInterval = setInterval(() => {
      if (this.buffer.length > 0) {
        this.coords = [...this.coords, ...this.buffer] // Forcer la réactivité
        this.buffer = [] // Réinitialiser le buffer
      }
    }, 500)
  },
  beforeUnmount() {
    // Fermer la WebSocket proprement
    if (this.ws) {
      this.ws.close()
    }
    // Nettoyer l'intervalle
    if (this.updateInterval) {
      clearInterval(this.updateInterval)
    }
  },
}
</script>
