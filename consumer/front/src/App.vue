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
      // 3) À chaque message, on parse et on ajoute au tableau
      try {
        const newCoord = JSON.parse(event.data)
        // On suppose que le message ressemble à :
        // { nom, latitude, longitude, date1, etc. }
        this.coords.push(newCoord)
      } catch (err) {
        console.error('Erreur de parsing message WebSocket:', err)
      }
    }
  },
  beforeUnmount() {
    // Fermer la WS proprement
    if (this.ws) {
      this.ws.close()
    }
  },
}
</script>
