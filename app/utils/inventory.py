import pandas as pd

class Inventory:
    def __init__(self):
        self.inventory = pd.read_excel('http://127.0.0.1:3001/inventory/netA.xlsx')

    def get_inventory(self):
        return self.inventory
    
    def get_inventory_by_name(self, device_name):
        return self.inventory[self.inventory['device_name'] == device_name].values.tolist()
