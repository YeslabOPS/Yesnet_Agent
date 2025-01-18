# Yesnet_Agent

## 简介

Yesnet_Agent 是一个用于收集网络各类设备数据以及进行自动化控制的工具。
 - 网络设备数据收集使用Zabbix、云端API、Telemetry以及SSH的方式来完成
 - 自动化控制通过Ansible来完成

## 功能

- 收集Cisco、华为等各厂商的监控数据，基于SNMP调用pyzabbix，通过Zabbix API进行数据收集
- 基于SSH协议收集老旧设备的监控数据，包括CPU、内存与接口RX/TX数据
- 基于SSH协议收集网络配置数据表（路由表、ARP表、MAC表）
- 调用Ansible的Playbook收集网络设备配置文件
- 基于Telemetry收集Cisco IOSXE设备的核心链路数据