from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_HOST = "localhost"
DB_USER = "ekip"
DB_PASSWORD = "projet1"
DB_NAME = "coord_gps"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"# Configuration du moteur
engine = create_async_engine(DATABASE_URL, echo=True)

# Fabrique de session
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dépendance pour la session
async def get_db():
    async with async_session_maker() as session:
        yield session

