from kafka import KafkaConsumer
import os
import json

from main import add_coord_internally, broadcast_to_websockets


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
            auto_offset_reset='latest',  # Options: 'latest', 'earliest', 'none'
            enable_auto_commit=True        # Commit automatique des offsets
        )
        print(f"Consumer connecté au topic: {topic_name}")
        return consumer
    except Exception as e:
        print(f"Erreur lors de la création du consumer: {e}")
        return None

async def read_messages(consumer):
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
            date = message_json.get('date')


            message_json = {
                "nom": user_id,  # Associez "user_id" à "nom" attendu par CoordCreate
                "latitude": latitude,
                "longitude": longitude,
                "date1": date  # Date au format ISO 8601
            }

            # Ajout à la base de données
            await add_coord_internally(message_json)

            # Diffusion via WebSocket
            await broadcast_to_websockets(json.dumps(message_json))
            # Envoie au front-end

    except Exception as e:
        print(f"Erreur lors de la lecture des messages: {e}")
