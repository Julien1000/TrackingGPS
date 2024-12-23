from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://ekip:projet1@localhost/coord_gps"
# Configuration du moteur
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
