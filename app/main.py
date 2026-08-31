# app/main.py
from app import models  # ensures all models are registered with SQLAlchemy
from fastapi import FastAPI
from app.routers import auth

app = FastAPI(title="IP-SAKTI Sahayak API")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "IP-SAKTI Sahayak API is running"}
from app.routers import auth, regimes

app.include_router(auth.router)
app.include_router(regimes.router)
from app.routers import auth, regimes, documents
app.include_router(documents.router)
from app.routers import auth, regimes, documents, query
app.include_router(query.router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon dev only — tighten if you have time later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)