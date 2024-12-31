from producerFct import create_producer
from coord import generate_route_points

if __name__ == "__main__":
    kafka_topic = "coordinates"
    user_id = "user_456"  # Identifiant de l'utilisateur
    producer = create_producer()  # Appel à la fonction du fichier producer.py
    
    # Point de départ (latitude, longitude)
    start_lat = 43.298121048991 
    start_lon = 5.382524571889416  
    
    # Générer et envoyer des points de route
    generate_route_points(producer, kafka_topic, user_id, start_lat, start_lon, delay=2, change_direction_probability=0.1, steps_per_edge=10)