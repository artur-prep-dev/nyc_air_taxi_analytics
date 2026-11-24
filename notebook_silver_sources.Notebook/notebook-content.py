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
# META     },
# META     "warehouse": {
# META       "default_warehouse": "044906ac-267a-41c6-87ee-07168e6154e6",
# META       "known_warehouses": [
# META         {
# META           "id": "044906ac-267a-41c6-87ee-07168e6154e6",
# META           "type": "Lakewarehouse"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

BRONZE_FX = "lh_bronze.ecb_fx_raw"
BRONZE_GDP = "lh_bronze.worldbank_gdp_raw"
BRONZE_AIR = "lh_bronze.openaq_daily_raw"
SILVER_FX = "lh_silver.fx_usd_eur"
SILVER_GDP = "lh_silver.gdp_usa"
SILVER_AIR = "lh_silver.air_quality_daily"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F 
def save_silver(df, table_name):
    clean = df.dropDuplicates()
    clean.write.mode("overwrite").format("delta").saveAsTable(table_name)
    print(table_name, clean.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def clean_fx(raw):
    return raw.select(
        F.to_date("TIME_PERIOD").alias("date"),
        F.col("OBS_VALUE").cast("double").alias("usd_per_eur")
    )
save_silver(clean_fx(spark.read.table(BRONZE_FX)), SILVER_FX)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def clean_gdp(raw):
    return raw.select(
        F.col("country_id"),
        F.col("country_name"),
        F.col("date").cast("int").alias("year"),
        F.col("value").alias("gdp_usd"),
    )
save_silver(clean_gdp(spark.read.table(BRONZE_GDP)), SILVER_GDP)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def clean_air(raw):
    return raw.select(
        "location_id", "sensor_id", "parameter",
        F.to_date("date").alias("date"),
        F.col("value").cast("double").alias("value"),
        "units",
    )
save_silver(clean_air(spark.read.table(BRONZE_AIR)), SILVER_AIR)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
