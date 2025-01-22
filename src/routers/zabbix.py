from fastapi import APIRouter, HTTPException, Depends
from ..utils.zabbix_client import ZabbixClient

router = APIRouter()

@router.post("/metrics", summary="添加Zabbix监控指标", description="为指定设备添加一个新的Zabbix监控指标。")
async def add_zabbix_metric(device_name: str, metric_name: str, zabbix_client: ZabbixClient = Depends()):
    """
    添加Zabbix监控指标

    - **device_name**: 设备的名称
    - **metric_name**: 要添加的监控指标名称
    """
    try:
        # 添加 Zabbix 监控指标
        zabbix_client.add_metric(device_name, metric_name)
        return {"message": "指标添加成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/metrics", summary="获取Zabbix监控指标", description="获取所有设备的Zabbix监控指标。")
async def get_zabbix_metrics(zabbix_client: ZabbixClient = Depends()):
    """
    获取Zabbix监控指标
    """
    # 获取 Zabbix 监控指标
    return zabbix_client.get_metrics()

@router.delete("/metrics", summary="移除Zabbix监控指标", description="从指定设备中移除一个Zabbix监控指标。")
async def remove_zabbix_metric(device_name: str, metric_name: str, zabbix_client: ZabbixClient = Depends()):
    """
    移除Zabbix监控指标

    - **device_name**: 设备的名称
    - **metric_name**: 要移除的监控指标名称
    """
    try:
        # 移除 Zabbix 监控指标
        zabbix_client.remove_metric(device_name, metric_name)
        return {"message": "指标移除成功"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 