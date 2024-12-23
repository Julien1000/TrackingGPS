from kafka import KafkaConsumer
import json
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from db.database2 import get_db
from db.model2 import Base, User, Coord
from db.schema import CoordBase, CoordResponse, CoordCreate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select


# Configuration PostgreSQL
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_NAME = "gps_data"

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

async def read_messages(consumer, websocket_broadcast, db_session: AsyncSession):
    """
    Lit les messages depuis Kafka, vérifie l'utilisateur, insère les coordonnées et diffuse via WebSocket.
    :param consumer: Instance de KafkaConsumer.
    :param websocket_broadcast: Fonction pour diffuser les messages via WebSocket.
    :param db_session: Instance de AsyncSession pour interagir avec la base.
    """
    try:
        for message in consumer:
            # Décoder et parser le message
            message_str = message.value.decode('utf-8')
            message_json = json.loads(message_str)

            nom = message_json.get('nom')
            latitude = message_json.get('latitude')
            longitude = message_json.get('longitude')
            date1 = message_json.get('date1')  # Format de date inclus

            # Vérifiez si l'utilisateur existe
            result = await db_session.execute(select(User).filter(User.nom == nom))
            user = result.scalars().first()
            if not user:
                user = User(nom=nom)
                db_session.add(user)

            # Ajouter les coordonnées
            new_coord = Coord(
                nom=nom,
                latitude=latitude,
                longitude=longitude,
                date1=date1
            )
            db_session.add(new_coord)

            try:
                # Sauvegarder dans la base
                await db_session.commit()
                await db_session.refresh(new_coord)

                # Diffuser les données via WebSocket
                await websocket_broadcast(json.dumps(message_json))
            except IntegrityError:
                await db_session.rollback()
                print("Erreur : Impossible d'ajouter les données.")
    except Exception as e:
        print(f"Erreur lors de la lecture des messages: {e}")
