from fastapi import APIRouter, HTTPException, Depends
from app.utils.zabbix_client import ZabbixClient

router = APIRouter()

@router.post("/metrics")
async def add_zabbix_metric(device_name: str, metric_name: str, zabbix_client: ZabbixClient = Depends()):
    try:
        zabbix_client.add_metric(device_name, metric_name)
        return {"message": "Metric added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics")
async def get_zabbix_metrics(zabbix_client: ZabbixClient = Depends()):
    return zabbix_client.get_metrics()

@router.delete("/metrics")
async def remove_zabbix_metric(device_name: str, metric_name: str, zabbix_client: ZabbixClient = Depends()):
    try:
        zabbix_client.remove_metric(device_name, metric_name)
        return {"message": "Metric removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 