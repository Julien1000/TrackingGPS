import osmnx as ox
import random
import time
from producerFct import create_producer, envoyer_message  # Importer depuis producer.py

def interpolate_coordinates(start, end, steps):
    """Interpoler des points entre deux coordonnées (lat, lon)."""
    lat_start, lon_start = start
    lat_end, lon_end = end
    lat_step = (lat_end - lat_start) / steps
    lon_step = (lon_end - lon_start) / steps
    return [(lat_start + i * lat_step, lon_start + i * lon_step) for i in range(1, steps + 1)]

def generate_route_points(producer, topic, user_id, lat, lon, delay=0.5, change_direction_probability=0.1, steps_per_edge=10):
    # Charger le graphe routier autour du point de départ
    graph = ox.graph_from_point((lat, lon), dist=5000, network_type='drive')
    
    # Obtenir un nœud de départ proche du point initial
    current_node = ox.nearest_nodes(graph, lon, lat)
    
    try:
        while True:
            # Obtenir les voisins du nœud actuel
            neighbors = list(graph.successors(current_node))
            
            # Si aucun voisin disponible, sortir de la boucle
            if not neighbors:
                print("Pas de voisins disponibles, arrêt.")
                break
            
            # Choisir un voisin aléatoire ou avancer dans une direction
            if random.random() < change_direction_probability:
                next_node = random.choice(neighbors)
            else:
                next_node = neighbors[0]
            
            # Obtenir les coordonnées des nœuds courant et suivant
            start_coords = (graph.nodes[current_node]['y'], graph.nodes[current_node]['x'])
            end_coords = (graph.nodes[next_node]['y'], graph.nodes[next_node]['x'])
            
            # Calculer des points intermédiaires
            interpolated_coords = interpolate_coordinates(start_coords, end_coords, steps_per_edge)
            
            # Envoyer les coordonnées intermédiaires
            for coord in interpolated_coords:
                message = {
                    "user_id": user_id,
                    "latitude": coord[0],
                    "longitude": coord[1]
                }
                envoyer_message(producer, topic, message)
                time.sleep(delay)
            
            # Mettre à jour le nœud actuel
            current_node = next_node
    except KeyboardInterrupt:
        print("Génération interrompue par l'utilisateur.")

# # Exemple d'utilisation
# if __name__ == "__main__":
#     kafka_topic = "coordinates"
#     user_id = "user_123"  # Identifiant de l'utilisateur
#     producer = create_producer()  # Appel à la fonction du fichier producer.py
    
#     # Point de départ (latitude, longitude)
#     start_lat = 48.8566
#     start_lon = 2.3522
    
#     # Générer et envoyer des points de route
#     generate_route_points(producer, kafka_topic, user_id, start_lat, start_lon, delay=1, change_direction_probability=0.1, steps_per_edge=10)