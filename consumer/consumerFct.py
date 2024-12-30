from kafka import KafkaConsumer
import os
import asyncio
import json

from main import add_coord_internally, broadcast_to_websockets


def create_consumer(topic_name, bootstrap_servers, group_id):
    """
    Crée un Kafka Consumer.
    """
    try:
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='latest',  # 'latest' ou 'earliest'
            enable_auto_commit=True
        )
        print(f"[consumerFct] Consumer connecté au topic: {topic_name}")
        return consumer
    except Exception as e:
        print(f"[consumerFct] Erreur lors de la création du consumer: {e}")
        return None
    
    

async def read_messages(consumer):
    """
    Lit les messages depuis un Kafka Consumer sans bloquer le backend.

    :param consumer: Instance de KafkaConsumer.
    """
    try:
        while True:  # Boucle infinie pour continuer à lire les messages
            # Récupérer les messages disponibles
            raw_messages = consumer.poll(timeout_ms=1000)  # Non-bloquant, attend 1 seconde max
            if raw_messages:
                for topic_partition, messages in raw_messages.items():
                    for message in messages:
                        print(f"Message reçu: {message.value.decode('utf-8')} | Partition: {message.partition} | Offset: {message.offset}")
                        
                        # Traiter le message
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
            else:
                print("Aucun message disponible, en attente...")

            # Temporisation pour éviter de surcharger la boucle
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Erreur lors de la lecture des messages: {e}")

