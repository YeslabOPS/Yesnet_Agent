from netmiko import ConnectHandler
import asyncio
from ..utils.database import DataController

class SSHClient():
    def __init__(self):
        self.data = {}
        self.command_loops = {}  # 存储设备及其命令的字典
        self.data_writer = DataController()  # 初始化 DataWriter

    def conn(self, device_info):
        # 建立 SSH 连接
        return ConnectHandler(**device_info)

    def disconnect(self, ssh_handle):
        # 断开 SSH 连接
        ssh_handle.disconnect()

    def run_command(self, ssh_handle, device_name, command):
        # 在设备上运行命令并存储结果
        if device_name not in self.data:
            self.data[device_name] = []
        result = ssh_handle.send_command(command)
        self.data[device_name].append({command: result})

    def add_command_to_loop(self, device_name, command):
        # 将命令添加到设备的循环命令列表中
        if device_name not in self.command_loops:
            self.command_loops[device_name] = []
        if command not in self.command_loops[device_name]:
            self.command_loops[device_name].append(command)

    async def execute_command_loops(self, inventory):
        # 异步执行命令循环
        while True:
            if not self.command_loops:
                await asyncio.sleep(300)  # 如果没有命令在循环中，等待并继续
                continue

            for device_name, commands in self.command_loops.items():
                device_info = inventory.get_inventory_by_name(device_name)
                if not device_info:
                    continue  # 如果设备信息不可用，则跳过

                device_ip, device_type, ssh_username, ssh_password = device_info
                device_details = {
                    'device_type': device_type,
                    'ip': device_ip,
                    'username': ssh_username,
                    'password': ssh_password,
                }

                ssh_handle = self.conn(device_details)
                for command in commands:
                    self.run_command(ssh_handle, device_name, command)

                self.data_writer.write_to_mongo({device_name: self.data[device_name]})
                self.disconnect(ssh_handle)

            await asyncio.sleep(300)  # 等待5分钟