from fastapi import APIRouter, HTTPException, Depends
from app.utils.zabbix_client import ZabbixClient

router = APIRouter()

@router.post("/metrics")
async def add_zabbix_metric(device_name: str, metric_name: str, zabbix_client: ZabbixClient = Depends()):
    try:
        # 添加 Zabbix 监控指标
        zabbix_client.add_metric(device_name, metric_name)
        return {"message": "指标添加成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics")
async def get_zabbix_metrics(zabbix_client: ZabbixClient = Depends()):
    # 获取 Zabbix 监控指标
    return zabbix_client.get_metrics()

@router.delete("/metrics")
async def remove_zabbix_metric(device_name: str, metric_name: str, zabbix_client: ZabbixClient = Depends()):
    try:
        # 移除 Zabbix 监控指标
        zabbix_client.remove_metric(device_name, metric_name)
        return {"message": "指标移除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 