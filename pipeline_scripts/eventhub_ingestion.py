from pyspark import pipelines as dp
from pyspark.sql.functions import *
from pyspark.sql.types import *

EH_NAMESPACE = spark.conf.get("eh.namespace")
EH_NAME = spark.conf.get("eh.name")
EH_CONN_STR = spark.conf.get("eh.connectionString")

KAFKA_OPTIONS = {
    "kafka.bootstrap.servers": f"{EH_NAMESPACE}.servicebus.windows.net:9093",
    "subscribe": EH_NAME,
    "kafka.sasl.mechanism": "PLAIN",
    "kafka.security.protocol": "SASL_SSL",
    "kafka.sasl.jaas.config": f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{EH_CONN_STR}";',
    "kafka.request.timeout.ms": "60000",
    "kafka.session.timeout.ms": "30000",
    "maxOffsetsPerTrigger": "50000",
    "failOnDataLoss": "true",
    "startingOffsets": "earliest",
}

@dp.table(
    name="orders",
    table_properties={"quality": "bronze"}
)
def orders():

    schema = StructType([
        StructField("order_id", StringType()),
        StructField("timestamp", StringType()),
        StructField("restaurant_id", StringType()),
        StructField("customer_id", StringType()),
        StructField("order_type", StringType()),
        StructField("items", StringType()),
        StructField("total_amount", DoubleType()),
        StructField("payment_method", StringType()),
        StructField("order_status", StringType())
    ])
    
    df = (
        spark.readStream    
        .format("kafka")
        .options(**KAFKA_OPTIONS)
        .load()
        .withColumn("value", col("value").cast("string"))
        .withColumn("payload", from_json(col("value"), schema))
        .select(col("payload.*"))
        .withColumn("timestamp", to_timestamp(col("timestamp"), 'yyyy-MM-dd\'T\'HH:mm:ss.SSSSSSXXX\'Z\''))
        .withColumnRenamed("timestamp", "order_timestamp")
    )

    return df
