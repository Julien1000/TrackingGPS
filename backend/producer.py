from kafka import KafkaProducer
import json
import os
from dotenv import load_dotenv

load_dotenv()

def create_producer():
    """
    Crée et retourne une instance de KafkaProducer.
    
    Returns:
        KafkaProducer: Le producteur Kafka configuré.
    """
    broker = os.getenv('KAFKA_BROKER')  # Charger l'adresse du broker depuis les variables d'environnement
    if not broker:
        raise ValueError("L'environnement 'KAFKA_BROKER' n'est pas configuré.")
    
    try:
        producer = KafkaProducer(
            bootstrap_servers=broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Sérialisation JSON
        )
        print(f"KafkaProducer connecté à {broker}")
        return producer
    except Exception as e:
        raise RuntimeError(f"Erreur lors de la création du KafkaProducer : {e}")

def envoyer_message(producer, topic, message):
    """
    Envoie un message au topic Kafka spécifié.
    
    Args:
        producer (KafkaProducer): Instance de KafkaProducer.
        topic (str): Le nom du topic où envoyer le message.
        message (dict): Le message à envoyer (sera converti en JSON).
    """
    try:
        producer.send(topic, value=message)
        producer.flush()  # S'assurer que le message est bien envoyé
        print(f"Message envoyé avec succès : {message}")
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")

