# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "698900e2-825b-490a-9d73-2480fbafe3c5",
# META       "default_lakehouse_name": "lh_bronze",
# META       "default_lakehouse_workspace_id": "58f3292a-4547-4418-8424-39062a13be44",
# META       "known_lakehouses": [
# META         {
# META           "id": "698900e2-825b-490a-9d73-2480fbafe3c5"
# META         }
# META       ]
# META     }
# META   }
# META }

# PARAMETERS CELL ********************

LOCATION_IDS = [857, 1122, 384, 628]
PARAMETERS = ["no2", "pm25"]
DATE_FROM = "2025-01-01"
DATE_TO = "2025-03-31"
KEY_PATH = "/lakehouse/default/Files/secrets/openaq_key.txt"
BASE_URL = "https://api.openaq.org/v3"
PAGE_LIMIT = 1000
TABLE_NAME = "openaq_daily_raw"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import requests
def read_api_key(path):
    with open(path) as file:
        return file.read().strip()
api_key = read_api_key(KEY_PATH)
print(len(api_key))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def get_json(path, params=None):
    response = requests.get(BASE_URL + path, headers={"X-API-Key": api_key}, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

sensors = get_json(f"/locations/{LOCATION_IDS[0]}/sensors")
for sensor in sensors["results"]:
    print(sensor["id"], sensor["parameter"]["name"])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def describe_sensor(location_id, sensor):
    return {"location_id": location_id, "sensor_id": sensor["id"], "parameter": sensor["parameter"]["name"]}
def sensors_for_location(location_id):
    sensors = get_json(f"/locations/{location_id}/sensors")["results"]
    return [describe_sensor(location_id, s) for s in sensors if s["parameter"]["name"] in PARAMETERS]
our_sensors = []
for location_id in LOCATION_IDS:
    our_sensors.extend(sensors_for_location(location_id))
for sensor in our_sensors:
    print(sensor)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def fetch_days_page(sensor_id, page):
    params = {"date_from": DATE_FROM, "date_to": DATE_TO, "limit": PAGE_LIMIT, "page": page}
    return get_json(f"/sensors/{sensor_id}/days", params)
test = fetch_days_page(our_sensors[0]["sensor_id"], 1)
print(test["meta"])
print(len(test["results"]))
print(test["results"][0]["period"]["datetimeFrom"]["local"])
print(test["results"][-1]["period"]["datetimeFrom"]["local"])

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def fetch_all_days(sensor_id):
    rows, page = [], 1
    while True:
        results = fetch_days_page(sensor_id, page)["results"]
        rows.extend(results)
        if len(results) < PAGE_LIMIT:
            return rows
        page += 1
print(len(fetch_all_days(our_sensors[0]["sensor_id"])))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def to_row(sensor, day):
    return {
        "location_id": sensor["location_id"],
        "sensor_id": sensor["sensor_id"],
        "parameter": sensor["parameter"],
        "date": day["period"]["datetimeFrom"]["local"][:10],
        "value": day["value"],
        "units": day["parameter"]["units"],
    }
def rows_for_sensor(sensor):
    return [to_row(sensor, day) for day in fetch_all_days(sensor["sensor_id"])]
all_rows = []
for sensor in our_sensors:
    all_rows.extend(rows_for_sensor(sensor))
print(len(all_rows))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.createDataFrame(all_rows)
display(df.limit(10))
df.write.mode("overwrite").format("delta").saveAsTable(TABLE_NAME)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.groupBy("location_id", "parameter").count().orderBy("location_id").show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
