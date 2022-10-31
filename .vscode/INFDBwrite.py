from sqlite3 import Timestamp
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "<PCLog>"
org = "<0ec150323a1852ef>"
token = "<-ZqXcvns2yjMkxZgEq7_Ktjl2RLufQZkM2X6Y9OpfgR4Omdt7a9tjfFAQV3PkyBOebRP6O0Aot4L_f_409sFJg==>"
url="https://192.168.0.165:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("myMeasuremnet").field("run",240)
write_api.write(bucket=bucket, org=org, record=p)