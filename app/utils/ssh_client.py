from netmiko import ConnectHandler
import asyncio
from app.utils.database import DataWriter

class SSHClient():
    def __init__(self):
        self.data = {}
        self.command_loops = {}  # Dictionary to store device and their commands
        self.data_writer = DataWriter()  # Initialize DataWriter

    def conn(self, device_info):
        return ConnectHandler(**device_info)

    def disconnect(self, ssh_handle):
        ssh_handle.disconnect()

    def run_command(self, ssh_handle, device_name, command):
        if device_name not in self.data:
            self.data[device_name] = []
        result = ssh_handle.send_command(command)
        self.data[device_name].append({command: result})

    def add_command_to_loop(self, device_name, command):
        if device_name not in self.command_loops:
            self.command_loops[device_name] = []
        if command not in self.command_loops[device_name]:
            self.command_loops[device_name].append(command)

    async def execute_command_loops(self, inventory):
        while True:
            for device_name, commands in self.command_loops.items():
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
                ssh_handle = self.conn(device_details)

                # Execute each command
                for command in commands:
                    self.run_command(ssh_handle, device_name, command)

                # Write data to MongoDB
                self.data_writer.write_to_mongo({device_name: self.data[device_name]})

                # Disconnect after all commands are executed
                self.disconnect(ssh_handle)

            await asyncio.sleep(300)  # Wait for 5 minutes