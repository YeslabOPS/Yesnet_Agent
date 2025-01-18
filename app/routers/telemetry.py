from fastapi import APIRouter, HTTPException
from app.utils.telemetry_client import TelemetryClient

router = APIRouter()
telemetry_client = TelemetryClient()

@router.post("/")
async def add_telemetry_subscription(device: str, xpath: str):
    try:
        telemetry_client.add_subscription(device, xpath)
        return {"message": "Telemetry subscription added"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_telemetry_status():
    try:
        return telemetry_client.get_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 