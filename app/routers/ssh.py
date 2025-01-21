from fastapi import APIRouter, HTTPException, Depends
from app.utils.ssh_client import SSHClient
from app.utils.inventory import Inventory

router = APIRouter()
ssh_client = SSHClient()
inventory = Inventory()

@router.post("/cmd")
async def run_ssh_command(device_name: str, command: str):
    try:
        # 从设备清单中获取设备信息
        device_info = inventory.get_inventory_by_name(device_name)
        device_ip, device_type, ssh_username, ssh_password = device_info

        # 准备设备连接详细信息
        device_details = {
            'device_type': device_type,
            'ip': device_ip,
            'username': ssh_username,
            'password': ssh_password,
        }

        # 建立 SSH 连接
        ssh_handle = ssh_client.conn(device_details)

        # 执行命令
        ssh_client.run_command(ssh_handle, device_name, command)

        return {"message": "命令执行成功", "result": ssh_client.data[device_name]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cmdloop")
async def run_ssh_command_loop(device_name: str, command: str):
    try:
        # 将命令添加到循环中
        ssh_client.add_command_to_loop(device_name, command)
        return {"message": "命令已添加到循环"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 