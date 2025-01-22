import os
import asyncio
import httpx
from fastapi import FastAPI
from .routers import zabbix, ssh, playbook, telemetry
from .utils.zabbix_client import ZabbixClient
from .utils.telemetry_client import serve
from contextlib import asynccontextmanager

app = FastAPI()

# 从环境变量加载 Zabbix 配置信息
zabbix_url = os.getenv("ZABBIX_URL")
zabbix_token = os.getenv("ZABBIX_TOKEN")

# 使用环境变量初始化 ZabbixClient
zabbix_client = ZabbixClient(zabbix_url=zabbix_url, token=zabbix_token)

# 将 zabbix_client 实例传递给 zabbix 路由
app.include_router(zabbix.router, prefix="/api/zabbix", tags=["Zabbix"])
app.include_router(ssh.router, prefix="/api/ssh", tags=["SSH"])
app.include_router(playbook.router, prefix="/api/playbook", tags=["Playbook"])
app.include_router(telemetry.router, prefix="/api/telemetry", tags=["Telemetry"])

# 定义一个周期性数据提取任务
async def periodic_data_extraction():
    while True:
        data = zabbix_client.get_datas()
        # 将数据发送到另一个微服务
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post("http://127.0.0.1:50002/api/data", json={"data": data})
                response.raise_for_status()  # 如果响应错误则抛出异常
                print("数据发送成功:", response.json())
            except httpx.HTTPStatusError as exc:
                print(f"发送数据时的错误响应 {exc.response.status_code}: {exc.response.text}")
            except Exception as e:
                print(f"发生错误: {str(e)}")
        await asyncio.sleep(60)  # 每分钟执行一次

# 使用 lifespan 事件管理器启动和关闭任务
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    task1 = asyncio.create_task(periodic_data_extraction())
    task2 = asyncio.create_task(ssh.ssh_client.execute_command_loops(ssh.inventory))
    grpc_task = asyncio.to_thread(serve)  # 在单独的线程中运行 gRPC 服务器
    yield
    # 关闭事件
    task1.cancel()
    task2.cancel()
    grpc_task.cancel()

#app = FastAPI(lifespan=lifespan)

# router = APIRouter()

# @router.post("/metrics")
# async def add_zabbix_metric(device_name: str, metric_name: str):
#     # Your implementation here
#     return {"message": "Metric added"} 