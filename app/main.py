import os
from fastapi import FastAPI
from app.routers import zabbix, ssh, playbook, telemetry
from app.utils.zabbix_client import ZabbixClient
import asyncio
from dotenv import load_dotenv
import httpx
from contextlib import asynccontextmanager

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Load environment variables
zabbix_url = os.getenv("ZABBIX_URL")
zabbix_token = os.getenv("ZABBIX_TOKEN")

# Initialize ZabbixClient with environment variables
zabbix_client = ZabbixClient(zabbix_url=zabbix_url, token=zabbix_token)

# Pass the zabbix_client instance to the zabbix router
app.include_router(zabbix.router, prefix="/api/zabbix", tags=["Zabbix"], dependencies=[zabbix_client])
app.include_router(ssh.router, prefix="/api/ssh", tags=["SSH"])
app.include_router(playbook.router, prefix="/api/playbook", tags=["Playbook"])
app.include_router(telemetry.router, prefix="/api/telemetry", tags=["Telemetry"])

async def periodic_data_extraction():
    while True:
        data = zabbix_client.get_datas()
        # Send data to another microservice
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post("http://127.0.0.1:50002/api/data", json={"data": data})
                response.raise_for_status()  # Raise an error for bad responses
                print("Data sent successfully:", response.json())
            except httpx.HTTPStatusError as exc:
                print(f"Error response {exc.response.status_code} while sending data: {exc.response.text}")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        await asyncio.sleep(60)  # Wait for 1 minute

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    task1 = asyncio.create_task(periodic_data_extraction())
    task2 = asyncio.create_task(ssh.ssh_client.execute_command_loops(ssh.inventory))
    yield
    # Shutdown event
    task1.cancel()
    task2.cancel()

app = FastAPI(lifespan=lifespan) 