# app/routers/regimes.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["regimes"])

REGIMES = [
    {"code": "IN-AYUSH", "label": "India — AYUSH", "language": "hi/en"},
    {"code": "US-FDA", "label": "United States — FDA", "language": "en"},
]

@router.get("/regimes")
def get_regimes():
    return REGIMES