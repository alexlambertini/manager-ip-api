# routes/auth_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter( tags=["auth"] )

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    correct_username = os.getenv("API_USER")
    correct_password = os.getenv("API_PASS")

    if data.username != correct_username or data.password != correct_password:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"message": "Login bem-sucedido", "token": "fake-jwt-token"}
