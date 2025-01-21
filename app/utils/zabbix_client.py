import json
from pyzabbix.api import ZabbixAPI

class ZabbixClient:
    def __init__(self, zabbix_url, token):
        # Create ZabbixAPI class instance
        self.zapi = ZabbixAPI(server=zabbix_url)
        self.zapi.login(api_token=token)
        self.inventory = {host['host']: host['hostid'] for host in self.zapi.host.get(monitored_hosts=1, output='extend')}
        self.metrics = {} # 设备名: 监控指标列表，例如：{'cisco_core': ['Cisco IOS: ICMP ping', 'Cisco IOS: ICMP loss', 'Cisco IOS: ICMP response time']}

    def get_metrics(self):
        return self.metrics

    def _get_data(self, device_name, metric_list):
        host_id = self.inventory[device_name]
        result = self.zapi.item.get(hostids=host_id)
        metrics: dict = {info['name']: info['itemid'] for info in result if info['name'] in metric_list}
        metric_id_list = list(metrics.values())
        item_list = self.zapi.item.get(hostids=host_id, itemids=metric_id_list)
        return item_list
        
    def get_datas(self):
        data = {}
        if not self.metrics:
            return data  # Return empty data if no metrics are defined

        for device_name, metric_list in self.metrics.items():
            if device_name not in self.inventory:
                continue  # Skip if device is not in inventory

            data[device_name] = []
            value_list = self._get_data(device_name, metric_list)
            for index in range(len(value_list)):
                data[device_name].append({metric_list[index]: value_list[index]})
        return data

    def add_metric(self, device_name, metric_name):
        if device_name not in self.metrics:
            self.metrics[device_name] = []
        self.metrics[device_name].append(metric_name)

    def remove_metric(self, device_name, metric_name):
        if device_name in self.metrics:
            if metric_name in self.metrics[device_name]:
                self.metrics[device_name].remove(metric_name)
            else:
                raise Exception(f"Metric {metric_name} not found in device {device_name}")
        else:
            raise Exception(f"Device {device_name} not found")






