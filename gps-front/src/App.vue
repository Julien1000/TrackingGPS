<template>
  <div id="app">
    OUAISOUAISOUAIS
    <Map />
  </div>
</template>

<script>
import Map from './components/Map.vue';

export default {
  name: 'App',
  components: {
    Map,
  },
};
</script>

<style>
/* Styles globaux si nécessaire */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  overflow: hidden; /* Désactive le scroll */
}


/* Animation de l'application */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Style des liens */
a {
  color: #007bff; /* Couleur bleue agréable */
  text-decoration: none; /* Suppression du soulignement */
  transition: color 0.3s ease;
}

a:hover {
  color: #0056b3; /* Couleur légèrement plus sombre au survol */
}

/* Boutons personnalisés */
button {
  background-color: #007bff; /* Couleur principale */
  color: #fff; /* Texte en blanc */
  border: none; /* Suppression des bordures */
  border-radius: 5px; /* Coins arrondis */
  padding: 10px 20px; /* Taille du bouton */
  cursor: pointer; /* Curseur de clic */
  transition: background-color 0.3s ease, transform 0.2s ease;
}

button:hover {
  background-color: #0056b3; /* Couleur au survol */
  transform: scale(1.05); /* Léger agrandissement au survol */
}

/* Ajout d'un comportement réactif */
@media (max-width: 768px) {
  #app {
    padding: 10px; /* Réduction des marges sur petits écrans */
    font-size: 90%; /* Taille de texte légèrement réduite */
  }
}
</style>
