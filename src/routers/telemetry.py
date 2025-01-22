from fastapi import APIRouter, HTTPException
from ..utils.telemetry_client import TelemetryClient

router = APIRouter()
telemetry_client = TelemetryClient()

@router.post("/", summary="添加Telemetry订阅", description="为指定设备添加Telemetry订阅。")
async def add_telemetry_subscription(device: str, xpath: str):
    """
    添加Telemetry订阅

    - **device**: 设备名称
    - **xpath**: Telemetry数据的XPath路径
    """
    try:
        # 添加 telemetry 订阅
        telemetry_client.add_subscription(device, xpath)
        return {"message": "Telemetry 订阅已添加"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", summary="获取Telemetry状态", description="获取当前所有设备的Telemetry订阅状态。")
async def get_telemetry_status():
    """
    获取Telemetry状态
    """
    try:
        # 获取 telemetry 状态
        return telemetry_client.get_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 