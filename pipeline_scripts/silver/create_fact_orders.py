from pyspark import pipelines as dp
from pyspark.sql.functions import *
from pyspark.sql.types import *


@dp.table(
    name="fact_orders",
    table_properties={"quality": "silver"}
)
@dp.expect_all_or_drop({
    "valid_order_id": "order_id IS NOT NULL",
    "valid_order_timestamp": "order_timestamp IS NOT NULL",
    "valid_customer_id": "customer_id IS NOT NULL",
    "valid_restaurant_id": "restaurant_id IS NOT NULL",
    "valid_item_count": "item_count > 0",
    "valid_amount": "total_amount > 0"
})
def fact_orders():

    schema_items = ArrayType(StructType([
        StructField("item_id", StringType()),
        StructField("name", StringType()),
        StructField("category", StringType()),
        StructField("quantity", IntegerType()),
        StructField("unit_price", DecimalType(10, 2)),
        StructField("subtotal", DecimalType(10, 2))
    ]))
    
    df = (
        spark.readStream.table("resturant.bronze.orders")
        .withColumn("order_date", to_date(col("order_timestamp")))
        .withColumn("order_hour", hour(col("order_timestamp")) )
        .withColumn("day_of_week", date_format(col("order_timestamp"), "E"))
        .withColumn("is_weekend", when(col("day_of_week").isin("Sat", "Sun"), True).otherwise(False))
        .withColumn("item_count", size(from_json(col("items"), schema_items)))
        .select(
            col("order_id"),
            col("order_timestamp"),
            col("order_date"),
            col("order_hour"),
            col("day_of_week"),
            col("is_weekend"),
            col("restaurant_id"),
            col("customer_id"),
            col("order_type"),
            col("item_count"),
            col("total_amount").cast("decimal(10,2)"),
            col("payment_method"),
            col("order_status")
        )
    )

    return df