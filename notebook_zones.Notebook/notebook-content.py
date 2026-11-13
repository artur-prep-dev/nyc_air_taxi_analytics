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

# CELL ********************

zones = spark.read.option("header", True).csv("Files/taxi/taxi_zone_lookup.csv")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

zones.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

zones.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print(zones.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
