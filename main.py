from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dbconfig import create_db_and_tables
from routes.group_routes import router as group_router
from routes.auth_routes import router as auth_router
from routes.site_routes import router as site_router
from routes.ping_routes import router as ping_router

app = FastAPI()

# Libera o frontend local (Expo web ou emulador)
origins = [
    "http://localhost:19006",
    "http://127.0.0.1:19006",
    "http://192.168.0.105:19006",
    "http://192.168.0.105:8000",
    # "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  
    allow_headers=["*"],
    expose_headers=["*"]

)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Registrar as rotas
app.include_router(group_router)
app.include_router(auth_router)
app.include_router(site_router)
app.include_router(ping_router)
