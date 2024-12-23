import os
from consumerFct import create_consumer, read_messages

# Exemple d'utilisation
if __name__ == "__main__":
    # Paramètres
    TOPIC = "coordinates"
    broker = os.getenv('KAFKA_BROKER')
    BOOTSTRAP_SERVERS = broker  # Remplacez par l'adresse de votre broker
    GROUP_ID = "gps-consumer-group"

    # Création du consumer
    consumer = create_consumer(TOPIC, BOOTSTRAP_SERVERS, GROUP_ID)
    
    if consumer:
        # Lecture des messages
        read_messages(consumer)