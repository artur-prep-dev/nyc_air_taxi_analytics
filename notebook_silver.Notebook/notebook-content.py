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
# META         },
# META         {
# META           "id": "6f0d4fb7-9842-401f-ab0f-dd5fc5dfa97f"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

trips = spark.read.parquet("Files/taxi/trips")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

trips.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

trips.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(trips.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(trips.limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

a = trips.filter(trips.total_amount > 0)
print(a.count())
b = a.filter((a.tpep_pickup_datetime >= "2025-01-01")&(a.tpep_pickup_datetime < "2025-04-01"))
print(b.count())
c = b.filter(b.tpep_dropoff_datetime > b.tpep_pickup_datetime)
print(c.count())
d = c.dropDuplicates()
print(d.count())


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
f = d.withColumn("pickup_date", F.to_date(d.tpep_pickup_datetime))
g = f.withColumn("pickup_hour", F.hour(f.tpep_pickup_datetime))
display(g.limit(5))
display(g.filter(g.pickup_hour > 10).limit(5))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

g.write.mode("overwrite").format("delta").saveAsTable("lh_silver.taxi_trips")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
