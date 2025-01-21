from concurrent import futures
import time
import grpc
from app.proto import protoxemdt_grpc_dialout_pb2_grpc
from app.proto import telemetry_pb2
from app.utils.database import DataController
from app.proto.telemetry_pb2 import Telemetry
import json

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    # 创建一个grpc server对象
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 注册huawei的telemetry数据监听服务
    protoxemdt_grpc_dialout_pb2_grpc.add_gRPCMdtDialoutServicer_to_server(
        TelemetryClient(), server)
    # 设置socket监听端口
    server.add_insecure_port('0.0.0.0:20000')
    # 启动grpc server
    server.start()
    # 死循环监听
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


class TelemetryClient(protoxemdt_grpc_dialout_pb2_grpc.gRPCMdtDialoutServicer):
    def __init__(self):
        self.data_controller = DataController()

    def parse_telemetry_data(self, telemetry_data, device_name):
        # Unified parsing function for telemetry data
        metrics = {}
        for field in telemetry_data.data_gpbkv:
            if field.name == "cpu_usage":
                metrics["CPU Usage"] = field.uint32_value
            elif field.name == "memory_usage":
                metrics["Memory Usage"] = field.uint32_value
            elif field.name == "interface_rx":
                metrics["Interface RX"] = field.uint64_value
            elif field.name == "interface_tx":
                metrics["Interface TX"] = field.uint64_value
            # Add more metrics as needed

        # Write each metric to InfluxDB
        for metric_name, metric_value in metrics.items():
            self.data_controller.write_to_influxdb(device_name, (metric_name, metric_value))

    def MdtDialout(self, request_iterator, context):
        for request in request_iterator:
            try:
                telemetry_data = Telemetry()
                telemetry_data.ParseFromString(request.data)
                device_name = telemetry_data.node_id.node_id_str
                if not device_name:
                    continue  # Skip if device name is not available
                self.parse_telemetry_data(telemetry_data, device_name)
            except Exception as e:
                print(f"Error processing telemetry data: {e}")
                continue


if __name__ == '__main__':
    serve()