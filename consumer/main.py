from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import IntegrityError
import os
import asyncio

from db.database2 import get_db
from db.model2 import Base, User, Coord
from db.schema import CoordBase, CoordResponse, CoordCreate
from db.database2 import async_session_maker



TOPIC = "coordinates"
broker = os.getenv('KAFKA_BROKER')
BOOTSTRAP_SERVERS = broker 
GROUP_ID = "gps-consumer-group"


app = FastAPI()

websocket_clients = []
@app.get("/")
async def get():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GPS Tracker</title>
    </head>
    <body>
        <h1>Real-Time GPS Tracker</h1>
        <div id="output"></div>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const output = document.getElementById("output");
                const div = document.createElement("div");
                div.textContent = `nom: ${data.nom}, Latitude: ${data.latitude}, Longitude: ${data.longitude}`;
                output.appendChild(div);
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)




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

# Lancer le consumer en arrière-plan
@app.on_event("startup")
async def startup_event():
    from consumerFct import create_consumer, read_messages

    """
    Fonction exécutée au démarrage de l'application.
    Configure le consumer Kafka et lance la tâche d'écoute.
    """
    # Création du consumer Kafka
    consumer = create_consumer(TOPIC, BOOTSTRAP_SERVERS, GROUP_ID)

    # Lancer la lecture des messages si le consumer est valide
    if consumer:
        try:
            asyncio.create_task(read_messages(consumer))
        except Exception as e:
            print(f"Erreur lors de la lecture des messages: {e}")
    else:
        print("Erreur : Impossible de créer le consumer Kafka.")
