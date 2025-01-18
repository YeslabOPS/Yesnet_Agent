import os
from dotenv import load_dotenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# InfluxDB credentials from environment variables
influx_token = os.getenv("INFLUXDB_TOKEN")
influx_org = os.getenv("INFLUXDB_ORG")
influx_bucket = os.getenv("INFLUXDB_BUCKET")
influx_server = os.getenv("INFLUXDB_SERVER")

class DataWriter:
    def __init__(self):
        self.influx_client = influxdb_client.InfluxDBClient(url=influx_server, token=influx_token, org=influx_org)
        self.api_writer = self.influx_client.write_api(write_options=SYNCHRONOUS)

        # MongoDB connection
        mongo_uri = os.getenv("MONGODB_URI")
        self.mongo_client = MongoClient(mongo_uri)
        self.mongo_db = self.mongo_client[os.getenv("MONGODB_DB")]
        self.mongo_collection = self.mongo_db[os.getenv("MONGODB_COLLECTION")]

    def write_ts_data(self, pname, field_tup):
        data_point = influxdb_client.Point(pname).field(field_tup[0], field_tup[1])
        self.api_writer.write(bucket=influx_bucket, org=influx_org, record=data_point)

    def write_to_mongo(self, data):
        self.mongo_collection.insert_one(data)