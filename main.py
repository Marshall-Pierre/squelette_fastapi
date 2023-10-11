from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from app.Db import Migration, Connection
from app.Router import UserRouter

# Migration.Base.metadata.create_all(bind=Connection.engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.include_router(UserRouter.router, prefix="/api/user")


@app.get("/")
def read_root():
    return {"msg": "Serveur démarré"}

