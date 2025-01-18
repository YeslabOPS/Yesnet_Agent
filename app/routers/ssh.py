from fastapi import APIRouter, HTTPException, Depends
from app.utils.ssh_client import SSHClient
from app.utils.inventory import Inventory

router = APIRouter()
ssh_client = SSHClient()
inventory = Inventory()

@router.post("/cmd")
async def run_ssh_command(device_name: str, command: str):
    try:
        # Retrieve device information from inventory
        device_info = inventory.get_inventory_by_name(device_name)
        device_ip, device_type, ssh_username, ssh_password = device_info

        # Prepare device connection details
        device_details = {
            'device_type': device_type,
            'ip': device_ip,
            'username': ssh_username,
            'password': ssh_password,
        }

        # Establish SSH connection
        ssh_handle = ssh_client.conn(device_details)

        # Execute the command
        ssh_client.run_command(ssh_handle, device_name, command)

        return {"message": "Command executed successfully", "result": ssh_client.data[device_name]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cmdloop")
async def run_ssh_command_loop(device_name: str, command: str):
    try:
        # Add command to the loop
        ssh_client.add_command_to_loop(device_name, command)
        return {"message": "Command added to loop"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 