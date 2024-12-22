from kafka import KafkaConsumer
import os
import json


def create_consumer(topic_name, bootstrap_servers, group_id):
    """
    Crée un Kafka Consumer.

    :param topic_name: Nom du topic Kafka à écouter.
    :param bootstrap_servers: Liste des adresses des brokers Kafka.
    :param group_id: Identifiant du groupe du consumer.
    :return: Instance de KafkaConsumer.
    """
    try:
        # Création du consumer Kafka
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='earliest',  # Options: 'latest', 'earliest', 'none'
            enable_auto_commit=True        # Commit automatique des offsets
        )
        print(f"Consumer connecté au topic: {topic_name}")
        return consumer
    except Exception as e:
        print(f"Erreur lors de la création du consumer: {e}")
        return None

def read_messages(consumer):
    """
    Lit les messages depuis un Kafka Consumer.

    :param consumer: Instance de KafkaConsumer.
    """
    try:
        # Boucle pour lire les messages
        for message in consumer:
            print(f"Message reçu: {message.value.decode('utf-8')} | Partition: {message.partition} | Offset: {message.offset}")


            message_str = message.value.decode('utf-8')
            message_json = json.loads(message_str)
            # Extraire les champs nécessaires
            user_id = message_json.get('user_id')
            latitude = message_json.get('latitude')
            longitude = message_json.get('longitude')

            # Ajout à la base de données

            
            # Envoie au front-end

    except Exception as e:
        print(f"Erreur lors de la lecture des messages: {e}")

# # Exemple d'utilisation
# if __name__ == "__main__":
#     # Paramètres
#     TOPIC = "coordinates"
#     broker = os.getenv('KAFKA_BROKER')
#     BOOTSTRAP_SERVERS = broker  # Remplacez par l'adresse de votre broker
#     GROUP_ID = "mon_groupe_consumer"

#     # Création du consumer
#     consumer = create_consumer(TOPIC, BOOTSTRAP_SERVERS, GROUP_ID)
    
#     if consumer:
#         # Lecture des messages
#         read_messages(consumer)
