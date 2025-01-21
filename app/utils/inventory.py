import pandas as pd
import os

# 从环境变量加载 MinIO 配置信息
minio_url = os.getenv("MINIO_URL")
minio_bucket = os.getenv("MINIO_BUCKET")
minio_inventory_file = os.getenv("MINIO_INVENTORY_FILE")

class Inventory:
    def __init__(self):
        # 从 MinIO 服务器加载设备清单
        self.inventory = pd.read_excel(f'{minio_url}/{minio_bucket}/{minio_inventory_file}')

    def get_inventory(self):
        # 返回完整的设备清单
        return self.inventory
    
    def get_inventory_by_name(self, device_name):
        # 根据设备名称返回设备信息
        return self.inventory[self.inventory['device_name'] == device_name].values.tolist()
