# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "7a1ad412-8b01-49e5-9f6e-b15ef4d7c7e4",
# META       "default_lakehouse_name": "lh_gold",
# META       "default_lakehouse_workspace_id": "58f3292a-4547-4418-8424-39062a13be44",
# META       "known_lakehouses": [
# META         {
# META           "id": "6f0d4fb7-9842-401f-ab0f-dd5fc5dfa97f"
# META         },
# META         {
# META           "id": "7a1ad412-8b01-49e5-9f6e-b15ef4d7c7e4"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

trips = spark.read.table("lh_silver.taxi_trips")
print(trips.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
daily = trips.groupBy("pickup_date", "PULocationID").agg(
    F.count("*").alias("trips_count"),
    F.sum("total_amount").alias("revenue"),
    F.avg("trip_distance").alias("avg_distance")
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(daily.limit(10))
print(daily.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

daily.agg(F.sum("trips_count")).show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

daily.write.mode("overwrite").format("delta").saveAsTable("lh_gold.fact_taxi_daily")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
