<template>
    <div id="map"></div>
  </template>
  
  <script>
  import * as L from 'leaflet';
  
  export default {
    name: 'Map',
    mounted() {
      this.initMap();
    },
    methods: {
      initMap() {
        // Initialisation de la carte
        this.map = L.map('map').setView([48.8566, 2.3522], 13); // Coordonnées de Paris
  
        // Ajouter des tuiles OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        }).addTo(this.map);
  
        // Ajouter un clic pour placer un point
        this.map.on('click', this.addMarker);
      },
      addMarker(event) {
        const { lat, lng } = event.latlng;
        const marker = L.marker([lat, lng]);
        marker.addTo(this.map).bindPopup(`Point ajouté :<br>Lat: ${lat}, Lng: ${lng}`).openPopup();
      },
    },
  };
  </script>
  
  <style>
  #map {
    height: 80vh; /* Utilisation d'une hauteur en fonction de la fenêtre */
    margin: 20px auto; /* Centre la carte avec un espace au-dessus et en dessous */
    border-radius: 15px; /* Ajout de coins arrondis */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Ombre douce */
    border: 2px solid #f0f0f0; /* Bordure subtile */
    background: #f9f9f9; /* Couleur de fond par défaut */
    min-width: 80rem;
    max-width: 80rem; /* Largeur maximale pour éviter un débordement sur des écrans très larges */
  }


  /* Animation d'apparition subtile */
  #map {
    animation: fadeIn 0.6s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>
