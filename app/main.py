from fastapi import FastAPI
from .database import Base,engine
from .routers import assets, relationships,import_data

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Asset Management API"
)

app.include_router(
    assets.router
)
app.include_router(
    relationships.router
)
app.include_router(
    import_data.router
)