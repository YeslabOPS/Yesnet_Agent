# Yesnet_Agent
这是Yeslab网络自动化大师课毕业项目其中一个微服务程序。

## 简介
Yesnet_Agent 是一个用于收集网络各类设备数据以及进行自动化控制的工具。
 - 网络设备数据收集使用Zabbix、云端API、Telemetry以及SSH的方式来完成
 - 自动化控制通过Ansible来完成

## 功能
- 收集Cisco、华为等各厂商的监控数据，基于SNMP调用pyzabbix，通过Zabbix API进行数据收集
- 提供基于SSH的运维接口，用户通过API来执行单次命令或循环命令
- 驱动Ansible来运行用户上传的Playbook
- 基于Telemetry收集Cisco IOSXE设备的常见监控指标

## 环境变量配置

在使用 Yesnet_Agent 之前，请确保在操作系统中配置以下环境变量：

| Environment Variable | Description                          | Example Value                  |
|----------------------|--------------------------------------|--------------------------------|
| `INFLUXDB_TOKEN`     | Token for InfluxDB authentication    | `your-influxdb-token`          |
| `INFLUXDB_ORG`       | Organization name in InfluxDB        | `your-org-name`                |
| `INFLUXDB_BUCKET`    | Bucket name in InfluxDB              | `your-bucket-name`             |
| `INFLUXDB_SERVER`    | URL of the InfluxDB server           | `http://localhost:8086`        |
| `MONGODB_URI`        | Connection URI for MongoDB           | `mongodb://localhost:27017`    |
| `MONGODB_DB`         | Database name in MongoDB             | `your-database-name`           |
| `MONGODB_COLLECTION` | Collection name in MongoDB           | `your-collection-name`         |
| `ZABBIX_URL`         | URL of the Zabbix server             | `http://your-zabbix-url`       |
| `ZABBIX_TOKEN`       | API token for Zabbix authentication  | `your-zabbix-api-token`        |
| `MINIO_URL`          | URL of the MinIO server             | `http://your-minio-url`       |
| `MINIO_BUCKET`       | Bucket name in MinIO              | `your-bucket-name`             |
| `MINIO_INVENTORY_FILE`| Inventory file name in MinIO           | `your-inventory-file-name`        |

请根据您的实际情况替换示例值。