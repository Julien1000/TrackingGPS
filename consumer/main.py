from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
import os
import asyncio

from db.database2 import get_db
from db.model2 import Base, User, Coord
from db.schema import CoordBase, CoordResponse, CoordCreate
from db.database2 import async_session_maker

from fastapi.middleware.cors import CORSMiddleware



TOPIC = "coordinates"
broker = os.getenv('KAFKA_BROKER')
BOOTSTRAP_SERVERS = broker 
GROUP_ID = "gps-consumer-group"


app = FastAPI()
consumer = None

origins = [
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",  # Alternative localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace par les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

websocket_clients = []

# Route pour récupérer toutes les coordonnées
@app.get("/coords", response_model=List[CoordResponse])
async def get_coords(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coord))
    coords = result.scalars().all()
    return coords


# Route pour récupérer les coordonnées d'un utilisateur spécifique
@app.get("/coords/{nom}", response_model=List[CoordResponse])
async def get_coords_by_user(nom: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coord).filter(Coord.nom == nom))
    coords = result.scalars().all()
    if not coords:
        raise HTTPException(status_code=404, detail="No coordinates found for this user")
    return coords

# Route pour ajouter une nouvelle coordonnée
@app.post("/coords", response_model=CoordResponse)
async def create_coord(coord: CoordCreate, db: AsyncSession = Depends(get_db)):
    # Vérifiez si l'utilisateur existe
    result = await db.execute(select(User).filter(User.nom == coord.nom))
    user = result.scalars().first()
    if not user:
        new_user = User(nom=coord.nom)
        print(new_user.nom)
        db.add(new_user)
        # raise HTTPException(status_code=404, detail="User not found")
        try:
            # Sauvegarder le nouvel utilisateur
            await db.commit()
            await db.refresh(new_user)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Failed to add the user")

    # Créer une nouvelle entrée Coord
    new_coord = Coord(
        nom=coord.nom,
        longitude=coord.longitude,
        latitude=coord.latitude,
        date1=coord.date1,
    )
    db.add(new_coord)

    try:
        # Sauvegarde dans la base
        await db.commit()
        await db.refresh(new_coord) 
        return new_coord
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Failed to add the coordinate")
    

# Fonction pour ajouter une coordonnée dans la base de données
async def add_coord_internally(coord_data):
    async with async_session_maker() as db:
        coord = CoordCreate(**coord_data)
        return await create_coord(coord, db)



# Fonction pour diffuser les messages via WebSocket
async def broadcast_to_websockets(message):
    disconnected_clients = []
    for client in websocket_clients:
        try:
            await client.send_text(message)
        except Exception:
            disconnected_clients.append(client)
    for client in disconnected_clients:
        websocket_clients.remove(client)

@app.delete("/clear_db", status_code=204)
async def clear_database(db: AsyncSession = Depends(get_db)):
    """
    Supprime toutes les données des tables 'coord' et 'user' en évitant les deadlocks.
    """
    try:
        async with db.begin():  # Démarre une transaction explicite
            # Supprime les données de 'coord' en premier pour éviter les conflits
            await db.execute(text("TRUNCATE TABLE coord CASCADE"))
            # Ensuite, supprime les données de 'user'
            await db.execute(text("TRUNCATE TABLE \"user\" CASCADE"))
        await db.commit()  # Valide les modifications
        return {"message": "Toutes les données ont été supprimées avec succès."}
    except Exception as e:
        await db.rollback()  # Annule les modifications en cas d'erreur
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression : {str(e)}")


# Route WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except Exception:
        websocket_clients.remove(websocket)


from consumerFct import create_consumer, read_messages
# Lancer le consumer en arrière-plan
@app.on_event("startup")
async def startup_event():
    """
    Au démarrage de FastAPI, on crée le consumer et on lance
    une tâche asynchrone pour lire les messages.
    """
    kafka_broker = os.getenv("KAFKA_BROKER")
    consumer = create_consumer(
        topic_name="coordinates", 
        bootstrap_servers=[kafka_broker], 
        group_id="my_consumer_group"
    )
    if consumer is not None:
        # On lance la lecture de messages dans une task asynchrone
        try:
            asyncio.create_task(read_messages(consumer))
        except Exception as e:
            print(f"[main] Erreur lors de la création de la tâche asynchrone: {e}")
    else:
        print("[main] Erreur : Impossible de créer le consumer Kafka.")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Arrête proprement le consommateur Kafka lors de l'arrêt de l'application.
    """
    try:
        if consumer is not None:
            consumer.close()
            print("Consumer Kafka fermé correctement.")
    except Exception as e:
        print(f"Erreur lors de la fermeture du consumer Kafka: {e}")

