from pyzabbix.api import ZabbixAPI

class ZabbixClient:
    def __init__(self, zabbix_url, token, running=False):
        if running:
            # 创建 ZabbixAPI 类实例
            self.zapi = ZabbixAPI(server=zabbix_url)
            self.zapi.login(api_token=token)
            # 获取监控的主机清单
            self.inventory = {host['host']: host['hostid'] for host in self.zapi.host.get(monitored_hosts=1, output='extend')}
            self.metrics = {} # 设备名: 监控指标列表，例如：{'cisco_core': ['Cisco IOS: ICMP ping', 'Cisco IOS: ICMP loss', 'Cisco IOS: ICMP response time']}

    def get_metrics(self):
        # 返回当前的监控指标
        return self.metrics

    def _get_data(self, device_name, metric_list):
        # 获取指定设备的监控数据
        host_id = self.inventory[device_name]
        result = self.zapi.item.get(hostids=host_id)
        metrics: dict = {info['name']: info['itemid'] for info in result if info['name'] in metric_list}
        metric_id_list = list(metrics.values())
        item_list = self.zapi.item.get(hostids=host_id, itemids=metric_id_list)
        return item_list
        
    def get_datas(self):
        # 获取所有设备的监控数据
        data = {}
        if not self.metrics:
            return data  # 如果没有定义指标，返回空数据

        for device_name, metric_list in self.metrics.items():
            if device_name not in self.inventory:
                continue  # 如果设备不在清单中，则跳过

            data[device_name] = []
            value_list = self._get_data(device_name, metric_list)
            for index in range(len(value_list)):
                data[device_name].append({metric_list[index]: value_list[index]})
        return data

    def add_metric(self, device_name, metric_name):
        # 为设备添加监控指标
        if device_name not in self.metrics:
            self.metrics[device_name] = []
        self.metrics[device_name].append(metric_name)

    def remove_metric(self, device_name, metric_name):
        # 从设备中移除监控指标
        if device_name in self.metrics:
            if metric_name in self.metrics[device_name]:
                self.metrics[device_name].remove(metric_name)
            else:
                raise Exception(f"Metric {metric_name} not found in device {device_name}")
        else:
            raise Exception(f"Device {device_name} not found")






