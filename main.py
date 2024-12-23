from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from sqlalchemy.exc import IntegrityError

from app.database2 import get_db
from app.model2 import Base, User, Coord
from app.schema import CoordBase, CoordResponse, CoordCreate

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


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

@app.post("/coords", response_model=CoordResponse)
async def create_coord(coord: CoordCreate, db: AsyncSession = Depends(get_db)):
    # Vérifiez si l'utilisateur existe
    result = await db.execute(select(User).filter(User.nom == coord.nom))
    user = result.scalars().first()
    if not user:
        new_user = User(nom=user.nom)
        db.add(new_user)
        # raise HTTPException(status_code=404, detail="User not found")

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




# Route pour ajouter une nouvelle coordonnée
# @app.post("/coords", response_model=CoordResponse)
# async def create_coord(coord: CoordBase, db: AsyncSession = Depends(get_db)):
#     new_coord = Coord(**coord.dict())
#     db.add(new_coord)
#     await db.commit()
#     await db.refresh(new_coord)
#     return new_coord