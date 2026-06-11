from pyspark import pipelines as dp
from pyspark.sql.functions import *
from pyspark.sql.types import *


@dp.table(
    name="fact_order_items",
    table_properties={"quality": "silver"}
)
@dp.expect_all_or_drop({
    "valid_order_id": "order_id IS NOT NULL",
    "valid_order_timestamp": "order_timestamp IS NOT NULL",
    "valid_item_id": "item_id IS NOT NULL",
    "valid_restaurant_id": "restaurant_id IS NOT NULL",
    "valid_quantity": "quantity > 0",
    "valid_unit_price": "unit_price > 0",
    "valid_subtotal": "subtotal > 0"
})
def fact_order_items():
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
        .withColumn("item", explode(from_json(col("items"), schema_items)))
        .select(
            col("order_id"),
            col("item.item_id").alias("item_id"),
            col("restaurant_id"),
            col("order_timestamp"),
            col("order_date"),
            col("item.name").alias("item_name"),
            col("item.category").alias("category"),
            col("item.quantity").alias("quantity"),
            col("item.unit_price").cast("decimal(10,2)").alias("unit_price"),
            col("item.subtotal").cast("decimal(10,2)").alias("subtotal")
        )
    )

    return df