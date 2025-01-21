from fastapi import APIRouter, HTTPException
from app.utils.telemetry_client import TelemetryClient

router = APIRouter()
telemetry_client = TelemetryClient()

@router.post("/")
async def add_telemetry_subscription(device: str, xpath: str):
    try:
        # 添加 telemetry 订阅
        telemetry_client.add_subscription(device, xpath)
        return {"message": "Telemetry 订阅已添加"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def get_telemetry_status():
    try:
        # 获取 telemetry 状态
        return telemetry_client.get_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 